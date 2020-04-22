from django.contrib import admin

from .models import *

models = [OrderItem, Order]

for model in models:
    admin.site.register(model)
