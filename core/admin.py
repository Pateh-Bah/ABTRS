from django.contrib import admin
from .models import SiteSettings

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_name", "primary_color", "header_color", "footer_color", "updated_at")
    readonly_fields = ("updated_at",)

    def has_add_permission(self, request):
        # Only allow a single settings object
        if SiteSettings.objects.exists():
            return False
        return super().has_add_permission(request)
