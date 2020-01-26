from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successfull(self):
        email = "test@email.com"
        password = "P@$$w0rd"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        email = "test@EMAIL.COM"
        password = "P@$$w0rd"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email=None,
                password="P@$$w0rd"
            )

    def test_create_new_super_user(self):
        user = get_user_model().objects.create_super_user(
            email="test@email.com",
            password="P@$$w0rd"
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
