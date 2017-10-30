# coding: utf-8
from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.core import mail

from model_mommy.mommy import make

from accounts.forms import RegistrationForm
from accounts.models import User


class LoginLogoutViewTest(TestCase):
    def test_correct_response(self):
        response = self.client.get(reverse('login'))

        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_redirect_to_home(self):
        people = make(settings.AUTH_USER_MODEL, email='foo@foo.com')
        people.set_password('123@123')

        data = {'username': 'foo@foo.com', 'password': '123@123'}
        response = self.client.post(reverse('login'), data)

        self.assertEqual(response.status_code, 200)

    def test_logout_user_logged(self):
        response = self.client.get(reverse('logout'))

        self.assertEqual(response.status_code, 302)


class RegistrationView(TestCase):
    def setUp(self):
        self.url = reverse('accounts:registration')
        self.response = self.client.get(self.url)

    def test_redirect_to_root_directory_if_logged(self):
        user = User.objects.create_user(
                email='testuser@example.com', first_name='foo')
        user.set_password('pass')
        user.save()

        self.client.login(email='testuser@example.com', password='pass')

        self.response = self.client.get(self.url)
        redirect_url = reverse('providers:dashboard')

        self.assertRedirects(self.response, redirect_url)

    def test_renders_correct_template(self):
        self.assertTemplateUsed(self.response, 'accounts/registration.html')

    def test_form_in_context(self):
        self.assertIn('form', self.response.context)
        form = self.response.context['form']
        self.assertIsInstance(form, RegistrationForm)

    def test_valid_post(self):
        response = self.client.post(self.url, {
            'email': 'jalim@example.com',
            'first_name': 'Jalim',
            'last_name': 'Rablin',
            'password1': '123qaz',
            'password2': '123qaz',
        })

        self.assertRedirects(response,
                             reverse(
                                 'accounts:registration_complete',
                             ))

    def test_registration_dont_activate_user(self):
        self.client.post(self.url, {
            'email': 'jalim@example.com',
            'first_name': 'Jalim',
            'last_name': 'Rablin',
            'password1': '123qaz',
            'password2': '123qaz',
        })
        user = User.objects.get(email='jalim@example.com')
        self.assertFalse(user.is_active)

    def test_registration_sends_confirmation_email(self):
        self.assertEqual(0, len(mail.outbox))
        self.client.post(self.url, {
            'email': 'jalim@example.com',
            'first_name': 'Jalim',
            'last_name': 'Rablin',
            'password1': '123qaz',
            'password2': '123qaz',
        })
        self.assertEqual(1, len(mail.outbox))

    def test_mail_content(self):
        self.assertEqual(0, len(mail.outbox))

        self.client.post(self.url, {
            'email': 'jalim@example.com',
            'first_name': 'Jalim',
            'last_name': 'Rablin',
            'password1': '123qaz',
            'password2': '123qaz',
        })
        msg = mail.outbox[0]
        user = User.objects.last()
        self.assertIn(user.confirmation_key, msg.body)
        self.assertIn(reverse('accounts:activation'), msg.body)

    def test_duplicate_user(self):
        make(settings.AUTH_USER_MODEL, email='foo@foo.com')

        response = self.client.post(self.url, {
            'email': 'foo@foo.com',
            'first_name': 'Jalim',
            'last_name': 'Rablin',
            'password1': '123qaz',
            'password2': '123qaz',
            })

        self.assertIn('messages', response.context)

        [self.assertEqual(
            message.message, '') for message in response.context['messages']]


class ActivationViewTestCase(TestCase):
    def test_activate_user(self):
        people = make(settings.AUTH_USER_MODEL, email='foo@foo.com',
                      is_active=False)
        people.set_password('123@123')
        people.save()

        response = self.client.get(
            reverse('accounts:activation'),
            {'activation_key': people.get_confirmation_key()})

        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.get(email='foo@foo.com').is_active)
