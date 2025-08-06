from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

class BookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = '__all__'

class ReviewForm(forms.ModelForm):
    class Meta:
        model =Review
        fields =['comment','rating']


