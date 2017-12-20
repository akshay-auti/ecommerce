from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import User_address, Contact_us, User_order

# class AddressMixin(forms.ModelForm):
# 	class Meta:
# 		model = User_address
# 		fields = {'address_one', 'address_two',
# 				  'city', 'state', 'country', 
# 				  'zipcode',}
# 		widgets = {
# 			'address_one': forms.TextInput(attrs={'class':'form-control'}),
# 			'address_two': forms.TextInput(attrs={'class':'form-control'}),
# 			'city': forms.TextInput(attrs={'class':'form-control'}),
# 			'state': forms.TextInput(attrs={'class':'form-control'}),
# 			'country': forms.TextInput(attrs={'class':'form-control'}),
# 			'zipcode': forms.TextInput(attrs={'class':'form-control'}),

# 		}  

class SignupForm(UserCreationForm):
	# first_name = forms.CharField(required=False, 
	# 							 widget=forms.TextInput(
	# 							 attrs={'class':'form-control'}))
	# last_name = forms.CharField(required=False, 
	# 							widget=forms.TextInput(
	# 							attrs={'class':'form-control'}))
	# email = forms.EmailField(widget=forms.EmailInput(
	# 						 attrs={'class':'form-control'}))
	# username = forms.CharField(widget=forms.TextInput(
	# 						   attrs={'class':'form-control'}))
	# password = forms.CharField(widget=forms.PasswordInput(
	# 						   attrs={'class':'form-control', 
	# 								  'type':'password'}))
	# confirm_password = forms.CharField(widget=forms.PasswordInput(
									    # attrs={'class':'form-control', 
										       # 'type':'password'}))

	class Meta:
		model = User 
		fields = ['username', 'email', 'password1', 'password2']

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



class CouponApplyForm(forms.Form):
	code = forms.CharField()



PRODUCT_QUANTITY_CHOICE = [(i, str(i)) for i in range(1, 21)]

class CartAddProductForm(forms.Form):
	quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICE,
									  coerce=int)
	update = forms.BooleanField(required=False, initial=False, 
								widget=forms.HiddenInput)	


class ContactForm(forms.ModelForm):
	class Meta:
		model = Contact_us
		fields = ['name', 'email', 'message']
		widgets = {
			'name' : forms.TextInput(attrs={'class':'form-control',
											'placeholder':'name'}),
			'email': forms.EmailInput(attrs={'class':'form-control',
											 'placeholder': 'email'}),
			'message' : forms.Textarea(attrs={'class':'form-control', 
											   'placeholder':'Type your message here'}),
		}


class OrderCreateForm(forms.ModelForm):
	class Meta:
		model = User_order
		fields = ['address', 'city', 'state', 'country', 'zipcode']