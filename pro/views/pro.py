from django.views import View
from django.db.transaction import atomic

from pro.models import ProModeFeature, Product, ProductCategory, ResellProduct, ProductSize
from utils.tasks import delete_file
from event_manager.settings import ICONCONTAINER, PROFILECONTAINER, PRODUCTCONTAINER, CATEGORYCONTAINER
from pro.validators import *
from event_app.utils import upload_file, copy_file
from pro.utils import convert_to_base64
from payments.models import Seller, RetrieveAmount
from utils.exceptions import AccessDenied


class ProModeHeaderView(View):
    def post(self, request):
        data = request.POST.dict()
        file = request.FILES.dict().get("icon")
        feature, _ = ProModeFeature.objects.get_or_create(user=request.User)
        if "header_text" in data:
            feature.header_text = data["header_text"]
        if file:
            if feature.header_icon:
                delete_file(feature.header_icon)
            feature.header_icon = upload_file(request, file, ICONCONTAINER)
        feature.save()
        return dict(feature=feature.detail())


class SetBgView(View):
    def post(self, request):
        data = request.POST.dict()
        feature, _ = ProModeFeature.objects.get_or_create(user=request.User)
        if 'background_color' in data:
            feature.background_color = data["background_color"]
        img = request.FILES.dict()
        if 'photo' in img:
            img = img['photo']
            delete_file(feature.background_image)
            feature.background_image = upload_file(request, img, PROFILECONTAINER)
            feature.preview_image = convert_to_base64(img)
        elif 'photo' in data:
            delete_file(feature.background_image)
            feature.background_image = None
            feature.preview_image = None
        if 'link_style' in data:
            feature.link_style = data['link_style']
        feature.save()
        return dict(
            background_color=feature.background_color,
            background_image=feature.background_image,
            link_style=feature.link_style,
            preview_image=feature.preview_image
        )


class CreateProductView(View):
    @create_product_schema
    def post(self, request):
        data = request.json
        seller = Seller.objects.get_or_create(user=request.User)[0]
        if 'category' not in data:
            data['category'] = 'Others'
        if data['category'] == 'Reselling Products':
            raise AccessDenied("The category name is reserved")
        data['category'] = ProductCategory.objects.get_or_create(name=data['category'], seller=request.User.seller)[0]
        sizes = data['sizes']
        del data['sizes']
        product = Product.objects.create(user=request.User, **data, images=[])
        product = Product.objects.first()
        if product.opt_for_reselling:
            ResellProduct.objects.create(product=product)
        return dict(product=product.detail())


class AddImageToProductView(View):
    @add_image_schema
    def post(self, request):
        data = request.POST.dict()['product_id']
        image = request.FILES.dict()['photo']
        product = Product.objects.get(id=data, user=request.User)
        product.images.append(upload_file(request, image, PRODUCTCONTAINER))
        if product.category is not None and product.category.image == '':
            product.category.image = copy_file(product.images[-1], CATEGORYCONTAINER)
            product.category.save()
        product.preview_images.append(convert_to_base64(image))
        product.save()
        return dict(product=product.detail())


class DeleteImageFromProductView(View):
    @delete_image_schema
    def post(self, request):
        data = request.json
        product = Product.objects.get(id=data['product_id'], user=request.User)
        image_ind = product.images.index(data['image'])
        delete_file(data['image'])
        try:
            del product.images[image_ind]
            del product.preview_images[image_ind]
            product.save()
        except ValueError:
            pass
        return dict(product=product.detail())


class UpdateProductView(View):
    @update_product_schema
    def post(self, request):
        data = request.json
        product = Product.objects.select_related('category').get(id=data['id'], user=request.User)
        changed_vals = dict()
        for k, v in data.items():
            if v != getattr(product, k):
                changed_vals[k] = v
        data = changed_vals
        if 'category' in data:
            if product.category is None or product.category.name != data['category']:
                data['category'] = ProductCategory.objects.get_or_create(
                    name=data['category'], seller=Seller.objects.get_or_create(user=request.User)[0]
                )[0]
            else:
                del data['category']
        sizes = data['sizes']
        del data['sizes']
        if 'sizes_available' in data:
            if product.sizes_available:
                product.sizes.all().delete()
            else:
                for i in ['stock', 'resell_margin', 'price', 'disc_price']:
                    if getattr(product, i) != 0:
                        data[i] = 0
                    else:
                        if i in data:
                            del data[i]
        if data:
            for k, v in data.items():
                setattr(product, k, v)
            product.save()
        if product.opt_for_reselling:
            ResellProduct.objects.get_or_create(product=product)
        if product.sizes_available:
            product_sizes = ProductSize.objects.filter(product=product).values_list('id', flat=True)
            new_sizes = [ProductSize(product=product, **size) for size in sizes if 'id' not in size]
            deleted_sizes = set(product_sizes).difference(set([_['id'] for _ in sizes if 'id' in _]))
            ProductSize.objects.filter(id__in=deleted_sizes).delete()
            ProductSize.objects.bulk_create(new_sizes)
        return dict(product=product.detail())


