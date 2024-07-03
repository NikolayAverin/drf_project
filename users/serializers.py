from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


class PaymentSerializer(ModelSerializer):
    """Сериализатор платежа"""
    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(ModelSerializer):
    """Сериализатор отображения авторизованного пользователя"""
    payments = PaymentSerializer(source="payment_set", many=True, read_only=True)

    class Meta:
        model = User
        fields = "__all__"


class UserViewSerializer(ModelSerializer):
    """Сериализатор отображения пользователей для просмотра"""

    class Meta:
        model = User
        fields = ("id", "email", "city", "avatar")
