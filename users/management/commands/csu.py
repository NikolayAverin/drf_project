from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        """Создание суперпользователя"""
        user = User.objects.create(email="admin@example.com")
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.set_password("Test1234!")
        user.save()
