from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView, get_object_or_404)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscription
from materials.paginations import CustomPagination
from materials.serializers import (CourseSerializer, LessonSerializer,
                                   SubscriptionSerializer)
from materials.tasks import send_new_lesson_email
from users.permissions import IsModerators, IsOwner


class CourseViewSet(ModelViewSet):
    """Вьюсет для модели курса"""

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        """Сохранение курса при создании"""
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        """Проверка доступов"""
        if self.action == "create":
            self.permission_classes = (~IsModerators, IsAuthenticated)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModerators | IsOwner,)
        elif self.action == "destroy":
            self.permission_classes = (~IsModerators | IsOwner,)
        return super().get_permissions()


class LessonCreateApiView(CreateAPIView):
    """Создание урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~IsModerators, IsAuthenticated)

    def perform_create(self, serializer):
        """Сохранение урока при создании"""
        lesson = serializer.save()
        lesson.owner = self.request.user
        send_new_lesson_email.delay(lesson.course)
        lesson.save()


class LessonListApiView(ListAPIView):
    """Вывод списка уроков"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerators | IsAuthenticated]
    pagination_class = CustomPagination


class LessonRetrieveApiView(RetrieveAPIView):
    """Вывод одного урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerators | IsOwner]


class LessonUpdateApiView(UpdateAPIView):
    """Обновление урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsModerators | IsOwner]


class LessonDestroyApiView(DestroyAPIView):
    """Удаление урока"""

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [~IsModerators, IsOwner]


class SubscriptionApiView(APIView):
    """Подписка на курс"""

    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """Подписка на курс или отписка от него"""
        user = request.user
        course_id = request.data.get("course")
        course_item = get_object_or_404(Course, id=course_id)
        subscription_exists = Subscription.objects.filter(
            user=user, course=course_item
        ).exists()
        if subscription_exists:
            Subscription.objects.filter(user=user, course=course_item).delete()
            message = "Вы отписались от курса"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Вы подписались на курс"
        return Response({"message": message})
