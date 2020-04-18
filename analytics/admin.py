from django.contrib import admin

from .models import *

models = [Click]

for model in models:
    admin.site.register(model)
