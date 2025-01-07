from django.test import TestCase
from django.urls import reverse
from users.models import Users
from statuses.models import Statuses
from tasks.models import Tasks


class TaskManagerTests(TestCase):

    def setUp(self):
        self.user = Users.objects.create(
            first_name="test",
            last_name="user",
            username="mileoa",
            password="test12345678",
        )
        Statuses.objects.create(name="new status")

    def test_get_status_list(self):
        self.client.force_login(Users.objects.get(id=1))
        response = self.client.get(reverse("status_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "statuses/statuses_list.html")
        self.assertContains(response, "new status")
        self.assertContains(response, "Создать статус")
        self.assertContains(response, reverse("status_create"))

    def test_get_status_create(self):
        self.client.force_login(Users.objects.get(id=1))
        response = self.client.get(reverse("status_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "statuses/statuses_create.html")

    def test_post_status_create(self):
        self.client.force_login(Users.objects.get(id=1))
        response = self.client.post(
            reverse("status_create"), {"name": "test_post_status_create"}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "statuses/statuses_list.html")
        self.assertContains(response, "Статус успешно создан")
        self.assertEqual(
            Statuses.objects.filter(name="test_post_status_create").count(), 1
        )

    def test_get_status_delete(self):
        status = Statuses.objects.create(name="test_get_status_delete")
        self.client.force_login(Users.objects.get(id=1))
        response = self.client.get(reverse("status_delete", kwargs={"pk": status.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "statuses/statuses_delete.html")

    def test_post_status_delete_unrelated(self):
        status = Statuses.objects.create(name="test_post_status_delete_unrelated")
        self.client.force_login(Users.objects.get(id=1))
        response = self.client.post(
            reverse("status_delete", kwargs={"pk": status.id}), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "statuses/statuses_list.html")
        self.assertContains(response, "Статус успешно удален")
        self.assertEqual(
            Statuses.objects.filter(name="test_post_status_delete_unrelated").count(), 0
        )

    def test_post_status_delete_related(self):
        status = Statuses.objects.create(name="test_post_status_delete_related")
        task = Tasks.objects.create(
            name="test_post_status_delete_related", author=self.user, status=status
        )
        self.client.force_login(Users.objects.get(id=1))
        response = self.client.post(
            reverse("status_delete", kwargs={"pk": status.id}), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "statuses/statuses_list.html")
        self.assertContains(
            response, "Невозможно удалить статус, потому что он используется"
        )
        self.assertEqual(
            Statuses.objects.filter(name="test_post_status_delete_related").count(), 1
        )

    def test_get_status_update(self):
        status = Statuses.objects.create(name="test_get_status_update")
        self.client.force_login(Users.objects.get(id=1))
        response = self.client.get(reverse("status_update", kwargs={"pk": status.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "statuses/statuses_update.html")

    def test_post_status_update(self):
        status = Statuses.objects.create(name="test_post_status_update")
        self.client.force_login(Users.objects.get(id=1))
        response = self.client.post(
            reverse("status_update", kwargs={"pk": status.id}),
            {"name": "another test_post_status_update"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "statuses/statuses_list.html")
        self.assertContains(response, "Статус успешно изменен")
        self.assertEqual(
            Statuses.objects.filter(name="test_post_status_update").count(), 0
        )
        self.assertEqual(
            Statuses.objects.filter(name="another test_post_status_update").count(), 1
        )

    def test_login_required(self):
        status = Statuses.objects.create(name="test_login_required")
        request_without_id = {"status_list": ["get"], "status_create": ["get", "post"]}
        request_with_id = {
            "status_delete": ["get", "post"],
            "status_update": ["get", "post"],
        }
        request_variants = request_without_id | request_with_id
        for url_name, methods in request_variants.items():
            for method in methods:
                prepared_reqest = getattr(self.client, method)
                if url_name in request_without_id:
                    response = prepared_reqest(reverse(url_name), follow=True)
                else:
                    response = prepared_reqest(
                        reverse(url_name, kwargs={"pk": status.id}), follow=True
                    )
                self.assertTemplateUsed(response, "registration/login.html")
                self.assertContains(
                    response, "Вы не авторизованы! Пожалуйста, выполните вход."
                )
