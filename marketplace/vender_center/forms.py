from django import forms 
from .models import Seller

class SellerProfileForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = [
            "store_name",
            "bio",
            "phone_number",
        ]
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
