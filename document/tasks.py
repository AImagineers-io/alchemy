from celery import shared_task
from core.models import TaskLog, Document, User
import time

@shared_task(bind=True)
def process_document(self, document_id, user_id):
    document = Document.objects.get(document_id=document_id)
    user = User.objects.get(user_id=user_id)

    task_log = TaskLog.objects.create(
        user=user,
        task_name=f"Processing Document: {document.file_name}",
        status="IN_PROGRESS",
        progress=0,
        log_messages="Task started... initiating hyperdrive.\n"
    )

    try:
        # Just a simulation for now
        time.sleep(5)
        task_log.progress = 0
        task_log.log_messages += "Hyperdrive loaded with sufficient fuel.\n"
        task_log.save()

        i = 0;
        while i < 10:
            i +=1
            time.sleep(2)
            task_log.progress = i * 10
            task_log.log_messages += f"Processing document {i}...{task_log.progress}%.\n"
            task_log.save()
        
        task_log.status = "SUCCESS"
        task_log.result = f"Document processed successfully: {document.file_name}"
        task_log.log_messages += "Task completed successfully.\n"
        task_log.save()

    except Exception as e:
        task_log.status = "FAILURE"
        task_log.error_message = str(e)
        task_log.log_messages += f"Task failed: {str(e)}\n"
        task_log.save()
        raise
    


