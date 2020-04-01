from django.views import View

from .models import User


class Register(View):
    def post(self, request):
        data = request.json
        user = User.objects.create_user(data)
        return dict(secret=user.secret)


class Update(View):
    def post(self, request):
        data = request.json
        updated, user = User.objects.update_user(data)
        if updated:
            return dict(secret=user.secret)
        return dict(message="No such user", status_code=404)
