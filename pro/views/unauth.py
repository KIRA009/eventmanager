from django.views import View

from pro.models import ProModeFeature, Product
from event_app.models import User
from pro.validators import *


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
                    link_style=feature.link_style
                )
            return dict(
                background_color=None,
                background_image=None,
                link_style=None
            )
        except User.DoesNotExist:
            return dict(
                background_color=None,
                background_image=None,
                link_style=None
            )


class GetProductsView(View):
    @get_user_schema
    def post(self, request):
        user = request.json['username']
        return dict(products=[_.detail() for _ in Product.objects.filter(user__username=user)])
