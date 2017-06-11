from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^loggedIn$', views.loggedIn),
    url(r'^register$', views.register),
    url(r'^registered$', views.registered),
    url(r'^dashboard$', views.dashboard),
    url(r'^home$', views.home),
    url(r'^reflection$', views.reflection),
    url(r'^essay$', views.essay),
    url(r'^delete/(?P<eid>\d+)$', views.delete)

]
