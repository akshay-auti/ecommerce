from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.
# class Profile(models.Model):
# 	user = models.OneToOneField(User, on_delete=models.CASCADE)
# 	firstname = models.CharField(max_length=45)
# 	lastname = models.CharField(max_length=45)
# 	created_date = models.DateTimeField(auto_now_add=True)

# 	def __str__(self):
		
# 		return self.user

			
# 	#fb_token = models.CharField(max_length=100)
# 	#twitter_token = models.CharField(max_length=100)
# 	#google_token = models.CharField(max_length=100)
# 	#mychoice = (('N', 'normal'),('F', 'fb'),('T', 'twitter'),('G','google'))
# 	#registration_method = models.CharField(max_length=1,choices=mychoice)
# 	#admin = model.BooleanField(default= False)

class User_address(models.Model):
	user_rec = models.OneToOneField(User, on_delete=models.CASCADE,db_index=True)
	address_one = models.CharField(max_length=100)
	address_two = models.CharField(max_length=100, blank=True)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=20)
	country = models.CharField(max_length=45)
	zipcode = models.CharField(max_length=45)
	

	class Meta:
		verbose_name_plural = 'User_address'

	def __unicode__(self):
		return u"%s's address " % self.user_rec



class Category(models.Model):
	name = models.CharField(max_length=100,db_index=True)
	slug = models.SlugField(max_length=100, db_index=True, unique=True)
	parent_id = models.ForeignKey('self',db_index=True, blank=True, null=True)
	created_date = models.DateTimeField(auto_now_add=True)
	modify_date = models.DateTimeField(auto_now=True)
	created_by = models.ForeignKey(User, related_name='Category_created_by',
								   default=True)
	modified_by = models.ForeignKey(User, related_name='Category_modified_by',
									default=True)
	#mychoice = ((1, 'active'),(0, 'inactive'))
	#status = models.CharField(max_length=1,choices=mychoice,default=1)
	# assigned_to = models.ForeignKey(User, related_name='Project_assigned_to', default=1)
	#status = models.ForeignKey('Status', related_name='Project_status', default=1)
	
	class Meta:
		ordering = ['name']
		verbose_name = 'category'
		verbose_name_plural = 'Categories'
		index_together = (('id', 'slug'),)		


	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('eshopper:product_list_by_category', args=[self.slug])	


class Product(models.Model):
	name = models.CharField(max_length=100)
	slug = models.SlugField(max_length=100, db_index=True, unique=True)
	category = models.ForeignKey(Category, related_name='Products', 
								 on_delete=models.CASCADE)
	short_description = models.CharField(max_length=100)
	long_description = models.TextField(blank=True, null=True)
	price = models.DecimalField(max_digits=14,decimal_places=2)
	special_price = models.DecimalField(max_digits=14,decimal_places=2,
										blank=True,null=True)
	special_price_from = models.DateField(null=True, blank=True)
	special_price_to = models.DateField(null=True, blank=True)
	quantity = models.PositiveIntegerField(default=0)
	available = models.BooleanField(default=False)
	created_by = models.ForeignKey(User, related_name='Product_created_by',
								   default=True)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_by = models.ForeignKey(User, related_name='Product_modified_by',
									default=True)
	modified_date = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ['-created_date']
		index_together = (('id', 'slug'),)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('eshopper:product_detail',
						args=[self.id, self.slug])	

class Product_images(models.Model):
	image_name = models.CharField(max_length=100)
	product = models.ForeignKey(Product, on_delete = models.CASCADE,db_index=True)
	created_date = models.DateTimeField(auto_now_add=True)
	modify_date = models.DateTimeField(auto_now=True)
	#created_by = models.OneToOneField(User)
	#modified_by = models.OneToOneField(User)
	image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)

class Product_attributes(models.Model):
	name = models.CharField(max_length=45)
	created_by = models.ForeignKey(User, related_name='Productattribute_created_by',
								   default=True)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_by = models.ForeignKey(User, related_name='Productattribute_modified_by',
									default=True)
	modified_date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

class Product_attribute_values(models.Model):
	product_attrbute = models.ForeignKey(Product_attributes,on_delete=models.CASCADE,
										 db_index=True)
	attribute_value = models.CharField(max_length=45)
	created_by = models.ForeignKey(User, related_name='AttributeValue_created_by',
								   default=True)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_by = models.ForeignKey(User, related_name='Attributevalue_modified_by',
									default=True)
	modified_date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.attribute_value

