from django.conf.urls import patterns, include, url
from .views import (
	PostDetailsAPIView,
	PostListAPIView,
	PostUpdateAPIView,
	PostCreateAPIView,
	details,
	edit
	)

urlpatterns = patterns('',

    url(r'^$',PostListAPIView.as_view(), name='list'),
    url(r'^details/$', details , name = 'details'),
    url(r'^add_edit/$', edit , name = 'add_edit'),
    url(r'^create/$', PostCreateAPIView.as_view() , name = 'create'),
    # user_info/1/
    url(r'^(?P<pk>\d+)/$', PostDetailsAPIView.as_view(), name='details'),
    url(r'^(?P<pk>\d+)/edit/$', PostUpdateAPIView.as_view(), name='update')

)