from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, View
from .models import Item, OrderItem, Order, CHATEGORY_CHOICES, BillingAddress, Payment
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CheckoutForm
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def product(request):
    context = {
        'object_list': Item.objects.all()
    }
    return render(request, 'product.html', context)
class CheckoutView(View):
    def get(self,*args, **kwargs):
        form = CheckoutForm()
        context = {
            'form': form
        }

        return render(self.request, 'checkout.html', context)
    def post(self,*args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street = form.cleaned_data.get('street')
                apartment = form.cleaned_data.get('apartment')
                country = form.cleaned_data.get('country')
                zip_code = form.cleaned_data.get('zip_code')
                payment_option = form.cleaned_data.get('payment_option')
                billing_address = BillingAddress(
                    user=self.request.user,
                    street=street,
                    apartment=apartment,
                    country=country,
                    zip_code=zip_code,
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                if payment_option == 'S':
                    return redirect('core:payment', payment_option='stripe')
                elif payment_option == 'P':
                    return redirect('core:payment', payment_option='paypal')
                else:
                    messages.warning(self.request, "Invalid payment option selected")
                    return redirect('core:checkout')
            messages.warning(self.request, "Failed checkout")
            return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have an active order")
            return redirect("core:order-summary")

class PaymentView(View):
    def get(self,*args, **kwargs):
        context = {

            'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY,
            'payment_option': self.kwargs['payment_option'],
            'order': Order.objects.get(user=self.request.user, ordered=False)
        }
        return render(self.request, 'payment.html', context)
    def post(self,*args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        print(token)

        amount = int(order.get_total() * 100)

        try:
            charge = stripe.Charge.create(
                amount= amount,
                currency="usd",
                source=token
            )

            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()
            order.ordered = True
            order.payment = payment
            order.save()
            messages.success(self.request, "Your order was successful!")
            return redirect("/")
        except stripe.error.CardError as e:
            body = e.json_body
            err = body.get('error', {})
            messages.error(self.request, f"{err.get('message')}")
            return redirect("/")
        except stripe.error.RateLimitError as e:
            messages.error(self.request, "Rate limit error")
            return redirect("/")
        except stripe.error.InvalidRequestError as e:
            messages.error(self.request, "Invalid parameters")
            return redirect("/")
        except stripe.error.AuthenticationError as e:
            messages.error(self.request, "Not authenticated")
            return redirect("/")
        except stripe.error.APIConnectionError as e:
            messages.error(self.request, "Network error")
            return redirect("/")
        except stripe.error.StripeError as e:
            messages.error(self.request, "Something went wrong. You were not charged. Please try again.")
            return redirect("/")
        except Exception as e:
            messages.error(self.request, "A serious error occurred. We have been notifed.")
            return redirect("/")
def payment_complete(request):
    order = Order.objects.get(user=request.user, ordered=False)
    payment = Payment()
    payment.user = request.user
    payment.amount = order.get_total()
    payment.save()
    order.ordered = True
    order.payment = payment

    order.save()
    messages.success(request, "Your order was successful!")
    return redirect("/")
class HomeView(ListView):
    model = Item
    template_name = 'home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = CHATEGORY_CHOICES
        return context
def search_for_products(request, search):
    search_result = Item.objects.filter(title__icontains=search)
    context = {
        'object_list': Item.objects.all(),
        'search_result': search_result,
        'categories': CHATEGORY_CHOICES
    }
    return render(request, 'home.html', context)
def search_for_product_in_category_page(request, search, category):
    search_result = Item.objects.filter(title__icontains=search, category=category)
    context = {
        'object_list': Item.objects.filter(category=category),
        'search_result': search_result,
        'categories': CHATEGORY_CHOICES,
        'category': category
    }
    return render(request, 'category.html', context)
def get_category(request, category):
    context = {
        'object_list': Item.objects.filter(category=category),
        'categories': CHATEGORY_CHOICES,
        'category': category
    }
    return render(request, 'category.html', context)
class OrderSummaryView(LoginRequiredMixin,View):
   def get(self, *args, **kwargs):
         try:
             order = Order.objects.get(user=self.request.user, ordered=False)
             context = {
                    'object': order
                }
             return render(self.request, 'order_summary.html', context)
         except ObjectDoesNotExist:
             messages.error(self.request, "You do not have an active order")
             return redirect("/")

class ItemDetailView(DetailView):
    model = Item
    template_name = 'product.html'
@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item,slug=slug)
    order_item, created= OrderItem.objects.get_or_create(
    item=item,
    user = request.user, ordered=False
    )
    order_s = Order.objects.filter(user=request.user, ordered=False)
    if order_s.exists():
        order = order_s[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item was added to your cart.")
            order.items.add(order_item)
            return redirect("core:order-summary")
    else:

        order_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=order_date)
        order.items.add(order_item)
        messages.info(request, "This item quantity was updated.")
        return redirect("core:order-summary")
@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_s = Order.objects.filter(user=request.user, ordered=False)
    if order_s.exists():
        order = order_s[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            order_item.delete()  # Ensure the order item is deleted
            messages.info(request, "This item was removed from your cart.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item wasn’t in your cart.")
            return redirect("core:order-summary")
    else:
        messages.info(request, "You don’t have an active order.")
        return redirect("core:order-summary")
@login_required
def remove_one_item_from_cart(request, slug):
    item = get_object_or_404(Item,slug=slug)
    order_s = Order.objects.filter(user=request.user, ordered=False)
    if order_s.exists():
        order = order_s[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
              item=item,
              user = request.user,
              ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)

            messages.info(request, "This item quantity was updated.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "This item wasn`t in your cart.")
            return redirect("core:product",  slug = slug)
    else:
        messages.info(request, "You don`t have an active order.")
        return redirect("core:product",  slug = slug)
