
from django.urls import path

from . import views

urlpatterns = [
    path('profiles/', views.ProfileCreateView.as_view()),
    path('profiles/<str:profile_id>/', views.ProfileView.as_view()),
    path('profiles/<str:profile_id>/roles', views.ProfileGetRoleView.as_view()),

    path('profiles/current-actions', views.ProfileSetCurrentActionView.as_view()),
    path('profiles/<str:profile_id>/current-actions', views.ProfileGetCurrentActionView.as_view()),

    path('media/<str:media_id>/', views.MediaGetByIdView.as_view()),

    path('medias/youtube/', views.MediaYoutubeCreateView.as_view()),
    path('medias/instagram/', views.MediaInstagramCreateView.as_view()),

    path('medias/download/delete', views.DownloaderDeleteFile.as_view()),
    path('medias/youtube/download', views.DownloaderYoutubeView.as_view()),
    path('medias/instagram/download', views.DownloaderInstagramView.as_view()),

    path('medias/telegram-video-id', views.MediaSetTelegramVideoIdView.as_view()),
    path('medias/telegram-audio-id', views.MediaSetTelegramAudioIdView.as_view()),

    path('profiles/<str:profile_id>/medias/count', views.MediaCountView.as_view()),
    path('profiles/<str:profile_id>/medias/favorite/count', views.MediaFavoriteCountView.as_view()),

    path('profiles/<str:profile_id>/medias/<str:media_id>', views.MediaProfileView.as_view()),
    path('profiles/<str:profile_id>/media', views.MediaForProfileOnCounterView.as_view()),
    path('profiles/<str:profile_id>/media/favorite', views.MediaFavoriteForProfileOnCounterView.as_view()),

    path('profiles/medias/downloads', views.MediaDownloadUpdateView.as_view()),

    path('profiles/medias', views.MediaProfileAddView.as_view()),
    path('profile/media/favorite', views.MediaAddToFavoriteView.as_view()),

    path('profiles/<str:profile_id>/medias/<str:media_id>/downloads', views.MediaDownloadGetView.as_view()),
]
