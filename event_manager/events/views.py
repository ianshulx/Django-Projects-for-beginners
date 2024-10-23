from django.shortcuts import render, get_object_or_404, redirect, resolve_url
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.views import generic
from django.db.models import Avg
from events.models import Event, Venue, Ticket, EventReview


# View for listing public events on the index page
class IndexView(generic.ListView):
    template_name = "events/index.html"
    context_object_name = "events"

    def get_queryset(self):
        """
        Return a filtered list of events based on the search query.
        """
        query = self.request.GET.get("q")
        if query:
            # Filter events based on the search query
            return Event.objects.filter(is_public=True, name__icontains=query).order_by("-pub_date")
        else:
            return Event.objects.filter(is_public=True).order_by("-pub_date")

    def get_context_data(self, **kwargs):
        """
        Add additional context data, including today's date.
        """
        context = super().get_context_data(**kwargs)
        context['today'] = timezone.now().date()
        return context


# View for displaying the user's dashboard with their events
class DashView(LoginRequiredMixin, generic.ListView):
    login_url = "/login/"
    template_name = "events/dashboard.html"
    context_object_name = "events_list"

    def get_queryset(self):
        # Return events organized by the logged-in user
        return Event.objects.filter(organizer=self.request.user).order_by("-pub_date")


# View for editing an event
@login_required(login_url="/login")
def EditEvent(request, pk):
    event = get_object_or_404(Event, pk=pk)
    venue = get_object_or_404(Venue, pk=event.venue.pk)

    if request.method == "POST":
        # Update event details from form input
        event.name = request.POST.get('name')
        event.description = request.POST.get('description')
        event.date = request.POST.get('date')
        event.start_time = request.POST.get('start_time')
        event.end_time = request.POST.get('end_time')
        event.is_public = request.POST.get('is_public') == 'on'
        event.location = request.POST.get('location')
        event.max_participants = request.POST.get('max_participants')
        event.status = request.POST.get('status', 'upcoming')

        # Update venue details from form input
        venue.name = request.POST.get('venue_name')
        venue.is_virtual = request.POST.get('is_virtual') == 'on'
        venue.address = request.POST.get('address')
        venue.capacity = request.POST.get('capacity')
        venue.virtual_meeting_link = request.POST.get('virtual_meeting_link')

        # Save the changes to the database
        venue.save()
        event.save()

        return redirect('dash')

    return render(request, "events/edit_event.html", {"event": event})


# View for adding a review to an event
@login_required
def AddReview(request, pk):
    next_url = request.GET.get('next')

    if request.method == "POST":
        event = get_object_or_404(Event, pk=pk)
        review = request.POST.get('review')
        rating = request.POST.get('rating')

        # Create and save a new review for the event
        review_event = EventReview.objects.create(
            event=event, reviewer=request.user, rating=rating, comment=review)
        review_event.save()

        return redirect(next_url or 'index')

    return redirect('index')


# View for deleting an event
@login_required(login_url="/login")
def DeleteEvent(request, pk):
    event = get_object_or_404(Event, pk=pk)
    next_url = request.GET.get('next')

    # Ensure only the organizer can delete the event
    if event.organizer != request.user:
        return redirect(next_url or 'index')

    if request.method == "POST":
        event.delete()
        return redirect(next_url or 'dash')

    return redirect("index")


# View for deleting a review
@login_required(login_url="/login")
def DeleteReview(request, pk):
    review = get_object_or_404(EventReview, pk=pk)
    next_url = request.GET.get('next')

    # Ensure only the reviewer can delete the review
    if review.reviewer != request.user:
        return redirect(next_url or 'index')

    if request.method == "POST":
        review.delete()
        return redirect(next_url or 'dash')

    return redirect("index")


# View for editing a review
@login_required(login_url="/login")
def EditReview(request, pk):
    review = get_object_or_404(EventReview, pk=pk)
    next_url = request.GET.get('next', '')
    print(next_url)

    # Check if the user is the owner of the review
    if review.reviewer != request.user:
        return redirect(next_url or "dash")

    if request.method == "POST":
        # Update review details from form input
        review_comment = request.POST.get('review')
        rating = request.POST.get('rating')
        review.comment = review_comment
        review.rating = rating
        review.save()

        if next_url:
            return redirect(next_url)

    return render(request, "events/edit_review.html", {"review": review, "event": review.event})


# View for displaying public event details
def PublicDetails(request, pk):
    event = get_object_or_404(Event, pk=pk)
    user = request.user
    ticket = None
    review = None
    past_event = timezone.now().date() > event.date

    # Get all reviews for the event
    reviews = EventReview.objects.filter(event=event)
    rating = reviews.aggregate(Avg('rating'))

    if user.is_authenticated:
        # Check if the user has a ticket or a review for the event
        ticket = Ticket.objects.filter(event=event, user=user).first()
        review = EventReview.objects.filter(event=event, reviewer=user).first()

    return render(request, "events/details_event.html", {
        "event": event,
        "user": user,
        "ticket": ticket,
        "date": timezone.now(),
        "tickets": event.get_remaining_tickets(),
        "past_event": past_event,
        "review": review,
        "reviews": reviews,
        "rating": rating
    })


# View for adding a new event
@login_required(login_url="/login")
def AddEvent(request):
    if request.method == "POST":
        # Collect event details from form input
        name = request.POST.get('name')
        description = request.POST.get('description')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        is_public = request.POST.get('is_public') == 'on'
        location = request.POST.get('location')
        max_participants = request.POST.get('max_participants')
        status = request.POST.get('status', 'upcoming')

        # Collect venue details from form input
        venue_name = request.POST.get('venue_name')
        is_virtual = request.POST.get('is_virtual') == 'on'
        address = request.POST.get('address')
        capacity = request.POST.get('capacity')
        virtual_meeting_link = request.POST.get('virtual_meeting_link')

        # Create a new venue instance
        venue = Venue.objects.create(
            name=venue_name,
            is_virtual=is_virtual,
            address=address,
            capacity=capacity,
            virtual_meeting_link=virtual_meeting_link,
        )

        organizer = request.user

        try:
            # Validate event times
            if start_time >= end_time:
                raise ValidationError('End time must be after start time.')

            # Create a new event instance
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


# View for handling user login
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


# View for handling user registration
def RegisterView(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]
        repeat_password = request.POST["repeat-password"]

        if password != repeat_password:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        try:
            # Create a new user account
            user = User.objects.create_user(
                email=email, username=username, password=password)
            user.save()
            return redirect("login")
        except Exception as e:
            messages.error(request, str(e))

    return render(request, "events/register.html")


# View for handling user logout
@login_required(login_url="/login")
def LogoutView(request):
    logout(request)
    return redirect("index")


# View for displaying user profile
@login_required(login_url="/login")
def ProfileView(request):
    return render(request, "events/profile.html", {"user": request.user})


# View for handling ticket purchase
@login_required(login_url="/login")
def BuyTicket(request, pk):
    event = get_object_or_404(Event, pk=pk)
    user = request.user

    if request.method == "POST":
        # Create a new ticket for the event
        ticket = Ticket.objects.create(
            event=event,
            user=user,
            price=0.00,
            purchase_date=timezone.now()
        )
        return render(request, "events/buy_ticket.html", {"event": event, "user": user, "ticket": ticket})

    return render(request, "events/buy_ticket.html", {"event": event, "user": user})
