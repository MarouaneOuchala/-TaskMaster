from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='tasks:task-list'), name='home'),
    path('tasks/', include('tasks.urls')),
    path('tasks/api/', include('tasks.api.urls')),
    path('users/', include('accounts.urls')),
] 