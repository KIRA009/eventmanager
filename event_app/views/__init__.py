from django.views import View
from django.shortcuts import render

from .unauth import *
from .auth import *


def index(request):
    return render(request, "index.html")


def manifest(request):
    return render(request, "manifest.json")
