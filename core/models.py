from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django_countries.fields import CountryField

CHATEGORY_CHOICES = (
    ('M', 'Makeup'),
    ('S', 'Skincare'),
    ('F', 'Fragrance'),
    ('BB', 'Bath & Body'),
    ('H', 'Hair'),
    ('N', 'Nails'),
)

class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    category = models.CharField(choices=CHATEGORY_CHOICES, max_length=2)
    slug = models.SlugField(max_length=255,default="test-product")
    discount_price = models.FloatField(blank=True, null=True)
    description = models.TextField(default="This is a product description")

    image = models.ImageField(default='default.jpeg')
    additional_info = models.TextField(default="This is an additional information about the product")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={
            'slug': self.slug
        })
    def get_category_display(self):
        return dict(CHATEGORY_CHOICES).get(self.category, "Unknown category")
    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={
            'slug': self.slug
        })
    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={
            'slug': self.slug
        })

class OrderItem(models.Model):
   user = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
   ordered = models.BooleanField(default=False)
   item = models.ForeignKey(Item, on_delete=models.CASCADE)
   quantity = models.IntegerField(default=1)
   def __str__(self):
       return f"{self.quantity} of {self.item.title}"
   def get_total_item_price(self):
         return self.quantity * self.item.price
   def get_total_discount_item_price(self):
        return self.quantity * self.item.discount_price
   def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(default=timezone.now)
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    def __str__(self):
        return self.user.username
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total
    def get_order_summary(self):
        order_summary = {}
        for order_item in self.items.all():
            order_summary[order_item.item.title] = order_item.quantity
        return order_summary

class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    street = models.CharField(max_length=100)
    apartment = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip_code = models.CharField(max_length=100)
    def __str__(self):
        return self.user.username
class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50, auto_created=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username