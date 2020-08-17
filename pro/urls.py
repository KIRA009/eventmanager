from django.urls import path

from utils.decorators import login_required
from .utils import pro_required
from .views import *

unauth_urls = list(
    map(
        lambda x: path(x[0], x[1].as_view()),
        [
            ("feature/", ProModeView),
            ("background/get/", GetBgView),
            ("products/get/", GetProductsView),
            ("product/get/<slug:slug>/", GetProductView),
            ("shop/get/", GetShopView),
            ("shop/homepage/get/", GetShopHomePageView),
            ("product/search/", SearchProductView),
            ("products/featured/get/", GetFeaturedProductsView)
        ],
    )
)

pro_urls = list(
    map(
        lambda x: path(x[0], pro_required(login_required(x[1].as_view()))),
        [
            ("feature/header/", ProModeHeaderView),
            ('background/set/', SetBgView),
            ("product/create/", CreateProductView),
            ("product/image/add/", AddImageToProductView),
            ("product/image/del/", DeleteImageFromProductView),
            ("product/update/", UpdateProductView),
            ("product/delete/", DeleteProductView),
            ("pending/get/", GetPendingAmountView),
            ("pending/retrieve/", RetrieveAmountView),
            ("banking/set/", UpdateBankView),
            ("pending/history/", GetRedeemHistoryView),
            ("banking/get/", GetBankView),
            ("shop/set/", SetShopView),
            ("category/del/", DeleteProductCategoryView),
            ("product/resell/", GetResellProductsView),
            ("product/resell/add/", AddResellProductView),
            ("product/resell/remove/", RemoveResellProductView),
            ('category/update/', UpdateCategoryView),
            ("shop/homepage/info/set/", UpdateShopInfoView),
            ("shop/homepage/cover/set/", UpdateShopCoverView),
            ("shop/homepage/cover/del/", DeleteShopCoverView),
        ],
    )
)

urlpatterns = unauth_urls + pro_urls
