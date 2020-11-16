"""musix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import musix.views as V

from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('', V.welcome, name='welcome'),
    path('oauth/github/authorize', V.oauth_github_authorize,
         name='oauth_github_authorize'),
    path('oauth/github/callback', V.oauth_github_callback,
         name='oauth_github_callback'),
    # Songs
    path('app/', include([
        path('', V.dashboard, name='dashboard'),
        path('songs/', include([
            path('index', V.songs_index, name='songs_index'),
            path('create', V.songs_create, name='songs_create'),
            path('play/<slug:song_id>', V.songs_show, name='songs_show')
        ])),
    ])),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
