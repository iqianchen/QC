from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^scan/(?P<barcode>[0-9a-zA-Z]+)', views.getGoodsItem,name='getGoodsItem'),
    url(r'^test', views.test, name="test"),
    url(r'^updateGoods/',views.updataGoods,name="updataGoods")
]