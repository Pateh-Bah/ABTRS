from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.contrib import messages

from .models import SiteSettings
from .forms import SiteSettingsForm


def superuser_required(user):
    return user.is_authenticated and user.is_superuser

@method_decorator(user_passes_test(superuser_required), name='dispatch')
class SystemSettingsUpdateView(UpdateView):
    model = SiteSettings
    form_class = SiteSettingsForm
    template_name = 'core/system_settings_form.html'
    success_url = reverse_lazy('core:system_settings')

    def get_object(self, queryset=None):
        return SiteSettings.get_solo()

    def form_valid(self, form):
        messages.success(self.request, 'System settings updated successfully.')
        return super().form_valid(form)
