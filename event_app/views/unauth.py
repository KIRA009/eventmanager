from django.contrib.auth import authenticate
from django.utils import timezone as tz
from django.views import View

from event_app.models import User, College, ProModeFeature
from utils import create_token
from event_app.utils import send_email


class RegisterView(View):
    def post(self, request):
        data = request.json
        created, user = User.objects.create_user(data)
        if created:
            return dict(message="User successfully created")
        return dict(error=user, status_code=401)


class CollegeView(View):
    def get(self, request):
        return dict(colleges=[college.detail() for college in College.objects.all()])


class SendValidateEmailView(View):
    def post(self, request):
        scheme = request.META["wsgi.url_scheme"]
        server = request.META["HTTP_HOST"]
        data = request.json
        user = User.objects.get(email=data["email"])
        email = f"""\
                    <html>
                        <head></head>
                        <body style="text-align:left;">
                            <header><img src="https://i.postimg.cc/Gh3gjht5/main-logo.png" height="200px" width="200px">
                            </header><br><br>
                            <div style="text-align:left; font-size:20px;">
                            Hi {user.name},<br><br>
                                Greetings from Team Extremist!<br>
                                To verify your email,<br>
                                please click on the button below<br>
                            </div>
                            <a style="font-size:20px; background-color:#007bff; text-decoration:none; padding-top:5px;
                            padding-bottom:10px; padding-left:10px; padding-right:10px; color:#fff; margin:auto auto;"
                            href="{scheme}://{server}/api/validate/{user.id}/{user.secret}/" type="button">
                            Click here to validate </a><br><br>
                            <p style="font-size:20px;">
                                Thank you,<br>
                                Team Extremist
                            </p><br><br>
                            If you face any problems, feel free to send your queries at xyz@gmail.com
                        </body>
                    </html>
                """
        send_email([data["email"]], "Validate your account", email)
        return dict(message="Email sent")


class CompleteValidateEmailView(View):
    def get(self, request, user_id, secret):
        user = User.objects.get(id=user_id)
        if not user.is_validated:
            if user.secret == secret:
                user.is_validated = True
                user.save()
        return dict(message="Email validated")


class LoginView(View):
    def post(self, request):
        data = request.json
        user = authenticate(
            request, username=data["username"], password=data["password"]
        )
        if user:
            # if not user.is_validated:
            #     return dict(error="Email not verified", status_code=401)
            user.last_login = tz.now()
            user.save()
            return dict(
                data="Successful",
                user=user.detail(),
                token=create_token(
                    username=f"{user.email}$$${user.password}",
                    len_email=len(user.email),
                ),
            )
        return dict(status_code=401, error="Invalid credentials")


class GetUserView(View):
    def post(self, request):
        user = User.objects.get(username=request.json["username"])
        return dict(user=user.detail())


class GetBgView(View):
    def post(self, request):
        user = User.objects.get(username=request.json['username'])
        return dict(
            background_color=user.background_color,
            background_image=user.background_image
        )
