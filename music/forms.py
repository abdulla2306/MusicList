from datetime import date

from django import forms


from music.models import Author


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['full_name', 'birthday', 'country', 'image',]

    def clean_full_name(self):
        full_name = self.cleaned_data['full_name']
        if len(full_name) < 3:
            raise forms.ValidationError('Full name must be at least 3 characters long')
        return full_name


from django import forms
from .models import Music, Author

class MusicForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = ['genre', 'text', 'published_year', 'author', 'audio',]

    author = forms.ModelChoiceField(queryset=Author.objects.all(), required=True)


    def clean_published_year(self):
        published_year = self.cleaned_data.get('published_year')
        if published_year and published_year.year > date.today().year:
            raise forms.ValidationError("Nashr yili hozirgi yildan katta bo'lishi mumkin emas.")
        return published_year



