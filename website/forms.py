from django import forms
from .models import ContactMessage


class ContactMessageForm(forms.ModelForm):
    SERVICE_CHOICES = [
        ('FDM Printing', 'FDM Printing'),
        ('Resin / SLA', 'Resin / SLA'),
        ('Rapid Prototyping', 'Rapid Prototyping'),
        ('Production Run', 'Production Run'),
        ('3D Design', '3D Design'),
    ]
    service = forms.ChoiceField(choices=SERVICE_CHOICES)

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'service', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'id': 'quoteName', 'placeholder': 'Arjun Kumar'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'id': 'quoteEmail', 'placeholder': 'arjun@company.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'id': 'quotePhone', 'placeholder': '+91 98765 43210'}),
            'service': forms.Select(attrs={'class': 'form-input', 'id': 'quoteService'}),
            'message': forms.Textarea(attrs={'class': 'form-input', 'id': 'quoteMessage', 'placeholder': 'Tell us about your project - material, quantity, deadline...'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data['phone'].strip()
        digits = ''.join(character for character in phone if character.isdigit())
        if len(digits) < 10 or len(digits) > 15:
            raise forms.ValidationError('Enter a valid phone number.')
        return phone

    def clean_message(self):
        message = self.cleaned_data['message'].strip()
        if len(message) < 10:
            raise forms.ValidationError('Project details must be at least 10 characters.')
        return message
