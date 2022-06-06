from django.urls import path
from .views import home, topic, tred, signin, signout, signup

urlpatterns = [
    path('', home, name='home'),
    path('topic/<slug>', topic, name='topic'),
    path('treds/<slug>', tred, name='tred'),
    path('signin', signin, name='signin'),
    path('signup', signup, name='signup'),
    path('signout', signout, name='signout')
]