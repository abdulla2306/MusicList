from django.urls import path
from music.views import get_music, create_music, edit_music, delete_music, music_detail, create_author, get_authors, \
    author_detail, edit_author, delete_author

urlpatterns = [
    # Music URLs
    path('', get_music, name='music_list'),
    path('detail/<int:pk>/', music_detail, name='music_detail'),
    path('create_music/', create_music, name='music_create'),
    path('edit/<int:pk>/', edit_music, name='music_edit'),
    path('delete/<int:pk>/', delete_music, name='music_delete'),

    # Author URLs
    path('author/', create_author, name='author_create'),
    path('Avtorlar/', get_authors, name='author_list'),
    path('author/detail/<int:pk>/', author_detail, name='author_detail'),
    path('author/edit/<int:pk>/', edit_author, name='author_edit'),
    path('author/delete/<int:pk>/', delete_author, name='author_delete'),

]
