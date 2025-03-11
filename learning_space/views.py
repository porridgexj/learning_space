from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template("index.html")
    context = {}
    return HttpResponse(template.render(context, request))

def login(request):
    template = loader.get_template("login.html")
    context = {}
    return HttpResponse(template.render(context, request))

def reserve(request):
    template = loader.get_template("reserve.html")
    context = {}
    return HttpResponse(template.render(context, request))

def favours(request):
    template = loader.get_template("favours.html")
    context = {}
    return HttpResponse(template.render(context, request))
