from django.contrib import admin

from .models import *

models = [User, College, Link, ProModeFeature]
for model in models:
    admin.site.register(model)
