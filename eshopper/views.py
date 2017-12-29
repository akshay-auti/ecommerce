
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django import forms
from .models import  Coupon, Category, Product, Order_details,Email_template, User_wish_list
from .cart import Cart
from .forms import *
from django.core.urlresolvers import reverse
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.template  import Context, Template
from django.contrib import messages
from django.utils import timezone
# Create your views here.

def home(request):
	
	return render(request, 'eshopper/home.html')

# def signup(request):
	
# 	if request.method == 'POST':
# 		form = SignupForm(request.POST)
# 		if form.is_valid():
			
# 			username = form.cleaned_data['username']
# 			email = form.cleaned_data['email']
# 			password = form.cleaned_data['password1']
# 			user = User(username=username, email=email)
# 			user.set_password(password)
# 			user.save()
			
# 			current_site = get_current_site(request)
# 			mail_template = Email_template.objects.get(title='Registration')
# 			message = Template(mail_template.content)
			
# 			to_mail = form.cleaned_data.get('email')
# 			email = EmailMessage(mail_template.subject, message.render(
# 					Context({'user': user})), to=[to_mail])
# 			email.send()
# 			return HttpResponseRedirect('/')
# 	else:
# 		form = SignupForm()

# 	return render(request, 'eshopper/search.html', {'form': form})


def product_list(request, category_slug=None):
	
	category = None
	categories = Category.objects.all()
	products = Product.objects.filter(available=True)
	
	if category_slug:
		category = get_object_or_404(Category, slug=category_slug)
		products = products.filter(category=category)
	return render(request, 'eshopper/list.html', 
				 {'category': category, 
				  'categories': categories, 
				  'products':products}) 


def product_detail(request, id, slug):
	
	product = get_object_or_404(Product, id=id, slug=slug, 
								available=True)
	category = None
	categories = Category.objects.all()
	cart_product_form = CartAddProductForm()
	return render(request, 'eshopper/detail.html', 
				 {'product': product, 
				  'category': category, 
				  'categories': categories,
				  'cart_product_form': cart_product_form})


@require_POST
def cart_add(request, product_id):
	
	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id)
	form = CartAddProductForm(request.POST)
	
	if form.is_valid():
		cd = form.cleaned_data
		cart.add(product=product, quantity=cd['quantity'], 
				 update_quantity=cd['update'])
	return redirect('eshopper:cart_detail') 

def cart_remove(request, product_id):
	
	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id)
	cart.remove(product)
	return redirect('eshopper:cart_detail')

def cart_detail(request):
	
	cart = Cart(request)
	for item in cart:
		item['update_quantity_form'] = CartAddProductForm(initial={
		'quantity': item['quantity'],'update' : True})
	coupon_apply_form = CouponApplyForm()
		
	return render(request, 'eshopper/cart_detail.html', {'cart': cart,
														 'coupon_apply_form': coupon_apply_form})



def contact(request):
	
	if request.method == "POST":
		form = ContactForm(request.POST)
		
		if form.is_valid():
			name = form.cleaned_data['name']
			email = form.cleaned_data['email']
			message = form.cleaned_data['message']
			user = Contact_us(name=name, email=email, 
							  message=message)
			user.save()
			messages.success(request,'message submission sucessful')
			

	form = ContactForm()        
	return render(request, 'eshopper/contact.html', 
				 {'form': form})

@require_POST
def coupon_apply(request):
  	
	now = timezone.now()

	form = CouponApplyForm(request.POST)
	if form.is_valid():
		code = form.cleaned_data['code']
		try:
			coupon = Coupon.objects.get(code__iexact=code,
										valid_from__lte=now,
										valid_to__gte=now,
										active=True)
			request.session['coupon_id'] = coupon.id
			messages.success(request, 'Coupon applied sucessfully.')
		except Coupon.DoesNotExist:
			request.session['coupon_id'] = None

	return redirect('eshopper:cart_detail')        

def coupon_remove(request):

	del request.session['coupon_id']
	return redirect('eshopper:cart_detail')

def order_create(request):
	
	cart = Cart(request)
	if request.method == "POST":
		form = OrderCreateForm(request.POST)
		if form.is_valid():
			if request.user.is_authenticated:
				order = form.save(commit=False)
				if  cart.coupon:
					order.coupon = cart.coupon	
					order.discount = cart.coupon.discount
					order.user = request.user
				order.save()

			else:
				return HttpResponseRedirect('/login')
			for item in cart:
				Order_details.objects.create(order=order,
											 product=item['product'],
											 price=item['price'],
											 quantity=item['quantity'])
			cart.clear()
			request.session['order_id'] = order.id
			return redirect(reverse('payment:process'))
			
	else:
		form =  OrderCreateForm()
	return render(request, 'eshopper/create_order.html', {'cart': cart,'form' : form})                                             





def search(request):
	search_query = request.GET.get('search', None)
	if request.method == 'GET':
		category = None
		categories = Category.objects.all()
		try:
			products = Product.objects.filter(name__icontains=search_query,available=True)
		except Product.DoesNotExist:
			products = None	
	return render(request, 'eshopper/list.html', 
				 {'category': category, 
				  'categories': categories, 
				  'products':products}) 


def signup(request):
	
	if request.method == 'POST':
		if request.POST.get('submit') == 'signup':
			form = SignupForm(request.POST)
			if form.is_valid():
			
				username = form.cleaned_data['username']
				email = form.cleaned_data['email']
				password = form.cleaned_data['password1']
				user = User(username=username, email=email)
				user.set_password(password)
				user.save()
			
				current_site = get_current_site(request)
				mail_template = Email_template.objects.get(title='Registration')
				message = Template(mail_template.content)
			
				to_mail = form.cleaned_data.get('email')
				email = EmailMessage(mail_template.subject, message.render(
					Context({'user': user})), to=[to_mail])
				email.send()
				return HttpResponseRedirect('/')
		elif request.POST.get('submit') == 'login':
			redirect('login')
	else:
		form1 = SignupForm()
		
	return render(request, 'eshopper/search.html', {'form': form1})
		