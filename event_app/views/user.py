from django.views import View
from django.contrib.auth import login, authenticate

from event_app.models import User, College


class RegisterView(View):
    def post(self, request):
        data = request.json
        user = User.objects.create_user(data)
        return dict(secret=user.secret)


class UpdateView(View):
    def post(self, request):
        data = request.json
        updated, user = User.objects.update_user(data)
        if updated:
            return dict(secret=user.secret)
        return dict(message="No such user", status_code=404)


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
            login(request, user)
            return dict(data="Successful")
        return dict(status_code=401, error="Invalid credentials")


class CheckView(View):
    def get(self, request):
        return dict(logged_in=request.user.is_authenticated)
