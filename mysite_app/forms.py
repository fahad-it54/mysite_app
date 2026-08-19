from django import forms
from .models import Profile, StudentProfile, FieldTrainingLog


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio']

class StudentEditForm(forms.ModelForm):

    class Meta:
        model = StudentProfile
        fields = ['student_class', 'email']


class FieldLogForm(forms.ModelForm):
    class Meta:
        model = FieldTrainingLog
        fields = ['activity', 'latitude', 'longitude', 'location_name']
        widgets = {
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
            'location_name': forms.HiddenInput(),
        }