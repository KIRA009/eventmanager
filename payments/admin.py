from django.contrib import admin

from .models import *
from utils.base_admin import BaseAdmin

admin.site.register([OrderItem, Order, Subscription], BaseAdmin)
