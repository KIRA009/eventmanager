from django.views import View
from django.utils.timezone import now, localdate, timedelta

from analytics.models import Click, ProfileView, LifeTimeClick, LifeTimeView
from event_app.models import Link, User
from utils.exceptions import NotFound


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
        try:
            user = User.objects.get(username=data['username'])
            view, _ = ProfileView.objects.get_or_create(user=user, day=localdate(now()))
            view.views += 1
            view.save()
            return dict(message="View added successfully")
        except User.DoesNotExist:
            raise NotFound('User does not exist')


class GetLinkData(View):
    def get(self, request):
        month_ago = localdate(now()) - timedelta(days=28)
        analytics = []
        if request.User.user_type == 'pro':
            for link in request.User.links.all():
                clicks = []
                total_clicks = 0
                i = 0
                for click in link.clicks.filter(day__gte=month_ago).order_by('day'):
                    while click.day != month_ago + timedelta(days=i):
                        clicks.append(dict(day=month_ago + timedelta(days=i), clicks=0))
                        i += 1
                    i += 1
                    clicks.append(dict(day=click.day, clicks=click.clicks))
                    total_clicks += click.clicks
                while i <= 28:
                    clicks.append(dict(day=month_ago + timedelta(days=i), clicks=0))
                    i += 1
                lifetime_clicks = LifeTimeClick.objects.get_or_create(link=link)[0].clicks + total_clicks
                analytics.append(dict(link_id=link.id, clicks=clicks, total_clicks=total_clicks,
                                      lifetime_clicks=lifetime_clicks))
            return dict(analytics=analytics)
        else:
            for link in request.User.links.all():
                total_clicks = link.clicks.get_count(day__gte=month_ago, link__user=request.User)['count']
                if total_clicks is None:
                    total_clicks = 0
                lifetime_clicks = LifeTimeClick.objects.get_or_create(link=link)[0].clicks + total_clicks
                analytics.append(dict(link_id=link.id, clicks=[], total_clicks=total_clicks,
                                      lifetime_clicks=lifetime_clicks))
            return dict(analytics=analytics)


class GetProfileViewData(View):
    def get(self, request):
        month_ago = localdate(now()) - timedelta(days=28)
        if request.User.user_type == 'pro':
            i = 0
            analytics = []
            total_views = 0
            for day in ProfileView.objects.filter(user=request.User, day__gte=month_ago).order_by('day'):
                while day.day != month_ago + timedelta(days=i):
                    analytics.append(dict(views=0, day=month_ago + timedelta(days=i)))
                    i += 1
                i += 1
                analytics.append(dict(views=day.views, day=day.day))
                total_views += day.views
            while i <= 28:
                analytics.append(dict(views=0, day=month_ago + timedelta(days=i)))
                i += 1
            lifetime_views = LifeTimeView.objects.get_or_create(user=request.User)[0].views + total_views
            return dict(analytics=analytics, lifetime_views=lifetime_views, total_views=total_views)
        else:
            views = ProfileView.objects.get_count(day__gte=month_ago, user=request.User)['count']
            if views is None:
                views = 0
            lifetime_views = LifeTimeView.objects.get_or_create(user=request.User)[0].views + views
            return dict(views=views, lifetime_views=lifetime_views)
