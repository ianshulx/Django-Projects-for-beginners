from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .forms import TaskForm
from .models import Task

# Create your tests here.


class TaskModelTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="username", password="password123"
        )
        self.task = Task.objects.create(
            user=self.user,
            title="test title",
            description="test description",
            is_completed=False,
            priority="mediom",
            due_date=timezone.now().date() + timedelta(days=1),
        )

    def test_task_creation(self):
        self.assertEqual(self.task.title, "test title"),
        self.assertFalse(self.task.is_completed),
        self.assertEqual(self.task.user.username, "username")

    def test_task_str_method(self):
        self.assertEqual(str(self.task), "test title")

    def test_due_date_not_in_past(self):
        self.assertGreater(self.task.due_date, timezone.now().date())


class TaskFormTest(TestCase):
    def test_valid_form(self):
        data = {
            "title": "new task",
            "description": "some description",
            "is_completed": False,
            "priority": "M",
            "due_date": (timezone.now() + timedelta(days=1)).date(),
        }
        form = TaskForm(data=data)
        self.assertTrue(
            form.is_valid(), f"Form should be valid, but got errors: {form.errors}"
        )

    def test_due_date_in_past_invalid(self):
        data = {
            "title": "old task",
            "description": "Invalid past date",
            "is_completed": False,
            "priority": "M",
            "due_date": (timezone.now() - timedelta(days=1)).date(),
        }
        form = TaskForm(data=data)
        self.assertFalse(
            form.is_valid(), "Form should not be valid with a past due date"
        )
        self.assertIn("due_date", form.errors, "Due date error should be raised")

    def test_missing_title_invalid(self):
        data = {
            "title": "",
            "description": "Invalid past date",
            "is_completed": False,
            "priority": "M",
            "due_date": (timezone.now() + timedelta(days=2)).date(),
        }
        form = TaskForm(data=data)
        self.assertFalse(
            form.is_valid(), f"Form should not be valid without a title{form.errors}"
        )
        self.assertIn("title", form.errors, "Title error should be raised")


class TaskViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="1234")

        self.task = Task.objects.create(
            user=self.user,
            title="sample title",
            description="sample description",
            is_completed=False,
            priority="M",
            due_date=timezone.now() + timedelta(days=2),
        )
        self.other_user = User.objects.create_user(
            username="otheruser", password="abcd"
        )

    def test_redirect_if_not_logged_in(self):
        url = reverse("task_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse("login")))

    def test_logged_in_user_can_see_tasks(self):
        self.client.login(username="testuser", password="1234")
        url = reverse("task_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "sample title")

    def test_logged_in_user_can_create_task(self):
        self.client.login(username="testuser", password="1234")
        url = reverse("task_create")
        response = self.client.post(
            url,
            {
                "title": "new task",
                "description": "Invalid new task",
                "is_completed": False,
                "priority": "M",
                "due_date": (timezone.now() + timedelta(days=2)).date(),
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title="new task").exists())

    def test_logged_in_user_can_update_task(self):
        self.client.login(username="testuser", password="1234")
        url = reverse("task_update", args=[self.task.id])
        response = self.client.post(
            url,
            {
                "title": "updated task",
                "description": "updated task description",
                "is_completed": True,
                "priority": "M",
                "due_date": (timezone.now() + timedelta(days=3)).date(),
            },
        )
        self.assertEqual(response.status_code, 302)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "updated task")
        self.assertTrue(self.task.is_completed)

    def test_user_cannot_update_others_task(self):
        login = self.client.login(username="otheruser", password="abcd")
        self.assertTrue(login)
        url = reverse("task_update", args=[self.task.id])
        response = self.client.post(
            url,
            {
                "title": "hacked task",
                "description": "hacked task description",
            },
        )
        self.assertIn(response.status_code, [403, 404])
        self.task.refresh_from_db()
        self.assertNotEqual(self.task.title, "hacked task")

    def test_logged_in_user_can_delete_task(self):
        self.client.login(username="testuser", password="1234")
        url = reverse("task_delete", args=[self.task.id])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_user_cannot_delete_others_task(self):
        self.client.login(username="otheruser", password="abcd")
        url = reverse("task_delete", args=[self.task.id])
        response = self.client.post(url)
        self.assertIn(response.status_code, [403, 404])
        self.assertTrue(Task.objects.filter(id=self.task.id).exists())
