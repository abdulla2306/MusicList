from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .forms import MusicForm, AuthorForm
from .models import Music, Author


def get_music(request):
    musics = Music.objects.all()
    return render(request, 'music/music_list.html', {'musics': musics})

def music_detail(request, pk):
    music = get_object_or_404(Music, pk=pk)
    return render(request, 'music/music_detail.html', {'music': music})

def create_music(request):
    authors = Author.objects.all()
    if request.method == 'POST':
        form = MusicForm(request.POST)
        if form.is_valid():
            music = form.save(commit=False)
            music.created_at = timezone.now()
            music.updated_at = timezone.now()
            music.save()
            return redirect('music_list')
    else:
        form = MusicForm()

    return render(request, 'music/create_music.html', {'form': form, 'authors': authors})


def edit_music(request, pk):
    music = get_object_or_404(Music, pk=pk)
    authors = Author.objects.all()

    if request.method == 'POST':
        form = MusicForm(request.POST, instance=music)
        if form.is_valid():
            music = form.save(commit=False)
            music.updated_at = timezone.now()
            music.save()
            return redirect('music_detail', pk=music.pk)
    else:
        form = MusicForm(instance=music)

    return render(request, 'music/edit_music.html', {'form': form, 'music': music, 'authors': authors})

def delete_music(request, pk):
    music = get_object_or_404(Music, pk=pk)
    if request.method == 'POST':
        music.delete()
        return redirect('music_list')
    return render(request, 'music/music_delete.html', {'music': music})

# Author views
def create_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('author_list')
    else:
        form = AuthorForm()

    return render(request, 'author/create-author.html', {'form': form})

def get_authors(request):
    authors = Author.objects.all()
    return render(request, 'author/author_list.html', {'authors': authors})
def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    return render(request, 'author/author_detail.html', {'author': author})


def edit_author(request, pk):
    author = get_object_or_404(Author, pk=pk)

    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect('author_list')
    else:
        form = AuthorForm(instance=author)

    return render(request, 'author/author_edit.html', {'form': form, 'author': author})


def delete_author(request, pk):
    author = get_object_or_404(Author, pk=pk)

    if request.method == 'POST':
        author.delete()
        return redirect('author_list')

    return render(request, 'author/author_delete.html', {'author': author})