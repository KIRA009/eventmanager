from django.views import View

from event_app.models import ProModeFeature
from event_app.utils import upload_file, delete_file
from event_manager.settings import ICONCONTAINER, PROFILECONTAINER
from utils.exceptions import AccessDenied


class ProModeHeaderView(View):
    def post(self, request):
        data = request.POST.dict()
        file = request.FILES.dict().get("icon")
        feature, _ = ProModeFeature.objects.get_or_create(user=request.User)
        if "header_text" in data:
            feature.header_text = data["header_text"]
        if file:
            if feature.header_icon:
                delete_file(feature.header_icon)
            feature.header_icon = upload_file(request, file, ICONCONTAINER)
        feature.save()
        return dict(feature=feature.detail())


class ProModeView(View):
    def post(self, request):
        data = request.json
        if 'username' not in data:
            raise AccessDenied("Username not found")
        feature = ProModeFeature.objects.filter(
            user__username=data['username']
        ).first()
        if feature:
            return dict(feature=feature.detail())
        return dict(feature=None)


class SetBgView(View):
    def post(self, request):
        data = request.POST.dict()
        feature, _ = ProModeFeature.objects.get_or_create(user=request.User)
        feature.background_color = data.get("background_color", None)
        img = request.FILES.dict().get('photo')
        delete_file(feature.background_image)
        feature.background_image = upload_file(request, img, PROFILECONTAINER)
        feature.link_style = data['link_style']
        feature.save()
        return dict(
            background_color=feature.background_color,
            background_image=feature.background_image,
            link_style=feature.link_style
        )

