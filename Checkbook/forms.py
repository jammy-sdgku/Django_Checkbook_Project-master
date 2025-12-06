from django.forms import ModelForm
from django import forms
from .models import Account, Transaction


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = '__all__'


class TransactionForm(ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'type': 'date',
                'class': 'form-control'
            }
        ),
        input_formats=['%Y-%m-%d']
    )
    
    class Meta:
        model = Transaction
        fields = '__all__'
        labels = {
            'to_from': 'To / From',
        }
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'to_from': forms.TextInput(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'cleared': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'account': forms.Select(attrs={'class': 'form-control'}),
        }