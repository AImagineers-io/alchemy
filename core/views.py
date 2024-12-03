from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from urllib.parse import urlencode
from .forms import CustomUserCreationForm
from django.http import JsonResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from .models import TaskLog
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            message = urlencode({'message': 'Registration successful. Please log in with your new account.'})
            return redirect(f"{redirect('core:login').url}?{message}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})

def redirect_to_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard:dashboard')
    return redirect('core:login')


### USER TASKS API ###
@login_required
def user_tasks(request: HttpRequest) -> JsonResponse:
    user = request.user
    tasks = TaskLog.objects.filter(user=user).values(
        'log_id',
        'task_name',
        'status',
        'progress',
        'result',
        'error_message',
        'created_at',
        'updated_at',
    )
    return JsonResponse(list(tasks), safe=False)

### TASK TRACKING VIEW ###
@method_decorator(login_required, name='dispatch')
class TaskTrackingView(TemplateView):
    template_name = 'task_tracking.html'