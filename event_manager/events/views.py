from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.views import generic
from events.models import Event, Venue


class IndexView(generic.ListView):
    template_name = "events/index.html"
    context_object_name = "events"

    def get_queryset(self):
        return Event.objects.filter(is_public=True).order_by("-pub_date")


class DashView(LoginRequiredMixin, generic.ListView):
    login_url = "/login/"
    template_name = "events/dashboard.html"
    context_object_name = "events_list"

    def get_queryset(self):
        return Event.objects.filter(organizer=self.request.user).order_by("-pub_date")


@login_required(login_url="/login")
def EditEvent(request, pk):
    pass


@login_required(login_url="/login")
def DeleteEvent(request, pk):
    pass


def PublicDetails(request, pk):
    pass


@login_required(login_url="/login")
def DashDetails(request, pk):
    pass


@login_required(login_url="/login")
def AddEvent(request):
    print(request.POST)
    if request.method == "POST":
        name = request.POST.get('name')
        description = request.POST.get('description')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        is_public = request.POST.get('is_public') == 'on'
        location = request.POST.get('location')
        max_participants = request.POST.get('max_participants')
        status = request.POST.get('status', 'upcoming')

        print(date)

        venue_name = request.POST.get('venue_name')
        is_virtual = request.POST.get('is_virtual') == 'on'
        address = request.POST.get('address')
        capacity = request.POST.get('capacity')
        virtual_meeting_link = request.POST.get('virtual_meeting_link')
        # Create the new venue instance
        venue = Venue.objects.create(
            name=venue_name,
            is_virtual=is_virtual,
            address=address,
            capacity=capacity,
            virtual_meeting_link=virtual_meeting_link,
        )

        organizer = request.user

        print(venue, organizer)

        print("---" * 20)

        # Create the new event instance
        try:
            if start_time >= end_time:
                raise ValidationError('End time must be after start time.')

            # Create the new event instance
            Event.objects.create(
                name=name,
                description=description,
                date=date,
                start_time=start_time,
                end_time=end_time,
                is_public=is_public,
                location=location,
                max_participants=max_participants,
                organizer=organizer,
                venue=venue,
                pub_date=timezone.now(),
                status=status,
            )
            return redirect('dash')
        except ValidationError as e:
            return render(request, 'events/add_event.html', {'error_message': str(e)})
    return render(request, "events/add_event.html")


def LoginView(request):
    if request.user.is_authenticated:
        return redirect('dash')
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have been logged in!")

            return redirect('index')
        else:
            messages.error(
                request, "There was an error logging in. Please try again.")
            return redirect('login')
    return render(request, "events/login.html")


def RegisterView(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        repeat_password = request.POST["repeat-password"]
        print(email, username, password, repeat_password)
        if password != repeat_password:
            messages.error(request, "Passwords do not match")
        try:
            user = User.objects.create_user(
                email=email, username=username, password=password)
            user.save()
            return redirect("login")
        except Exception as e:
            messages.error(request, str(e))
    return render(request, "events/register.html")


@login_required(login_url="/login")
def LogoutView(request):
    logout(request)
    return redirect("index")


@login_required(login_url="/login")
def ProfileView(request):
    return render(request, "events/profile.html")
