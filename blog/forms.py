from django import forms
from .models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        labels = {'email': 'Email Address'}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control mt-1', 'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control mt-1', 'placeholder': 'name@example.com'}),
            'subject': forms.TextInput(attrs={'class': 'form-control mt-1', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'form-control mt-1', 'placeholder': 'Enter your message here',
                                             'rows': 5}),
        }
