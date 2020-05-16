from django.views import View

from pro.models import ProModeFeature, Product
from event_app.models import User
from pro.validators import *
from payments.models import Seller
from utils.exceptions import AccessDenied


class GetBgView(View):
    @get_user_schema
    def post(self, request):
        try:
            user = User.objects.get(username=request.json['username'])
            if user.user_type == 'pro':
                feature, _ = ProModeFeature.objects.get_or_create(user=user)
                return dict(
                    background_color=feature.background_color,
                    background_image=feature.background_image,
                    link_style=feature.link_style,
                    preview_image=feature.preview_image
                )
            return dict(
                background_color=None,
                background_image=None,
                link_style=None,
                preview_image=None
            )
        except User.DoesNotExist:
            return dict(
                background_color=None,
                background_image=None,
                link_style=None,
                preview_image=None
            )


class GetProductsView(View):
    @get_user_schema
    def post(self, request):
        user = request.json['username']
        page_no = int(request.GET.get('pageNo', 1))
        return dict(products=Product.objects.filter(user__username=user).paginate(page_no).detail())


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


class GetShippingAddressView(View):
    @get_user_schema
    def post(self, request):
        data = request.json
        user = User.objects.get(username=data['username'])
        if user.user_type != 'pro':
            raise AccessDenied('User is not a pro user')
        seller = Seller.objects.get_or_create(user=user)[0]
        return dict(address=seller.shipping_area)
