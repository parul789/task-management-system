from celery import Celery
from celery.decorators import task
from django.core.mail import send_mail

@task(name="sum_two_numbers")
def add(x, y):
    return x + y

@task(name="send the email")
def email():
    return send_mail('Poll', 'info', 'creofridaygames@gmail.com',['prlgupta789@gmail.com','parul@creoit.com'],fail_silently=False)

@task(name='task assignment email')
def task_assignment(info):
    try:
        return send_mail('Poll', 'click on the link to vote:http://192.168.1.43:8000/', 'creofridaygames@gmail.com',['prlgupta789@gmail.
    except:
        return None

