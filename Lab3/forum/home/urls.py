from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('detail/<slug>', views.detail, name='detail'),
    path('treds/<slug>', views.treds, name='treds')
]