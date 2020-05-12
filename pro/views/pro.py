from django.views import View
from django.db.transaction import atomic

from pro.models import ProModeFeature, Product
from utils.tasks import delete_file
from event_manager.settings import ICONCONTAINER, PROFILECONTAINER, PRODUCTCONTAINER
from event_app.models import User
from pro.validators import *
from event_app.utils import upload_file
from pro.utils import convert_to_base64
from payments.models import OrderItem, Order, Seller, RetrieveAmount
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


class ProModeView(View):
    @get_user_schema
    def post(self, request):
        data = request.json
        feature = ProModeFeature.objects.filter(
            user__username=data['username']
        ).first()
        if feature:
            return dict(feature=feature.detail())
        return dict(feature=None)


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
        product = Product.objects.create(user=request.User, **data, images=[])
        return dict(product=product.detail())


class AddImageToProductView(View):
    @add_image_schema
    def post(self, request):
        data = request.POST.dict()['product_id']
        image = request.FILES.dict()['photo']
        product = Product.objects.get(id=data, user=request.User)
        product.images.append(upload_file(request, image, PRODUCTCONTAINER))
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
        Product.objects.filter(id=data['id'], user=request.User).update(**data)
        return dict(product=Product.objects.get(id=data['id']).detail())


class DeleteProductView(View):
    @delete_product_schema
    def post(self, request):
        data = request.json
        Product.objects.filter(id=data['product_id'], user=request.User).delete()
        return dict(message="Deleted")


class GetSoldProductsView(View):
    def get(self, request):
        return dict(orders=Order.objects.get_sold_products(request.User).detail())


class UpdateSoldProductsView(View):
    @update_order_schema
    def post(self, request):
        data = request.json
        item = OrderItem.objects.get(id=data['item_id'], product__user=request.User)
        item.status = data['status']
        item.save()
        return dict(item=item.detail())


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


class GetBankView(View):
    @get_user_schema
    def post(self, request):
        data = request.json
        seller = Seller.objects.get_or_create(user=User.objects.get(username=data['username']))[0]
        return dict(seller=seller.detail())


class GetRedeemHistoryView(View):
    def get(self, request):
        return dict(history=RetrieveAmount.objects.filter(user=request.User).detail())
