from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.handlers.wsgi import WSGIRequest


def index(request: WSGIRequest):
    return render(request, "shop/index.html")


def redirect_to_index(request, exception=None):
    return HttpResponseRedirect('/')
