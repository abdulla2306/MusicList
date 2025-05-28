from django.core.mail import send_mail
from django.http import HttpResponse
from music_site.settings import EMAIL_HOST_USER as my_email

def send_message(request):
    send_mail(
        subject="salom",
        message="alik",
        from_email= my_email,
        recipient_list=["aliyer.temur95@gmail.com"],
        fail_silently=False
    )
    return HttpResponse("ok")