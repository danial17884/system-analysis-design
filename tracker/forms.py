from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        # فیلد title اضافه شد
        fields = ['title', 'kind', 'category', 'amount', 'date_time', 'description']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان تراکنش را وارد کنید...'
            }),
            'kind': forms.Select(attrs={
                'class': 'form-select'
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'list': 'category-options',
                'placeholder': 'دسته‌بندی را انتخاب کنید یا بنویسید...'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'مبلغ را وارد کنید'
            }),
            'date_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'توضیحات (اختیاری)'
            }),
        }

        labels = {
            'title': 'عنوان',
            'kind': 'نوع تراکنش',
            'category': 'دسته‌بندی',
            'amount': 'مبلغ',
            'date_time': 'تاریخ و زمان',
            'description': 'توضیحات',
        }
