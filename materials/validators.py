import re

from rest_framework.serializers import ValidationError


class VideoUrlValidator:

    def __call__(self, url):
        """Проверка ссылки на видео"""
        link = r"^(?:https?:\/\/)?(?:www\.)?youtu\.?be(?:\.com)?\/?.*(?:watch|embed)?(?:.*v=|v\/|\/)([\w\-_]+)\&?"
        if not re.match(link, url):
            raise ValidationError("Ссылка должна вести на YouTube")
