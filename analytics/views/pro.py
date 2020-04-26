from django.views import View
from django.utils.timezone import now, localdate

from analytics.models import Click, ProfileView
from event_app.models import Link, User


class AddClickView(View):
    def post(self, request):
        data = request.json
        link = Link.objects.get(id=data["link_id"])
        link, _ = Click.objects.get_or_create(link=link, day=localdate(now()))
        link.clicks += 1
        link.save()
        return dict(message="Click added successfully")


class AddViewView(View):
    def post(self, request):
        data = request.json
        user = User.objects.get(username=data['username'])
        view, _ = ProfileView.objects.get_or_create(user=user, day=tz.now().date())
        view.views += 1
        view.save()
        return dict(message="View added successfully")


class GetLinkData(View):
    def post(self, request):
        data = request.json
        if request.User.user_type == 'pro':
            analytics = Click.objects.filter(link__user=request.User, link__id=data['link_id'])
            return dict(analytics=[_.detail() for _ in analytics])
        else:
            return dict(clicks=Click.objects.get_count(link__user=request.User, link__id=data['link_id'])['count'])


class GetProfileViewData(View):
    def get(self, request):
        if request.User.user_type == 'pro':
            analytics = ProfileView.objects.filter(user=request.User)
            return dict(analytics=[_.detail() for _ in analytics])
        else:
            return dict(views=ProfileView.objects.get_count(user=request.User)['count'])
