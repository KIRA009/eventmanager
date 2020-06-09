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
            ("shop/get/", GetShopView),
            ("product/search/", SearchProductView)
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
            ("category/del/", DeleteProductCategoryView)
        ],
    )
)

urlpatterns = unauth_urls + pro_urls
