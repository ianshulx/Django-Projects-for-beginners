from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib.auth.models import User, auth 
from datetime import date, datetime, timedelta
from .models import Expense, Income, IncomeCategory, ExpenseCategory, Account, Budget
# Create your views here.

# Dashboard
def dashboard(request):
    if request.user.is_authenticated:
        my_account= Account.objects.get(user=request.user.id)
        balance= my_account.balance

        # Expenses By category
        out_dict={}
        my_catg=ExpenseCategory.objects.filter(user=request.user.id)
        for catg in my_catg:
            out_dict[catg.name]=0

        expenses= Expense.objects.filter(user=request.user.id).order_by('id')
        for expense in expenses:
            catg=expense.category
            pre_amount=expense.amount
            pre_total=out_dict[catg.name]
            out_dict[catg.name]=pre_amount+pre_total
        # create list from above dict
        catg_list = []
        catg_total_list = []
        items = out_dict.items()
        for item in items:
            catg_list.append(item[0]), catg_total_list.append(item[1])



        # For Last 10 days  Income Data
        Income_last_10days_amount=[]
        for i in range(10):
            _10days_income = Income.objects.filter(user=request.user.id,date__gte=date.today()-timedelta(days=i),date__lt=date.today()-timedelta(days=i-1)).order_by("id")

            total_of_aday=0
            for income in _10days_income:
                total_of_aday+=income.amount
            Income_last_10days_amount.append(total_of_aday)
        Income_last_10days_amount.reverse()

        # Last 10 days Expense Data
        Expense_last_10days_amount=[]
        for i in range(10):
            _10days_expense = Expense.objects.filter(user=request.user.id,date__gte=date.today()-timedelta(days=i),date__lt=date.today()-timedelta(days=i-1)).order_by("id")

            total_of_aday=0
            for expense in _10days_expense:
                total_of_aday+=expense.amount
            Expense_last_10days_amount.append(total_of_aday)
        Expense_last_10days_amount.reverse()

        # Data Month format list i.e. 03/Feb,..
        temp_pre_10days_list= [datetime.now().date()-timedelta(days=i) for i in range(10)]
        pre_10days_list=[]            
        for i in temp_pre_10days_list:
            day=i.day
            if i.month==1:
                month="Jan"
            if i.month==2:
                month="Feb"
            if i.month==3:
                month="Mar"
            if i.month==4:
                month="Apil"
            if i.month==5:
                month="May"
            if i.month==6:
                month="June"
            if i.month==7:
                month="Jul"
            if i.month==8:
                month="Aug"
            if i.month==9:
                month="Sept"
            if i.month==10:
                month="Oct"
            if i.month==11:
                month="Nov"
            else:
                month="Dec"
            pre_10days_list.append(f"{day}{month}")
        pre_10days_list.reverse()


        return render(request,"dashboard.html",{"balance":balance,"category_list":catg_list,"catg_total_list":catg_total_list,"pre_10days_list":pre_10days_list,"Income_last_10days_amount":Income_last_10days_amount,"Expense_last_10days_amount":Expense_last_10days_amount})
    else:
        return redirect("/")

