from django.contrib import admin
from .models import Profile
from .models import StudentProfile, Subject, Result

from django.contrib import admin
from .models import (
    PlacementOrganization, FieldSupervisor, StudentPlacement,
    AttendanceRecord, FieldTrainingLog, SupervisorVisit,
)

admin.site.register(PlacementOrganization)
admin.site.register(FieldSupervisor)
admin.site.register(StudentPlacement)
admin.site.register(AttendanceRecord)
admin.site.register(SupervisorVisit)

@admin.register(FieldTrainingLog)
class FieldTrainingLogAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'time_logged', 'location_name', 'approved')
    list_editable = ('approved',)
    list_filter = ('approved', 'date')
    search_fields = ('student__username', 'activity', 'location_name')
    readonly_fields = ('date', 'time_logged', 'latitude', 'longitude')

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
  list_display = ('user', 'admission_number', 'is_paid', 'is_verified')
  list_editable = ('is_paid', 'is_verified')


  readonly_fields = ('admission_number',)

admin.site.register(Profile)
admin.site.register(Subject)
admin.site.register(Result)



# Register your models here.
