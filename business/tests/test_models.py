from django.test import TestCase
from django.template.defaultfilters import slugify

from model_mommy import mommy

from business.models import (Category, CategoryManager)


class CategoryTestCase(TestCase):

    def setUp(self):
        top = Category(description='Top category',
                       slug=slugify('Top category'))
        top.save()
        level1_first = Category(description='Level1 first',
                                slug=slugify('Level1 first'), parent=top)
        level1_first.save()
        level1_second = Category(description='Level1 second',
                                 slug=slugify('Level1 second'),  parent=top)
        level1_second.save()
        level2_first = Category(description='Level2 first',
                                slug=slugify('Level2 first'),
                                parent=level1_first)
        level2_first.save()
        level2_first_sub = Category(description='Level2 first sub',
                                    slug=slugify('Level2 first sub'),
                                    parent=level2_first)
        level2_first_sub.save()
        level2_second = Category(description='Level2 second',
                                 slug=slugify('Level2 second'),
                                 parent=level1_first)
        level2_second.save()
        top_two = Category(description='Top category two',
                           slug=slugify('Top category two'))
        top_two.save()
        level1_two_first = Category(description='Level1 two first',
                                    slug=slugify('Level1 two first'),
                                    parent=top_two)
        level1_two_first.save()
        level1_two_second = Category(description='Level1 two second',
                                     slug=slugify('Level1 two second'),
                                     parent=top_two)
        level1_two_second.save()
        level1_two_second_sub = Category(description='Level1 two second sub',
                                         slug=slugify('Level1 two second sub'),
                                         parent=level1_two_second)
        level1_two_second_sub.save()


    def tearDown(self):
        Category.objects.all().delete()

    def test_category_str(self):
        self.assertEqual(str(Category.objects.get(slug='level1-first')),
                                        'Top category => Level1 first')

    def test_objects_created(self):
        self.assertEqual(Category.objects.count(), 10)


    def test_category_search(self):
        """
            Test search objects using manager
        """
        search = Category.objects.search('Top category')
        self.assertEqual(len(search), 2)
