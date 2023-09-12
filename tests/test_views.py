from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus

from dishes.models import Dish, DishCategory
from restaurant.settings import LOGIN_REDIRECT_URL
from users.models import User


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


# users app views

class UserRegistrationTest(TestCase):
    def setUp(self):
        self.path = reverse('users:register')
        self.data = {
            'first_name': 'Maxim',
            'last_name': 'Maxim',
            'username': 'Maxim12345',
            'email': 'maxim12345@gmail.com',
            'password1': '123456Qrthjdq',
            'password2': '123456Qrthjdq',
        }

    def test_user_registration_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_registration_post(self):
        username = self.data['username']
        response = self.client.post(self.path, data=self.data)

        self.assertFalse(User.objects.filter(username=username).exists())
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))
        self.assertTrue(User.objects.filter(username=username).exists())

    def test_errors(self):
        User.objects.create(username=self.data['username'])
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, 'Пользователь с таким именем уже существует.', html=True)


class UserLoginTest(TestCase):
    def setUp(self):
        self.path = reverse('users:login')

    def test_user_login_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')
