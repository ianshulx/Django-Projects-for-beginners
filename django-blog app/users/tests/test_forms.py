from django.test import TestCase

from ..models import User
from ..forms import EditProfileForm


class EditProfileFormTest(TestCase):
    def test_username_already_taken(self):
        User.objects.create_user(
            username='user1', email='user1@gmail.com', password='1234')

        form = EditProfileForm(
            data={
                'username': 'user1',
                'about_me': 'somthing about me'
            },
            original_username='user'
        )

        self.assertFalse(form.is_valid())
