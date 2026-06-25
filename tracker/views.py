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
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse



from django.db.models import Sum

def home(request):
    if not request.user.is_authenticated:
        return render(request, 'tracker/index.html')

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

    return render(request, 'tracker/index.html', context)



from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import datetime
from dateutil.relativedelta import relativedelta
# ایمپورت مدل‌ Transaction فراموش نشود

@login_required
def dashboard(request):
    user = request.user
    today = datetime.today().date()
    
    # کوئری پایه برای تراکنش‌های کاربر لاگین شده
    user_transactions = Transaction.objects.filter(user=user)

    # --- بخش اول: محاسبات ماه جاری و پیش‌بینی ---
    current_month_expenses = user_transactions.filter(
        kind='Expense',  # اصلاح شد به حرف بزرگ
        date_time__year=today.year,
        date_time__month=today.month
    ).aggregate(total=Sum('amount'))['total'] or 0

    current_month_income = user_transactions.filter(
        kind='Income',   # اصلاح شد به حرف بزرگ
        date_time__year=today.year,
        date_time__month=today.month
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    past_months_expenses = []
    for i in range(1, 4):
        target_date = today - relativedelta(months=i)
        expense = user_transactions.filter(
            kind='Expense', # اصلاح شد به حرف بزرگ
            date_time__year=target_date.year,
            date_time__month=target_date.month
        ).aggregate(total=Sum('amount'))['total'] or 0
        past_months_expenses.append(expense)
    
    predicted_expense = sum(past_months_expenses) / 3 if past_months_expenses else 0

    # --- بخش دوم: محاسبات کل و تراکنش‌های اخیر ---
    total_income = user_transactions.filter(kind='Income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = user_transactions.filter(kind='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense

    recent_transactions = user_transactions.order_by('-date_time')[:5]

    budget_status = []

    # --- بخش سوم: ارسال اطلاعات در یک context ---
    context = {
        'current_month_expenses': current_month_expenses,
        'current_month_income': current_month_income,
        'predicted_expense': predicted_expense,
        'total_income': total_income,
        'total_expense': total_expense,
        'balance': balance,
        'recent_transactions': recent_transactions,
        'budget_status': budget_status, 
    }
    
    return render(request, 'tracker/dashboard.html', context)



from django.contrib import messages
from django.shortcuts import redirect

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            # ثبت موفق: برگشت به صفحه دشبورد
            return redirect('dashboard') 
        else:
            # اگر فرم نامعتبر بود، ارورها را در ترمینال چاپ کن تا بفهمیم مشکل چیست
            print("Form Errors:", form.errors) 
            messages.error(request, 'خطا در ثبت تراکنش. لطفاً ترمینال را چک کنید.')
            # فرم مشکل دارد: برگشت به صفحه دشبورد
            return redirect('dashboard')
            
    # اگر کسی سعی کرد آدرس را مستقیماً در مرورگر باز کند
    return redirect('dashboard')




def signup_view(request):
    if request.method == 'POST':
        # دریافت اطلاعات با استفاده از nameهای فرم
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # چک کردن فیلدهای خالی
        if not fullname or not email or not password or not confirm_password:
            return render(request, 'tracker/signup.html', {
                'error': 'لطفاً تمام فیلدها را پر کنید.'
            })


        if len(password) < 8:
            return render(request, 'tracker/signup.html', {
                'error': 'رمز عبور باید حداقل 8 کاراکتر باشد.'
            })
        # بررسی یکی بودن رمزها
        if password == confirm_password:
            # بررسی اینکه آیا کاربری با این ایمیل (به عنوان یوزرنیم) از قبل وجود دارد؟
            if User.objects.filter(username=email).exists():
                return render(request, 'tracker/signup.html', {
                    'error': 'این ایمیل قبلاً ثبت شده است.'
                })
            else:
                # ذخیره کاربر جدید: ایمیل را جایگزین username می‌کنیم
                user = User.objects.create_user(username=email, email=email, password=password)
                
                # اگر خواستید نام کامل را هم در فرست‌نِیم ذخیره کنید
                user.first_name = fullname
                user.save()
                
                return redirect('login') # انتقال به صفحه ورود پس از ثبت‌نام
        else:
            return render(request, 'tracker/signup.html', {
                'error': 'رمز عبور و تکرار آن یکسان نیستند.'
            })
            
    return render(request, 'tracker/signup.html')


def about_view(request):
    return render(request, 'tracker/about.html')


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
    return render(request, 'tracker/transactions.html', context)
def forgot_password(request):
    return render(request, 'tracker/forgot-password.html')
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.shortcuts import redirect, render

def login_view(request):
    if request.method == 'POST':
        # تشخیص روش ورود (ایمیل یا شماره همراه)
        login_method = request.POST.get('loginMethod', 'email')
        password = request.POST.get('password')
        remember_me = request.POST.get('rememberMe') == 'on'

        if login_method == 'email':
            identifier = request.POST.get('email', '').strip()
        else:
            identifier = request.POST.get('phone', '').strip()
            # اگر شماره همراه است، فعلاً پیام می‌دهیم چون مدل کاربر شماره ندارد
            messages.error(request, 'ورود با شماره همراه فعلاً پشتیبانی نمی‌شود. لطفاً از ایمیل استفاده کنید.')
            return redirect('login')

        if not identifier or not password:
            return render(request, 'tracker/login.html', {
                'error': 'لطفاً ایمیل و رمز عبور را وارد کنید.'
            })

        # احراز هویت با استفاده از ایمیل به عنوان username
        user = authenticate(request, username=identifier, password=password)

        if user is not None:
            auth_login(request, user)
            # مدیریت "مرا به خاطر بسپار"
            if not remember_me:
                request.session.set_expiry(0)  # نشست پس از بستن مرورگر از بین می‌رود
            return redirect('dashboard')  # نام الگوی داشبورد خود را بررسی کنید
        else:
            return render(request, 'tracker/login.html', {
                'error': 'ایمیل یا رمز عبور اشتباه است.'
            })


    # اگر درخواست GET بود، فقط صفحه لاگین را نشان بده
    return render(request, 'tracker/login.html')


def statistics_view(request):
    # بعداً می‌توانید محاسبات مربوط به نمودارها را اینجا اضافه کنید
    return render(request, 'tracker/statistics.html')



@login_required
def profile_view(request):
    user = request.user
    
    # فرم تغییر رمز عبور جنگو
    password_form = PasswordChangeForm(user)

    if request.method == 'POST':
        # بررسی اینکه کدام فرم ارسال شده است (اطلاعات کاربری یا رمز عبور)
        
        # ۱. اگر فرم تغییر اطلاعات کاربری ارسال شده باشد
        if 'update_profile' in request.POST:
            # دریافت اطلاعات از فرم (نام فیلدهای HTML باید با این نام‌ها مطابقت داشته باشد)
            first_name = request.POST.get('first_name')
            email = request.POST.get('email')

            # آپدیت کردن اطلاعات
            user = request.user
            user.first_name = first_name  # کل نام اینجا ذخیره میشود
            user.email = email
            user.username = email
            user.save()
            messages.success(request, 'پروفایل با موفقیت بروزرسانی شد.')
            return redirect('profile')
            
        # ۲. اگر فرم تغییر رمز عبور ارسال شده باشد
        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                # برای جلوگیری از خروج کاربر بعد از تغییر رمز، سشن او را آپدیت می‌کنیم
                update_session_auth_hash(request, user)  
                messages.success(request, 'رمز عبور شما با موفقیت تغییر کرد.')
                return redirect('profile')
            else:
                messages.error(request, 'لطفاً خطاهای فرم تغییر رمز عبور را برطرف کنید.')

    context = {
        'user': user,
        'password_form': password_form
    }
    
    # مسیر رندر با توجه به صحبت‌های قبلی روی پوشه tracker تنظیم شده است
    return render(request, 'tracker/profile.html', context)

@login_required
def delete_transaction(request, transaction_id):
    if request.method == 'POST':
        transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
        transaction.delete()
        messages.success(request, "تراکنش با موفقیت حذف شد.")
    return redirect('transaction_list') # نام url صفحه تراکنش‌ها را اینجا قرار دهید



@login_required
def chart_data_api(request):
    user = request.user
    user_transactions = Transaction.objects.filter(user=user)

    chart_labels = []
    chart_incomes = []
    chart_expenses = []

    # محاسبه درآمد و هزینه برای ۶ ماه گذشته
    for i in range(5, -1, -1):
        target_date = datetime.today() - relativedelta(months=i)
        
        month_transactions = user_transactions.filter(
            date_time__year=target_date.year,
            date_time__month=target_date.month
        )
        
        # محاسبه مجموع درآمدها و هزینه‌های این ماه
        income = month_transactions.filter(kind='Income').aggregate(Sum('amount'))['amount__sum'] or 0
        expense = month_transactions.filter(kind='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
        
        # نام ماه (مثلاً 2023-10) را به لیست اضافه می‌کنیم
        chart_labels.append(target_date.strftime("%Y-%m")) 
        chart_incomes.append(float(income))
        chart_expenses.append(float(expense))

    # --- بخش اضافه شده برای نمودار دسته‌بندی (Category Chart) ---
    # استخراج مجموع هزینه‌ها به تفکیک دسته‌بندی (فقط برای تراکنش‌های نوع Expense کاربر)
    category_qs = user_transactions.filter(kind='Expense').values('category').annotate(total=Sum('amount'))
    
    category_labels = [item['category'] for item in category_qs]
    category_data = [float(item['total']) for item in category_qs]
    # -------------------------------------------------------------

    # ارسال اطلاعات به صورت JSON برای جاوا اسکریپت
    return JsonResponse({
        'labels': chart_labels,
        'incomes': chart_incomes,
        'expenses': chart_expenses,
        'category_labels': category_labels, # ارسال نام دسته‌بندی‌ها
        'category_data': category_data      # ارسال مجموع مبلغ هر دسته
    })

    



@login_required
def statistics_view(request):
    current_month = datetime.today().month

    # محاسبه مجموع درآمدها و هزینه‌های این ماه
    current_month_income = Transaction.objects.filter(
        user=request.user, 
        kind='Income', 
        date_time__month=current_month
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    current_month_expenses = Transaction.objects.filter(
        user=request.user, 
        kind='Expense', 
        date_time__month=current_month
    ).aggregate(Sum('amount'))['amount__sum'] or 0

    # محاسبه موجودی کل
    total_income = Transaction.objects.filter(user=request.user, kind='Income').aggregate(Sum('amount'))['amount__sum'] or 0
    total_expense = Transaction.objects.filter(user=request.user, kind='Expense').aggregate(Sum('amount'))['amount__sum'] or 0
    balance = total_income - total_expense

    context = {
        'balance': balance,
        'current_month_income': current_month_income,
        'current_month_expenses': current_month_expenses,
    }

    return render(request, 'tracker/statistics.html', context)


# در فایل views.py
def error_404_view(request):
    return render(request, 'tracker/404.html') # یا هر نامی که برای قالب خود گذاشته‌اید

