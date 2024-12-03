from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from.models import*
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q 

def homefunction(request):
    categories = Category.objects.all().prefetch_related('catcategory_set')
    category=Category.objects.all()
    return render(request, 'home.html', {'categories': categories,'category':category})

def productfunction(request):
    products=Product.objects.all()
    print(products)
    return render(request,'products.html',{'products':products})
def categoryfunction(request):
    category=Category.objects.all()
    return render(request,'category.html',{'category':category})
def catcategoryfunction(request,id):
    category=Category.objects.get(id=id)
    catcategories = Catcategory.objects.filter(category=category)
    products = Product.objects.filter(catcategory__category=category)
    return render(request,'catcat.html',{'category': category, 
        'catcategories': catcategories,
        'products': products})

def catcategory_products(request, id):
    catcategory = get_object_or_404(Catcategory, id=id)
    products = Product.objects.filter(catcategory=catcategory)

    return render(request, 'productbycatcategory.html', {
        'catcategory': catcategory,
        'products': products
    })

def viewproductfunction(request,id):
    product=Product.objects.get(id=id)
    return render(request,'viewproduct.html',{'viewproduct':product})
def signfunction(request):
    if request.method == 'POST':
        username=request.POST.get('name')
        email=request.POST['email']
        password=request.POST['password']
        user = User.objects.create_user(username, email, password)
        user.save()
        # saved_cart_items = request.session.get('cart_items', [])
        # for product_id in saved_cart_items:
        #     try:
        #         product = Product.objects.get(id=product_id)
        #         cart_item, created = Cart.objects.get_or_create(user=user, product=product)
        #         if created:
        #             cart_item.quantity = 1
        #             cart_item.price = product.price
        #             cart_item.save()
        #     except Product.DoesNotExist:
        #         messages.error(request, f"Product with ID {product_id} does not exist.")

        # # Clear session cart items
        # request.session.pop('cart_items', None)
        
        # messages.success(request, "Signup successful! Please log in.")
        # return redirect('login_page') 
        previous_url = request.META.get('HTTP_REFERER', 'home')  # Get previous page or fallback to 'home'
        return redirect(previous_url)
    return render(request,'home.html')
    
