from django.views import View

from event_app.models import ProModeFeature
from event_app.utils import upload_file, delete_file
from event_manager.settings import ICONCONTAINER, PROFILECONTAINER
from utils.exceptions import AccessDenied
from event_app.validators import *


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
    @get_user_schema
    def post(self, request):
        data = request.json
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
        if 'background_color' in data:
            feature.background_color = data["background_color"]
        img = request.FILES.dict()
        if 'photo' in img:
            img = img['photo']
            delete_file(feature.background_image)
            feature.background_image = upload_file(request, img, PROFILECONTAINER)
        if 'link_style' in data:
            feature.link_style = data['link_style']
        feature.save()
        return dict(
            background_color=feature.background_color,
            background_image=feature.background_image,
            link_style=feature.link_style
        )

