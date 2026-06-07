from django import forms
from .models import Transaction
from .models import Budget

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        
        fields = ['title', 'category', 'amount', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ['category', 'limit_amount', 'month', 'year']
        
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'limit_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'مثال: 5000000'}),
            'month': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 12, 'placeholder': 'ماه (۱ تا ۱۲)'}),
            'year': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'سال (مثلاً ۱۴۰۲)'}),
        }
        
        labels = {
            'category': 'دسته‌بندی',
            'limit_amount': 'سقف بودجه (تومان)',
            'month': 'ماه',
            'year': 'سال',
        }
