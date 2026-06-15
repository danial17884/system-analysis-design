from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Transaction
from .forms import TransactionForm
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
#from .forms import BudgetForm
import csv
from django.http import HttpResponse
from django.db.models import Q


from django.db.models import Sum

def home(request):
    if not request.user.is_authenticated:
        return render(request, 'tracker/home.html')

    user_transactions = Transaction.objects.filter(user=request.user)

    # محاسبه درآمد، هزینه و موجودی کل با استفاده از فیلد جدید kind
    # نکته: اگر مقادیر kind را با حروف کوچک (income/expense) ذخیره کردید، آن‌ها را در خطوط زیر تغییر دهید
    total_income = user_transactions.filter(kind='Income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = user_transactions.filter(kind='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense

    # ۵ تراکنش آخر با استفاده از فیلد جدید date_time
    recent_transactions = user_transactions.order_by('-date_time')[:5]

    # با توجه به اینکه مدل Budget را حذف کردیم، کدهای مربوط به آن برداشته شد.
    # برای اینکه فایل HTML ارور ندهد، یک لیست خالی به عنوان budget_status می‌فرستیم.
    budget_status = []

    context = {
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'recent_transactions': recent_transactions,
        'budget_status': budget_status, 
    }

    return render(request, 'tracker/home.html', context)



@login_required
def dashboard(request):
    user = request.user
    today = datetime.today().date()

    current_month_expenses = Transaction.objects.filter(
        user=user, 
        kind='expense',  # تغییر از category__type به kind
        date_time__year=today.year,  # تغییر از date به date_time
        date_time__month=today.month
    ).aggregate(total=Sum('amount'))['total'] or 0

    current_month_income = Transaction.objects.filter(
        user=user,
        kind='income',  # تغییر از category__type به kind
        date_time__year=today.year,  # تغییر از date به date_time
        date_time__month=today.month
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    past_months_expenses = []
    for i in range(1, 4):
        target_date = today - relativedelta(months=i)
        expense = Transaction.objects.filter(
            user=user, 
            kind='expense',  # تغییر از category__type به kind
            date_time__year=target_date.year,  # تغییر از date به date_time
            date_time__month=target_date.month
        ).aggregate(total=Sum('amount'))['total'] or 0
        past_months_expenses.append(expense)
    
    predicted_expense = sum(past_months_expenses) / 3 if past_months_expenses else 0

    context = {
        'current_month_expenses': current_month_expenses,
        'current_month_income': current_month_income,
        'predicted_expense': predicted_expense,
    }
    return render(request, 'tracker/dashboard.html', context)


@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('dashboard')
    else:
        form = TransactionForm()
    return render(request, 'tracker/transaction_form.html', {'form': form})
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('dashboard') 
    else:
        form = UserCreationForm()
    return render(request, 'tracker/signup.html', {'form': form})

def about_view(request):
    return render(request, 'tracker/about.html')
@login_required(login_url='/login/')
def transaction_list(request):
    # دریافت تمام تراکنش‌های کاربر فعلی و مرتب‌سازی از جدید به قدیم
    # فرض بر این است که فیلد تاریخ شما date یا created_at نام دارد
    transactions = Transaction.objects.filter(user=request.user).order_by('-date')
    
    context = {
        'transactions': transactions
    }
    return render(request, 'tracker/transaction_list.html', context)
#@login_required
#def add_budget(request):
 #   if request.method == 'POST':
  #      form = BudgetForm(request.POST)
       # if form.is_valid():
   #         
          #  budget = form.save(commit=False)
           
          #  budget.user = request.user
           
           # budget.save()
            
           # return redirect('dashboard')  
   # else:
       # form = BudgetForm()
        
   # return render(request, 'tracker/add_budget.html', {'form': form})
@login_required
def export_transactions_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="transactions.csv"'
    
    
    response.write(u'\ufeff'.encode('utf8')) 

    writer = csv.writer(response)
    
    writer.writerow(['تاریخ', 'مبلغ', 'دسته‌بندی', 'توضیحات'])

    
    transactions = Transaction.objects.filter(user=request.user)
    
    
    for tx in transactions:
        writer.writerow([tx.date_time, tx.amount, tx.category, tx.description])


    return response






@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user)
    
    # گرفتن لیست نام دسته‌بندی‌های یکتایی که کاربر استفاده کرده است
    categories = Transaction.objects.filter(user=request.user).values_list('category', flat=True).distinct()

    search_query = request.GET.get('q', '') 
    category_filter = request.GET.get('category', '')
    # تغییر پیش‌فرض مرتب‌سازی به date_time-
    sort_by = request.GET.get('sort', '-date_time')

    # جستجو روی عنوان و توضیحات
    if search_query:
        transactions = transactions.filter(
            Q(title__icontains=search_query) | Q(description__icontains=search_query)
        )

    # اعمال فیلتر دسته‌بندی (اکنون بر اساس نام دسته‌بندی است نه ID)
    if category_filter:
        transactions = transactions.filter(category=category_filter)

    # فیلدهای مرتب‌سازی را به date_time تغییر دادیم
    valid_sort_fields = ['date_time', '-date_time', 'amount', '-amount'] 
    if sort_by in valid_sort_fields:
        transactions = transactions.order_by(sort_by)

    context = {
        'transactions': transactions,
        'categories': categories,
        'query': search_query,
        'selected_category': category_filter,
        'sort_by': sort_by,
    }
    return render(request, 'tracker/transaction_list.html', context)


