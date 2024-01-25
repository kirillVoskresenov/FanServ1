import os

from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import *


@shared_task
def new_com_task(pk):
    new_com = Post.objects.get(id=pk)
    subject = f'Новое объявление: {new_com.title}'
    message = f'Уважаемый пользователь,\n\n' \
              f'у нас появилось новое объявление в категории {new_com.category},\n\n' \

    mail_sent = send_mail(subject, message, os.getenv('DEFAULT_FROM_EMAIL'), [User.email])
    return mail_sent