def loginfunction(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('adminhome')


            next_url = request.META.get('HTTP_REFERER', 'home')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid credentials")
            return redirect('loginfunction')

    return redirect('home')
def adminhome(request):
    return render(request,'adminhome.html')
def logoutfunction(request):
    logout(request)
    return redirect('home')
def removefunction(request,id):
    if request.user.is_authenticated:
        cartitems=Cart.objects.get(id=id,user=request.user)

        cartitems.delete()
        return redirect('cartpage')

    else:
        return redirect('login')
def remove_wishitem(request,id):
    if request.user.is_authenticated:
        wishitems=Wishlist.objects.get(id=id,user=request.user)

        wishitems.delete()
        return redirect('wishpage')

    else:
        return redirect('login')
def men_wear(request):
    men_wear=Category.objects.get(name='MEN')
    product=Product.objects.filter(category=men_wear)
    return render(request,'men.html',{'products':product})
def women_wear(request):
    women_wear=Category.objects.get(name='WOMEN')
    product=Product.objects.filter(category=women_wear)
    return render(request,'women.html',{'products':product})
def kids_wear(request):
    kids_wear=Category.objects.get(name='KIDS')
    product=Product.objects.filter(category=kids_wear)
    return render(request,'kids.html',{'products':product})
def beauty_(request):
    beauty_=Category.objects.get(name='BEAUTY')
    product=Product.objects.filter(category=beauty_)
    return render(request,'beauty.html',{'products':product})
def home_living(request):
    home_living=Category.objects.get(name='HOME & LIVING')
    product=Product.objects.filter(category=home_living)
    return render(request,'home_living.html',{'products':product})
def jewellery(request):
    jewellery=Category.objects.get(name='JEWELLERY')
    product=Product.objects.filter(category=jewellery)
    return render(request,'jewellery.html',{'products':product})
def placeorderfunction(request):
    cartitems=Cart.objects.filter(user=request.user)
    if not cartitems.exists():
        return redirect('home')
    
    exist_order=Order.objects.filter(user=request.user).first()
    total=sum(item.quantity * item.product.price for item in cartitems)

    if request.method=='POST':
        if exist_order:
            exist_order.name=request.POST['name']
            exist_order.mobile=request.POST['mobile']
            exist_order.pin_code=request.POST['pincode']
            exist_order.locality=request.POST['locality']
            exist_order.flat_building=request.POST['flat_building']
            exist_order.landmark=request.POST['landmark']
            exist_order.city=request.POST['city']
            exist_order.state=request.POST['state']
            exist_order.save()

        # if exist_order:
            # exist_order.address=address
            # exist_order.save()
        else:
           
            new_order = Order.objects.create(
                user=request.user,
                name=request.POST['name'],
                mobile=request.POST['mobile'],
                pin_code=request.POST['pincode'],
                locality=request.POST['locality'],
                flat_building=request.POST['flat_building'],
                landmark=request.POST.get('landmark', ''),  # Use .get() for optional fields
                city=request.POST['city'],
                state=request.POST['state'],
                # total_amount=total  # Assuming you have a field for total amount in Order model
            )
        cartitems.delete()
        return redirect('thankyou')
    return render(request,'place_order.html',{'cartitems':cartitems,'total':total,'user':request.user,'exist_name':exist_order.name if exist_order else '','exist_mobile':exist_order.mobile if exist_order else '','exist_pincode':exist_order.pin_code if exist_order else '','exist_state':exist_order.state if exist_order else '' ,'exist_city':exist_order.city if exist_order else '' ,'exist_flat':exist_order.flat_building if exist_order else '','exist_locality':exist_order.locality if exist_order else '','exist_landmark':exist_order.landmark  if exist_order else ''})          

def orderconfirmfunction(request):
    return render(request,'thankyou.html')
def product_search(request):
    query = request.GET.get('q', '').strip()
    
    if query:
        results = Product.objects.filter(
            Q(name__icontains=query) |
            Q(describein1__icontains=query) |
            Q(category__name__icontains=query)
        )
    else:
        results = []  
    
    return render(request, 'search.html', {'query': query, 'results': results})    
def addtocart(request, id):
    product = Product.objects.get(id=id)
    
    if request.user.is_authenticated:
        user = request.user
        cart_item = Cart.objects.filter(user=user, product=product).first()

        if cart_item:
            cart_item.quantity += 1
            cart_item.price = cart_item.quantity * product.price
            cart_item.save()
        else:
            Cart.objects.create(user=user, product=product, quantity=1, price=product.price)
        
        return redirect('cartpage')
    else:
        if 'cart_item' not in request.session:
            request.session['cart_item'] = []

        cart_item_found = False

        for item in request.session['cart_item']:
            if item['product_id'] == id:
                item['quantity'] += 1
                cart_item_found = True
                break

        if not cart_item_found:
            request.session['cart_item'].append({'product_id': id, 'quantity': 1})

        request.session.modified = True

        return redirect('login_page')

def cartpage(request):
    if request.user.is_authenticated:
        user = request.user
        
        session_cart = request.session.get('cart', [])
        for item in session_cart:
            product = Product.objects.get(id=item['product_id'])
            cart_item = Cart.objects.filter(user=user, product=product).first()
            
            if cart_item:
                cart_item.quantity += item['quantity']
                cart_item.save()
            else:
                Cart.objects.create(user=user, product=product, quantity=item['quantity'],price=product.price)
        
        request.session['cart'] = []
        
        cart_item = Cart.objects.filter(user=user)
        totalprice = sum(i.quantity * i.product.price for i in cart_item)
        
        both = {
            'products_in_cart': cart_item,
            'total': totalprice,
        }
        return render(request, 'cartpage.html', both)
    else:
        return redirect('login_page')


from django.contrib.auth import login as auth_login
def loginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            auth_login(request, user)
            
            session_cart = request.session.get('cart_item', []) 
            
            for item in session_cart:
                product = Product.objects.get(id=item['product_id'])
                cart_item = Cart.objects.filter(user=user, product=product).first()
                if cart_item:
                    cart_item.quantity += item['quantity']
                    cart_item.save()
                else:
                    Cart.objects.create(user=user, product=product, quantity=item['quantity'], price=product.price)

            request.session['cart_item'] = []  
            request.session.modified = True

            return redirect('cartpage')  
        else:
            context = {'error': 'Invalid username or password'}
            return render(request, 'loginpage.html', context)
    return render(request, 'loginpage.html')


from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from .models import Product, Cart

def signupPage(request):
    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            context = {'error': 'Username already exists'}
            return render(request, 'signup.html', context)
        if User.objects.filter(email=email).exists():
            context = {'error': 'Email already exists'}
            return render(request, 'signup.html', context)

        user = User.objects.create_user(username=username, email=email, password=password)
        auth_login(request, user)

        session_cart = request.session.get('cart_item', [])  
        
        if not isinstance(session_cart, list):
            session_cart = []

        for item in session_cart:
            product_id = item.get('product_id')
            quantity = item.get('quantity', 0)
            if product_id and quantity > 0:
                product = Product.objects.filter(id=product_id).first()
                if product:
                    cart_item = Cart.objects.filter(user=user, product=product).first()
                    if cart_item:
                        cart_item.quantity += quantity
                        cart_item.save()
                    else:
                        Cart.objects.create(user=user, product=product, quantity=quantity, price=product.price * quantity)

        request.session['cart_item'] = []  
        request.session.modified = True  

        return redirect('cartpage')

    return render(request, 'signup.html')

def movetowish(request, id):
    product = get_object_or_404(Product, id=id)

    if request.user.is_authenticated:
        user = request.user
        if not Wishlist.objects.filter(user=user, product=product).exists():
            Wishlist.objects.create(user=user, product=product)
        return redirect('wishpage')
    else:
        if 'wishlist_item' not in request.session:
            request.session['wishlist_item'] = []

        for item in request.session['wishlist_item']:
            if item['product_id'] == id:
                break
        else:
            request.session['wishlist_item'].append({'product_id': id})

        request.session.modified = True

        return redirect('login_wish')
def wishpage(request):
    if request.user.is_authenticated:
        user = request.user

        session_wishlist = request.session.get('wishlist_item', [])
        for item in session_wishlist:
            product = Product.objects.filter(id=item['product_id']).first()
            if product and not Wishlist.objects.filter(user=user, product=product).exists():
                Wishlist.objects.create(user=user, product=product)

        request.session['wishlist_item'] = []
        request.session.modified = True

        wishlist_items = Wishlist.objects.filter(user=user)
        return render(request, 'wishpage.html', {'wishlist_items': wishlist_items})
    else:
        return redirect('login_wish')
def login_wish(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)

            # Merge session cart with user's cart
            # session_cart = request.session.get('cart_item', [])
            # for item in session_cart:
            #     product = Product.objects.filter(id=item['product_id']).first()
            #     if product:
            #         cart_item = Cart.objects.filter(user=user, product=product).first()
            #         if cart_item:
            #             cart_item.quantity += item['quantity']
            #             cart_item.save()
            #         else:
            #             Cart.objects.create(user=user, product=product, quantity=item['quantity'], price=product.price)

            # Merge session wish list with user's wish list
            session_wishlist = request.session.get('wishlist_item', [])
            for item in session_wishlist:
                product = Product.objects.filter(id=item['product_id']).first()
                if product and not Wishlist.objects.filter(user=user, product=product).exists():
                    Wishlist.objects.create(user=user, product=product)

            request.session['wishlist_item'] = []
            request.session.modified = True

            return redirect('wishpage')
        else:
            context = {'error': 'Invalid username or password'}
            return render(request, 'login_wish.html', context)
    return render(request, 'login_wish.html')
def signup_wish(request):
    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'signup_wish.html', {'error': 'Username already exists'})
        if User.objects.filter(email=email).exists():
            return render(request, 'signup_wish.html', {'error': 'Email already exists'})

        user = User.objects.create_user(username=username, email=email, password=password)
        auth_login(request, user)

        session_wishlist = request.session.get('wishlist_item', [])
        for item in session_wishlist:
            product = Product.objects.filter(id=item['product_id']).first()
            if product and not Wishlist.objects.filter(user=user, product=product).exists():
                Wishlist.objects.create(user=user, product=product)

        request.session['wishlist_item'] = []
        request.session.modified = True

        return redirect('wishpage')

    return render(request, 'signup_wish.html')
