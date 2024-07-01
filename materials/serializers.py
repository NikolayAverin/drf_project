from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson, Subscription
from materials.validators import VideoUrlValidator


class LessonSerializer(ModelSerializer):
    video = serializers.URLField(validators=[VideoUrlValidator()])

    class Meta:
        model = Lesson
        fields = "__all__"


class SubscriptionSerializer(ModelSerializer):

    class Meta:
        model = Subscription
        fields = ("user", "course")


class CourseSerializer(ModelSerializer):
    count_lessons = SerializerMethodField()
    lessons = LessonSerializer(source="lesson_set", many=True, read_only=True)
    # subscriptions = SubscriptionSerializer(source="subscription_set", many=True, read_only=True)
    is_subscribed = SerializerMethodField()

    def get_is_subscribed(self, instance):
        """Проверяем, подписан ли пользователь на курс"""
        user = self.context.get("request").user
        return Subscription.objects.filter(user=user, course=instance).exists()

    def get_count_lessons(self, instance):
        """Получаем количество уроков в курсе"""
        return instance.lesson_set.count()

    class Meta:
        model = Course
        fields = "__all__"
