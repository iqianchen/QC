from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^getUserInfo/(?P<code>[0-9a-zA-Z]+)',views.getUserInfo, name="getUserInfo"),
    url(r'^addUser$',views.addUser, name="addUser"),
    url(r'^update$', views.update, name="update"),
    url(r'^delete/(?P<userId>[0-9a-zA-Z]+)', views.delete, name="delete"),
    url(r'^getJSAPI/',views.getJSAPI,name="getJSAPI")
]