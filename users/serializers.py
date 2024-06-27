from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from users.models import Payment, User


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(ModelSerializer):
    payments = PaymentSerializer(source="payment_set", many=True, read_only=True)

    class Meta:
        model = User
        fields = "__all__"


class UserViewSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ("id", "email", "city", "avatar")
