import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','wakafine_bus.settings')
import django
django.setup()
from django.test.client import RequestFactory
from accounts.admin_views import UserCreateModalView
from django.contrib.auth import get_user_model
User=get_user_model()
# create a superuser if not exists
u=User.objects.filter(is_superuser=True).first()
if not u:
    u=User.objects.create_superuser('admin','admin@example.com','pass')
    print('created super')
rf=RequestFactory()
req=rf.get('/accounts/admin/users/create/',HTTP_X_REQUESTED_WITH='XMLHttpRequest')
# attach user
req.user=u
view=UserCreateModalView.as_view()
resp=view(req)
print('status',resp.status_code)
if hasattr(resp,'content'):
    print(resp.content[:200])
