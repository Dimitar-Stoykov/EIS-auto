from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from eis_project.eisauto.views import stream_media

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('eis_project.eisauto.urls')),
]

# Serve uploaded media files with Range request support (needed for video seeking)
if settings.DEBUG:
    urlpatterns += [path('media/<path:path>', stream_media)]

