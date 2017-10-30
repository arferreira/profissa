# django imports
from django.test import TestCase
from django.urls import reverse

# third imports
from model_mommy.mommy import make

# zummbee imports
from core.models import Newsletter


class NewsletterModelTest(TestCase):
    """
    Teste unitário para Newsletter
    """
    def setUp(self):
        """
        Setup de todos os testes
        """
        self.newsletter = make(Newsletter)

    def tearDown(self):
        Newsletter.objects.all().delete()

    def test_created_object(self):
        print("** testing the creation of a newsletter **")
        self.assertEqual(Newsletter.objects.all().count(), 1)

    def test_created_newsletter_blank(self):
        print("** testing the creation of a newsletter with blank email **")
        blank_email = Newsletter.objects.create(email='')




