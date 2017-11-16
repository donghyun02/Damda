from django.conf.urls import url

from capture import views

urlpatterns = [
    url(r'^$', views.Index.as_view()),
    url(r'^folders/$', views.FolderView.as_view()),
    url(r'^folders/delete/$', views.FolderDestroyView.as_view()),
    url(r'^tags/$', views.TagView.as_view()),
    url(r'^tags/delete/$', views.TagDestroyView.as_view()),
    url(r'^bookmarks/$', views.BookmarkView.as_view()),
    url(r'^username/$', views.ChangeNameView.as_view()),
]