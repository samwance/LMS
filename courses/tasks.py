from datetime import datetime
from time import timezone

from celery import shared_task

from courses.models import Course
from courses.services import send_mailing
from users.models import User


@shared_task
def send_course_update_email(subscription_pk):
    send_mailing(subscription_pk)


@shared_task
def blocks_the_user():
    now = datetime.datetime.now()
    users = User.objects.filter(is_active=True)

    for user in users:
        if user.last_login:
            if user.last_login.timestamp() < (now - datetime.timedelta(days=30)).timestamp():
                user.is_active = False
                user.save()
