from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import TemplateView,ListView,DetailView
from account.models import products,Cart,Orders
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

# Create your views here.



# class CustomerHomeView(View):
#     def get(self,request):
#         return render(request,"home.html")



def signin_required(fn):
    def inner(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)

        else:
            messages.error(request,"please login")
            return redirect('log')
        
    return inner

decorators=[never_cache,signin_required]

@method_decorator(decorator=decorators,name='dispatch')    
class CustomerHomeView(TemplateView):
    template_name="home.html"
    
    
@method_decorator(decorator=decorators,name='dispatch')    
class ProductListView(ListView):
    template_name='productlist.html'
    queryset=products.objects.all()
    context_object_name="products"
    def get_queryset(self):
        cat=self.kwargs.get('cat')
        self.request.session['category']
        return self.queryset.filter(category=cat)

# class ProductListView(View):
#     template_name='productlist.html'
#     queryset=products.objects.all()
#     context_object_name="products"
#     def get(self,request):
#         queryset=self.queryset
#         return render(request,self.template_name,{self.context_object_name:queryset})
        
        
def SearchProduct(request,*args,**kwargs):
    keyword=request.POST['searchkey']
    cat=request.session['category']
    if keyword:
        product=products.objects.filter(title__icontains=keyword,category=cat)
        return render(request,"productlist.html",{"products":product})
    else:
        messages.warning(request,"invalid search keyword!!")
        return redirect('plist',cat=cat)


@method_decorator(decorator=decorators,name='dispatch')    
class ProductDetailView(DetailView):
    template_name="productdetails.html"
    queryset=products.objects.all()
    context_object_name="product"
    pk_url_kwarg="pid"

decorators
def addtocart(request,*args,**kwargs):
    try:
        pid=kwargs.get('id')
        product=products.objects.get(id=pid)
        user=request.user
        cartcheck=Cart.objects.filter(product=product,user=user).exists()
        if cartcheck:
            cartitem=Cart.objects.create(product=product,user=user)
            cartitem.quantity+=1
            cartitem.save()
            messages.success(request,"cart-item quantity increased")
            return redirect('home')
        else:
            Cart.objects.create(product=product,user=user)
            messages.success(request,f"{product.title}Added to cart")
            return redirect ('home')
    except Exception as e:
        print(e)
        messages.warning(request,"something went wrong")
        return redirect('home')            

@method_decorator(decorator=decorators,name='dispatch')     
class CartListview(ListView):
        template_name="cart.html"
        queryset=Cart.objects.all()
        context_object_name="carts"
        
        def get_queryset(self):
            qs=self.queryset.filter(user=self.request.user)
            return qs
            
            
decorators      
def increasequantity(request,*args,**kwargs):
    try:
        cid=kwargs.get('id')
        cart=Cart.objects.get(id=cid)
        cart.quantity+=1
        cart.save()
        return redirect('cartlist')
    except:
        messages.warning(request,"spomething went wrong!!")
        return redirect('cartlist')
    
    
    
decorators
def decreasequantity(request,*args,**kwargs):
    try:
        cid=kwargs.get('id')
        cart=Cart.objects.get(id=cid)
        if cart.quantity==1:
            cart.delete()
            return redirect('cartlist')
        else:
            cart.quantity-=1
            cart.save()
        return redirect('cartlist')
    except:
        messages.warning(request,"spomething went wrong!!")
        return redirect('cartlist')
    

decorators
def deletecartitem(request,*args,**kwargs):
    try:
        cid=kwargs.get('id')
        cart=Cart.objects.get(id=cid)
        cart.delete()
        messages.success(request,"item removed from cart")
        return redirect('cartlist')
    except:
        messages.warning(request,"spomething went wrong!!")
        return redirect('cartlist')

decorators
def placeorder(request,**kwargs):
    try:
        cid=kwargs.get('id')
        cart=Cart.objects.get(id=cid)
        Orders.objects.create(product=cart.product,user=request.user,quantity=cart.quantity)
        cart.delete()
        
        #mail sending
        
        subject="Egadgets order verification"
        msg=f"order for {cart.product.title} is placed"
        f_rom="aromalek20@gmail.com"
        to_id=request.user.email
        send_mail(subject,msg,f_rom,[to_id],fail_silently=True)
        
        messages.success(request,f'{cart.product.title}\' s order placed')
        return redirect('cartlist')
    
    except:
        messages.warning(request,"spomething went wrong!!")
        return redirect('cartlist')

@method_decorator(decorator=decorators,name='dispatch')     
class OrderListView(ListView):
    template_name='orders.html'
    queryset=Orders.objects.all()
    context_object_name='orders'
    def get_queryset(self):
        return Orders.objects.filter(user=self.request.user)
    


decorators
def cancelorder(request,**kwargs):
    try:
        oid=kwargs.get('id')
        order=Orders.objects.get(id=oid)
        order.status="cancelled"
        order.save()
        messages.success(request,"order cancelled!!")
        return redirect('orders')
    
    except:
        messages.warning(request,"something went wrong!!")
        
        return redirect('orders')
    
