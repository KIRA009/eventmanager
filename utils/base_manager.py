from django.db.models import Manager
from .base_queryset import BaseQuerySet


class BaseManager(Manager.from_queryset(BaseQuerySet)):
    pass
