from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import ProfileForm
from .models import Profile
from .models import StudentProfile, Subject, Result


# LOGIN PAGE
def login_view(request):

    if request.method == 'POST':

        username = request.POST.get['username']
        password = request.POST.get['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('dashboard')

        else:

            return render(request, 'login.html', {
                'error': 'Username or password is incorrect'
            })

    return render(request, 'login.html')


# SIGNUP PAGE
def signup_view(request):

    if request.method == 'POST':

        form = UserCreationForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect('login')

    else:

        form = UserCreationForm()

    return render(request, 'signup.html', {
        'form': form
    })


# PAGE YA NDANI
@login_required
def dashboard(request):
    profile, created= Profile.objects.get_or_create(user=request.user)

    return render(request, 'dashboard.html',{'profile':profile})
@login_required
def edit_profile(request):
     
    profile, created= Profile.objects.get_or_create(user=request.user)


    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "edit_profile.html", {"form": form})


def grader_view(request):

    grade = None
    score = None
    student_name = None

    if request.method == "POST":

        student_name = request.POST.get("student_name")
        score = int(request.POST.get("score"))

        if score >= 90:
            grade = "A"

        elif score >= 80:
            grade = "B"

        elif score >= 70:
            grade = "C"

        elif score >= 60:
            grade = "D"

        else:
            grade = "F"

    return render(request, "grader.html", {
        "grade": grade,
        "score": score,
        "student_name": student_name
    })

@login_required
def profile_view(request):
    student = request.user

    
        
    user_profile = StudentProfile.objects.filter(user=student).first()
    

    

    subjects = Result.objects.filter(student=student)
    

    return render(request, "user_profile.html", {
        "student": student,
        "user_profile": user_profile,
        "subjects": subjects
    })
def Courses_view(request):
    return render(request, 'Courses.html')
