from django.conf import settings
from django.conf.urls import url,include
from django.conf.urls.static import static
from django.contrib import admin

""" Note: 'namespace' helps us to make urls to the particular app, we use it when we have a set of urls """

urlpatterns = [
    url(r'^admin/', admin.site.urls),
	url(r'^posts/', include('posts.urls', namespace='posts')),    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]