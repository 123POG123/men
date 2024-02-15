from time import sleep

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task()
def send_feedback(message):
    sleep(10)
    send_mail(
        subject='hello',
        message=message,
        from_email='vinogradovpavel32@gmail.com',
        recipient_list=['{}'.format(settings.EMAIL_HOST_USER), ], )
    print('send')
