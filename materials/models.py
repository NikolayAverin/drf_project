from django.conf import settings
from django.db import models


class Course(models.Model):
    """Модель курса"""

    title = models.CharField(
        max_length=150,
        verbose_name="Название курса",
        help_text="Введите название курса",
    )
    description = models.TextField(
        verbose_name="Описание курса", help_text="Введите описание курса"
    )
    preview = models.ImageField(
        upload_to="course",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите превью для курса",
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Создатель курса",
    )
    cost = models.PositiveIntegerField(
        verbose_name="Цена курса", help_text="Укажите цену курса", default=10000
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    """Модель урока"""

    title = models.CharField(
        max_length=150,
        verbose_name="Название урока",
        help_text="Введите название урока",
    )
    description = models.TextField(
        verbose_name="Описание урока", help_text="Введите описание урока"
    )
    preview = models.ImageField(
        upload_to="lesson",
        blank=True,
        null=True,
        verbose_name="Превью",
        help_text="Загрузите превью для курса",
    )
    video = models.URLField(
        verbose_name="Видеоурок",
        help_text="Введите ссылку на видео с уроком",
        blank=True,
        null=True,
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="Курс", help_text="Выберите курс"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Создатель урока",
    )
    cost = models.PositiveIntegerField(
        verbose_name="Цена урока", help_text="Укажите цену урока", default=500
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    """Модель подписки на курс"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name="Подписчик",
    )
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Курс"
    )

    def __str__(self):
        return f"{self.user} подписан на {self.course}"

    class Meta:
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        unique_together = ("user", "course")  # уникальная связка
