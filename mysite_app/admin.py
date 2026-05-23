from django.contrib import admin
from .models import Profile
from .models import StudentProfile, Subject, Result

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):

	readonly_fields = ('admission_number',)

admin.site.register(Profile)
admin.site.register(Subject)
admin.site.register(Result)

# Register your models here.
