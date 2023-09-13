from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus

from dishes.models import Dish, DishCategory
from users.models import User, Reservation


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


class UserReservationVerificationTest(TestCase):
    def test_verification_get(self):
        path = reverse('users:reservation_verification')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/reservation_verification.html')


class UserReservationTest(TestCase):
    def setUp(self):
        User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.path = reverse('users:reservation')
        self.data = {
            'name': 'testuser',
            'how_many_people': '3',
            'date_time': '2023-09-15 12:00:00',
            'table_number': '5'
        }

    def test_form_valid(self):
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:reservation_verification'))

    def test_reservation_form_duplicate(self):
        Reservation.objects.create(
            name='testuser', how_many_people='3', date_time='2023-09-15 12:00:00', table_number='5'
        )
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(
            response, 'Данное место на указанное время уже занято, выберите другое место, или время'
        )
