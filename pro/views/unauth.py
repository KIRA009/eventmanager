from django.views import View

from pro.models import ProModeFeature, Product, ResellProduct
from event_app.models import User
from pro.validators import *
from payments.models import Seller
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
        page = page.detail()
        if category == 'Reselling Products':
            product_ids = [_['id'] for _ in page]
            resell_products = {
                _['product_id']: _['resell_margin'] for _ in
                ResellProduct.objects.filter(
                    product_id__in=product_ids, seller__user__username=user
                ).values('product_id', 'resell_margin')
            }
            for i in page:
                i['disc_price'] += resell_products.get(i['id'], 0)
        return dict(products=page, num_pages=num_pages)


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
        seller = Seller.objects.get(user__username=data['username'])
        cols = ['shipping_area', 'shop_address', 'city', 'state', 'country', 'pincode', 'is_category_view_enabled',
                'commission']
        return {"categories": seller.categories.all().detail(), **{k: getattr(seller, k) for k in cols}}


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


class GetProductView(View):
    def get(self, request, slug):
        return dict(product=Product.objects.get(slug=slug).detail())
