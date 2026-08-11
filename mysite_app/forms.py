from django import forms
from .models import Profile, StudentProfile


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['profile_picture', 'bio']

class StudentEditForm(forms.ModelForm):

    class Meta:
        model = StudentProfile
        fields = ['student_class', 'email']