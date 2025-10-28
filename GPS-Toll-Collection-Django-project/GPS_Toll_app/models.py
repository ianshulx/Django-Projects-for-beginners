from django.db import models
from django.contrib.auth.models import User
# from .forms import 

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_token = models.CharField(max_length=100)
    isverified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


from django.db import models
from django.utils import timezone

class Vehicle_details(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    vehicle_number = models.CharField(max_length=100, unique=True,primary_key=True)
    vehicle_type = models.CharField(max_length=100)
    vehicle_model = models.CharField(max_length=100)
    vehicle_company = models.CharField(max_length=100)
    vehicle_color = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    
    
    
    def __str__(self):
        return f'{self.vehicle_number}'
    
    
    
    
    
    
    


class Trip(models.Model):
    vehicle_number = models.ForeignKey(
        Vehicle_details, to_field='vehicle_number', on_delete=models.CASCADE, related_name='trips'
    )
    starting_point = models.CharField(max_length=100, choices=[
        ('', 'From'),
        ('Mathura', 'Mathura'),
        ('Aligarh', 'Aligarh'),
        ('Palwal', 'Palwal'),
        ('Hathras', 'Hathras'),
    ])
    ending_point = models.CharField(max_length=100, choices=[
        ('', 'To'),
        ('Mathura', 'Mathura'),
        ('Aligarh', 'Aligarh'),
        ('Palwal', 'Palwal'),
        ('Hathras', 'Hathras'),
    ])
    
    uuid_field = models.CharField(max_length=10, null=True)
    vehicle_type = models.CharField(max_length=100, null=True) 
    date_entered = models.DateTimeField(default=None, blank=True, null=True)
    charge_per_km = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    total_km = models.DecimalField(max_digits=8, decimal_places=2)
    destination_reached_time = models.DateTimeField(default=timezone.now)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,)

    def __str__(self):
        return f'Trip from {self.starting_point} to {self.ending_point} field name {self.uuid_field}'
    
    
    
    
 
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# class Trip(models.Model):
#     vehicle_details = models.ForeignKey(
#         Vehicle_details, on_delete=models.CASCADE, related_name='trips'
#     )
#     starting_point = models.CharField(max_length=100, choices=[('','From'),('mathura','Mathura'),('gla','GLA University'),('Bangalore','Bangalore'),('Chennai','Chennai'),('Kolkata','Kolkata')])
#     ending_point = models.CharField(max_length=100, choices=[('','To'),('mathura','Mathura'),('gla','GLA University'),('Bangalore','Bangalore'),('Chennai','Chennai'),('Kolkata','Kolkata')])
#     vehicle_type = models.CharField(max_length=100, blank=True)  # Reflect choices set in form
#     vehicle_number = models.CharField(max_length=100)  # Reflect choices set in form
#     date_entered = models.DateTimeField(auto_now_add=True)
#     total_km = models.DecimalField(max_digits=8, decimal_places=2, default=5.0)
#     destination_reached_time = models.DateTimeField(default=timezone.now)
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

#     def __str__(self):
#         return f"Trip for {self.vehicle_details.vehicle_number} - {self.vehicle_details.vehicle_model} from {self.starting_point} to {self.ending_point}"


# class Vehicle_details(models.Model):
#     user = models.ForeignKey(Profile, on_delete=models.CASCADE)
#     vehicle_number = models.CharField(max_length=100)
#     vehicle_type = models.CharField(max_length=100)
#     vehicle_model = models.CharField(max_length=100)
#     vehicle_company = models.CharField(max_length=100)
#     vehicle_color = models.CharField(max_length=100)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f'{self.vehicle_number} - {self.vehicle_model}'
    


# # class Profile_google(models.Model):
# #     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
# #     firstname = models.CharField(max_length=50, blank=True)
# #     lastname = models.CharField(max_length=50, blank=True)
# #     email = models.EmailField(blank=True)
# #     isverified = models.BooleanField(default=True)
# #     created_at = models.DateTimeField(auto_now_add=True)

# #     def __str__(self):
# #         return self.user.username if self.user else 'No associated user'


# from django.db import models
# from django.utils import timezone

# class Trip(models.Model):
#     vehicle_details = models.ForeignKey(
#         Vehicle_details, on_delete=models.CASCADE, related_name='trip'
#     )
#     starting_point = models.CharField(max_length=100,choices=[('','From'),('mathura','Mathura'),('gla','GLA University'),('Bangalore','Bangalore'),('Chennai','Chennai'),('Kolkata','Kolkata')])
#     ending_point = models.CharField(max_length=100, choices=[('','To'),('mathura','Mathura'),('gla','GLA University'),('Bangalore','Bangalore'),('Chennai','Chennai'),('Kolkata','Kolkata')])
    # vehicle_type = models.CharField(max_length=100, blank=True)  # Reflect choices set in form
    # vehicle_number = models.CharField(max_length=100)  # Reflect choices set in form
#     date_entered = models.DateTimeField(auto_now_add=True)
#     total_km = models.DecimalField(max_digits=8, decimal_places=2, default=5.0)
#     destination_reached_time = models.DateTimeField(default=timezone.now)
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

#     def __str__(self):
#         return f"Trip for {self.vehicle_details.vehicle_number} - {self.vehicle_details.vehicle_model} from {self.starting_point} to {self.ending_point}"
