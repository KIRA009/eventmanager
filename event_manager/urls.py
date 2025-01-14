"""event_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

import event_app.urls
import analytics.urls
import payments.urls
import pro.urls
import notifications.urls
import shipping.urls
import logger.urls

from event_app.views import *

urlpatterns = [
    path("admin-dashboard/", admin.site.urls),

    path("api/", include(event_app.urls)),
    path("pro/", include(pro.urls)),
    path("analytics/", include(analytics.urls)),
    path("payment/", include(payments.urls)),
    path("notifications/", include(notifications.urls)),
    path("shipping/", include(shipping.urls)),
    path("log/", include(logger.urls)),

    re_path(
        r"^forgot-password/?$",
        ForgotPwdView.as_view(),
        name="forgot-password",
    ),
    path(
        "reset-password/<str:username>/<str:secret>/",
        ResetPwdView.as_view(),
        name="reset-password",
    ),
    path("manifest.json", manifest),
    re_path(r"^.*", index, name="index"),
]
