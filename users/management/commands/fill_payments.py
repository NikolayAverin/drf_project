import json

from django.core.management import BaseCommand

from materials.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):
    @staticmethod
    def get_payments():
        """Считывает платежи из фикстуры"""
        with open("users/fixtures/payments.json") as file:
            payments = json.load(file)
            return payments

    def handle(self, *args, **options):
        """Стирает информацию о платежах из БД и заполняет заново"""
        Payment.objects.all().delete()
        payments_for_load = []
        for payment in Command.get_payments():
            if payment["fields"]["course"] is None:
                payments_for_load.append(
                    Payment(
                        id=payment["pk"],
                        user=User.objects.get(pk=payment["fields"]["user"]),
                        payment_data=payment["fields"]["payment_data"],
                        course=None,
                        lesson=Lesson.objects.get(pk=payment["fields"]["lesson"]),
                        payment_sum=payment["fields"]["payment_sum"],
                        payment_method=payment["fields"]["payment_method"],
                    )
                )
            elif payment["fields"]["lesson"] is None:
                payments_for_load.append(
                    Payment(
                        id=payment["pk"],
                        user=User.objects.get(pk=payment["fields"]["user"]),
                        payment_data=payment["fields"]["payment_data"],
                        course=Course.objects.get(pk=payment["fields"]["course"]),
                        lesson=None,
                        payment_sum=payment["fields"]["payment_sum"],
                        payment_method=payment["fields"]["payment_method"],
                    )
                )
            else:
                payments_for_load.append(
                    Payment(
                        id=payment["pk"],
                        user=User.objects.get(pk=payment["fields"]["user"]),
                        payment_data=payment["fields"]["payment_data"],
                        course=Course.objects.get(pk=payment["fields"]["course"]),
                        lesson=Lesson.objects.get(pk=payment["fields"]["lesson"]),
                        payment_sum=payment["fields"]["payment_sum"],
                        payment_method=payment["fields"]["payment_method"],
                    )
                )
        Payment.objects.bulk_create(payments_for_load)
