from django.http import HttpResponse
from django.shortcuts import render


def signup_index(request):
    return HttpResponse("<h1>Страница регистрации</h1>")
