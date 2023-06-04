from django.urls import path 
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('singlepage/<slug:slug_id>/',views.singlepage,name='singlepage'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('products/',views.products,name='products'),
    path('search/',views.search,name='search'),
    path('register/',views.register,name='register'),
    path('login/',views.userlogin,name='login'),
    path('logoutuser/',views.logoutuser,name='logoutuser'),
    path('addtocart/<int:id>/',views.addtocart,name='addtocart'),
    path('myCart/',views.myCart,name='myCart'),
    path('manageCart/<int:id>/',views.manageCart,name='manageCart'),
    path('emptyCart/',views.emptyCart,name='emptyCart'),
    path('checkout/',views.checkout,name='checkout'),
    path('transfer/',views.transferPage,name='transfer'),
    path('payment/<int:id>/',views.paymentPage,name='payment'),
    path('<str:ref>/',views.verify_payment,name='verify-payment'),
    path('profile',views.profile,name='profile'),
    path('blog',views.blog,name='blog'),
    path('blog/<slug:slug_id>/',views.blogdetail,name='blogdetail'),
    path('flatdiscount/<slug:slug_id>/',views.flatdiscountdetail,name='flatdiscountdetail'),
    path('terms',views.terms,name='terms'),
    path('privacy',views.privacy,name='privacy'),
]

