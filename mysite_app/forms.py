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

class FieldTrainingLogForm(forms.ModelForm):
    latitude = forms.FloatField(widget=forms.HiddenInput(), required=False)
    longitude = forms.FloatField(widget=forms.HiddenInput(), required=False)
    location_name = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = FieldTrainingLog
        fields = ['activity', 'latitude', 'longitude', 'location_name']
        widgets = {
            'activity': forms.Textarea(attrs={'placeholder': 'Write your day activity...'}),
        }


