from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils.timezone import now, timedelta
from core.models import QAPair

@login_required
def dashboard(request):
    # Stats
    total_qas = QAPair.objects.count()
    pending_qas = QAPair.objects.filter(status='Pending').count()
    reviewed_qas = QAPair.objects.filter(status='Reviewed').count()

    reviewed_percentage = (reviewed_qas / total_qas * 100) if total_qas > 0 else 0

    last_30_days = now() - timedelta(days=30)
    uploads_per_day = (
        QAPair.objects.filter(created_at__gte=last_30_days)
        .annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(total=Count('qa_id'))
        .order_by('day')
    )

    chart_data = {str(entry['day']): entry['total'] for entry in uploads_per_day}

    context = {
        'user_email': request.user.email,
        'total_qas': total_qas,
        'pending_qas': pending_qas,
        'reviewed_qas': reviewed_qas,
        'reviewed_percentage': round(reviewed_percentage, 2),
        'chart_data': chart_data,
        }
    return render(request, 'dashboard/dashboard.html', context)