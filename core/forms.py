from django import forms
from .models import SiteSettings

class SiteSettingsForm(forms.ModelForm):
    class Meta:
        model = SiteSettings
        fields = [
            'site_name', 'logo', 'primary_color', 'header_color', 'footer_color', 'accent_color', 'header_text_color', 'top_nav_text_color', 'sidebar_text_color', 'sidebar_color'
        ]
        widgets = {
            'site_name': forms.TextInput(attrs={'class': 'w-full p-2 border rounded'}),
            'primary_color': forms.TextInput(attrs={'type': 'color', 'class': 'w-16 h-10 p-1 border rounded'}),
            'header_color': forms.TextInput(attrs={'type': 'color', 'class': 'w-16 h-10 p-1 border rounded'}),
            'footer_color': forms.TextInput(attrs={'type': 'color', 'class': 'w-16 h-10 p-1 border rounded'}),
            'accent_color': forms.TextInput(attrs={'type': 'color', 'class': 'w-16 h-10 p-1 border rounded'}),
            'header_text_color': forms.TextInput(attrs={'type': 'color', 'class': 'w-16 h-10 p-1 border rounded'}),
            'top_nav_text_color': forms.TextInput(attrs={'type': 'color', 'class': 'w-16 h-10 p-1 border rounded'}),
            'sidebar_text_color': forms.TextInput(attrs={'type': 'color', 'class': 'w-16 h-10 p-1 border rounded'}),
            'sidebar_color': forms.TextInput(attrs={'type': 'color', 'class': 'w-16 h-10 p-1 border rounded'}),
        }
