from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^addTest$',views.addTest, name="addTest")
]