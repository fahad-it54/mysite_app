from django.urls import path
from .views import dashboard, edit_profile
from . import views

urlpatterns = [

    path('', views.login_view, name='login'),

    path('signup/', views.signup_view, name='signup'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path("profile/edit/", edit_profile, name="edit_profile"),
    path('grader/', views.grader_view, name='grader'),
    path('profile/', views.profile_view, name='profile'),
    path('Courses/', views.Courses_view, name='Courses'),


]
