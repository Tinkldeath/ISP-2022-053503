from django.http import HttpResponse
from django.shortcuts import render


def forum_index(request):
    return HttpResponse("<h1>Страница формуа</h1>")
