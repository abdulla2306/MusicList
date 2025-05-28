import random

from django.contrib.auth import logout, authenticate, login, get_user_model
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import redirect, render

from music_site import settings
from music_site.settings import EMAIL_HOST_USER
from .forms import UserForm
from .models import PasswordResetRequest, CustomUser


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('login')
    else:
        form = UserForm()

    return render(request, 'user/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('music_list')
        else:
            error = "Login yoki parol noto‘g‘ri"
            return render(request, 'login.html', {'error': error})
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('music_list')


User=get_user_model()
def send_reset_code_view(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        try:
            user = User.objects.get(username=login)
        except User.DoesNotExist:
            return render(request, 'password_reset/request_invalid.html', {'error': 'Login topilmadi.'})
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        reset_request = PasswordResetRequest.objects.create(user=user, code=code)
        reset_link = f"http://127.0.0.1:8000/reset-password/{reset_request.token}/"


        send_mail(
            subject="Parolni tiklash uchun kod",
            message=(
                f"Salom {user.username},\n\n"
                f"Siz parolni tiklashni so‘radingiz.\n"
                f"6 xonali tasdiqlash kodingiz: {code}\n"
                f"Parolni yangilash uchun ushbu havolani oching:\n{reset_link}\n\n"
                f"Agar bu siz bo‘lmasangiz, bu xabarni e'tiborsiz qoldiring."
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email,EMAIL_HOST_USER],
            fail_silently=False
        )

        return render(request, 'password_reset/code_sent.html')

    return render(request, 'password_reset/request_form.html')



def reset_password_view(request, token):
    try:
        reset_request = PasswordResetRequest.objects.get(token=token)
    except PasswordResetRequest.DoesNotExist:
        return render(request, 'password_reset/invalid_token.html')

    if not reset_request.is_valid():
        return render(request, 'password_reset/expired.html')

    if request.method == 'POST':
        code = request.POST.get('code')
        new_password = request.POST.get('new_password')

        if reset_request.code == code:
            user = reset_request.user
            user.set_password(new_password)
            user.save()


            reset_request.delete()

            return redirect('login')

        else:
            return render(request, 'password_reset/new_password.html', {
                'error': 'Kod noto‘g‘ri!',
                'token': token
            })

    return render(request, 'password_reset/new_password.html', {'token': token})

def google_login(request):
    auth_url = (

        f"{settings.GOOGLE_AUTH_URL}"

        f"?client_id={settings.GOOGLE_CLIENT_ID}"

        f"&redirect_uri={settings.GOOGLE_REDIRECT_URI}"

        f"&response_type=code"

        f"&scope=openid email profile"

    )

    return redirect(auth_url)


import requests
from django.http import HttpResponse
from django.conf import settings

def google_callback(request):
    code = request.GET.get('code')
    if not code:
        return HttpResponse("Kod yo‘q", status=400)

    token_data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    token_response = requests.post(settings.GOOGLE_TOKEN_URL, data=token_data)
    token_json = token_response.json()
    access_token = token_json.get("access_token")

    if not access_token:
        return HttpResponse("Access token olinmadi", status=400)


    user_info_response = requests.get(
        settings.GOOGLE_USER_INFO_URL,
        headers={"Authorization": f"Bearer {access_token}"}
    )

    user_info = user_info_response.json()
    user,_=CustomUser.objects.get_or_create(
        username=user_info.get("name"),
        email=user_info.get("email"),
    )
    if user:
        login(request,user)
        return redirect('music_list')


    return redirect('login')

from django.http import HttpResponse

def slow_down_view(request):
    return HttpResponse("""
        <html>
            <head><title>Too Many Requests</title></head>
            <body style="text-align:center; padding-top: 100px;">
                <h1>🥱 Sekinroq...</h1>
                <p>Siz juda tez so‘rov yubordingiz. Iltimos, biroz kuting.</p>
                <a href="/">🔙 Bosh sahifaga qaytish</a>
            </body>
        </html>
    """)
