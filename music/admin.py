from django.contrib import admin

from music.models import Author,Music

admin.site.register(Author)
admin.site.register(Music)


# class MusicAdmin(admin.ModelAdmin):
#     # list_display = ('genre', 'text', 'published_year')
#     # search_fields = ('published_year')
#     # list_filter = ('author',)
#     # ordering = ('genre',)
#     readonly_fields = ('created_at',)
# admin.site.register(Music, MusicAdmin)