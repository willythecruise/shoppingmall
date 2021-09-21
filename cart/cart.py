
from django.conf import settings
from shop.models import Product
from coupons.models import Coupon
from decimal import Decimal

class Cart(object):
    def __init__(self, request):
        self.session= request.session
        cart=self.session.get(settings.CART_SESSION_ID)#cart=request.session.get('cart')
        if not cart:
            cart= self.session[settings.CART_SESSION_ID]={}#cart = request.session('cart')=[empty]
        self.cart= cart#define app wide variable named cart  = request.session('cart')
        self.coupon_id = self.session.get('coupon_id')
    def add(self, product, quantity=1, override_quantity=False):
         """
         Add a product to the cart or update its quantity.
         """
         product_id = str(product.id)#get the product id and make it a string
         if product_id not in self.cart:#if product.id is not in request.session('cart')
             self.cart[product_id] = {'quantity': 0,
             'price': str(product.price)}#eg request.session('cart')['0']='{quantity': 0, 'price':5000}

         if override_quantity:
             self.cart[product_id]['quantity'] = quantity
         else:
             self.cart[product_id]['quantity'] += quantity
         self.save()

    def save(self):
        """ mark the session as "modified" to make sure it gets saved"""
        self.session.modified = True#request.session.modified=True
    def remove(self, product):
        """
        Remove a product from the cart.
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    def __iter__(self):
        """
        Iterate over the items in the cart and get the products
        from the database.
        """
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
    def __len__(self):
        """
        Count all items in the cart.
        """
        return sum(item['quantity'] for item in self.cart.values())
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item
                    in self.cart.values())
    def clear(self):
        """
     Remove cart from session
     """
        del self.session[settings.CART_SESSION_ID]
        self.save()

    """Code for coupon:

    get_discount(): If the cart contains a coupon, retrieve its discount
    rate and return the amount to be deducted from the total amount of the cart.

    get_total_price_after_discount(): return the total amount of the
    cart after deducting the amount returned by the get_discount() method"""
    @property
    def coupon(self):
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None

    def get_discount(self):
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)

    def get_total_price_after_discount(self):
        return self.get_total_price() - self.get_discount()
