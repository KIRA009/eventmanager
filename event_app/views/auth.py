from django.views import View
from django.db import transaction
from django.db.utils import IntegrityError

from event_manager.settings import PROFILECONTAINER, ICONCONTAINER
from event_app.utils import upload_file
from utils.tasks import delete_file
from event_app.models import Link
from utils.token import create_token
from utils.exceptions import AccessDenied


class UploadProfilePicView(View):
    def post(self, request):
        if request.User.profile_pic:
            delete_file(request.User.profile_pic)
        file = request.FILES.dict().get("photo")
        if file is None:
            request.User.profile_pic = None
        else:
            request.User.profile_pic = upload_file(request, file, PROFILECONTAINER)
        request.User.save()
        return dict(message="Profile pic set successfully", data=request.User.detail())


class UserLinkView(View):
    def get(self, request):
        return dict(links=[_.detail() for _ in request.User.links.all()])

    def post(self, request):
        data = request.json
        if "id" in data:
            link_id = data["id"]
            del data["id"]
            link = Link.objects.get(id=link_id, user=request.User)
            Link.objects.filter(id=link_id).update(**data)
        else:
            link = Link.objects.create(**data, user=request.User)
        return dict(link=link.detail())

    def delete(self, request):
        data = request.json
        link = Link.objects.get(id=data["id"])
        link.delete()
        return dict(message="The links are deleted")


class UploadIconView(View):
    def post(self, request):
        data = request.POST.dict()
        file = request.FILES.dict().get("photo")
        link = Link.objects.get(id=data["link_id"], user=request.User)
        if link.icon:
            delete_file(link.icon)
        if file is None:
            link.icon = None
        else:
            link.icon = upload_file(request, file, ICONCONTAINER)
        link.save()
        return dict(link=link.detail())


class UpdateLinkSequenceView(View):
    def post(self, request):
        try:
            with transaction.atomic():
                links = request.json["links"]
                for i in range(len(links)):
                    link = Link.objects.get(id=links[i])
                    if link:
                        link.index = i
                        link.save()
                return dict(links=[_.detail() for _ in request.User.links.all()])
        except IntegrityError:
            return dict(error="Some error happened", status_code=501)


class UpdateUserDetailsView(View):
    def post(self, request):
        user = request.User
        data = request.json
        for i in data:
            if i not in ['name', 'username', 'email']:
                del data[i]
        if 'username' in data:
            if '@' in data:
                raise AccessDenied('Cannot have @ in username')
            data['username'] = data['username'].lower()
        user.name = data['name']
        user.username = data['username']
        user.email = data['email']
        user.save()
        return dict(
            user=user.detail(),
            token=create_token(
                username=f"{user.email}$$${user.password}",
                len_email=len(user.email),
            ))


class CheckAuthView(View):
    def get(self, request):
        return dict()
