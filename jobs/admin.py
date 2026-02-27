# jobs/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Job


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):

    list_display  = ('logo_preview', 'title', 'company', 'location', 'job_type', 'skill', 'salary')
    list_filter   = ('job_type', 'skill')
    search_fields = ('title', 'company', 'location', 'skill')
    ordering      = ('-id',)
    readonly_fields = ('logo_preview',)

    def logo_preview(self, obj):
        # Safe check — works whether logo field exists or is empty
        if hasattr(obj, 'logo') and obj.logo:
            return format_html(
                '<img src="{}" width="40" height="40" style="border-radius:8px;object-fit:cover;" />',
                obj.logo.url
            )
        # Fallback: coloured initial box
        return format_html(
            '<div style="width:40px;height:40px;border-radius:8px;background:linear-gradient(135deg,#4f8ef7,#0ea5e9);'
            'display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:16px;">'
            '{}</div>',
            obj.company[0].upper() if obj.company else '?'
        )

    logo_preview.short_description = 'Logo'