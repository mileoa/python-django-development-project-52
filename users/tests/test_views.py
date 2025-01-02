from django.test import TestCase
from django.urls import reverse
from users.models import User


class UserTests(TestCase):

    def test_user_create_get(self):
        response = self.client.get(reverse("user_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/user_create.html")

    def test_user_create_post_invalid_data(self):
        response = self.client.post(
            reverse("user_create"),
            {
                "first_name": "test",
                "last_name": "user",
                "username": "1",
                "password1": "1234",
                "password2": "1234",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/user_create.html")
        self.assertQuerySetEqual(User.objects.all(), [])

    def test_user_create_post_successful(self):
        self.assertEqual(
            User.objects.filter(username="test_user_create_post_successful").count(), 0
        )
        response = self.client.post(
            reverse("user_create"),
            {
                "first_name": "test",
                "last_name": "user",
                "username": "test_user_create_post_successful",
                "password1": "test12345678",
                "password2": "test12345678",
            },
        )
        self.assertRedirects(response, reverse("login"), 302)
        self.assertEqual(
            User.objects.filter(username="test_user_create_post_successful").count(), 1
        )

    def test_user_create_post_successful_message_displays(self):
        response = self.client.post(
            reverse("user_create"),
            {
                "first_name": "test",
                "last_name": "user",
                "username": "test_user_create_post_successful",
                "password1": "test12345678",
                "password2": "test12345678",
            },
            follow=True,
        )
        self.assertContains(response, "Пользователь успешно зарегистрирован")

    def test_user_create_post_user_already_exists(self):
        self.client.post(
            reverse("user_create"),
            {
                "first_name": "test",
                "last_name": "user",
                "username": "test_user_create_post_user_already_exists",
                "password1": "test12345678",
                "password2": "test12345678",
            },
        )
        self.assertEqual(
            User.objects.filter(
                username="test_user_create_post_user_already_exists"
            ).count(),
            1,
        )
        response = self.client.post(
            reverse("user_create"),
            {
                "first_name": "test",
                "last_name": "user",
                "username": "test_user_create_post_user_already_exists",
                "password1": "test12345678",
                "password2": "test12345678",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/user_create.html")
        self.assertEqual(
            User.objects.filter(
                username="test_user_create_post_user_already_exists"
            ).count(),
            1,
        )

    def test_user_update_get_unlogined(self):
        user = User.objects.create(
            first_name="test",
            last_name="user",
            username="test_user_update_get_unlogined_message",
            email="test@google.ru",
            password="test12345678",
        )
        message_response = self.client.get(
            reverse("user_update", kwargs={"pk": user.pk}), follow=True
        )
        self.assertContains(
            message_response, "Вы не авторизованы! Пожалуйста, выполните вход."
        )

        redirect_response = self.client.get(
            reverse("user_update", kwargs={"pk": user.pk})
        )
        self.assertRedirects(redirect_response, reverse("login"), 302)

    def test_user_update_get_logined_self(self):
        user = User.objects.create(
            first_name="test",
            last_name="user",
            username="test_user_update_get_logined_self",
            email="test@google.ru",
            password="test12345678",
        )
        self.client.force_login(user)
        response = self.client.get(reverse("user_update", kwargs={"pk": user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/user_update.html")

    def test_user_update_get_logined_not_self(self):
        first_user = User.objects.create(
            first_name="test",
            last_name="user",
            username="test_user_update_get_logined_self_1",
            email="test@google.ru",
            password="test12345678",
        )
        second_user = User.objects.create(
            first_name="test",
            last_name="user",
            username="test_user_update_get_logined_self_2",
            email="test@google.ru",
            password="test12345678",
        )
        self.client.force_login(first_user)
        self.assertEqual(
            self.client.get(
                reverse("user_update", kwargs={"pk": second_user.pk})
            ).status_code,
            302,
        )
        response = self.client.get(
            reverse("user_update", kwargs={"pk": second_user.pk}), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/user_list.html")
        self.assertContains(
            response, "У вас нет прав для изменения другого пользователя."
        )

    def test_user_update_post(self):
        user = User.objects.create(
            first_name="test",
            last_name="user",
            username="test_user_update_post_1",
            email="test@google.ru",
            password="test12345678",
        )
        self.client.force_login(user)
        response = self.client.post(
            reverse("user_update", kwargs={"pk": user.pk}),
            {
                "first_name": "test",
                "last_name": "user",
                "username": "test_user_update_post_2",
                "password1": "test12345678",
                "password2": "test12345678",
            },
            follow=True,
        )
        self.assertContains(response, "Пользователь успешно изменен")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/user_list.html")
        self.assertEqual(
            User.objects.get(pk=user.pk).username, "test_user_update_post_2"
        )

    def test_user_delete_get_logined_self(self):
        user = User.objects.create(
            first_name="test",
            last_name="user",
            username="test_user_update_get_logined_self",
            email="test@google.ru",
            password="test12345678",
        )
        self.client.force_login(user)
        response = self.client.get(reverse("user_delete", kwargs={"pk": user.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/user_delete.html")

    def test_user_delete_get_logined_not_self(self):
        first_user = User.objects.create(
            first_name="test",
            last_name="user",
            username="test_user_delete_get_logined_not_self_1",
            email="test@google.ru",
            password="test12345678",
        )
        second_user = User.objects.create(
            first_name="test",
            last_name="user",
            username="test_user_delete_get_logined_not_self_2",
            email="test@google.ru",
            password="test12345678",
        )
        self.client.force_login(first_user)
        self.assertEqual(
            self.client.get(
                reverse("user_delete", kwargs={"pk": second_user.pk})
            ).status_code,
            302,
        )
        response = self.client.get(
            reverse("user_delete", kwargs={"pk": second_user.pk}), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/user_list.html")
        self.assertContains(
            response, "У вас нет прав для изменения другого пользователя."
        )

    def test_user_delete_post(self):
        user = User.objects.create(
            first_name="test",
            last_name="user",
            username="test_user_delete_post",
            email="test@google.ru",
            password="test12345678",
        )
        self.client.force_login(user)
        response = self.client.post(
            reverse("user_delete", kwargs={"pk": user.pk}),
            follow=True,
        )
        self.assertContains(response, "Пользователь успешно удален")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/user_list.html")
        self.assertEqual(User.objects.filter(pk=user.pk).count(), 0)
