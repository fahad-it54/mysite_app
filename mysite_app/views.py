from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import ProfileForm, StudentEditForm, FieldLogForm
from .models import Profile
from .models import StudentProfile, Subject, Result, FieldTrainingLog
from .models import Profile, StudentProfile


# LOGIN PAGE
def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

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
    student, created= StudentProfile.objects.get_or_create(user=request.user)

    return render(request, 'dashboard.html',{'profile':profile, 'student': student,})
@login_required
def edit_profile(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    student, _ = StudentProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        pform = ProfileForm(request.POST, request.FILES, instance=profile)
        sform = StudentEditForm(request.POST, instance=student)
        if pform.is_valid() and sform.is_valid():
            pform.save()
            sform.save()
            return redirect('dashboard')
    else:
        pform = ProfileForm(instance=profile)
        sform = StudentEditForm(instance=student)

    return render(request, 'edit_profile.html', {'pform': pform, 'sform': sform})

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

@login_required
def payment(request):
    student, _ = StudentProfile.objects.get_or_create(user=request.user)
    return render(request, 'payment.html', {'student': student})

@login_required
def results(request):
    student_profile, created = StudentProfile.objects.get_or_create(user=request.user)
    student_results = Result.objects.filter(student=request.user).select_related('subject')
    return render(request, 'user_profile.html', {'results': student_results})


@login_required
def field_log_create(request):
    if request.method == 'POST':
        form = FieldLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.student = request.user
            log.save()
            return redirect('field_log_list')
    else:
        form = FieldLogForm()
    return render(request, 'field_log_create.html', {'form': form})

@login_required
def field_log_list(request):
    logs = FieldTrainingLog.objects.filter(student=request.user).order_by('-date', '-time_logged')
    return render(request, 'field_log_list.html', {'logs': logs})
