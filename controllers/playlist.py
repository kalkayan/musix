import uuid
import django.shortcuts as S

from django import template
from django import forms
from musix.models import Playlist, Song
from django.contrib.auth.decorators import login_required


def init_user(user):
    p = Playlist(title='liked Songs', user_id=user)
    p.save()


@login_required
def playlist_index(request):
    playlists = Playlist.objects.filter(user_id=request.user._id)
    return S.render(request, 'pages/playlist_index.html', {
        'playlists': playlists
    })


@login_required
def playlist_create(request):
    class PlaylistForm(forms.ModelForm):
        class Meta:
            model = Playlist
            fields = ('title',)

    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            print(form)
        return S.redirect(S.reverse('playlist_index'))


@login_required
def playlist_show(request, slug):
    playlist = Playlist.objects.get(slug=slug)
    songs  = playlist.song.all()
    return S.render(request, 'pages/playlist_show.html', {'playlist': playlist, 'songs': songs})


@login_required
def playlist_song_toggle(request, slug, song):
    from django.http import JsonResponse
    playlist = Playlist.objects.get(slug=slug)
    song = Song.objects.get(slug=song)

    playlist.song.add(song)
    print(song, playlist)
    return JsonResponse('ok', safe=False)