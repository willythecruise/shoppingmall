from django.shortcuts import render,redirect
from django.urls import reverse
from .models import OrderItem
from cart.cart import Cart
from .forms import OrderCreateForm

# Create your views here.
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                            product=item['product'],
                                            price=item['price'],
                                            quantity=item['quantity'])

            request.session['order_id'] = order.id
            cart.clear()
            return render(request,
                         'orders/created.html',
                         {'order': order})


    else:
        form = OrderCreateForm()


    return render(request,
     'orders/create.html',
                 {'cart': cart,'form': form})
