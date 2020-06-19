from django.urls import path

from .views import *
from pro.utils import pro_required

pro_urls = list(
    map(lambda x: path(x[0], pro_required(x[1].as_view())), [
        ('options/', GetShipmentExpenseView),
        ("create/", CreateShippingView)
    ])
)

urlpatterns = pro_urls
