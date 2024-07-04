from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated

from materials.models import Course, Lesson
from users.models import Payment, User
from users.permissions import IsUser
from users.serializers import (PaymentSerializer, UserSerializer,
                               UserViewSerializer)
from users.services import (check_payment, create_price, create_product,
                            create_session_payment)


class UserCreateApiView(CreateAPIView):
    """Создание нового пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        """Шифрование пароля при создании пользователя"""
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListApiView(ListAPIView):
    """Отображение пользователей"""

    queryset = User.objects.all()
    serializer_class = UserViewSerializer


class UserRetrieveApiView(RetrieveAPIView):
    """Отображение одного пользователя"""

    queryset = User.objects.all()

    def get_serializer_class(self):
        """Переопределение сериализатора, если пользователь открывает свой профиль"""
        if self.request.user.email == self.get_object().email:
            return UserSerializer
        else:
            return UserViewSerializer


class UserUpdateApiView(UpdateAPIView):
    """Изменение профиля пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsUser)

    def perform_update(self, serializer):
        """Шифрование пароля при изменении профиля"""
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()


class UserDestroyApiView(DestroyAPIView):
    """Удаление пользователя"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsUser)


class PaymentCreateApiView(CreateAPIView):
    """Создание нового платежа"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        """Сохранение платежа и создание сессии оплаты"""
        payment = serializer.save(user=self.request.user)
        course_id = self.request.data.get("course")
        lesson_id = self.request.data.get("lesson")
        if course_id:
            course_name = create_product(Course.objects.get(pk=course_id).title)
            course_price = create_price(payment.course.cost, course_name)
            session_id, payment_link = create_session_payment(course_price)
        else:
            lesson_name = create_product(Lesson.objects.get(pk=lesson_id).title)
            lesson_price = create_price(payment.lesson.cost, lesson_name)
            session_id, payment_link = create_session_payment(lesson_price)
        payment_status = check_payment(session_id)
        payment.payment_status = payment_status
        payment.session_id = session_id
        payment.payment_link = payment_link
        payment.save()


class PaymentListAPIView(ListAPIView):
    """Отображение платежей"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = (
        "course",
        "lesson",
        "payment_method",
    )
    ordering_fields = ("payment_data",)


class PaymentRetrieveApiView(RetrieveAPIView):
    """Отображение одного платежа"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer


class PaymentUpdateApiView(UpdateAPIView):
    """Изменение статуса платежа"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
