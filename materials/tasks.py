from celery import shared_task
from django.core.mail import send_mail
from config import settings
from materials.models import Subscription


@shared_task
def send_new_lesson_email(course):
    """Отправка письма пользователю о новом уроке в курсе, на который он подписан"""
    subscriptions = Subscription.objects.filter(course=course)
    if subscriptions:
        course_name = subscriptions[0].course.title
        emails = []
        for subscription in subscriptions:
            emails.append(subscription.user.email)
        send_mail(
            f"Обновление курса {course_name}",
            f"По вашей подписке на курс {course_name} вышел новый урок",
            settings.EMAIL_HOST_USER,
            emails,
        )
