from django.conf.urls import url

from accounts import views

urlpatterns = [
    url(r'^login/$', views.Login.as_view()),
    url(r'^logout/$', views.Logout.as_view()),
    url(r'^register/$', views.Register.as_view()),
]