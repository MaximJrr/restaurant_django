from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse


class IndexViewTest(TestCase):
    def test_index_view(self):
        path = reverse('index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'dishes/index.html')


class DishesViewTest(TestCase):
    fixtures = ['goods.json', 'categories.json']

    def test_dishes_view(self):
        path = reverse('dishes:index')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'dishes/menu.html')


