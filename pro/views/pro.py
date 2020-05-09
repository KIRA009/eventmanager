from django.views import View

from pro.models import ProModeFeature, Product
from event_app.utils import upload_file
from utils.tasks import delete_file
from event_manager.settings import ICONCONTAINER, PROFILECONTAINER, PRODUCTCONTAINER
from pro.validators import *


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
        elif 'photo' in data:
            delete_file(feature.background_image)
            feature.background_image = upload_file(request, None, PROFILECONTAINER)
        if 'link_style' in data:
            feature.link_style = data['link_style']
        feature.save()
        return dict(
            background_color=feature.background_color,
            background_image=feature.background_image,
            link_style=feature.link_style
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
        product.save()
        return dict(product=product.detail())


class DeleteImageFromProductView(View):
    @delete_image_schema
    def post(self, request):
        data = request.json
        product = Product.objects.get(id=data['product_id'], user=request.User)
        delete_file(data['image'])
        try:
            product.images.remove(data['image'])
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
