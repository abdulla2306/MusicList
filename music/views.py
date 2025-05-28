import openpyxl
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils import timezone

from user.models import CustomUser
from .forms import MusicForm, AuthorForm, EmailNotificationForm
from .models import Music, Author


def get_music(request):
    q = request.GET.get('q')
    musics = Music.objects.all()

    if q:
        musics = musics.filter(
            Q(text__icontains=q) |
            Q(genre__icontains=q)
        )

    paginator = Paginator(musics, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    context = {
        'musics': page_obj,
        'page_obj': page_obj,
        'q': q,
    }

    return render(request, 'music/music_list.html', context)


def music_detail(request, pk):
    music = get_object_or_404(Music, pk=pk)
    return render(request, 'music/music_detail.html', {'music': music})


@permission_required('music.add_music', raise_exception=True)
def create_music(request):
    authors = Author.objects.all()
    if request.method == 'POST':
        form = MusicForm(request.POST,request.FILES)
        if form.is_valid():
            music = form.save(commit=False)
            music.created_at = timezone.now()
            music.updated_at = timezone.now()
            music.save()
            return redirect('music_list')
    else:
        form = MusicForm()

    return render(request, 'music/create_music.html', {'form': form, 'authors': authors})

@permission_required('music.change_music', raise_exception=True, login_url='/login/?next=/music/edit_music/1/')
def edit_music(request, pk):
    music = get_object_or_404(Music, pk=pk)
    authors = Author.objects.all()

    if request.method == 'POST':
        form = MusicForm(request.POST,request.FILES, instance=music)
        if form.is_valid():
            music = form.save(commit=False)
            music.updated_at = timezone.now()
            music.save()
            return redirect('music_detail', pk=music.pk)
    else:
        form = MusicForm(instance=music)

    return render(request, 'music/edit_music.html', {'form': form, 'music': music, 'authors': authors})
@permission_required('music.delete_music', raise_exception=True, login_url='/login/?next=/music/delete_music/1/')
def delete_music(request, pk):
    music = get_object_or_404(Music, pk=pk)
    if request.method == 'POST':
        music.delete()
        return redirect('music_list')
    return render(request, 'music/music_delete.html', {'music': music})


def get_authors(request):
    authors = Author.objects.all().order_by('-created_at')
    q = request.GET.get('q')


    if q:
        authors = authors.filter(
            Q(full_name__icontains=q) |
            Q(country__icontains=q)
        )

    paginator = Paginator(authors, 10)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    context = {
        'authors': page_obj,
        'page_obj': page_obj,
        'q': q,
    }
    return render(request, 'author/author_list.html', context)

def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    return render(request, 'author/author_detail.html', {'author': author})


@permission_required('music.add_author', raise_exception=True)
def create_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('author_list')
    else:
        form = AuthorForm()

    return render(request, 'author/create-author.html', {'form': form})

@permission_required('music.change_author', raise_exception=True, login_url='/login/?next=/music/edit_author/1/')
def edit_author(request, pk):
    author = get_object_or_404(Author, pk=pk)

    if request.method == 'POST':
        form = AuthorForm(request.POST, request.FILES, instance=author)
        if form.is_valid():
            form.save()
            return redirect('author_list')
    else:
        form = AuthorForm(instance=author)
    return render(request, 'author/author_edit.html', {'form': form, 'author': author})

@permission_required('music.delete_author', raise_exception=True, login_url='/login/?next=/music/delete_author/1/')
def delete_author(request, pk):
    author = get_object_or_404(Author, pk=pk)

    if request.method == 'POST':
        author.delete()
        return redirect('author_list')

    return render(request, 'author/author_delete.html', {'author': author})

@permission_required('music.add_emailnotification', raise_exception=True)
def send_email_view(request):
    User = get_user_model()

    if request.method == 'POST':
        form = EmailNotificationForm(request.POST)
        if form.is_valid():
            notification = form.save()
            users = User.objects.filter(is_active=True).exclude(email='')

            for user in users:
                email = EmailMultiAlternatives(
                    subject=notification.subject,
                    body=notification.message,
                    from_email="abdullagulomjonov2306@gmail.com",
                    to=[user.email]
                )
                email.send()

            messages.success(request, f"{users.count()} foydalanuvchiga xabar yuborildi.")
            return redirect('email_content')
    else:
        form = EmailNotificationForm()

    return render(request, 'music/email_content.html', {'form': form})



def export_to_xslx(request):
    workbook=openpyxl.Workbook()
    sheet=workbook.active
    sheet.title="Music"
    sheet.append([
        'genre',
        'text',
        'author',
    ])
    musics=Music.objects.all()
    for music in musics:
        sheet.append([
            music.genre,
            music.text,
            music.author.full_name,
        ])
    response=HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition']='attachment;filename="musics.xlsx"'
    workbook.save(response)
    return response