# Income
def income(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            name = request.POST['name']
            category_id = request.POST.get('category')
            amount = request.POST['amount']
            date = request.POST['date']
            note = request.POST.get('note')
            category = get_object_or_404(IncomeCategory, user=request.user.id, id=int(category_id))

            my_account = get_object_or_404(Account, user=request.user.id)
            my_account.balance += float(amount)
            my_account.save()
            print("Account Balance Updated!!")
            # Create Income record
            Income.objects.create(
                name=name,
                user=request.user,
                category=category,
                amount=amount,
                date=date,
                note=note
            )
            return redirect('/incomes')

        incomes_catg = IncomeCategory.objects.filter(user=request.user.id)
        incomes = Income.objects.filter(user=request.user.id)

        return render(request, "income.html", {"categories": incomes_catg, "incomes": incomes})
    else:
        return redirect("/")

# Expenses
def expenses(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            name=request.POST['name']
            category_id=request.POST.get('category')
            amount=request.POST['amount']
            date=request.POST['date']
            note=request.POST.get('note')
            category = ExpenseCategory.objects.get(user=request.user.id,id=int(category_id))

            my_account= Account.objects.get(user=User.objects.get(id = request.user.id))
            my_account.balance-=float(amount)
            my_account.save()
            print("Account Balance Updated!!")
            # Create Expenses record
            Expense.objects.create(name=name,user=User.objects.get(id = request.user.id),category=category,amount=amount,date=date,note=note)
            return redirect('/expenses')

        expenses_catg= ExpenseCategory.objects.filter(user=request.user.id)
        expenses= Expense.objects.filter(user=request.user.id)

        return render(request,"expense.html",{"categories":expenses_catg,"expenses":expenses})
    else:
        return redirect("/")


# EDIT Income
def edit_income(request,id):
    if request.user.is_authenticated:
        income=Income.objects.get(id=id)
        if request.method=="POST":
            name=request.POST['name']
            category_id=request.POST.get('category')
            amount=request.POST['amount']
            date=request.POST['date']
            note=request.POST.get('note')
            category = IncomeCategory.objects.get(user=request.user.id,id=int(category_id))

            # Update Account Balance
            my_account= Account.objects.get(user=User.objects.get(id = request.user.id))
            if float(amount)<income.amount:
                my_account.balance-=float((income.amount-float(amount)))
            else:
                my_account.balance+=float((float(amount)-income.amount))
            
            my_account.save()
            print("Account balance updated")

            # Update income 
            income.name=name
            income.amount=float(amount)
            if date:
                income.date=date
            income.note=note
            income.category=category
            income.save()
            print("Income Details Updated")
            return redirect("/incomes")

        categories= IncomeCategory.objects.filter(user=request.user.id)
        return render(request,"income_edit.html",{"income":income,"categories":categories})
    else:
        return redirect("/")

# EDIT Expense
def edit_expense(request,id):
    if request.user.is_authenticated:
        expense=Expense.objects.get(id=id)
        if request.method=="POST":
            name=request.POST['name']
            category_id=request.POST.get('category')
            amount=request.POST['amount']
            date=request.POST['date']
            note=request.POST.get('note')
            category = ExpenseCategory.objects.get(user=request.user.id,id=int(category_id))

            # Update Account Balance
            my_account= Account.objects.get(user=User.objects.get(id = request.user.id))
            if float(amount)<expense.amount:
                my_account.balance+=float((expense.amount-float(amount)))
            else:
                my_account.balance-=float((float(amount)-expense.amount))
            
            my_account.save()
            print("Account balance updated")

            # Update expense 
            expense.name=name
            expense.amount=float(amount)
            if date:
                expense.date=date
            expense.note=note
            expense.category=category
            expense.save()
            print("expense Details Updated")
            return redirect("/expenses")

        categories= ExpenseCategory.objects.filter(user=request.user.id)
        return render(request,"expense_edit.html",{"expense":expense,"categories":categories})
    else:
        return redirect("/")


# Delete Expense
def delete_expense(request,id):
    if request.user.is_authenticated:
        expense=Expense.objects.get(id=id)
        my_account= Account.objects.get(user=User.objects.get(id = request.user.id))
        my_account.balance+=float(expense.amount)
        my_account.save()
        print("Account balance updated")

        Expense.objects.get(id=id).delete()
        print("Expense deleted")
        return redirect("/expenses")
    else:
        return redirect("/")
    
# Delete Incmoe
def delete_income(request,id):
    if request.user.is_authenticated:
        income=Income.objects.get(id=id)
        my_account= Account.objects.get(user=User.objects.get(id = request.user.id))
        my_account.balance-=float(income.amount)
        my_account.save()
        print("Account balance updated")

        Income.objects.get(id=id).delete()
        print("Income Deleted")
        return redirect("/incomes")
    else:
        return redirect("/")


# For Report generation
import csv
def expense_report(request, duration):
    if duration=="daily":
        expenses = Expense.objects.filter(user=request.user.id,date__gte=datetime.now()).order_by("date")
    elif duration=="weekly":
        expenses = Expense.objects.filter(user=request.user.id,date__gte=datetime.now()-timedelta(days=7)).order_by("date")
    elif duration=="monthly":
        expenses = Expense.objects.filter(user=request.user.id,date__gte=datetime.now()-timedelta(days=30)).order_by("date")
    else:
        expenses = Expense.objects.filter(user=request.user.id).order_by("date")  

    response = HttpResponse(content_type='text/csv')  
    response['Content-Disposition'] = f'attachment; filename="Expenses_{duration}_report.csv"'  
    writer = csv.writer(response)  
    writer.writerow(["Sr.No.","Name","Category","Amount","Date","Note"]) 
    counter=1 
    for expense in expenses:  
        writer.writerow([counter,expense.name,expense.category,expense.amount,expense.date,expense.note])  
        counter+=1
    return response

# For Report generation
import csv
def income_report(request, duration):
    if duration=="daily":
        incomes = Income.objects.filter(user=request.user.id,date__gte=datetime.now()).order_by("date")
    elif duration=="weekly":
        incomes = Income.objects.filter(user=request.user.id,date__gte=datetime.now()-timedelta(days=7)).order_by("date")
    elif duration=="monthly":
        incomes = Income.objects.filter(user=request.user.id,date__gte=datetime.now()-timedelta(days=30)).order_by("date")
    else:
        incomes = Income.objects.filter(user=request.user.id).order_by("date")

    response = HttpResponse(content_type='text/csv')  
    response['Content-Disposition'] = f'attachment; filename="Incomes_{duration}_report.csv"'  
    writer = csv.writer(response)  
    writer.writerow(["Sr.No.","Name","Category","Amount","Date","Note"]) 
    counter=1 
    for income in incomes:  
        writer.writerow([counter,income.name,income.category,income.amount,income.date,income.note])  
        counter+=1
    return response

# Settings
def settings(request):
    if request.user.is_authenticated:
        profile= User.objects.get(id=request.user.id)
        expense_categories=ExpenseCategory.objects.filter(user=request.user.id)
        income_categories=IncomeCategory.objects.filter(user=request.user.id)
        if request.method== "POST":
            first_name= request.POST['first_name']
            last_name= request.POST['last_name']
            email= request.POST['email']

            profile.first_name=first_name
            profile.last_name=last_name
            profile.email=email
            profile.save()

            print("Profile Updated")
            return redirect("/profile")
        else:
            return render(request,"settings.html",{"profile":profile,"expense_categories":expense_categories,"income_categories":income_categories})
    else:
        return render(request, "/",{})



# Add Income category
def add_income_category(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            catg_name=request.POST['name']
            user=User.objects.get(id=request.user.id)
            IncomeCategory.objects.create(user=user,name=catg_name)
            print("Category Created")
        return redirect("/settings")
    else:
        return redirect("/")

# Add Ecpense category
def add_expense_category(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            catg_name=request.POST['name']
            user=User.objects.get(id=request.user.id)
            ExpenseCategory.objects.create(user=user,name=catg_name)
            print("Category Created")
        return redirect("/settings")
    else:
        return redirect("/")

# Remove expense category
def remove_expense_category(request,id):
    if request.user.is_authenticated:
        ExpenseCategory.objects.get(user=request.user.id,id=id).delete()
        print("Category Deleted")
        return redirect("/settings")
    else:
        return redirect("/")
    
# Remove Income category
def remove_income_category(request,id):
    if request.user.is_authenticated:
        IncomeCategory.objects.get(user=request.user.id,id=id).delete()
        print("Category Deleted")
        return redirect("/settings")
    else:
        return redirect("/")


# Index page
def index(request):
    if request.user.is_authenticated:
        return redirect("/dashboard")
    else:
        return render(request, "index.html",{})

# Signup 
def signup(request):
    if request.method == "POST":
        first_name= request.POST['first_name']
        last_name= request.POST['last_name']
        email= request.POST['email']
        password= request.POST['password']

        if User.objects.filter(username=email).exists():
            print("Username is already used")
            return redirect('/')
        else:
            user = User.objects.create_user(username=email,password= password, email=email, first_name=first_name,last_name=last_name)
            user.save()
            print("User Account created successfully")
            # Create Account for users
            Account.objects.create(user=user,balance=0,details="Primary account for User="+str(user.id),name=f'Account for {user.id}-{first_name}')
            print("Users Account Created!!")
            return redirect('/')
        
    return render(request,"index.html",{})
    
# Profile
def profile(request):
    if request.user.is_authenticated:
        profile= User.objects.get(id=request.user.id)
        account= Account.objects.get(user=request.user.id)
        if request.method== "POST":
            first_name= request.POST['first_name']
            last_name= request.POST['last_name']
            email= request.POST['email']

            profile.first_name=first_name
            profile.last_name=last_name
            profile.email=email
            profile.save()

            print("Profile Updated")
            return redirect("/profile")
        else:
            return render(request,"profile.html",{"profile":profile,"balance":account.balance})
    else:
        return render(request, "/",{})
    

# Login
def login(request):
    if request.method== "POST":
        username = request.POST['email']
        password = request.POST['password']

        user= auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            print(f"User {username} is logged in")
            return redirect("/dashboard")
        else:
            print("Invalid Login details")
            return redirect("/")
    else:
        return render(request, "/",{})


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect("/")