class Product_attribute_assoc(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
	product_attribute = models.ForeignKey(Product_attributes,db_index=True)
	product_attribute_value = models.ForeignKey(Product_attribute_values,db_index=True)

	def __str__(self):
		return '%s %s %s' % (self.product , self.product_attribute,
							 self.product_attribute_value)
			

class Product_categories(models.Model):
	product =  models.ForeignKey(Product, on_delete=models.CASCADE, db_index=True)
	category = models.ForeignKey(Category,on_delete=models.CASCADE, db_index=True)




class User_wish_list(models.Model):
	profile = models.ForeignKey(User, on_delete=models.CASCADE,
								db_index=True)
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	


class User_order(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE,
							 db_index=True, blank=True,
							 null=True)

	address = models.CharField(max_length=100)
	city = models.CharField(max_length=45)
	state = models.CharField(max_length=45)
	country = models.CharField(max_length=45)
	zipcode = models.CharField(max_length=45)
	created_date = models.DateTimeField(auto_now_add=True)
	updated_date = models.DateTimeField(auto_now=True)
	paid = models.BooleanField(default=False)
	# AWB_NO = models.CharField(max_length=100)
	# payment_gateway = models.ForeignKey(Payment_gateway,on_delete=models.CASCADE)
	# transaction_id = CharField(max_length=100)
	
	# grand_total  = DecimalField(max_digits=12, decimal_places=10)
	# shipping_charges = DecimalField(max_digits=12, decimal_places=10)
	# coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE)
	# shipping_address = CharField(max_length=100)
	# shipping_city = CharField(max_length=45)
	# shipping_state = CharField(max_length=45)
	# shipping_country = CharField(max_length=45)
	# shipping_zipcode = CharField(max_length=45)

	class Meta:
		ordering = ['-created_date']
		verbose_name_plural = 'User_orders'

	def __str__(self):
		return 'Order {}'.format(self.id)

	def get_total_cost(self):
		return sum(item.get_cost() for item in self.items.all()) 		

class Order_details(models.Model):
	order = models.ForeignKey(User_order,related_name='items')
	product = models.ForeignKey(Product,related_name='order_items')
	quantity = models.PositiveIntegerField(default=1)
	price = models.DecimalField(max_digits=12, decimal_places=2)

	class Meta:
		verbose_name_plural = 'Order_details'

	def __str__(self):
		return '{}'.format(self.id)

	def get_cost(self):
		return self.price * self.quantity		




class Coupon(models.Model):
	code = models.CharField(max_length=45, unique=True)
	discount = models.IntegerField(validators=[MinValueValidator(0),
											   MaxValueValidator(100)])
	active = models.BooleanField()
	valid_from = models.DateTimeField()
	valid_to = models.DateTimeField()
	
	def __str__(self):
		return self.code

# class Coupons_used(models.Model):
# 	coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, db_index=True)
# 	user = models.ForeignKey(User, on_delete=models.CASCADE)
# 	user_order = models.ForeignKey(User_order,on_delete=models.CASCADE)
# 	created_date = DateTimeField(auto_now_add=True)	

class Contact_us(models.Model):
	name = models.CharField(max_length=45)
	email = models.EmailField()
	contact_no = models.CharField(max_length=45,blank=True, null=True)
	message = models.TextField()
	note_admin = models.TextField(blank=True, null=True)
	# created_by = models.ForeignKey('Self',default=True)
	created_date = models.DateTimeField(auto_now_add=True)
	# modified_by = models.ForeignKey('Self',default=True)
	modified_date = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name 

	class Meta:
		verbose_name_plural = 'Contact_us'	

		
# class Payment_gateway(models.Model):
# 	name = models.CharField(max_length=45)
# 	created_by = models.DateTimeField()
# 	created_date = models.DateTimeField(datetime.now())
# 	modify_by = models.IntegerField()
# 	modify_date = DateTimeField()

class Email_template(models.Model):
	title = models.CharField(max_length=45)
	subject = models.CharField(max_length=255)
	content = models.TextField()
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(auto_now=True)


	def __str__(self):
		return self.title