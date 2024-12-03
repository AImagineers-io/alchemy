from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import CustomAuthenticationForm
from core.views import user_tasks
from django.views.generic import TemplateView

app_name = 'core'

urlpatterns = [
    path('', views.redirect_to_login, name='redirect_to_login'),
    path('login/', auth_views.LoginView.as_view(
        template_name='core/login.html',
        authentication_form=CustomAuthenticationForm,
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='core/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('task-tracing/', TemplateView.as_view(template_name='core/task_tracking.html'), name='task-tracking'),
    path('tasks/', user_tasks, name='user-tasks'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete-task'),
    path('tasks/delete-all/', views.delete_all_tasks, name='delete-all-tasks'),
]

