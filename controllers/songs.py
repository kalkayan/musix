import uuid
import django.shortcuts as S

from django import template
from django import forms
from musix.models import Song
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.decorators import login_required


@login_required
def songs_index(request):
    songs = Song.objects.all().values()
    return S.render(request, 'pages/songs_index.html', {'songs': songs})


@login_required
def songs_create(request):
    class SongUploadForm(forms.ModelForm):
        class Meta:
            model = Song
            fields = ('title', 'cover', 'audio', 'description',)

    if request.method == 'POST' and request.FILES['cover']:
        form = SongUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return S.redirect(S.reverse('songs_index'))
    else:
        form = SongUploadForm()
    return S.render(request, 'pages/songs_create.html', {'form': form})


@login_required
def songs_show(request, song_id):
    song = Song.objects.get(slug=song_id)
    return S.render(request, 'pages/songs_show.html', {'song': song})
