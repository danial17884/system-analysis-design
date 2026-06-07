from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def econ_calculator(request):
    result = None
    if request.method == 'POST':
        try:
            
            calc_type = request.POST.get('calc_type')
            amount = float(request.POST.get('amount'))
            rate = float(request.POST.get('rate')) / 100  
            periods = int(request.POST.get('periods'))

            
            if calc_type == 'future':
                
                calculated_value = amount * ((1 + rate) ** periods)
                result = f"ارزش آینده (F) برابر است با: {calculated_value:,.2f}"
            
            elif calc_type == 'present':
                
                calculated_value = amount * ((1 + rate) ** -periods)
                result = f"ارزش فعلی (P) برابر است با: {calculated_value:,.2f}"

        except (ValueError, TypeError):
            result = "خطا: لطفاً اعداد معتبر وارد کنید."

    return render(request, 'econ_calc/calculator.html', {'result': result})
