from django.contrib.auth import logout
from django.shortcuts import render, redirect
from .forms import UserForm  # CustomUserCreationForm ishlatilmoqda

def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)  # CustomUserCreationForm ishlatilyapti
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Parolni xesh qilish
            user.save()
            return redirect('music_list')  # Ro‘yxatdan o‘tgandan keyin boshqa sahifaga yo‘naltirish
    else:
        form = UserForm()

    return render(request, 'user/register.html', {'form': form})

# def logout_user(request):
#     logout(request)
#     return redirect('music_list')  # Tizimdan chiqishdan keyin foydalanuvchini yo‘naltirish
#
#
# from django.contrib.auth import logout,login
# from django.shortcuts import render, redirect
#
# from user.forms import UserForm
#
#
# def register(request):
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password'])
#             user.save()
#             return redirect('login')
#     else:
#         form = UserForm()
#     return render(request, 'register.html', {'form': form})


from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

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

