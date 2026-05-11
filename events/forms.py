from django import forms
from .models import ContactEnquiry

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactEnquiry
        fields = ['name', 'email', 'phone', 'message']