from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Reservation

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = [ 'username','password1', 'password2']


class BookingForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ['customer_name','room','start_date','end_date',]
        labels = {
            'customer_name': 'Customer Name',
            'room' : 'room number',
            'start_date': 'Check in Date',
            'end_date': 'Check out Date',

        }
        widgets = {
            'customer_name': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'enter your name'}
            ),

            'start_date': forms.DateInput(
                attrs={'class': 'form-control', 'placeholder': 'enter check in'}
            ),
            'end_date' : forms.DateInput(
                attrs={'class':'form-control','placeholder': 'enter check out'}
            )

        }

