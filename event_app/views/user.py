from django.views import View
from django.contrib.auth import authenticate
from django.utils import timezone as tz

from event_app.models import User, College
from utils import create_token


class RegisterView(View):
    def post(self, request):
        data = request.json
        created, user = User.objects.create_user(data)
        if created:
            return dict(secret=user.secret)
        return dict(error=user, status_code=401)


class UpdateView(View):
    def post(self, request):
        data = request.json
        updated, user = User.objects.update_user(data)
        if updated:
            return dict(secret=user.secret)
        return dict(message=user, status_code=404)


class CollegeView(View):
    def get(self, request):
        return dict(colleges=[college.detail() for college in College.objects.all()])


class LoginView(View):
    def post(self, request):
        data = request.json
        user = authenticate(
            request, username=data["username"], password=data["password"]
        )
        if user:
            user.last_login = tz.now()
            user.save()
            return dict(
                data="Successful",
                token=create_token(
                    username=f"{user.email}$$${user.password}",
                    login_time=user.last_login.isoformat(),
                    len_email=len(user.email),
                ),
            )
        return dict(status_code=401, error="Invalid credentials")
