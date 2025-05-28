from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth import get_user_model
from captcha.fields import CaptchaField
User = get_user_model()

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    captcha = CaptchaField()
    class Meta:
        model = User
        fields = ['username', 'last_name','email','password','captcha']
        widgets = {'password': forms.PasswordInput()}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
