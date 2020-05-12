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
            ("banking/get/", GetBankView)
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
            ("products/sold/get/", GetSoldProductsView),
            ("products/sold/update/", UpdateSoldProductsView),
            ("pending/get/", GetPendingAmountView),
            ("pending/retrieve/", RetrieveAmountView),
            ("banking/set/", UpdateBankView),
            ("pending/history/", GetRedeemHistoryView)
        ],
    )
)

urlpatterns = unauth_urls + pro_urls
