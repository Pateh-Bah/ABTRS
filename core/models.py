from django.db import models
from django.core.validators import RegexValidator

class SiteSettings(models.Model):
    site_name = models.CharField(max_length=100, default="Waka-Fine Bus")
    logo = models.ImageField(upload_to="branding/", blank=True, null=True)
    primary_color = models.CharField(max_length=7, default="#1e40af", validators=[RegexValidator(r'^#[0-9A-Fa-f]{6}$', 'Enter a valid hex color code.')])
    header_color = models.CharField(max_length=7, default="#ffffff", validators=[RegexValidator(r'^#[0-9A-Fa-f]{6}$', 'Enter a valid hex color code.')])
    footer_color = models.CharField(max_length=7, default="#1f2937", validators=[RegexValidator(r'^#[0-9A-Fa-f]{6}$', 'Enter a valid hex color code.')])
    accent_color = models.CharField(max_length=7, default="#fbbf24", validators=[RegexValidator(r'^#[0-9A-Fa-f]{6}$', 'Enter a valid hex color code.')])
    header_text_color = models.CharField(max_length=7, default="#1f2937", validators=[RegexValidator(r'^#[0-9A-Fa-f]{6}$', 'Enter a valid hex color code.')])
    sidebar_text_color = models.CharField(max_length=7, default="#ffffff", validators=[RegexValidator(r'^#[0-9A-Fa-f]{6}$', 'Enter a valid hex color code.')])
    sidebar_color = models.CharField(max_length=7, default="#1e40af", validators=[RegexValidator(r'^#[0-9A-Fa-f]{6}$', 'Enter a valid hex color code.')])
    top_nav_text_color = models.CharField(max_length=7, default="#1f2937", validators=[RegexValidator(r'^#[0-9A-Fa-f]{6}$', 'Enter a valid hex color code.')])
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Site Settings"
        verbose_name_plural = "Site Settings"

    def __str__(self):
        return self.site_name

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
