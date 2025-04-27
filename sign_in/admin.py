from django.contrib import admin
from .models import SignInRecord, StudentReference

@admin.register(SignInRecord)
class SignInRecordAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'student_name', 'time_in', 'time_out', 'reason', 'created_by')
    list_filter = ('reason', 'created_by')

    def student_id(self, obj):
        return obj.student.student_id if obj.student else 'Unknown'

    def student_name(self, obj):
        if obj.student:
            return f"{obj.student.first_name} {obj.student.last_name}"
        return 'Unknown'

@admin.register(StudentReference)
class StudentReferenceAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'first_name', 'last_name')
    search_fields = ('student_id', 'first_name', 'last_name')
