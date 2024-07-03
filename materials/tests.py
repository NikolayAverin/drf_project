from django.urls import reverse
from rest_framework import status
from rest_framework.serializers import ValidationError
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscription
from users.models import User


class CourseTestCase(APITestCase):
    """Тесты для курса"""

    def setUp(self):
        self.user = User.objects.create(email="test@test.com")
        self.course = Course.objects.create(
            title="Test Course", description="Test Course description", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title="Test Lesson",
            description="Test Lesson description",
            owner=self.user,
            video="youtube.com",
            course=self.course,
        )
        self.client.force_authenticate(user=self.user)

    def test_course_create(self):
        """Создание курса"""
        url = reverse("materials:course-list")
        data = {"title": "Test Course 2", "description": "Test Course 2 description"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.count(), 2)

    def test_course_list(self):
        """Получение списка курсов"""
        url = reverse("materials:course-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.course.pk,
                    "count_lessons": 1,
                    "lessons": [
                        {
                            "id": self.lesson.pk,
                            "video": self.lesson.video,
                            "title": self.lesson.title,
                            "description": self.lesson.description,
                            "preview": None,
                            "course": self.course.pk,
                            "owner": self.user.pk,
                        }
                    ],
                    "is_subscribed": False,
                    "title": self.course.title,
                    "description": self.course.description,
                    "preview": None,
                    "owner": self.user.pk,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_course_retrieve(self):
        """Получение курса"""
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["title"], self.course.title)

    def test_course_update(self):
        """Обновление курса"""
        url = reverse("materials:course-detail", args=(self.course.pk,))
        data = {"title": "Updated Test Course"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["title"], "Updated Test Course")

    def test_course_delete(self):
        """Удаление курса"""
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.count(), 0)


class LessonTestCase(APITestCase):
    """Тесты для урока"""

    def setUp(self):
        self.user = User.objects.create(email="test@test.com")
        self.course = Course.objects.create(
            title="Test Course", description="Test Course description", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title="Test Lesson",
            description="Test Lesson description",
            owner=self.user,
            video="youtube.com",
            course=self.course,
        )
        self.client.force_authenticate(user=self.user)

    def test_lesson_create(self):
        """Создание урока"""
        url = reverse("materials:lessons_create")
        data = {'title': 'Test Lesson 2', 'description': 'Test Lesson 2 description', 'video': 'http://www.youtube.com/watch?v=DFYRQ_zQ-gk', 'course': self.course.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_lesson_list(self):
        """Получение списка уроков"""
        url = reverse("materials:lessons_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "video": self.lesson.video,
                    "title": self.lesson.title,
                    "description": self.lesson.description,
                    "preview": None,
                    "course": self.course.pk,
                    "owner": self.user.pk,
                }
            ],
        }
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_lesson_retrieve(self):
        """Получение урока"""
        url = reverse("materials:lessons_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["title"], self.lesson.title)

    def test_lesson_update(self):
        """Обновление урока"""
        url = reverse("materials:lessons_update", args=(self.lesson.pk,))
        data = {"title": "Updated Test Lesson"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data["title"], "Updated Test Lesson")
        data = {"video": "vk.com"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertRaises(ValidationError)

    def test_lesson_delete(self):
        """Удаление урока"""
        url = reverse("materials:lessons_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)


class SubscriptionTestCase(APITestCase):
    """Тесты для подписки"""

    def setUp(self):
        self.user = User.objects.create(email="test@test.com")
        self.course = Course.objects.create(
            title="Test Course", description="Test Course description", owner=self.user
        )
        self.client.force_authenticate(user=self.user)

    def test_subscription(self):
        """Проверка подключения и отключения подписки на курс"""
        url = reverse("materials:subscriptions")
        data = {"course": self.course.pk, "user": self.user.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Вы подписались на курс")
        self.assertEqual(Subscription.objects.count(), 1)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Вы отписались от курса")
        self.assertEqual(Subscription.objects.count(), 0)
