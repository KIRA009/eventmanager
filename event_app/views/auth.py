from django.views import View
import uuid
from django.db import transaction
from django.db.utils import IntegrityError

from event_manager.settings import PROFILECONTAINER, ICONCONTAINER
from utils import upload_file, delete_file
from event_app.models import Link


class UploadProfilePicView(View):
    def post(self, request):
        if request.User.profile_pic:
            delete_file(request.User.profile_pic)
        file = request.FILES.dict().get("photo")
        if file is None:
            request.User.profile_pic = None
        else:
            file_name = request.User.username + str(uuid.uuid4()) + file.name
            upload_file(file, file_name, PROFILECONTAINER)
            request.User.profile_pic = f"https://storageeventmanager.blob.core.windows.net/{PROFILECONTAINER}/{file_name}"
        request.User.save()
        return dict(message="Profile pic set successfully", data=request.User.detail())


class UserLinkView(View):
    def get(self, request):
        return dict(links=[link.detail() for link in request.User.links.all()])

    def post(self, request):
        data = request.json
        if "id" in data:
            link_id = data["id"]
            del data["id"]
            link = Link.objects.get(id=link_id)
            if link.user != request.User:
                return dict(error="User not authorized", status_code=401)
            Link.objects.filter(id=link_id).update(**data)
        else:
            link = Link.objects.create(**data, user=request.User)
        return dict(link=link.detail())

    def delete(self, request):
        data = request.json
        Link.objects.get(id=data["id"]).delete()
        return dict(message="The links are deleted")


class UploadIconView(View):
    def post(self, request):
        data = request.POST.dict()
        file = request.FILES.dict().get("photo")
        link = Link.objects.filter(id=data["link_id"], user=request.User).first()
        if link:
            if link.icon:
                delete_file(link.icon)
            file_name = request.User.username + str(uuid.uuid4()) + file.name
            upload_file(file, file_name, ICONCONTAINER)
            link.icon = f"https://storageeventmanager.blob.core.windows.net/{ICONCONTAINER}/{file_name}"
            link.save()
            return dict(link=link.detail())
        return dict(error="Link not found", status_code=404)


class UpdateLinkSequenceView(View):
    def post(self, request):
        try:
            with transaction.atomic():
                links = request.json["links"]
                for i in range(len(links)):
                    link = Link.objects.get(id=links[i])
                    link.index = i
                    link.save()
                return dict(links=[link.detail() for link in request.User.links.all()])
        except IntegrityError:
            return dict(error="Some error happened", status_code=501)
