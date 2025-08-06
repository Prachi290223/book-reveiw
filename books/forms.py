from django import forms
from .models import *

class BookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = '__all__'
