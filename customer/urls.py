from egadgets.urls import path,include 
from .views import *

urlpatterns=[
    path('chome',CustomerHomeView.as_view(),name='home'),
    path('plist/<str:cat>',ProductListView.as_view(),name='plist'),
    path('pdetail/<int:pid>',ProductDetailView.as_view(),name='pdetail'),
    path("cart/<int:id>",addtocart,name='acart'),
    path('carts',CartListview.as_view(),name='cartlist'),
    path('inc/<int:id>',increasequantity,name='inc'),
    path('dec/<int:id>',decreasequantity,name='dec'),
    path('removeitem<int:id>',deletecartitem,name='delcart'),
    path('placeorder<int:id>',placeorder,name='porder'),
    path('orderlist',OrderListView.as_view(),name='orders'),
    path('cancel<int:id>',cancelorder,name='cancel'),
    path('search',SearchProduct,name='search'),
]