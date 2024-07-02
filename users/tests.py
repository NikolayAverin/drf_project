from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import Payment, User


class UserTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@test.com")
        self.client.force_authenticate(user=self.user)

    def test_user_register(self):
        url = reverse("users:register")
        data = {"email": "test2@test.com", "password": "111111"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_user_list(self):
        url = reverse("users:users")
        response = self.client.get(url)
        data = response.json()
        result = [
            {"id": self.user.pk, "email": self.user.email, "city": None, "avatar": None}
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_user_retrieve(self):
        url = reverse("users:user_detail", args=(self.user.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["email"], self.user.email)

    def test_user_update(self):
        url = reverse("users:user_update", args=(self.user.pk,))
        data = {"city": "Test city"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["city"], "Test city")

    def test_user_delete(self):
        url = reverse("users:user_delete", args=(self.user.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 0)


class PaymentTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test@test.com")
        self.payment = Payment.objects.create(
            user=self.user, payment_sum=1000, payment_method="cash"
        )
        self.client.force_authenticate(user=self.user)

    def test_payment_list(self):
        url = reverse("users:payments")
        response = self.client.get(url)
        data = response.json()
        result = [
            {
                "id": self.payment.pk,
                "user": self.user.pk,
                "payment_data": "2024-07-02",
                "course": None,
                "lesson": None,
                "payment_sum": self.payment.payment_sum,
                "payment_method": self.payment.payment_method,
            }
        ]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)
