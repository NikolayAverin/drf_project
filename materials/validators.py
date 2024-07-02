import re

from rest_framework.serializers import ValidationError


class VideoUrlValidator:

    def __call__(self, url):
        """Проверка ссылки на видео"""
        link = r"^((?:https?:)?\/\/)?((?:www|m)\.)?((?:youtube(?:-nocookie)?\.com|youtu.be))(\/(?:[\w\-]+\?v=|embed\/|live\/|v\/)?)([\w\-]+)(\S+)?$"
        if not re.match(link, url):
            raise ValidationError("Ссылка должна вести на YouTube")
