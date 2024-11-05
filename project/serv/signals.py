# import os
#
# from django.db.models.signals import post_save
# from django.dispatch import receiver  # импортируем нужный декоратор
# from django.core.mail import send_mail
# from .models import Comment, Post
#
# # в декоратор передаётся первым аргументом сигнал, на который будет реагировать эта функция, и в отправители надо передать также модель
# @receiver(post_save, sender=Comment)
# def notify_managers_appointment(sender, instance, created, **kwargs):
#     if created:
#         subject = f'{instance.user} {instance.time_in.strftime("%d %m %Y")}'
#     else:
#         subject = f'Appointment changed for {instance.user} {instance.time_in.strftime("%d %m %Y")}'
#
#     send_mail(
#
#         subject=subject,
#         message=instance.text,
#         from_email=os.getenv('DEFAULT_FROM_EMAIL'),
#         # здесь указываете почту, с которой будете отправлять (об этом попозже)
#         recipient_list=[post.user.email]
#     )
#
# post_save.connect(notify_managers_appointment, sender=Comment)