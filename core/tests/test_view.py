from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Item, OrderItem, Order

class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.item = Item.objects.create(
            title='Test_item',
            price=1.00,
            category='M',
            slug='test-item'
        )
        self.order = Order.objects.create(user=self.user, ordered=False)
        self.order_item = OrderItem.objects.create(
            user=self.user,
            item=self.item,
            ordered=False,
            quantity=2
        )
        self.order.items.add(self.order_item)

    def test_checkout_view_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('core:checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout.html')
        # Add more assertions as needed

    def test_checkout_view_post(self):
        self.client.force_login(self.user)
        data = {
            'street': 'Street',
            'apartment': 'Apartment',
            'country': 'US',
            'zip_code': '12345',
            'payment_option': 'S',
        }
        response = self.client.post(reverse('core:checkout'), data)
        self.assertRedirects(response, reverse('core:payment', kwargs={'payment_option': 'stripe'}))
        # Add more assertions as needed

    def test_payment_view_get(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('core:payment', kwargs={'payment_option': 'stripe'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payment.html')
        # Add more assertions as needed

    def test_payment_view_post(self):
        self.client.force_login(self.user)
        token = 'tok_visa'  # Replace with a valid token for testing
        response = self.client.post(reverse('core:payment', kwargs={'payment_option': 'stripe'}), {'stripeToken': token})
        self.assertRedirects(response, '/')
        # Add more assertions as needed

    def test_payment_complete_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('core:payment-complete'))
        self.assertRedirects(response, '/')
        # Add more assertions as needed

    def test_home_view(self):
        response = self.client.get(reverse('core:'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        # Add more assertions as needed

    def test_search_for_products_view(self):
        response = self.client.get(reverse('core:search_product', kwargs={'search': 'test'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        # Add more assertions as needed

    def test_search_for_product_in_category_view(self):
        response = self.client.get(reverse('core:search_product_in_category_page', kwargs={'search': 'test', 'category': 'test_category'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category.html')
        # Add more assertions as needed

    def test_get_category_view(self):
        response = self.client.get(reverse('core:category', kwargs={'category': 'test_category'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category.html')
        # Add more assertions as needed

    def test_order_summary_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('core:order-summary'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'order_summary.html')
        # Add more assertions as needed

    def test_add_to_cart_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('core:add-to-cart', kwargs={'slug': self.item.slug}))
        self.assertRedirects(response, reverse('core:order-summary'))
        # Add more assertions as needed

    def test_remove_from_cart(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('core:remove-from-cart', kwargs={'slug': 'test-item'}))
        self.assertRedirects(response, reverse('core:order-summary'))
        self.assertEqual(OrderItem.objects.filter(user=self.user, item=self.item, ordered=False).count(), 0)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), "This item was removed from your cart.")

    def test_remove_one_item_from_cart(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('core:remove-one-item-from-cart', kwargs={'slug': 'test-item'}))

        self.assertRedirects(response, reverse('core:order-summary'))
        self.order_item.refresh_from_db()
        self.assertEqual(self.order_item.quantity, 1)
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), "This item quantity was updated.")
