from django.views import View
from django.db.transaction import atomic

from pro.models import ProModeFeature, Product, ProductCategory
from utils.tasks import delete_file
from event_manager.settings import ICONCONTAINER, PROFILECONTAINER, PRODUCTCONTAINER
from pro.validators import *
from event_app.utils import upload_file
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
        data['category'] = ProductCategory.objects.get_or_create(name=data['category'], seller=seller)[0] \
            if 'category' in data else None
        product = Product.objects.create(user=request.User, **data, images=[])
        return dict(product=product.detail())


class AddImageToProductView(View):
    @add_image_schema
    def post(self, request):
        data = request.POST.dict()['product_id']
        image = request.FILES.dict()['photo']
        product = Product.objects.get(id=data, user=request.User)
        product.images.append(upload_file(request, image, PRODUCTCONTAINER))
        if product.category is not None and product.category.image == '':
            product.category.image = upload_file(request, image, PRODUCTCONTAINER)
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
        product = Product.objects.get(id=data['id'])
        if 'category' in data:
            if product.category is None or product.category.name != data['category']:
                data['category'] = ProductCategory.objects.get_or_create(
                    name=data['category'], seller=Seller.objects.get_or_create(user=request.User)[0]
                )[0]
            else:
                del data['category']
        Product.objects.filter(id=data['id'], user=request.User).update(**data)
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


class SetShippingAddressView(View):
    @update_shipping_schema
    def post(self, request):
        data = request.json
        seller = Seller.objects.get_or_create(user=request.User)[0]
        seller.shipping_area = data['address']
        seller.save()
        return dict(address=seller.shipping_area)


class GetBankView(View):
    def get(self, request):
        seller = Seller.objects.get_or_create(user=request.User)[0]
        return dict(seller=seller.detail())


class DeleteProductCategoryView(View):
    @delete_category_schema
    def post(self, request):
        ProductCategory.objects.filter(id=request.json['category_id'], seller__user=request.User).delete()
        return dict(message='Deleted succesfully')
