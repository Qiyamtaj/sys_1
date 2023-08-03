from django import forms
# this is where all forms for this app will be created and stored
from.models import * 
# imorting models from models.py
from django import forms
from django.contrib import admin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError




class UserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required fields, plus a repeated password.
    """
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name')
        
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



class UserChangeForm(forms.ModelForm):
    """
    A form for updating users. Includes all the fields except the password.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email',  'first_name', 'last_name', 'is_admin')


class UserAdmin(admin.ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin that reference specific fields on auth.User.
    list_display = ('email',  'first_name', 'last_name', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ( 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email',  'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()



COMFORTABILITY_CHOICES = [
        ('very_comfortable', 'Very Comfortable'),
        ('comfortable', 'Comfortable'),
        ('kind_of_comfortable', 'Kind of Comfortable'),
        ('a_bit_uncomfortable', 'A Bit Uncomfortable'),
        ('uncomfortable', 'Uncomfortable'),

    ]

# Surfer form
class SurferForm(forms.ModelForm):

    comfortability_in_ocean = forms.ChoiceField(
        choices=COMFORTABILITY_CHOICES,
        label='How comfortable are you in the ocean?',
        widget=forms.Select(attrs={'class': 'border w-full border-gray-300 rounded px-4 py-2 mb-4 input-field'}),
        required=True
    )

    swim_longer_than_5_min = forms.BooleanField(
        label='Can Swim Longer Than 5 Minutes',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'checkbox-field'})
    )

    widgets = {
            'role': forms.HiddenInput(attrs={'value': 'surfer'})  # Add this line to make the "role" field hidden
        }

    class Meta:
        model = Surfer
        fields = (
            'age',
            'phone_number',
            'address',
            'country',
            'DOB',
            'gender',
            'race',
            'medical_issues',
            'occupation',
            'school',
            'onset_of_condition',
            'diagnosis_and_needs',
            'medication',
            'extra_info',
            'swim_longer_than_5_min',
            'comfortability_in_ocean',
            'emergency_contact_first_name',
            'emergency_contact_last_name',
            'emergency_contact_cell',
            'medical_aid',
            'medical_aid_num',
            'receive_newsletter',
            'accept_TandC',
            )

class VolunteerForm(forms.ModelForm):

    comfortability_in_ocean = forms.ChoiceField(
        choices=COMFORTABILITY_CHOICES,
        label='How comfortable are you in the ocean?',
        widget=forms.Select(attrs={'class': 'border w-full border-gray-300 rounded px-4 py-2 mb-4 input-field'}),
        required=True
    )

    swim_longer_than_5_min = forms.BooleanField(
        label='Can Swim Longer Than 5 Minutes',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'checkbox-field'})
    )
    widgets = {
            'role': forms.HiddenInput(attrs={'value': 'volunteer'})  # Add this line to make the "role" field hidden
        }
    
    class Meta:
            model = Volunteer
            # specifying which model we are working with
            fields = (
                'age',
                'phone_number',
                'address',
                'country',
                'DOB',
                'gender',
                'race',
                'medical_issues',
                'occupation',
                'offered_services',
                'availablity',
                'extra_info',
                'swim_longer_than_5_min',
                'comfortability_in_ocean',
                'previous_volunteer',
                'emergency_contact_first_name',
                'emergency_contact_last_name',
                'emergency_contact_cell',
                'medical_aid',
                'medical_aid_num',
                'receive_newsletter',
                'accept_TandC',
                )
        

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'email',
            'password',
        )

class LogoutForm(forms.ModelForm):
    fields = (
        'Logout',
    ) 

    

class EventForm(forms.ModelForm):
    surfers = forms.ModelMultipleChoiceField(queryset=Surfer.objects.filter(role='Surfer'))
    volunteers = forms.ModelMultipleChoiceField(queryset=Volunteer.objects.filter(role='Volunteer'))

    class Meta:
        model = Event
        fields = (
            'title', 
            'description', 
            'start_time', 
            'end_time', 
            'surfers', 
            'volunteers'
        )
