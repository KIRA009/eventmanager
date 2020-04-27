from django.urls import path

from .utils import admin_required
from .views import DeleteLogsView

urlpatterns = list(
    map(lambda x: path(x[0], admin_required(x[1].as_view()), name=x[2]), [
        ('delete_logs/', DeleteLogsView, 'delete_logs')
    ])
)