class DeleteProductView(View):
    @delete_product_schema
    def post(self, request):
        data = request.json
        product = Product.objects.filter(id=data['product_id'], user=request.User).first()
        product.delete()
        return dict(message="Deleted")


class GetPendingAmountView(View):
    def get(self, request):
        return dict(amount=Seller.objects.get_or_create(user=request.User)[0].amount)


class RetrieveAmountView(View):
    @retrieve_amount_schema
    def post(self, request):
        data = request.json
        seller = Seller.objects.get_or_create(user=request.User)[0]
        if seller.amount >= data['amount']:
            with atomic():
                RetrieveAmount.objects.create(user=request.User, amount=data['amount'])
                seller.amount -= data['amount']
                seller.save()
        else:
            raise AccessDenied("Cannot retrieve more than owed amount")
        return dict(message='Done')


class UpdateBankView(View):
    @update_bank_details
    def post(self, request):
        data = request.json
        seller = Seller.objects.get_or_create(user=request.User)[0]
        seller.account_number = data['account_number']
        seller.account_holder_name = data['account_holder_name']
        seller.ifsc_code = data['ifsc_code']
        seller.save()
        return dict(seller=seller.detail())


class GetRedeemHistoryView(View):
    def get(self, request):
        return dict(history=RetrieveAmount.objects.filter(user=request.User).detail())


class SetShopView(View):
    @update_shipping_schema
    def post(self, request):
        data = request.json
        seller = request.User.seller
        cols = ['shipping_area', 'shop_address', 'city', 'state', 'country', 'pincode', 'is_category_view_enabled']
        for column in cols:
            setattr(seller, column, data[column])
        seller.save()
        return {k: getattr(seller, k) for k in cols}


class GetBankView(View):
    def get(self, request):
        seller = Seller.objects.get_or_create(user=request.User)[0]
        return dict(seller=seller.detail())


class DeleteProductCategoryView(View):
    @delete_category_schema
    def post(self, request):
        ProductCategory.objects.get(id=request.json['category_id'], seller__user=request.User).delete()
        return dict(message='Deleted succesfully')


class GetResellProductsView(View):
    def get(self, request):
        page_no = int(request.GET.get('pageNo', 1))
        num_pages, products = ResellProduct.objects.select_related(
            'product', 'product__category', 'product__user__feature'
        ).filter(product__opt_for_reselling=True).paginate(page_no)
        products = products.detail()
        product_ids = [_['id'] for _ in products]
        added_products = ResellProduct.objects.filter(
            id__in=product_ids, sellers__user_id=request.User.id
        ).values_list('id', flat=True)
        for product in products:
            product['added'] = product['id'] in added_products
        return dict(products=products, num_pages=num_pages)


class AddResellProductView(View):
    @delete_product_schema
    def post(self, request):
        resell_product = ResellProduct.objects.get_or_create(product_id=request.json['product_id'])[0]
        if resell_product.product.user_id != request.User.id:
            resell_product.sellers.add(request.User.seller.id)
        resell_product.product.update_last_interaction()
        return dict(message="Product added")


class RemoveResellProductView(View):
    @delete_product_schema
    def post(self, request):
        resell_product = ResellProduct.objects.get_or_create(product_id=request.json['product_id'])[0]
        if resell_product.product.user_id != request.User.id:
            resell_product.sellers.remove(request.User.seller.id)
        return dict(message="Product removed")


class UpdateCategoryView(View):
    @update_category_schema
    def post(self, request):
        data = request.POST.dict()
        files = request.FILES.dict()
        category = ProductCategory.objects.get(id=data['category_id'], seller__user=request.User)
        if 'photo' in files:
            file = files['photo']
            category.image = upload_file(request, file, CATEGORYCONTAINER)
        category.name = data['name']
        category.save()
        return dict(category=category.detail())
