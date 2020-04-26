from django.views import View
from django.db import transaction
from django.db.utils import IntegrityError

from event_manager.settings import PROFILECONTAINER, ICONCONTAINER
from event_app.utils import upload_file, delete_file
from event_app.models import Link, ProModeFeature, User


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
        return dict(links=[link.detail() for link in request.User.links.all()])

    def post(self, request):
        data = request.json
        if "id" in data:
            link_id = data["id"]
            del data["id"]
            try:
                link = Link.objects.get(id=link_id, user=request.User)
            except Link.DoesNotExist:
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
            if file is None:
                link.icon = None
            else:
                link.icon = upload_file(request, file, ICONCONTAINER)
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


class SetBgView(View):
    def post(self, request):
        data = request.POST.dict()
        user = request.User
        user.background_color = data.get("background_color", None)
        img = request.FILES.dict().get('photo')
        delete_file(user.background_image)
        user.background_image = upload_file(request, img, PROFILECONTAINER)
        user.save()
        return dict(
            background_color=user.background_color,
            background_image=user.background_image
        )


class UpdateUserDetailsView(View):
    def post(self, request):
        user = request.User
        data = request.json
        for i in ['user_type', 'is_validated', 'secret', 'is_staff', 'is_superuser', 'password', 'id']:
            if i in data:
                del data[i]
        try:
            User.objects.filter(id=user.id).update(**data)
        except IntegrityError as e:
            return dict(error=str(e), status_code=401)
        user = User.objects.get(id=user.id)
        return dict(user=user.detail())