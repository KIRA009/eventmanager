from django.shortcuts import render, redirect

from .unauth import *
from .auth import *
from .pro import *
from utils.email import send_email


def index(request):
    if request.path_info == 'admin-dashboard':
        return redirect(request.path_info + '/')
    return render(request, "index.html")


def manifest(request):
    return render(request, "manifest.json")


class ForgotPwdView(View):
    def get(self, request):
        return render(request, "forgot-password.html")

    def post(self, request):
        email = request.POST.dict().get("email")
        if not email:
            return redirect("/forgot-password/")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return redirect("/forgot-password/")
        email = f"""
            <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <div style="min-width:100%;box-sizing:border-box;color:#0a0a0a;font-family:'Cereal',Helvetica,Arial,sans-serif;font-weight:normal;padding:0;margin:0;text-align:left;font-size:16px;line-height:19px;width:100%!important">
        <div style="opacity:0;color:transparent;height:0;width:0;font-size:0px;display:none!important"></div>
        <table dir="ltr" style="border-spacing:0;border-collapse:collapse;vertical-align:top;background:#f3f3f3;height:100%;width:100%;color:#0a0a0a;font-family:'Cereal',Helvetica,Arial,sans-serif;font-weight:normal;padding:0;margin:0;text-align:left;font-size:16px;line-height:19px;margin-bottom:0px!important;background-color:white">
        <tbody><tr style="padding:0;vertical-align:top;text-align:left">
        <td align="center" valign="top" style="word-wrap:break-word;vertical-align:top;color:#0a0a0a;font-family:'Cereal',Helvetica,Arial,sans-serif;font-weight:normal;padding:0;margin:0;text-align:left;font-size:16px;line-height:19px;border-collapse:collapse!important">
        <center style="width:100%;min-width:580px">
        <table style="border-spacing:0;border-collapse:collapse;padding:0;vertical-align:top;background:#fefefe;width:580px;margin:0 auto;text-align:inherit;max-width:580px">
        <tbody><tr style="padding:0;vertical-align:top;text-align:left">
        <td style="word-wrap:break-word;vertical-align:top;color:#0a0a0a;font-family:'Cereal',Helvetica,Arial,sans-serif;font-weight:normal;padding:0;margin:0;text-align:left;font-size:16px;line-height:19px;border-collapse:collapse!important">
        <div>
        <table style="border-spacing:0;border-collapse:collapse;vertical-align:top;text-align:left;padding:0;width:100%;display:table">
        <tbody><tr style="padding:0;vertical-align:top;text-align:left">
        <th style="color:#0a0a0a;font-family:'Cereal',Helvetica,Arial,sans-serif;font-weight:normal;padding:0;text-align:left;font-size:16px;line-height:19px;margin:0 auto;padding-bottom:16px;width:564px;padding-left:16px;padding-right:16px">
        <a href="http://{request.META['HTTP_HOST']}/">
        <img align="center" alt="event_manager" src="https://i.postimg.cc/Gh3gjht5/main-logo.png" style="outline:none;text-decoration:none;width:50px;max-width:100%;clear:both;display:block;border:none;padding-bottom:16px;padding-top:48px;height:auto"> </a>
        </th>
        </tr>
        </tbody></table>
        </div>
        <div>
        <table style="border-spacing:0;border-collapse:collapse;vertical-align:top;text-align:left;padding:0;width:100%;display:table">
        <tbody><tr style="padding:0;vertical-align:top;text-align:left">
        <th style="color:#0a0a0a;font-family:'Cereal',Helvetica,Arial,sans-serif;font-weight:normal;padding:0;text-align:left;font-size:16px;line-height:19px;margin:0 auto;padding-bottom:16px;width:564px;padding-left:16px;padding-right:16px">
        <p style="padding:0;margin:0;font-family:&quot;Cereal&quot;,&quot;Helvetica&quot;,Helvetica,Arial,sans-serif;font-weight:300;color:#484848;font-size:18px;line-height:1.4;text-align:left;margin-bottom:0px!important">
        Hi {user.username},
        </p>
        </th>
        </tr>
        </tbody></table>
        </div>
        <div>
        <table style="border-spacing:0;border-collapse:collapse;vertical-align:top;text-align:left;padding:0;width:100%;display:table">
        <tbody><tr style="padding:0;vertical-align:top;text-align:left">
        <th style="color:#0a0a0a;font-family:'Cereal',Helvetica,Arial,sans-serif;font-weight:normal;padding:0;text-align:left;font-size:16px;line-height:19px;margin:0 auto;padding-bottom:16px;width:564px;padding-left:16px;padding-right:16px">
        <p style="padding:0;margin:0;font-family:&quot;Cereal&quot;,&quot;Helvetica&quot;,Helvetica,Arial,sans-serif;font-weight:300;color:#484848;font-size:18px;line-height:1.4;text-align:left;margin-bottom:0px!important">
        We’ve received a request to reset your password.
        </p>
        </th>
        </tr>
        </tbody></table>
        </div>
        <div>
        <table style="border-spacing:0;border-collapse:collapse;vertical-align:top;text-align:left;padding:0;width:100%;display:table">
        <tbody><tr style="padding:0;vertical-align:top;text-align:left">
        <th style="color:#0a0a0a;font-family:'Cereal',Helvetica,Arial,sans-serif;font-weight:normal;padding:0;text-align:left;font-size:16px;line-height:19px;margin:0 auto;padding-bottom:16px;width:564px;padding-left:16px;padding-right:16px">
        <p style="padding:0;margin:0;font-family:&quot;Cereal&quot;,&quot;Helvetica&quot;,Helvetica,Arial,sans-serif;font-weight:300;color:#484848;font-size:18px;line-height:1.4;text-align:left;margin-bottom:0px!important">
        If you didn’t make the request, just ignore this message. Otherwise, you can reset your password.
        </p>
        </th>
        </tr>
        </tbody></table>
        </div>
        <div>
        <table style="border-spacing:0;border-collapse:collapse;vertical-align:top;text-align:left;padding:0;width:100%;display:table">
        <tbody><tr style="padding:0;vertical-align:top;text-align:left">
        <th style="color:#0a0a0a;font-family:'Cereal',Helvetica,Arial,sans-serif;font-weight:normal;padding:0;margin:0;text-align:left;font-size:16px;line-height:19px;padding-left:16px;padding-right:16px">
        <a href="http://{request.META['HTTP_HOST']}/reset-password/{user.username}/{user.secret}/" style="font-family:'Cereal',Helvetica,Arial,sans-serif;font-weight:normal;margin:0;text-align:left;line-height:1.3;color:#2199e8;text-decoration:none;background-color:#ff5a5f;border-radius:4px;display:inline-block;padding:12px 24px 12px 24px" target="_blank">
        <p style="font-weight:normal;padding:0;margin:0;text-align:center;font-family:&quot;Cereal&quot;,&quot;Helvetica&quot;,Helvetica,Arial,sans-serif;color:white;font-size:18px;line-height:26px;margin-bottom:0px!important">
        Reset your password
        </p>
        </a>
        </th>
        </tr>
        </tbody></table>
        </div>
        <div style="padding-top:24px">
        <table style="border-spacing:0;border-collapse:collapse;vertical-align:top;text-align:left;padding:0;width:100%;display:table">
        <tbody><tr style="padding:0;vertical-align:top;text-align:left">
        <th style="color:#0a0a0a;font-family:'Cereal',Helvetica,Arial,sans-serif;font-weight:normal;padding:0;text-align:left;font-size:16px;line-height:19px;margin:0 auto;padding-bottom:16px;width:564px;padding-left:16px;padding-right:16px">
        <p style="padding:0;margin:0;font-family:&quot;Cereal&quot;,&quot;Helvetica&quot;,Helvetica,Arial,sans-serif;font-weight:300;color:#484848;font-size:18px;line-height:1.4;text-align:left;margin-bottom:0px!important">
        Thanks</p>
        </th>
        </tr>
        </tbody></table>
        </div>
        </td>
        </tr>
        </tbody></table>
        </center>
        </td>
        </tr>
        </tbody></table>
        <div style="white-space:nowrap;font:15px courier;line-height:0;color:white">
        &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;
        &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;
        &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;
        </div>
        </div>
</body>
</html>
            """
        send_email([user.email], "Reset password", email)
        return redirect("/forgot-password/")


class ResetPwdView(View):
    def get(self, request, username, secret):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return redirect("/forgot-password/")
        if str(user.secret) != secret:
            return redirect("/forgot-password/")
        return render(
            request,
            "reset-password.html",
            context=dict(username=username, secret=secret),
        )

    def post(self, request, username, secret):
        password = request.POST.dict().get("password")
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return redirect("/forgot-password/")
        if str(user.secret) != secret:
            return redirect("/forgot-password/")
        user.change_password(password)
        if not user.is_validated:
            user.is_validated = True
            user.save()
        return redirect("/")
