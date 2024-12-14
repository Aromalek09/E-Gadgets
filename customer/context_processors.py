from account.models import Cart,Orders

def item_count(request):
    if request.user.is_authenticated:
        cart_count=Cart.objects.filter(user=request.user).count()
        order_count=Orders.objects.filter(user=request.user).count()
        return {'cart':cart_count,'order':order_count}
    else:
        return {"orders":0,"cart":0}