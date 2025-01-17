from django.urls import path
from . import views

urlpatterns = [
    path('', views.homefunction, name='home'),
    path('products', views.productfunction, name='products'),
    path('category', views.categoryfunction, name='category'),
    path('catcat<int:id>', views.catcategoryfunction, name='catcat'),
    path('catcategoryproducts/<int:id>/', views.catcategory_products, name='catcatproducts'),
    path('viewproduct/<int:id>/', views.viewproductfunction, name='viewproduct'),
    path('signup', views.signfunction, name='signfunction'),
    path('login', views.loginfunction, name='loginfunction'),  
    path('logout', views.logoutfunction, name='logoutfunction'),  
    path('cartpage',views.cartpage,name='cartpage'),
    path('addtocart<int:id>',views.addtocart,name='addtocart'),
    path('remove<int:id>',views.removefunction,name='remove'),
    path('movetowish<int:id>',views.movetowish,name='movetowish'),
    path('wishpage',views.wishpage,name='wishpage'),
    path('remove_wishitem<int:id>',views.remove_wishitem,name='remove_wishitem'),
    path('men',views.men_wear,name='men'),
    path('women',views.women_wear,name='women'),
    path('beauty',views.beauty_,name='beauty'),
    path('kids',views.kids_wear,name='kids'),
    path('home_living',views.home_living,name='home_living'),
    path('jewellery',views.jewellery,name='jewellery'),
    path('placeorder',views.placeorderfunction,name='placeorder'),
    path('thankyou',views.orderconfirmfunction,name='thankyou'),
    path('adminhome',views.adminhome,name='adminhome'),
    path('login_page',views.loginPage,name='login_page'),
    path('signup_page',views.signupPage,name='signup_page'),
    path('login_wish', views.login_wish, name='login_wish'),
    path('signup_wish', views.signup_wish, name='signup_wish'),
    path('product_search',views.product_search,name='product_search'),

]