from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from users.models import Payment, User
from users.services import check_payment


class PaymentSerializer(ModelSerializer):
    """Сериализатор платежа"""

    payment_status = SerializerMethodField()

    class Meta:
        model = Payment
        fields = "__all__"

    def get_payment_status(self, instance):
        """Получаем статус оплаты"""
        payment_id = self.instance.session_id
        payment_status = check_payment(payment_id)
        return payment_status


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
