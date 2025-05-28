from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from music_site.settings import EMAIL_HOST_USER
from user.models import CustomUser

@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = "Saytimizga xush kelibsiz!"
        message = (
            f"Salom, {instance.username}!\n\n"
            "Saytimizga ro‘yxatdan o‘tganingiz uchun rahmat.\n"
            "Saytimizda yangiliklar va maxsus takliflar bor, ulardan foydalaning.\n\n"

        )
        send_mail(
            subject,
            message,
            EMAIL_HOST_USER,
            [instance.email,'abdullagulomjonov2306@gmail.com'],
            fail_silently=False,
        )
