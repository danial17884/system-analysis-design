from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    TYPES = (('income', 'درآمد'), ('expense', 'هزینه'))
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=7, choices=TYPES)

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, verbose_name='عنوان')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.amount} - {self.category.name}"

class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    limit_amount = models.DecimalField(max_digits=12, decimal_places=2) # سقف بودجه
    month = models.IntegerField() # ماه (مثلا 1 تا 12)
    year = models.IntegerField() # سال

    def __str__(self):
        return f"{self.category.name} - {self.limit_amount}"
