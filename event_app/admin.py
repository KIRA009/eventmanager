from django.contrib import admin

from .models import *

models = [User, College, Link, ProModeFeature, ProPack, ProPackHolder]
for model in models:
    admin.site.register(model)
