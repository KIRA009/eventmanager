from django.views import View
from django.db.models import F

from pro.models import ProModeFeature, Product
from event_app.models import User
from pro.validators import *
from payments.models import Seller
from utils.exceptions import AccessDenied, NotFound
from pro.documents import ProductDocument


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
        if 'category' in request.GET.dict():
            category = request.GET.dict()['category']
            if category == 'Reselling Products':
                query = Product.objects.get_resell_products(user)
            else:
                query = Product.objects.get_products(user, category__name=category)
        else:
            query = Product.objects.get_products(user)
        num_pages, page = query.paginate(page_no)
        return dict(products=page.detail(), num_pages=num_pages)


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


class GetShopView(View):
    @get_user_schema
    def post(self, request):
        data = request.json
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            raise NotFound()
        if user.user_type != 'pro':
            raise AccessDenied('User is not a pro user')
        seller = Seller.objects.get_or_create(user=user)[0]
        return dict(
            address=seller.shipping_area,
            commission=seller.commission,
            categories=seller.categories.all().detail(),
            is_category_view_enabled=seller.is_category_view_enabled
        )


class SearchProductView(View):
    @search_products_schema
    def post(self, request):
        data = request.json
        query = f"*{data['query']}*"
        products = ProductDocument.search().filter({
            "bool": {
                "should": [
                    {
                        "wildcard": {
                            "category.name": {
                                "value": query
                            }
                        }
                    },
                    {
                        "wildcard": {
                            "name": {
                                "value": query
                            }
                        }
                    },
                    {
                        "wildcard": {
                            "description": {
                                "value": query
                            }
                        }
                    }
                ]
            }
        }).to_queryset()
        page_no = int(request.GET.get('pageNo', 1))
        num_pages, products = products.filter(user__username=data['seller']).paginate(page_no)
        return dict(products=products.detail(), num_pages=num_pages)
