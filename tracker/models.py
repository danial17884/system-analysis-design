from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Transaction(models.Model):
    KIND_CHOICES = (
        ('Income', 'Income'),
        ('Expense', 'Expense'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kind = models.CharField(max_length=10, choices=KIND_CHOICES)
    amount = models.FloatField()
    date_time = models.DateTimeField(default=timezone.now, blank=True, null=True)
    #date_time = models.DateTimeField()  # تاریخی که کاربر با ساعت و دقیقه وارد می‌کند
    category = models.CharField(max_length=100)  # ذخیره مستقیم متن دسته‌بندی بدون نیاز به ForeignKey
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)  # برای یادداشت‌های آزاد کاربر
    created_at = models.DateTimeField(auto_now_add=True)  # زمان دقیق ثبت در دیتابیس توسط سیستم
    date_time = models.DateTimeField(default=timezone.now) 
    def __str__(self):
        return f"{self.user.username} - {self.kind} - {self.amount}"
