from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from banking import models
from django.views.generic import ListView
from django.contrib import messages

# Create your views here.

def index(request):
    return render(request,'banking/index.html',{})

def customers(request):
    customers_list = models.User.objects.all()
    customers_extended = models.UserExtension.objects.all()
    return render(request,'banking/customers.html',{'customers':customers_extended,})

def customers_search(request):
    query = request.GET.get('query')
    customers_extended_list = models.UserExtension.objects.filter(user__first_name__contains=query)
    customers_extended_list2 = models.UserExtension.objects.filter(user__last_name__contains=query)
    customers_extended_list = customers_extended_list.union(customers_extended_list2)
    return render(request,'banking/customers.html',{'customers':customers_extended_list,})


def transaction(request,pk):
    if request.method == "POST":
        customers = models.UserExtension.objects.all()
        to_customer = models.User.objects.get(pk=pk)
        to_customer_extended = models.UserExtension.objects.get(user=to_customer)  
        amount = request.POST.get('amount')
        from_id = request.POST.get('from_id')
        from_customer = models.User.objects.get(pk=from_id)
        from_customer_extended = models.UserExtension.objects.get(user=from_customer)
        amount = int(amount)
        from_customer_extended.current_balance -= amount
        to_customer_extended.current_balance += amount
        from_customer_extended.save()
        to_customer_extended.save()
        transact = models.Transactions()
        transact.from_user = from_customer
        transact.to_user = to_customer
        transact.amount = amount
        transact.save()
        messages.info(request, 'Transaction was successful!')
        return redirect('banking:customers')
        
    else:  
        customers = models.UserExtension.objects.all()
        from_customer = models.User.objects.get(pk=pk)
        from_customer_extended = models.UserExtension.objects.get(user=from_customer)  

        # Allow MAX AMOUNT ONLY
        return render(request,'banking/transaction.html',{'customers':customers,'id_from':pk,'from_customer':from_customer_extended,})

def transact_customers_search(request, pk):
    query = request.GET.get('query')
    customers_extended_list = models.UserExtension.objects.filter(user__first_name__contains=query)
    customers_extended_list2 = models.UserExtension.objects.filter(user__last_name__contains=query)
    customers_extended_list = customers_extended_list.union(customers_extended_list2)
    from_customer = models.User.objects.get(pk=pk)
    from_customer_extended = models.UserExtension.objects.get(user=from_customer)  
    return render(request,'banking/transaction.html',{'customers':customers_extended_list,'id_from':pk,'from_customer':from_customer_extended,})

class RecordsView(ListView):
    model = models.Transactions
    template_name = 'banking/records.html'
    context_object_name = 'records'

    ordering = ['-timestamp']