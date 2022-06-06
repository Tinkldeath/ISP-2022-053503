from django.urls import path
from .views import home, topic, tred, signin, signout, signup, update, add_topic, add_tred, search_view, profile

urlpatterns = [
    path('', home, name='home'),
    path('topic/<slug>', topic, name='topic'),
    path('treds/<slug>', tred, name='tred'),
    path('signin', signin, name='signin'),
    path('signup', signup, name='signup'),
    path('signout', signout, name='signout'),
    path('update', update, name='update'),
    path('topics/add', add_topic, name='addtopic'),
    path('treds/new/add', add_tred, name='addtred'),
    path('search', search_view, name='search'),
    path('users/<slug>', profile, name='profile')
]
