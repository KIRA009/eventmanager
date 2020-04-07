from django.views import View
import uuid

from event_manager.settings import PROFILECONTAINER
from utils import upload_file, delete_file


class UploadProfilePicView(View):
    def post(self, request):
        if request.user.profile_pic != "":
            delete_file(request.user.profile_pic)
        file = request.FILES.dict()["photo"]
        file_name = request.user.username + str(uuid.uuid4()) + file.name
        upload_file(file, file_name, PROFILECONTAINER)
        request.user.profile_pic = f"https://storageeventmanager.blob.core.windows.net/{PROFILECONTAINER}/{file_name}"
        request.user.save()
        return dict(message="Profile pic set successfully", data=request.user.detail())
