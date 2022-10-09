# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Author, Books, Student, Librarian
from .forms import UserForm, StudentForm, BookForm, StaffForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.models import Group
# Create your views here.
def home(request):
    if request.user.is_authenticated():
        try:
            query = request.GET.get('q')
        except ValueError:
            query = None
        if query:
            q_type = request.GET.get('type')
            if q_type == 'author':
                detail = Books.objects.filter(author__fullname__icontains=query)
            if q_type == 'title':
                detail = Books.objects.filter(title__icontains=query)
            if q_type == 'isbn':
                detail = Books.objects.filter(isbn=query)
            if q_type == 'users':
                detail = Student.objects.filter(fullname__icontains=query) or Student.objects.filter(enrollment_no__icontains=query) \
                         or Librarian.objects.filter(fullname__icontains=query) or Librarian.objects.filter(librarian_id__icontains=query)
            if not detail:
                detail = ['No results found!']
            return render(request, 'library/index.html', {'detail': detail})            
        return render(request, 'library/index.html', {})
    else:
        return redirect('accounts/login')

def student_dashboard(request):
    if request.user.is_authenticated():
        if request.user.groups.filter(name='student').exists():    
            detail = Books.objects.filter(request_issue=True)
            return render(request, 'library/student_dashboard.html', {'detail': detail})
        return HttpResponse("You don't have specific permsission to access this page.")
    return redirect('../accounts/login')

def staff_issue(request):
    if request.user.is_authenticated():    
        if request.user.groups.filter(name='staff').exists():
            detail = Books.objects.filter(request_issue=True)
            return render(request, 'library/staff_issue.html', {'detail': detail})
        return HttpResponse("You don't have specific permsission to access this page.")    
    return render('../accounts/login')

def staff_addbook(request):
    if request.user.is_authenticated():
        if request.user.groups.filter(name='staff').exists():        
            if request.method == 'POST':
                form = BookForm(request.POST)
                if form.is_valid():
                    detail = form.save(commit=False)
                    detail.save()
                    form = BookForm
                    return render(request, 'library/staff_addbook.html', {'form': form})
            else:
                form = BookForm
            return render(request, 'library/staff_addbook.html', {'form': form})
        return HttpResponse("You don't have specific permsission to access this page.")
    else:
        return redirect('../accounts/login')

def change_request_issue(request):
    request_issue = request.GET.get('request_val')
    bookid = request.GET.get('bookid')
    email = request.GET.get('usermail')
    myobject = Books.objects.filter(book_id=bookid)
    if myobject.exists():
        myobject.update(request_issue=request_issue, email=email)
        boolval = 'True'
    else:
        boolval = 'False'
    data = {
        'valdb': boolval
    }
    return JsonResponse(data)

def change_issue_status(request):
    issue_status = request.GET.get('issue_val')
    bookid = request.GET.get('bookid')
    myobject = Books.objects.filter(book_id=bookid)
    duedate = datetime.now().date() + timedelta(days=14)
    returndate = datetime.now().date()
    issuedate = datetime.now().date()
    email_subject = 'IIIT Allahabad Library - Book Issue Notice'
    recipient_mail = myobject[0].email.encode('utf-8')
    if myobject.exists():
        myobject.update(issue_status=issue_status)
        if issue_status == 'True':
            myobject.update(issue_date=issuedate, due_date=duedate, return_date=None, fine=0)
            email_body = 'The following book has been issued to you.\n\n'\
                 'Book: ' + myobject[0].title.encode('utf-8') + '\n\n'\
                 'Due Date: ' + myobject[0].due_date.strftime('%d/%m/%Y') + '\n'
            send_mail(email_subject, email_body, "Anupam Dagar <anupam@dagar.com>", [recipient_mail])
        if issue_status == 'False':
            fine = (returndate - issuedate).days
            myobject.update(return_date=returndate, due_date=None, fine=fine)
        boolval = 'True'
    else:
        boolval = 'False'
    data = {
        'valdb': boolval
    }
    return JsonResponse(data)

def create_user(request):
    if request.user.is_authenticated():
        if request.user.groups.filter(name='admin').exists():
            if request.method == "POST":
                form = UserForm(request.POST)
                if form.is_valid():
                    detail = form.save(commit=False)
                    detail.save()
                    if request.POST.get('acctype') == 'student':
                        return redirect('create_student', username=detail.username, admin=request.user.username)
                    else:
                        return redirect('create_staff', username=detail.username, admin=request.user.username)
            else:	
                form = UserForm
            return render(request, 'library/adminpage.html', {'form':form})
        return HttpResponse("You don't have specific permsission to access this page.")
    else:
        return redirect('../accounts/login')

def create_student(request, username, admin):
    if request.user.username == admin:
        if request.user.groups.filter(name='admin').exists():        
            user_instance = get_object_or_404(User, username=username)
            if request.method == "POST":
                form = StudentForm(request.POST)
                if form.is_valid():
                    detail = form.save(commit=False)
                    detail.user = user_instance
                    detail.fullname = detail.first_name + ' ' + detail.last_name
                    detail.save()
                    detail.user.groups.add(Group.objects.get(name='student'))
                    return redirect('create_user')
            else:
                form = StudentForm
            return render(request, 'library/createstudent.html', {'form':form})
        return HttpResponse("You don't have specific permsission to access this page.")
    else:
        return redirect('../accounts/login')

def create_staff(request, username, admin):
    if request.user.username == admin:
        if request.user.groups.filter(name='admin').exists():        
            user_instance = get_object_or_404(User, username=username)
            if request.method == "POST":
                form = StaffForm(request.POST)
                if form.is_valid():
                    detail = form.save(commit=False)
                    detail.user = user_instance
                    detail.save()
                    detail.user.groups.add(Group.objects.get(name='staff'))
                    return redirect('create_user')
            else:
                form = StaffForm
            return render(request, 'library/createstaff.html', {'form':form})
        return HttpResponse("You don't have specific permsission to access this page.")
    else:
        return redirect('../accounts/login')
