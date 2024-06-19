from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Item, OrderItem, Order, BillingAddress, Payment

class ModelTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='123')
        self.item = Item.objects.create(
            title='Test_item',
            price=1.0,
            category='M',
            slug='test_product',
            description='Test description'
        )
        self.order_item = OrderItem.objects.create(
            user=self.user,
            ordered=False,
            item=self.item,
            quantity=2
        )
        self.order = Order.objects.create(
            user=self.user,
            billing_address=None,
            payment=None
        )
        self.order.items.add(self.order_item)
        self.billing_address = BillingAddress.objects.create(
            user=self.user,
            street='Street',
            apartment='Apartment',
            country='US',
            zip_code='12345'
        )
        self.payment = Payment.objects.create(
            stripe_charge_id='str_test_payment',
            user=self.user,
            amount=1.0
        )

    def test_item_model(self):
        self.assertEqual(self.item.get_absolute_url(), reverse('core:product', kwargs={'slug': self.item.slug}))
        self.assertEqual(self.item.get_add_to_cart_url(), reverse('core:add-to-cart', kwargs={'slug': self.item.slug}))
        self.assertEqual(self.item.get_remove_from_cart_url(), reverse('core:remove-from-cart', kwargs={'slug': self.item.slug}))
        self.assertEqual(self.item.get_category_display(), 'Makeup')

    def test_order_item_model(self):
        self.assertEqual(self.order_item.get_total_item_price(), 2.0)
        self.assertEqual(self.order_item.get_final_price(), 2.0)

    def test_order_model(self):
        self.assertEqual(self.order.get_total(), 2.0)
        order_summary = self.order.get_order_summary()
        self.assertIn(self.item.title, order_summary)
        self.assertEqual(order_summary[self.item.title], 2)
        self.assertEqual(str(self.order), 'test_user')

    def test_billing_address_model(self):
        self.assertEqual(str(self.billing_address), 'test_user')

    def test_payment_model(self):
        self.assertEqual(str(self.payment), 'test_user')

    def test_remove_order_item(self):
        self.order.items.remove(self.order_item)
        self.assertEqual(self.order.get_total(), 0)
        self.assertEqual(self.order.get_order_summary(), {})

    def test_order_item_string_representation(self):
        self.assertEqual(str(self.order_item), '2 of Test_item')

    def test_order_item_final_price_with_discount(self):
        self.item.discount_price = 0.5
        self.item.save()
        self.assertEqual(self.order_item.get_final_price(), 1.0)

    # Additional important tests

    def test_order_item_increases_quantity(self):
        order_item_2 = OrderItem.objects.create(
            user=self.user,
            ordered=False,
            item=self.item,
            quantity=1
        )
        self.order.items.add(order_item_2)
        self.assertEqual(self.order.get_total(), 3.0)

    def test_item_string_representation(self):
        self.assertEqual(str(self.item), 'Test_item')

    def test_order_empty_items(self):
        order = Order.objects.create(user=self.user)
        self.assertEqual(order.get_total(), 0)
        self.assertEqual(order.get_order_summary(), {})

    def test_order_with_multiple_items(self):
        item2 = Item.objects.create(
            title='Test_item1',
            price=10.0,
            category='S',
            slug='another-product',
            description='This is another test description'
        )
        order_item2 = OrderItem.objects.create(
            user=self.user,
            ordered=False,
            item=item2,
            quantity=1
        )
        self.order.items.add(order_item2)
        self.assertEqual(self.order.get_total(), 12.0)

    def test_item_get_absolute_url(self):
        url = self.item.get_absolute_url()
        self.assertEqual(url, reverse('core:product', kwargs={'slug': self.item.slug}))

    def test_order_item_total_discount_price(self):
        self.item.discount_price = 8.0
        self.item.save()
        self.assertEqual(self.order_item.get_total_discount_item_price(), 16.0)
