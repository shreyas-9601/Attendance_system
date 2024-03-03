from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from .views import HomePageView, Attend

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('video_feed', views.video_feed, name="video_feed"),
    path('attendance/', Attend.as_view(), name='attendance')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
