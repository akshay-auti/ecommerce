# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
# Register your models here.

class CatogeryAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug':('name',)}
	list_display = ['name']


class ProductImageInline(admin.TabularInline):
    model = Product_images

class ProductAdmin(admin.ModelAdmin):
    
    list_display = ['name','category', 'price', 'quantity', 'available', 'created_date', 'modified_date']
    list_filter = ['available', 'created_date', 'modified_date','category']
    list_editable = ['price', 'quantity', 'available'] 
    prepopulated_fields = {'slug':('name',)}
    inlines = [
        ProductImageInline,
    ]

class CouponAdmin(admin.ModelAdmin):
	list_display = ['code', 'valid_from', 'valid_to','discount', 'active']
	list_filter = ['active', 'valid_from', 'valid_to']
	search_fields = ['code']


class Contact_usAdmin(admin.ModelAdmin):
	
	list_display = ['name', 'email','message']
	search_fields = ['name']	


class OrderDetailInline(admin.TabularInline):
	model = Order_details
	raw_id_fields = ['product']

class UserOrderAdmin(admin.ModelAdmin):
	list_display = ['id','address', 'city', 'state', 'country', 'zipcode']
	list_filter = ['paid', 'created_date', 'updated_date']
	inlines = [OrderDetailInline]			

admin.site.register(Product, ProductAdmin)
admin.site.register(User_wish_list)
admin.site.register(User_address)
admin.site.register(Category, CatogeryAdmin)
admin.site.register(Product_categories)
admin.site.register(Product_images)
admin.site.register(Coupon, CouponAdmin)
admin.site.register(Product_attributes)
admin.site.register(Product_attribute_values)
admin.site.register(Product_attribute_assoc)
admin.site.register(Contact_us, Contact_usAdmin)
admin.site.register(User_order, UserOrderAdmin)
admin.site.register(Email_template)