from django.contrib import admin

from .models import *

models = [OrderItem, Order, Subscription]

for model in models:
    admin.site.register(model)
