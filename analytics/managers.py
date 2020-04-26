from django.db.models import Manager, Sum


class ClickManager(Manager):
    def get_count(self, **kwargs):
        return self.filter(**kwargs).aggregate(count=Sum('clicks'))


class ProfileViewManager(Manager):
    def get_count(self, **kwargs):
        return self.filter(**kwargs).aggregate(count=Sum('views'))
