from django.utils import timezone
from celery import shared_task
from dateutil.relativedelta import relativedelta

from users.models import User


@shared_task
def check_users_active():
    """Блокирует пользователей, которые не заходили в течении месяца"""
    users = User.objects.all()
    now_date = timezone.now()
    for user in users:
        if user.last_login:
            if user.last_login < (now_date - relativedelta(months=1)):
                user.is_active = False
                user.save()
        else:
            user.last_login = now_date
