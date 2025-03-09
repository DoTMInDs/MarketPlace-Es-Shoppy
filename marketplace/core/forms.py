# from django.forms import ModelForm
from typing import Any
from django import forms 
from .models import ProfileModel,Product,Category,ProductSpecification,ProductImage
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm 
from django.forms import inlineformset_factory
from vender_center.models import Seller
from cloudinary.forms import CloudinaryFileField

class CreateUserForm(UserCreationForm):
    username = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Enter your username....'}))
    email = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Enter your email....'}))
    password1 = forms.CharField(label="",widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password....'}))
    password2 = forms.CharField(label="",widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password....'}))
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
    
    def __init__(self, *args: Any, **kwargs: Any):
        super(CreateUserForm, self).__init__(*args, **kwargs)

        for fieldname in ["username", "email", "password1", "password2"]:
            self.fields[fieldname].help_text = None 

class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Enter your username....'}))
    email = forms.CharField(label="",widget=forms.EmailInput(attrs={'placeholder': 'Enter your email....'}))
    class Meta:
        model = User
        fields = [ "username", "email"]
    def __init__(self, *args: Any, **kwargs: Any):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        for fieldname in [ "username", "email"]:
            self.fields[fieldname].help_text = None

class ProfileUpdateForm(forms.ModelForm):
    full_name = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Enter your fullname....'}))
    about = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Tell us something about you....'}))
    talks_about = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Type something here....'}))
    class Meta:
        model = ProfileModel
        fields = [ "full_name", "image", "about", "talks_about"]

class ProductForm(forms.ModelForm):
    name = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Enter product name....'}))
    class Meta:
        model = Product
        fields = [
            "category",
            "name",
            "description",
            "price",
            "canceled_price",
            "image"
        ]
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 5}),
        }

class CategoryForm(forms.ModelForm):
    name = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Enter category name....'}))
    class Meta:
        model = Category
        fields = [
            "name",
            "image",
            "is_featured"
        ]
        widgets = {
            'image': forms.FileInput(attrs={'accept': 'image/*'})
        }

SpecificationFormSet = inlineformset_factory(
    Product,
    ProductSpecification,
    fields=('key', 'value'),
    extra=3,  # Show 1 empty spec field by default
    can_delete=True,  # Allow deleting specs
    widgets={
        'key': forms.TextInput(attrs={'placeholder': 'Enter specification name...'}),
        'value': forms.TextInput(attrs={'placeholder': 'Enter specification value...'}),
        'value': forms.Textarea(attrs={'rows': 4}),
    }
)

class BecomeSellerForm(forms.ModelForm):
    store_name = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Enter store name....'}))
    phone_number = forms.CharField(label="",widget=forms.TextInput(attrs={'placeholder': 'Enter phone number....'}))
    class Meta:
        model = Seller
        fields = [
            "store_name",
            "phone_number",
            "bio",
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
    
class ProductImageForm(forms.ModelForm):
    attached_image = CloudinaryFileField(
        options={'folder': 'product_images'}
    )
    class Meta:
        model = ProductImage
        fields = [
            "attached_image"
        ]
        widgets = {
            'attached_image': forms.FileInput(attrs={
                'class': 'form-control-file',
                'accept': 'image/*'
            })
    }
ProductImageFormSet = inlineformset_factory(
    Product,
    ProductImage,
    form=ProductImageForm,
    fields=('attached_image',),
    extra=3,
    can_delete=True,
    max_num=6,  # Maximum total images (existing + new)
    validate_max=True,
    
)