from django.http import HttpResponse
from django.shortcuts import render


def login_index(request):
    return HttpResponse("<h1>Страница логина</h1>")

