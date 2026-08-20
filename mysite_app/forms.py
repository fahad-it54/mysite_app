from django import forms
from .models import Profile, StudentProfile, FieldTrainingLog, Application


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['full_name', 'email', 'phone', 'programme', 'citizenship', 'certificate']


class RegNumberSignupForm(forms.Form):
    reg_number = forms.CharField(label="Registration Number")
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Rudia Password", widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        reg_number = cleaned_data.get('reg_number')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if reg_number:
            try:
                profile = StudentProfile.objects.get(admission_number=reg_number)
            except StudentProfile.DoesNotExist:
                raise forms.ValidationError("Registration Number hii haipo. Hakikisha umeandika sahihi kama ulivyotumiwa.")

            if profile.user.has_usable_password():
                raise forms.ValidationError("Akaunti hii tayari ina password. Tumia ukurasa wa Login.")

            cleaned_data['user'] = profile.user

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password hazifanani.")

        return cleaned_data




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


