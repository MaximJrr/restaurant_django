from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus


class TestViews(TestCase):
    def test_index(self):
        path = reverse('index')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'dishes/index.html')