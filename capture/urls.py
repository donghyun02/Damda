from django.conf.urls import url

from capture import views

urlpatterns = [
    url(r'^$', views.Index.as_view()),
]