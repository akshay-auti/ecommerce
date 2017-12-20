from django.conf.urls import url
from django.contrib.auth.views import login,logout

from . import views

app_name = 'eshopper'

urlpatterns = [
	url(r'^$', views.home, name='home'),
	url(r'^signup/$', views.signup, name='signup'),
	url(r'^login/$',login, name='login',kwargs={'template_name': 'eshopper/login.html'}),
	url(r'^logout/$',logout,name='logout',kwargs={'next_page': '/'}),
	url(r'^cart/$', views.cart_detail, name='cart_detail'),
	url(r'^cart/add/(?P<product_id>\d+)/$', views.cart_add, name='cart_add'),
	url(r'^cart/remove/(?P<product_id>\d+)/$', views.cart_remove, name='cart_remove'),
	url(r'^orders/$', views.order_create, name='order_create'),
	url(r'^products/$', views.product_list, name='product_list'),
	url(r'^products/(?P<category_slug>[-\w]+)/$', views.product_list, name='product_list_by_category'),
	url(r'^products/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail'),
	
	url(r'^contact/$', views.contact, name='contact'),


]