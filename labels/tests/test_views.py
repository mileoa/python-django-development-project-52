from django.test import TestCase
from django.urls import reverse
from users.models import Users
from statuses.models import Statuses
from tasks.models import Tasks
from labels.models import Labels


class LabelsTests(TestCase):

    def setUp(self):
        self.user = Users.objects.create(
            first_name="test",
            last_name="user",
            username="mileoa",
            password="test12345678",
        )
        Labels.objects.create(name="new label")

    def test_get_label_list(self):
        self.client.force_login(Users.objects.get(id=1))
        response = self.client.get(reverse("label_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/labels_list.html")
        self.assertContains(response, "new label")
        self.assertContains(response, "Создать метку")
        self.assertContains(response, reverse("label_create"))

    def test_get_label_create(self):
        self.client.force_login(Users.objects.get(id=1))
        response = self.client.get(reverse("label_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/labels_create.html")

    def test_post_label_create(self):
        self.client.force_login(Users.objects.get(id=1))
        response = self.client.post(
            reverse("label_create"), {"name": "test_post_label_create"}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/labels_list.html")
        self.assertContains(response, "Метка успешно создана")
        self.assertEqual(
            Labels.objects.filter(name="test_post_label_create").count(), 1
        )

    def test_get_label_delete(self):
        label = Labels.objects.create(name="test_get_label_delete")
        self.client.force_login(Users.objects.get(id=1))
        response = self.client.get(reverse("label_delete", kwargs={"pk": label.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/labels_delete.html")

    def test_post_label_delete_unrelated(self):
        label = Labels.objects.create(name="test_post_label_delete_unrelated")
        self.client.force_login(Users.objects.get(id=1))
        response = self.client.post(
            reverse("label_delete", kwargs={"pk": label.id}), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/labels_list.html")
        self.assertContains(response, "Метка успешно удалена")
        self.assertEqual(
            Labels.objects.filter(name="test_post_label_delete_unrelated").count(), 0
        )

    def test_post_label_delete_related(self):
        status = Statuses.objects.create(name="test_post_label_delete_related")
        label = Labels.objects.create(name="test_post_label_delete_related")
        task = Tasks.objects.create(
            name="test_post_label_delete_related", author=self.user, status=status
        )
        task.labels.add(label)
        self.client.force_login(Users.objects.get(id=1))
        response = self.client.post(
            reverse("label_delete", kwargs={"pk": label.id}), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/labels_list.html")
        self.assertContains(
            response, "Невозможно удалить метку, потому что она используется"
        )
        self.assertEqual(
            Labels.objects.filter(name="test_post_label_delete_related").count(), 1
        )

    def test_get_label_update(self):
        label = Labels.objects.create(name="test_get_label_update")
        self.client.force_login(Users.objects.get(id=1))
        response = self.client.get(reverse("label_update", kwargs={"pk": label.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/labels_update.html")

    def test_post_label_update(self):
        label = Labels.objects.create(name="test_post_label_update")
        self.client.force_login(Users.objects.get(id=1))
        response = self.client.post(
            reverse("label_update", kwargs={"pk": label.id}),
            {"name": "another test_post_label_update"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "labels/labels_list.html")
        self.assertContains(response, "Метка успешно изменена")
        self.assertEqual(
            Labels.objects.filter(name="test_post_label_update").count(), 0
        )
        self.assertEqual(
            Labels.objects.filter(name="another test_post_label_update").count(), 1
        )

    def test_login_required(self):
        label = Labels.objects.create(name="test_login_required")
        request_without_id = {"label_list": ["get"], "label_create": ["get", "post"]}
        request_with_id = {
            "label_delete": ["get", "post"],
            "label_update": ["get", "post"],
        }
        request_variants = request_without_id | request_with_id
        for url_name, methods in request_variants.items():
            for method in methods:
                prepared_reqest = getattr(self.client, method)
                if url_name in request_without_id:
                    response = prepared_reqest(reverse(url_name), follow=True)
                else:
                    response = prepared_reqest(
                        reverse(url_name, kwargs={"pk": label.id}), follow=True
                    )
                self.assertTemplateUsed(response, "registration/login.html")
                self.assertContains(
                    response, "Вы не авторизованы! Пожалуйста, выполните вход."
                )
