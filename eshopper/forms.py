from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import User_address, Contact_us, User_order, Product, Coupon
from ckeditor.widgets import CKEditorWidget
from ckeditor.fields import RichTextField



class SignupForm(UserCreationForm):
	
	class Meta:
		model = User 
		fields = ['username', 'email', 'password1', 
				  'password2']

	def clean_confirm_password(self):
		
		password = self.cleaned_data['password1']
		confirm_password = self.cleaned_data['password2']
		
		if password and confirm_password and password != confirm_password:
			raise forms.ValidationError("password do not match.")
		return confirm_password

	def clean_username(self):
		
		username = self.cleaned_data['username']

		try:
			User.objects.get(username=username)
		except User.DoesNotExist:
			return username	
		raise forms.ValidationError("Username is already taken.")	
		
	def save(self, commit=True):
		
		user = super(SignupForm, self).save(commit)
		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()
		return user 			





# PRODUCT_QUANTITY_CHOICE = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
	quantity = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'form-control' , 'autocomplete': 'off','pattern':'[0-9]+'}))
	# quantity = forms.TextInput(coerce=int)
	update = forms.BooleanField(required=False, initial=False, 
								widget=forms.HiddenInput)	


class ContactForm(forms.ModelForm):
	message = forms.CharField(widget=CKEditorWidget())
	class Meta:
		model = Contact_us
		fields = ['name', 'email', 'message']
		widgets = {'name' :forms.TextInput(attrs={'class':'form-control',
				   'placeholder':'name'}),
				   'email':forms.EmailInput(attrs={'class':'form-control',
				   'placeholder':'email'}),
			    #    'message' :forms.Textarea(attrs={'class':'form-control', 
				   # 'placeholder':'Type your message here'}),
		}


class OrderCreateForm(forms.ModelForm):
	
	class Meta:
		model = User_order
		fields = ['address', 'city', 'state', 'country', 'zipcode', 'message']
		widgets = {'address' :forms.TextInput(attrs={'class':'form-control',
				   'placeholder':'address'}),
				   'city':forms.TextInput(attrs={'class':'form-control',
				   'placeholder':'city'}),
			       'state' :forms.TextInput(attrs={'class':'form-control', 
				   'placeholder':'state'}),
				   'country' :forms.TextInput(attrs={'class':'form-control',
				   'placeholder':'country'}),
				   'zipcode':forms.TextInput(attrs={'class':'form-control',
				   'placeholder':'zipcode'}),
			       'message' :forms.Textarea(attrs={'class':'form-control', 
				   'placeholder':'Notes about your order, Special Notes for Delivery'}),
		}

class CouponApplyForm(forms.Form):
	
	code = forms.CharField(max_length=255)

	def clean_code(self):
		code = self.cleaned_data['code']

		if Coupon.objects.filter(code=code):
			return code

		raise forms.ValidationError("Coupon code Does not exist.")	