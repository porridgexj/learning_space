from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template("index.html")
    context = {"is_home": True}
    return HttpResponse(template.render(context, request))


def login(request):
    template = loader.get_template("login.html")
    context = {"is_login_page": True}
    return HttpResponse(template.render(context, request))


def reserve(request, id):
    template = loader.get_template("reserve.html")
    context = {"is_reserve_page": True}
    return HttpResponse(template.render(context, request))


def comments(request, id):
    template = loader.get_template("comments.html")
    context = {"is_comments_page": True}
    return HttpResponse(template.render(context, request))


def favours(request):
    template = loader.get_template("favours.html")
    context = {}
    return HttpResponse(template.render(context, request))


def reservations(request):
    template = loader.get_template("reservations.html")
    context = {"is_reservations_page": True}
    return HttpResponse(template.render(context, request))
