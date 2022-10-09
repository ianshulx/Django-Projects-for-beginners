import tempfile
from PIL import Image

from django.test import TestCase, override_settings
from django.urls import reverse

from ..models import User, Profile
from ..forms import SignUpForm


class TestSignUpView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='user1', email='user1@gmail.com', password='1234'
        )
        self.data = {
            'username': 'test',
            'email': 'test@hotmail.com',
            'password1': 'test12345',
            'password2': 'test12345'
        }

    def test_signup_returns_200(self):
        response = self.client.get(reverse('users:signup'))
        self.assertEqual(response.status_code, 200)
        # Check we used correct template
        self.assertTemplateUsed(response, 'users/signup.html')

    def test_user_is_logged_in(self):
        response = self.client.post(
            reverse('users:signup'), self.data, follow=True
        )
        user = response.context.get('user')

        self.assertTrue(user.is_authenticated)

    def test_new_user_is_registered(self):
        # We can check that a user has been registered by trying to find
        # it in the database but I prefer the method with count()
        nb_old_users = User.objects.count()  # count users before a request
        self.client.post(reverse('users:signup'), self.data)
        nb_new_users = User.objects.count()  # count users after
        # make sure 1 user was added
        self.assertEqual(nb_new_users, nb_old_users + 1)

    def test_redirect_if_user_is_authenticated(self):
        # If the user is authenticated and try to access
        # the signup page, he is redirected to the home page
        login = self.client.login(email='user1@gmail.com', password='1234')
        response = self.client.get(reverse('users:signup'))

        self.assertRedirects(response, reverse('core:home'))

    def test_invalid_form(self):
        # We don't give a username
        response = self.client.post(reverse('users:signup'), {
            "email": "test@admin.com",
            "password1": "test12345",
            "password2": "test12345",
        })
        form = response.context.get('form')

        self.assertFalse(form.is_valid())


class ProfileViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="user1", email="user1@gmail.com", password="1234"
        )
        self.user2 = User.objects.create_user(
            username="user2", email="user2@gmail.com", password="1234"
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse(
            "users:profile", kwargs=({"username": self.user1.username}))
        )

        self.assertRedirects(
            response, "/users/login/?next=/users/profile/user1/")

    def test_returns_200(self):
        self.client.login(email="user1@gmail.com", password="1234")
        response = self.client.get(reverse(
            "users:profile", kwargs=({"username": self.user1.username})
        ))

        self.assertEqual(response.status_code, 200)

    def test_view_returns_profile_of_current_user(self):
        self.client.login(email="user1@gmail.com", password="1234")
        response = self.client.get(reverse(
            "users:profile", kwargs=({"username": self.user1.username}))
        )
        # Check we got the profile of the current user
        self.assertEqual(response.context["user"], self.user1)
        self.assertEqual(response.context["profile"], self.user1.profile)

    def test_view_returns_profile_of_a_given_user(self):
        self.client.login(email="user1@gmail.com", password="1234")
        # access the profile of the user 'user'
        response = self.client.get(reverse(
            "users:profile", kwargs=({"username": self.user2.username}))
        )
        self.assertEqual(response.context["user"], self.user2)
        # Check we got the profile of the user 'user2'
        self.assertEqual(response.context["profile"], self.user2.profile)


class EditProfileViewTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username='user1', email='user1@gmail.com', password='1234'
        )

    def test_edit_profile_returns_200(self):
        self.client.login(email='user1@gmail.com', password='1234')
        response = self.client.get(reverse('users:edit_profile'))
        self.assertEqual(response.status_code, 200)

    def test_edit_profile_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('users:edit_profile'))
        self.assertRedirects(
            response, '/users/login/?next=/users/edit-profile/')

    def test_edit_profile_change_username(self):
        self.client.login(email='user1@gmail.com', password='1234')
        response = self.client.post(reverse('users:edit_profile'), {
            'username': 'user2',
            'about_me': 'Hello world'
        })

        # Check that the username 'user1' becomes 'user2'
        user2 = User.objects.filter(email='user1@gmail.com')[0]
        self.assertEqual(user2.username, 'user2')

    # override settings for media dir to avoid filling up your disk
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_upload_image(self):
        login = self.client.login(email='user1@gmail.com', password='1234')
        image = self._create_image()
        profile = Profile.objects.get(user=self.user1)

        # check that no image exists before the request
        self.assertFalse(bool(profile.image))

        with open(image.name, 'rb') as f:
            response = self.client.post(reverse('users:edit_profile'), {
                'username': 'user1',
                'about_me': 'Hello world',
                'image': f
            })
        profile.refresh_from_db()

        self.assertTrue(bool(profile.image))

    def _create_image(self):
        """Create a temporary image to test with it"""

        f = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        image = Image.new('RGB', (200, 200), 'white')
        image.save(f, 'PNG')

        return f
