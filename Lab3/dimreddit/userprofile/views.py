from django.http import HttpResponse
from django.shortcuts import render


def profile_index(request):
    return HttpResponse("<h1>Страница профиля</h1>")

