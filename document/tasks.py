from celery import shared_task
from core.models import TaskLog, Document, User, QAPair
from document.utils import *
import time

openai_model_generic = "gpt-4o-mini"

@shared_task(bind=True)

def process_document(self, document_id, user_id, extracted_text, source_name, publication_date):
    user = User.objects.get(user_id=user_id)

    task_log = TaskLog.objects.create(
        user=user,
        task_name=f"{document_id}",
        status="IN_PROGRESS",
        progress=0,
        log_messages="Task started...\n",
    )
    try:
        task_log.log_messages += f"Extracted text length: {len(extracted_text)}\n"
        task_log.log_messages += "Chunking text...\n"
        task_log.progress = 10
        task_log.save()

        start_time_chunking = time.time()
        chunks = chunk_text_with_context(extracted_text, model=openai_model_generic)
        end_time_chunking = time.time()

        task_log.log_messages += f"Chunking text completed in {end_time_chunking - start_time_chunking:.2f} seconds.\n"
        task_log.log_messages += f"Cleaning text with GPT...\n"
        task_log.save()

        cleaned_chunks = []
        start_time_clean_GPT = time.time()

        # revisit this later, we might add try-except block or timeout to handle large files
        for i, chunk in enumerate(chunks, start=1):
            cleaned_chunk = clean_text_with_GPT(chunk, model=openai_model_generic)
            cleaned_chunks.append(cleaned_chunk)
            task_log.progress = min(50, 25 + int((i / len(chunks)) * 25))
            task_log.save()

        end_time_clean_GPT = time.time()
        task_log.log_messages += f"Cleaning text completed in {end_time_clean_GPT - start_time_clean_GPT:.2f} seconds.\n"
        task_log.save()

        cleaned_document = Document.objects.get(document_id=document_id)
        cleaned_document.cleaned_data = json.dumps(cleaned_chunks)
        cleaned_document.status = 'extracted'
        cleaned_document.save()

        task_log.log_messages += "Completed Cleaning Extracted Text.\n"
        task_log.save()

        all_q_and_a_pairs = []
        window = 1

        MAX_PROGRESS = 90

        start_time_generateQA = time.time()
        for i, chunk in enumerate(cleaned_chunks, start=1):
            context_chunk = " ".join(cleaned_chunks[max(0, i - window): i])
            q_and_a_pairs = generate_q_and_a(
                chunk, context_chunk, source_name, publication_date, model=openai_model_generic
            )
            all_q_and_a_pairs.extend(q_and_a_pairs)

            progress_increment = int((i / len(chunks)) * (MAX_PROGRESS - task_log.progress))
            task_log.progress = min(task_log.progress + progress_increment, MAX_PROGRESS)
            task_log.log_messages += f"Generated {len(q_and_a_pairs)} Q&A pairs from chunk {i+1}.\n"
            task_log.save()
        
        end_time_generateQA = time.time()
        document = Document.objects.get(document_id=document_id)

        # Save Q&A pairs to the database
        q_and_a_instances = [
            QAPair(
                document=document,
                question=pair['question'],
                answer=pair['answer'],
                source_name=pair.get('source_name', source_name),
                publication_date=pair.get('publication_date', publication_date),
            )
            for pair in all_q_and_a_pairs
        ]

        QAPair.objects.bulk_create(q_and_a_instances)

        task_log.log_messages += f"Saved {len(all_q_and_a_pairs)} Q&A pairs to the database. Completed in {end_time_clean_GPT - start_time_clean_GPT:.2f} seconds.\n"
        task_log.progress = 100
        task_log.status = "SUCCESS"
        task_log.save()
    
    except Exception as e:
        task_log.status = "FAILURE"
        task_log.error_message = str(e)
        task_log.log_messages += f"Task failed: {str(e)}\n"
        task_log.save()
        raise



# @shared_task(bind=True)
# def process_document(self, document_id, user_id):
#     document = Document.objects.get(document_id=document_id)
#     user = User.objects.get(user_id=user_id)

#     task_log = TaskLog.objects.create(
#         user=user,
#         task_name=f"Processing Document: {document.file_name}",
#         status="IN_PROGRESS",
#         progress=0,
#         log_messages="Task started... initiating hyperdrive.\n"
#     )

#     try:
#         # Just a simulation for now
#         time.sleep(5)
#         task_log.progress = 0
#         task_log.log_messages += "Hyperdrive loaded with sufficient fuel.\n"
#         task_log.save()

#         i = 0;
#         while i < 10:
#             i +=1
#             time.sleep(2)
#             task_log.progress = i * 10
#             task_log.log_messages += f"Processing document {i}...{task_log.progress}%.\n"
#             task_log.save()
        
#         task_log.status = "SUCCESS"
#         task_log.result = f"Document processed successfully: {document.file_name}"
#         task_log.log_messages += "Task completed successfully.\n"
#         task_log.save()

#     except Exception as e:
#         task_log.status = "FAILURE"
#         task_log.error_message = str(e)
#         task_log.log_messages += f"Task failed: {str(e)}\n"
#         task_log.save()
#         raise
    


