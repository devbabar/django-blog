from django.conf.urls import url
from django.contrib import admin
from .views import (search, dashboard_future,dashboard_draft,signup,login_view,logout_view,post_list,post_create,post_detail,post_update,post_delete,dashboard)

"""Note: 'name' parameter in url help us to make a dynamic url in templates """

urlpatterns = [
	
	url(r'^signup/$',signup, name='signup'),
	url(r'^accounts/login/$',login_view, name='login'),
    url(r'^logout/$',logout_view, name='logout'),

    # Dashboard Options: urls for $Ajax calls 

    url(r'^dashboard/(?P<id>[\w-]+)/draft/$', dashboard_draft, name='dashboard-draft'),
    url(r'^dashboard/(?P<id>[\w-]+)/future-posts/$', dashboard_future, name='dashboard-future'),
    url(r'^dashboard/(?P<id>[\w-]+)/create-posts/$', post_create, name='dashboard-create'),

    url(r'^dashboard/(?P<id>[\w-]+)/$', dashboard, name='dashboard'),
    url(r'^search/$', search, name='search'),
	url(r'^$', post_list, name='list'),
	url(r'^(?P<slug>[\w-]+)/$', post_detail,name='detail'),
	url(r'^dashboard/(?P<id>[\w-]+)/(?P<slug>[\w-]+)/edit/$', post_update, name='update'),

	url(r'^(?P<slug>[\w-]+)/delete/$', post_delete, name='delete'),    

]