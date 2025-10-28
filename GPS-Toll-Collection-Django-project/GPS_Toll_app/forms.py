from django import forms
from .models import Vehicle_details, Trip, Profile
from django.core.exceptions import ValidationError


import uuid


# forms.py

from django import forms
from .models import Vehicle_details

class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle_details
        fields = ['vehicle_number', 'vehicle_type', 'vehicle_model', 'vehicle_company', 'vehicle_color']
        widgets = {
            'vehicle_number': forms.TextInput(attrs={'class': 'form-control border border-primary rounded-pill fs-5','id':'Id_Vehicle_Number'}),
            'vehicle_type': forms.TextInput(attrs={'class': 'form-control border border-primary rounded-pill fs-5','id':'Id_Vehicle_Type'}),
            'vehicle_model': forms.TextInput(attrs={'class': 'form-control border border-primary rounded-pill fs-5','id':'Id_Vehicle_Model'}),
            'vehicle_company': forms.TextInput(attrs={'class': 'form-control border border-primary rounded-pill fs-5','id':'Id_Vehicle_Company'}),
            'vehicle_color': forms.TextInput(attrs={'class': 'form-control border border-primary rounded-pill fs-5','id':'Id_Vehicle_Color'}),
        }

    def clean_vehicle_number(self):
        vehicle_number = self.cleaned_data['vehicle_number']
        # Check if the vehicle number already exists in the database
        if Vehicle_details.objects.filter(vehicle_number=vehicle_number).exists():
            raise forms.ValidationError("Vehicle number already exists.")
        return vehicle_number































class TripForm(forms.ModelForm):
    uuid_field = forms.CharField(widget=forms.HiddenInput(), required=False)
    class Meta:
        model = Trip
        fields = ['starting_point','total_amount', 'ending_point', 'vehicle_number','total_amount','uuid_field', 'charge_per_km']
        widgets = {
            'starting_point': forms.Select(attrs={'class': 'rounded-select my-4 ml-5 start-point rounded-pill '}),
            'ending_point': forms.Select(attrs={'class': 'rounded-select my-4 ml-5 end-point rounded-pill'}),
            'vehicle_number': forms.Select(attrs={'class': 'rounded-select mt-3 mb-5'}),
            'uuid_field': forms.HiddenInput(),
            
        }
        
        error_messages = {
            'starting_point': {
                'required': "Please Select the Starting Location.",
                
            },
            'ending_point': {
                'required': "Please Select the Ending Location.",
            },
            'vehicle_number': {
                'required': "Please select a Vehicle Number.",
            },
        }
        
    def clean(self):
        cleaned_data = super().clean()
        starting_point = cleaned_data.get('starting_point')
        ending_point = cleaned_data.get('ending_point')
        

        # Check if starting_point and ending_point are the same
        if starting_point == ending_point:
            raise ValidationError("Starting Location and Ending Location cannot be the same.")
        
        return cleaned_data
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if not instance.uuid_field:
            instance.uuid_field = uuid.uuid4().hex[:10].upper()  # Generate and assign UUID if not already set
            commit = True
            print(f"form.py uuid_field: {instance.uuid_field}")
            
        if commit:
            instance.save()
        return instance
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Pop the user from the kwargs, default to None
        super().__init__(*args, **kwargs)
        if user is not None:
            # Get the profile of the current user
            profile = Profile.objects.get(user=user)
            # Filter vehicle_number queryset based on the user's profile
            self.fields['vehicle_number'].queryset = Vehicle_details.objects.filter(user=profile)
        self.fields['vehicle_number'].empty_label = "Choose the Vehicle Number"
        
        
      