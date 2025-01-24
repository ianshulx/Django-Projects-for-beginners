from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Student, Allocation
from django.contrib.auth.models import User
from django.contrib.auth import logout

def login_view(request):
    if request.method == 'POST':
        name = request.POST['name'] 
        password = request.POST['password']
        
        try:
            user = User.objects.get(username=name.lower())
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            if hasattr(user, 'student'):
                return redirect('student_dashboard')
            elif user.username == 'rector':
                return redirect('rector_dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password.'})
    
    return render(request, 'login.html')

@login_required
def student_dashboard(request):
    student = Student.objects.get(user=request.user)
    allocations = Allocation.objects.filter(allocated_seat=True)
    return render(request, 'student_dashboard.html', {'student': student, 'allocations': allocations})

@login_required
def allocate_seats(request):
    all_students = Student.objects.all()

    if request.method == 'POST':
        if 'clear' in request.POST:
            Allocation.objects.all().delete()  
            return render(request, 'allocation.html', {'open_allocations': [], 'reserved_allocations': [], 'all_students': all_students})

        open_students = list(Student.objects.filter(category='open').order_by('-cet_marks')[:5])
        reserved_students = list(Student.objects.filter(category='reserved').order_by('-cet_marks')[:5])

        open_allocations = []
        reserved_allocations = []

        for student in open_students:
            allocation, created = Allocation.objects.get_or_create(student=student)
            allocation.allocated_seat = True
            allocation.save()
            open_allocations.append(student)

        for student in reserved_students:
            allocation, created = Allocation.objects.get_or_create(student=student)
            allocation.allocated_seat = True
            allocation.save()
            reserved_allocations.append(student)

        return render(request, 'allocation.html', {
            'open_allocations': open_allocations,
            'reserved_allocations': reserved_allocations,
            'all_students': all_students
        })

    return render(request, 'allocation.html', {'open_allocations': [], 'reserved_allocations': [], 'all_students': all_students})


@login_required
def view_allocation(request):
    open_allocations = Allocation.objects.filter(student__category='open', allocated_seat=True).order_by('-student__cet_marks')
    reserved_allocations = Allocation.objects.filter(student__category='reserved', allocated_seat=True).order_by('-student__cet_marks')
    
    return render(request, 'view_allocation.html', {
        'open_allocations': open_allocations,
        'reserved_allocations': reserved_allocations
    })


def view_application(request):
    student = request.user.student  
    return render(request, 'view_application.html', {'student': student})


@login_required
def rector_dashboard(request):
    return render(request, 'rector_dashboard.html')


def logout_view(request):
    logout(request)  
    return redirect('login')