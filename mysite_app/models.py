from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
import resend
from django.conf import settings
#import requests  # kwa SMS API




class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        default='default.png'
    )

    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

   



class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class StudentProfile(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    admission_number = models.CharField(max_length=50, blank=True, null=True)
    student_class = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField()

    is_paid = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)



    def __str__(self):
        return f"{self.user.username} - {self.admission_number}"



   
    

class Result(models.Model):

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE
    )

    score = models.IntegerField()

    grade = models.CharField(max_length=2)

    def __str__(self):
        return f"{self.student.username} - {self.subject.name}"


class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    programme = models.CharField(max_length=200)
    citizenship = models.CharField(max_length=100, blank=True, null=True)
    certificate = models.FileField(upload_to='applications/certificates/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    submitted_at = models.DateTimeField(auto_now_add=True)
    generated_user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.full_name} - {self.status}"


# ===== SIGNAL - chini kabisa, baada ya class Application =====

@receiver(post_save, sender=Application)
def create_account_on_approval(sender, instance, **kwargs):
    if instance.status == 'approved' and not instance.generated_user:
        current_year = datetime.now().year
        reg_number = f"BIT{current_year}{instance.id:04d}"

        new_user = User.objects.create_user(username=reg_number, email=instance.email)
        new_user.set_unusable_password()
        new_user.save()

        student_profile, _ = StudentProfile.objects.get_or_create(user=new_user)
        student_profile.admission_number = reg_number
        student_profile.email = instance.email
        student_profile.is_paid = False
        student_profile.is_verified = False
        student_profile.save()

        instance.generated_user = new_user
        instance.save(update_fields=['generated_user'])

        send_registration_email(instance.email, instance.full_name, reg_number)


def send_registration_email(email, name, reg_number):
    resend.api_key = settings.RESEND_API_KEY

    html_content = f"""
    <div style="font-family: Arial, sans-serif; padding: 20px;">
        <h2 style="color:#14524a;">Hongera {name}!</h2>
        <p>Ombi lako la masomo limekubaliwa.</p>
        <p style="font-size:18px;"><b>Registration Number yako:</b> {reg_number}</p>
        <p>Tumia namba hii kufungua akaunti yako kwenye ukurasa wa Sign Up.</p>
        <p>Karibu.</p>
    </div>
    """

    try:
        resend.Emails.send({
            "from": "SUZA Admissions <onboarding@resend.dev>",
            "to": [email],
            "subject": "Umekubaliwa - Registration Number yako",
            "html": html_content,
        })
    except Exception as e:
        print(f"Email haikutumwa: {e}")
# Create your models here.
    

class PlacementOrganization(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    po_box = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.name


class FieldSupervisor(models.Model):
    name = models.CharField(max_length=255)
    organization = models.ForeignKey(PlacementOrganization, on_delete=models.CASCADE, related_name='supervisors')
    title = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class StudentPlacement(models.Model):
    student = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='placement')
    organization = models.ForeignKey(PlacementOrganization, on_delete=models.CASCADE)
    supervisor = models.ForeignKey(FieldSupervisor, on_delete=models.SET_NULL, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.student} @ {self.organization}"


class AttendanceRecord(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.localdate)
    sign_in_time = models.TimeField(null=True, blank=True)
    sign_out_time = models.TimeField(null=True, blank=True)
    sign_in_lat = models.FloatField(null=True, blank=True)
    sign_in_lng = models.FloatField(null=True, blank=True)
    sign_out_lat = models.FloatField(null=True, blank=True)
    sign_out_lng = models.FloatField(null=True, blank=True)

    class Meta:
        unique_together = ('student', 'date')

    def hours_worked(self):
        if self.sign_in_time and self.sign_out_time:
            today = timezone.localdate()
            dt_in = timezone.datetime.combine(today, self.sign_in_time)
            dt_out = timezone.datetime.combine(today, self.sign_out_time)
            return round((dt_out - dt_in).seconds / 3600, 2)
        return None


class FieldTrainingLog(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.localdate)
    time_logged = models.TimeField(default=timezone.now)
    activity = models.TextField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    location_name = models.CharField(max_length=255, blank=True)
    approved = models.BooleanField(default=False)
    supervisor_comment = models.TextField(blank=True)

    class Meta:
        ordering = ['-date', '-time_logged']


class SupervisorVisit(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='visits')
    supervisor = models.ForeignKey(FieldSupervisor, on_delete=models.SET_NULL, null=True)
    visit_date = models.DateField()
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[
        ('scheduled', 'Scheduled'), ('completed', 'Completed'), ('missed', 'Missed'),
    ], default='scheduled')

    class Meta:
        ordering = ['-visit_date']