from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from materials.models import Course, Lesson

PAYMENT_METHOD = [
    ("cash", "наличные"),
    ("transaction", "перевод на счет"),
]


class User(AbstractUser):
    """Модель пользователя"""
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите свою почту"
    )
    phone = PhoneNumberField(
        null=True,
        blank=True,
        verbose_name="Телефон",
        help_text="Укажите свой номер телефона",
    )
    city = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name="Город",
        help_text="Укажите свой город",
    )
    avatar = models.ImageField(
        upload_to="users",
        null=True,
        blank=True,
        verbose_name="Аватар",
        help_text="Загрузите свой аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    """Модель платежа"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Плательщик")
    payment_data = models.DateField(verbose_name="Дата оплаты", auto_now_add=True)
    course = models.ForeignKey(
        Course,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="Оплаченный курс",
    )
    lesson = models.ForeignKey(
        Lesson,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="Оплаченный урок",
    )
    payment_sum = models.PositiveIntegerField(verbose_name="Сумма оплаты")
    payment_method = models.CharField(
        max_length=100, choices=PAYMENT_METHOD, verbose_name="Способ оплаты"
    )
    session_id = models.CharField(max_length=255, verbose_name="ИД сессии", null=True, blank=True)
    payment_link = models.URLField(max_length=400, verbose_name="Ссылка на оплату", null=True, blank=True)
    payment_status = models.CharField(max_length=255, verbose_name="Статус оплаты", null=True, blank=True)

    def __str__(self):
        return f"{self.user} оплатил {self.payment_sum} руб."

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"
