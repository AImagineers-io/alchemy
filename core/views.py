from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from urllib.parse import urlencode
from .forms import CustomUserCreationForm
from django.http import JsonResponse, HttpRequest
from django.contrib.auth.decorators import login_required
from .models import TaskLog, QAPair
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse

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


# ### USER TASKS API ###
# -----------------------

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
        'log_messages',
        'created_at',
        'updated_at',
    )
    return JsonResponse(list(tasks), safe=False)

### TASK TRACKING VIEW ###
# -----------------------

@method_decorator(login_required, name='dispatch')
class TaskTrackingView(TemplateView):
    template_name = 'task_tracking.html'


### TASK DELETION API ###
# -----------------------

@csrf_exempt
def delete_task(request, task_id):
    if request.method == 'DELETE':
        try:
            task = TaskLog.objects.get(log_id=task_id)
            task.delete()
            return JsonResponse({'message': f'Task {task_id} deleted successfully.'}, status=200)
        except TaskLog.DoesNotExist:
            return JsonResponse({'error': 'Task not found.'}, status=404)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

### TASK DELETION ALL ###
# -----------------------

@csrf_exempt
def delete_all_tasks(request):
    if request.method == 'DELETE':
        TaskLog.objects.all().delete()
        return JsonResponse({'message': 'All tasks deleted successfully.'}, status=200)
    return JsonResponse({'error': 'Invalid request method.'}, status=405)

### MANAGE Q AND A PAIRS ###
# -----------------------

@login_required
def manage_q_and_a(request):
    status = request.GET.get('status', '')
    search_query = request.GET.get('q', '')
    page_number = request.GET.get('page', 1)

    qa_pairs = QAPair.objects.all().order_by('qa_id')

    if status:
        qa_pairs = qa_pairs.filter(status=status)
    if search_query:
        qa_pairs = qa_pairs.filter(
            question__icontains=search_query,
        ) | qa_pairs.filter(
            answer__icontains=search_query,
        )

    paginator = Paginator(qa_pairs, 10)
    page_obj = paginator.get_page(page_number)

    context = {
        'qa_pairs': page_obj,
    }

    return render(request, 'core/manage_q_and_a.html', context)


### EDIT Q AND A PAIR ###
# -----------------------

@login_required
def edit_q_and_a(request, qa_id):
    qa_pair = get_object_or_404(QAPair, qa_id=qa_id)
    page_number = request.GET.get('page', 1)

    if request.method == 'POST':
        qa_pair.question = request.POST.get('question', qa_pair.question)
        qa_pair.answer = request.POST.get('answer', qa_pair.answer)
        qa_pair.status = request.POST.get('status', qa_pair.status)
        qa_pair.save()

        messages.success(request, "Q&A Pair updated successfully.")
        return redirect(f"{reverse('core:manage-q-and-a')}?page={page_number}")
    
    context = {
        'qa_pair': qa_pair,
        'page_number': page_number,
    }

    return render(request, 'core/edit_qa_pair.html', context)


### DELETE Q AND A PAIR ###
# -----------------------

@login_required
def delete_q_and_a(request, qa_id):
    if request.method == "POST":
        qa_pair = get_object_or_404(QAPair, qa_id=qa_id)
        qa_pair.delete()

        messages.success(request, "Q&A Pair deleted successfully.")
        return redirect('core:manage-q-and-a')
    else:
        messages.error(request, "Invalid request method.")
        return redirect('core:manage-q-and-a')
    

### CREATE Q AND A PAIR ###
# -----------------------

@login_required
def create_q_and_a(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        answer = request.POST.get('answer')
        status = request.POST.get('status', 'Pending')

        if question and answer:
            QAPair.objects.create(
                question=question,
                answer=answer,
                status=status,
            )
            messages.success(request, "Q&A Pair created successfully.")
            return redirect('core:create-q-and-a')
        else:
            messages.error(request, "Both question and answer fields are required.")
    
    return render(request, 'core/create_q_and_a.html')