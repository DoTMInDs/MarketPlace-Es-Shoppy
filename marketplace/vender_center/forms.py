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
    def clean_phone_number(self):
        phone = self.cleaned_data['phone_number']
        if Seller.objects.exclude(pk=self.instance.pk).filter(phone_number=phone).exists():
            raise forms.ValidationError("This phone number is already registered")
        return phone