from django.contrib import admin
from django.urls import path

from .views import VideosApi, VideoMetadataApi

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', VideosApi.as_view()),
    path('<int:video_id>', VideoMetadataApi.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
