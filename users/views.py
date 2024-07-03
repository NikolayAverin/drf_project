from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny, IsAuthenticated
from users.models import Payment, User
from users.permissions import IsUser
from users.serializers import (PaymentSerializer, UserSerializer,
                               UserViewSerializer)


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
        pass


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
