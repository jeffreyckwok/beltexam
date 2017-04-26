from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name ="index"),
    url(r'^register$', views.register, name = "register"),
    url(r'^success$', views.success, name = "success"),
    url(r'^login$', views.login, name = "login"),
    url(r'^logout$', views.logout, name = "logout"),
    url(r'^add$', views.add, name = "add"),
    url(r'^jointrip/(?P<id>\d+)?$', views.jointrip, name = "jointrip"),
    url(r'^travels/destination/(?P<id>\d+)?$', views.viewdestination, name = "viewdestination"),
    url(r'^addtrip$', views.addtrip, name = "addtrip")
]
