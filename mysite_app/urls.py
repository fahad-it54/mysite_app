from django.urls import path
from .views import dashboard, edit_profile
from . import views
from .views import payment, results
urlpatterns = [

    path('', views.login_view, name='login'),

    path('signup/', views.signup_view, name='signup'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path("profile/edit/", edit_profile, name="edit_profile"),
    path('grader/', views.grader_view, name='grader'),
    path('profile/', views.profile_view, name='profile'),
    path('Courses/', views.Courses_view, name='Courses'),
    path('payment/', views.payment, name='payment'),
    path('results/', views.results, name='results'),
    path('field-training/', views.field_training_hub, name='field_training_hub'),
    path('field-training/attendance-action/', views.attendance_action, name='attendance_action'),
    path('field-training/logs/', views.field_log_list, name='field_log_list'),
    path('field-training/logs/add/', views.field_log_create, name='field_log_create'),
    


]
