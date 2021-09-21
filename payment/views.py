from django.shortcuts import render,redirect,get_object_or_404
import braintree
from django.urls import reverse
from django.conf import settings
from orders.models import Order
from requests.exceptions import ConnectionError
from django.http import JsonResponse

gateway=braintree.BraintreeGateway(settings.BRAINTREE_CONF)

def payment_process(request):
    order_id= request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()
    if request.method=='POST':
        nonce= request.POST.get('payment_method_nonce',None)

        result = gateway.transaction.sale({
             'amount': f'{total_cost:.2f}',
             'payment_method_nonce': nonce,
             'options': {
             'submit_for_settlement': True
             }
             })
        if result.is_success:
            order.paid = True
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        #generate token
        try:
            client_token = gateway.client_token.generate()
            return render(request,
                         'payment/process.html',
                         {'order': order,
                   'client_token': client_token})
        except ConnectionError as e:
            return redirect('orders:order_create')


def payment_done(request):
    return render(request, 'payment/done.html')
def payment_canceled(request):
    return render(request, 'payment/canceled.html')
