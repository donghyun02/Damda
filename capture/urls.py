from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view()),
    url(r'^folders/$', views.FolderListCreateView.as_view()),
    url(r'^folders/(?P<pk>[0-9]+)/$', views.FolderRetrieveUpdateDestroyView.as_view()),
    url(r'^tags/$', views.TagListCreateView.as_view()),
    url(r'^tags/(?P<pk>[0-9]+)$', views.TagRetrieveUpdateDestroyView.as_view()),
    url(r'^bookmarks/$', views.BookmarkListCreateView.as_view()),
    url(r'^bookmarks/(?P<pk>[0-9]+)$', views.BookmarkRetrieveUpdateDestroyView.as_view()),
    url(r'^username/$', views.ChangeNameView.as_view()),
    url(r'^profile/$', views.ChangeProfileImageView.as_view()),
    url(r'^test/$', views.TestView.as_view()),
]