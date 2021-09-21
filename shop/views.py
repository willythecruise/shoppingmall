from django.shortcuts import render,get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from .forms import SearchForm
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import TrigramSimilarity
# Create your views here.
@login_required
def product_list(request, category_slug=None):
     category = None
     categories = Category.objects.all()
     products = Product.objects.filter(available=True)
     cart_product_form = CartAddProductForm()
     form=SearchForm()

     if category_slug:
         category = get_object_or_404(Category, slug=category_slug)
         products = products.filter(category=category)
     return render(request,
                     'shop/product/list.html',
                     {'category': category,
                     'categories': categories,
                     'products': products,'cart_product_form': cart_product_form,
                    'section': product_list , 'form':form})

@login_required
def product_search(request):
    form = SearchForm()
    query= None
    results=[]
    if 'query' in request.GET:
        form=SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results=Product.objects.annotate(similarity=TrigramSimilarity('name', query),).filter(available=True,similarity__gt=0.1).order_by('-similarity')
    return render(request,'shop/product/search.html',{'form': form, 'query': query,
                                       'results': results})




@login_required
def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                     id=id,
                                     slug=slug,
                                     available=True)
    cart_product_form = CartAddProductForm()
    return render(request,
                 'shop/product/detail.html',
                 {'product': product,'cart_product_form': cart_product_form})
