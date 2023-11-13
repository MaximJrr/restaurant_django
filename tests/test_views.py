from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus

from dishes.models import Dish, DishCategory, Basket
from orders.models import Order
from users.models import User, Reservation, EmailVerification


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


class EmailVerificationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user', password='test_user12345', email='testuser@gmail.com'
        )
        self.email_verification = EmailVerification.objects.create(
            user=self.user,
            unique_code='9edff54c-5914-4aba-ac5a-65cbfda96093',
            expiration_time='2035-09-20 16:11:00'
        )
        self.path = reverse(
            'users:email_verification',
            kwargs={'email': self.user.email, 'unique_code': '9edff54c-5914-4aba-ac5a-65cbfda96093'}
        )
        self.response = self.client.get(self.path)

    def test_email_verification_valid_data(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.response, 'users/email_verification.html')
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_verified_email)


class UserProfileTest(TestCase):
    def setUp(self):
        get_user_model().objects.create_user(username='test_user', email='test@example.com',
                                                         password='test_password')
        self.client.login(username='test_user', password='test_password')
        self.data = {
            'first_name': 'test_user',
            'last_name': 'test_last_name'
        }
        self.path = reverse('users:profile')

    def test_form_get(self):
        response = self.client.get(self.path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/profile.html')

    def test_valid_data(self):
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:profile'))

    def test_invalid_first_name(self):
        self.data['first_name'] = 'q' * 21
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Длина имени не должна превышать 20 символов", html=True)

    def invalid_last_name(self):
        self.data['last_name'] = 'q' * 21
        response = self.client.post(self.path, self.data)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "Длина фамилии не должна превышать 20 символов", html=True)


# orders app views

class SuccessTemplateTest(TestCase):
    def test_template(self):
        path = reverse('orders:order-success')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'orders/success.html')


class CancelTemplateTest(TestCase):
    def test_template(self):
        path = reverse('orders:order-cancel')
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'orders/cancel.html')


class OrderListTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.client.login(username='test_user', password='test_password')
        self.path = reverse('orders:orders-list')
        self.response = self.client.get(self.path)

    def test_order_list(self):
        Order.objects.create(
            first_name='test_order',
            last_name='test_last_name',
            email='test_email123@gmail.com',
            address='test_address123',
            basket_history={},
            initiator=self.user
        )

        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.response, 'orders/orders.html')


class OrderDetailTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.order = Order.objects.create(
            first_name='test_order',
            last_name='test_last_name',
            email='test_email123@gmail.com',
            address='test_address123',
            basket_history={},
            initiator=self.user
        )
        self.path = reverse('orders:order-detail', kwargs={'pk': self.order.id})
        self.response = self.client.get(self.path)

    def test_order_detail(self):
        self.assertEqual(self.response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(self.response, 'orders/order.html')


class OrderCreateTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='test_password')
        self.client.login(username='test_user', password='test_password')

    @patch('stripe.checkout.Session.create')
    def test_order_create(self, mock_stripe_session_create):
        mock_stripe_session_create.return_value.url = 'https://example.com/stripe-checkout'
        category = DishCategory.objects.create(
            name='тест',
            slug='test',
            description='test'
        )
        dish = Dish.objects.create(
            name='тест',
            slug='slug',
            description='test_description',
            price=300,
            weight=300,
            category=category
        )
        Basket.objects.create(user=self.user, dish=dish, quantity=1)
        data = {
            'first_name': 'Test',
            'last_name': 'Test',
            'email': 'test12345@gmail.com',
            'address': 'test address 123',
        }
        path = reverse('orders:order-create')
        response = self.client.post(path, data)

        self.assertEqual(response.status_code, HTTPStatus.SEE_OTHER)
        self.assertEqual(Order.objects.count(), 1)
        created_order = Order.objects.first()
        self.assertEqual(created_order.initiator, self.user)
