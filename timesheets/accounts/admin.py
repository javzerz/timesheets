from django.contrib import admin
from .models import UserProfile, Timecard, TimecardSummary
from django.shortcuts import render
from django.db.models import Sum
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class TimecardAdmin(admin.ModelAdmin):
    list_display = ['created','project','department','date', 'funded']
    list_editable = ['funded']
    list_filter = ['project','funded','date']
    ordering = ['created']
    date_hierarchy = 'date'
    save_as = True

    fieldsets = (
        (None, {
        'classes':('wide'),
        'fields': (('user', 'department'),
        'project','date','hours',
        'comments',
        'funded')}),)

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user','department','position','phone']
    list_editable = ['department','position']
    list_filter = ['department']
    search_fields = ['user']

class TimecardSummaryAdmin(admin.ModelAdmin):
    date_hierarchy = 'date'
    list_filter = ['project']
    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context)

        try:
            qs = response.context_data['cl'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
            'total_hours': Sum('hours'),
        }

        response.context_data['summary'] = list(
            qs.values('project').annotate(**metrics).order_by('created')
        )

        response.context_data['summary_total'] = dict(
            qs.aggregate(**metrics)
        )

        return response

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Timecard, TimecardAdmin)
admin.site.register(TimecardSummary, TimecardSummaryAdmin)
