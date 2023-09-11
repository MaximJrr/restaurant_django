from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus

from dishes.models import Dish, DishCategory


# dishes app views


class IndexViewTest(TestCase):
    fixtures = ['dishes.json', 'dishes_categories.json']

    def test_view(self):
        path = reverse('index')
        response = self.client.get(path)
        dishes = Dish.objects.all().order_by('-id')[:3]

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'dishes/index.html')
        self.assertEqual(list(response.context_data['dishes']), list(dishes))


class DishesListViewTest(TestCase):
    fixtures = ['dishes.json', 'dishes_categories.json']

    def test_dishes_list(self):
        path = reverse('dishes:index')
        response = self.client.get(path)
        dishes = Dish.objects.all()[:9]

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'dishes/menu.html')
        self.assertEqual(list(response.context_data['dishes']), list(dishes))

    def test_categories_list(self):
        category = DishCategory.objects.first()
        path = reverse('dishes:category', kwargs={'category_slug': category.slug})
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'dishes/menu.html')
        self.assertEqual(len(response.context['categories']), 7)


