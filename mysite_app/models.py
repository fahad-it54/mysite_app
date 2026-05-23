from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import datetime


class Profile(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    profile_picture = models.ImageField(
        upload_to='profile_pics/',
        default='default.jpg'
    )

    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

   



class Subject(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:

       
        current_year = datetime.now().year

        for user in User.objects.all():


           user_profile, created =  StudentProfile.objects.get_or_create(user=user)
       

        if not user_profile.admission_number:
         admission_number = f"FAHA/{current_year}/{instance.id:03d}"

        user_profile.admission_number = admission_number
        user_profile.save()

class StudentProfile(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    admission_number = models.CharField(max_length=50, blank=True, null=True)
    student_class = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField()


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
# Create your models here.
