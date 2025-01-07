from django.test import TestCase
from django.urls import reverse
from users.models import Users
from django.contrib import auth


class TaskManagerTests(TestCase):

    def setUp(self):
        self.client.post(
            reverse("user_create"),
            {
                "first_name": "test",
                "last_name": "user",
                "username": "mileoa",
                "password1": "test12345678",
                "password2": "test12345678",
            },
        )

    def test_get_login(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_post_login(self):
        response = self.client.post(
            reverse("login"),
            {"username": "mileoa", "password": "test12345678"},
            follow=True,
        )
        self.assertTemplateUsed(response, "index.html")
        self.assertContains(response, "Вы залогинены")
        self.assertContains(response, reverse("user_list"))
        self.assertContains(response, reverse("status_list"))
        self.assertContains(response, reverse("label_list"))
        self.assertContains(response, reverse("task_list"))
        self.assertContains(response, reverse("logout"))

    def test_post_logout(self):
        self.client.force_login(Users.objects.get(id=1))
        response = self.client.post(reverse("logout"), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertContains(response, "Вы разлогинены")
        self.assertContains(response, reverse("user_list"))
        self.assertContains(response, reverse("login"))
        self.assertContains(response, reverse("user_create"))
