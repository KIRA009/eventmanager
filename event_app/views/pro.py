from django.views import View

from event_app.models import ProModeFeature
from utils import upload_file, delete_file
from event_manager.settings import ICONCONTAINER


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


class ProModeBgView(View):
    def post(self, request):
        data = request.json
        feature, _ = ProModeFeature.objects.get_or_create(user=request.User)
        feature.background_color = data["background_color"]
        feature.save()
        return dict(feature=feature.detail())


class ProModeView(View):
    def get(self, request):
        return dict(feature=request.User.feature.get().detail())
