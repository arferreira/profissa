from django.test import TestCase

from model_mommy import mommy

from accounts.models import (User, Profile, Document)



class UserTestModel(TestCase):

    def setUp(self):
        self.users = mommy.make(User, _quantity=2)

    def tearDown(self):
        User.objects.all().delete()

    def test_create_user(self):
        print("** Test create user model **")
        self.assertEqual(User.objects.count(), 2)


class ProfileTestModel(TestCase):
    def setUp(self):
        self.user = mommy.make(User)

    def tearDown(self):
        User.objects.all().delete()

    def test_created_instance(self):
        print("** testing create a profile instance for user **")
        profile = self.user.profile
        profile.bio = 'Im building web apps like a zummbee'
        profile.save()
        self.assertEqual(self.user.profile.bio, 'Im building web apps like' \
                                                ' a zummbee')

class DocumentTestModel(TestCase):
    def setUp(self):
        self.user = mommy.make(User)
        self.document = mommy.make(Document, profile=self.user.profile)

    def tearDown(self):
        User.objects.all().delete()

    def test_status_document(self):
        print("** testing a status of a document **")
        self.assertFalse(self.document.status, False)
