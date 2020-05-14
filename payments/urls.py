from django.urls import path

from .views import *
from utils.decorators import login_required
from pro.utils import pro_required

auth_urls = list(
    map(lambda x: path(x[0], login_required(x[1].as_view())), [
        ("subscribe/", SubscriptionView),
        ("cancel/", CancelSubscriptionView),
    ])
)

unauth_urls = list(
    map(lambda x: path(x[0], x[1].as_view()), [
        ("order/", OrderView),
        ('webhook/', PaymentWebhookView)
    ])
)

pro_urls = list(
    map(lambda x: path(x[0], pro_required(x[1].as_view())), [
        ("products/sold/update/", UpdateSoldProductsView),
        ("products/sold/get/", GetSoldProductsView),
    ])
)

urlpatterns = auth_urls + unauth_urls + pro_urls
