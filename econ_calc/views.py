from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import math


def calculator_view(request):
    result = None
    if request.method == 'POST':
        try:
            calc_type = request.POST.get('calc_type')
            # amount می‌تواند نماینده P (ارزش فعلی)، F (ارزش آینده)، A (سری یکنواخت) یا G (گرادیان) باشد
            amount = float(request.POST.get('amount', 0))
            rate = float(request.POST.get('rate', 0)) / 100  # نرخ بهره (i) یا (r)
            periods = int(request.POST.get('periods', 0))    # تعداد دوره‌ها (n)
            
            # برای گرادیان هندسی و ترکیب پیوسته در صورت نیاز
            g_rate = float(request.POST.get('g_rate', 0)) / 100 # نرخ گرادیان هندسی (g)
            m = int(request.POST.get('m', 1)) # دفعات ترکیب در سال

            if calc_type == 'future_from_present': # 1. (F/P, i, n)
                calculated_value = amount * ((1 + rate) ** periods)
                result = f"ارزش آینده (F) برابر است با: {calculated_value:,.2f}"
            
            elif calc_type == 'present_from_future': # 2. (P/F, i, n)
                calculated_value = amount * ((1 + rate) ** -periods)
                result = f"ارزش فعلی (P) برابر است با: {calculated_value:,.2f}"
                
            elif calc_type == 'future_from_annuity': # 3. (F/A, i, n) - ارزش آینده یک سری یکنواخت
                calculated_value = amount * (((1 + rate) ** periods - 1) / rate)
                result = f"ارزش آینده سری یکنواخت (F) برابر است با: {calculated_value:,.2f}"

            elif calc_type == 'annuity_from_future': # 4. (A/F, i, n) - وجوه استهلاکی
                calculated_value = amount * (rate / ((1 + rate) ** periods - 1))
                result = f"مبلغ سری یکنواخت (A) برابر است با: {calculated_value:,.2f}"

            elif calc_type == 'present_from_annuity': # 5. (P/A, i, n) - ارزش فعلی یک سری یکنواخت
                calculated_value = amount * (((1 + rate) ** periods - 1) / (rate * (1 + rate) ** periods))
                result = f"ارزش فعلی سری یکنواخت (P) برابر است با: {calculated_value:,.2f}"

            elif calc_type == 'annuity_from_present': # 6. (A/P, i, n) - بازیافت سرمایه
                calculated_value = amount * ((rate * (1 + rate) ** periods) / ((1 + rate) ** periods - 1))
                result = f"مبلغ سری یکنواخت (A) برابر است با: {calculated_value:,.2f}"

            elif calc_type == 'present_from_gradient': # 7. (P/G, i, n) - ارزش فعلی گرادیان حسابی
                calculated_value = amount * (((1 + rate) ** periods - 1 - periods * rate) / ((rate ** 2) * (1 + rate) ** periods))
                result = f"ارزش فعلی گرادیان حسابی (P) برابر است با: {calculated_value:,.2f}"

            elif calc_type == 'annuity_from_gradient': # 8. (A/G, i, n) - تبدیل گرادیان حسابی به سری یکنواخت
                calculated_value = amount * ((1 / rate) - (periods / ((1 + rate) ** periods - 1)))
                result = f"سری یکنواخت معادل گرادیان (A) برابر است با: {calculated_value:,.2f}"

            elif calc_type == 'present_from_geometric_gradient': # 9. (P/A1, g, i, n) - ارزش فعلی گرادیان هندسی
                if rate == g_rate:
                    calculated_value = amount * (periods / (1 + rate))
                else:
                    calculated_value = amount * ((1 - ((1 + g_rate) ** periods) * ((1 + rate) ** -periods)) / (rate - g_rate))
                result = f"ارزش فعلی گرادیان هندسی (P) برابر است با: {calculated_value:,.2f}"

            elif calc_type == 'effective_interest_rate': # 10. نرخ بهره موثر
                calculated_value = ((1 + (rate / m)) ** m) - 1
                result = f"نرخ بهره موثر (ieff) برابر است با: {calculated_value * 100:,.2f}%"

            elif calc_type == 'continuous_future': # 11. ارزش آینده با ترکیب پیوسته
                calculated_value = amount * math.exp(rate * periods)
                result = f"ارزش آینده با ترکیب پیوسته (F) برابر است با: {calculated_value:,.2f}"

            elif calc_type == 'continuous_present': # 12. ارزش فعلی با ترکیب پیوسته
                calculated_value = amount * math.exp(-rate * periods)
                result = f"ارزش فعلی با ترکیب پیوسته (P) برابر است با: {calculated_value:,.2f}"

        except (ValueError, TypeError, ZeroDivisionError):
            result = "خطا: لطفاً مقادیر معتبر وارد کنید (دقت کنید نرخ بهره برای برخی فرمول‌ها نمی‌تواند صفر باشد)."

    return render(request, 'econ_calc/calculator.html', {'result': result})
