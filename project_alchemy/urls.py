from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from dashboard.views import dashboard

#prevents caching the dashboard page
def redirect_to_dashboard(request):
    response = redirect('/dashboard/', permanent=False)
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_dashboard),
    path('dashboard/', include('dashboard.urls')),
]

