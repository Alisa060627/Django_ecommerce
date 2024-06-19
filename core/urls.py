from django.urls import path
from .views import CheckoutView, HomeView, ItemDetailView, add_to_cart, remove_from_cart, OrderSummaryView,remove_one_item_from_cart, PaymentView, payment_complete, get_category, search_for_products, search_for_product_in_category_page
app_name = 'core'
urlpatterns = [
    path('', HomeView.as_view(), name=''),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('checkout/',CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-one-item-from-cart/<slug>/', remove_one_item_from_cart, name='remove-one-item-from-cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('payment-complete/', payment_complete, name='payment-complete'),
    path('category/<category>/',get_category, name='category'),
    path('search_product/<search>/',search_for_products, name='search_product'),
    path('search_product_in_category_page/<category>/<search>/',search_for_product_in_category_page, name='search_product_in_category_page'),



]
