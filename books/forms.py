from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm

class BookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields=['title','book_description','genre','book_image']

class ReviewForm(forms.ModelForm):
    class Meta:
        model =Review
        fields =['comment','rating']


