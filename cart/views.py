from django.shortcuts import render,redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from cart.forms import CartAddProductForm
from coupons.forms import CouponApplyForm
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import path
# Create your views here.
@require_POST
def cart_add(request, product_id,site):
     cart = Cart(request)
     product = get_object_or_404(Product, id=product_id)
     form = CartAddProductForm(request.POST)
     if form.is_valid():
         cd = form.cleaned_data
         cart.add(product=product,
         quantity=cd['quantity'],
         override_quantity=cd['override'])
     return redirect(reverse(site))

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect("cart:cart_detail")

@login_required
def cart_detail(request):
     cart = Cart(request)
     if cart.get_total_price()<=0:
         return redirect("shop:product_list")
     for item in cart:
         item['update_quantity_form'] = CartAddProductForm(initial={
                                                 'quantity': item['quantity'],
                                                'override': True})
     coupon_apply_form = CouponApplyForm()
     return render(request, 'cart/detail.html', {'cart': cart,'coupon_apply_form': coupon_apply_form })