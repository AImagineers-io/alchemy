from django.shortcuts import render, get_object_or_404, redirect
from docx import Document as DocxDocument
from core.models import Document, ProcessedData
from django.contrib.auth.decorators import login_required
from openai import OpenAI
from dotenv import load_dotenv
from .utils import *
from .tasks import process_document
from django.http import HttpResponse, HttpRequest

import os
import json
import  PyPDF2
import time
import datetime

load_dotenv()
client = OpenAI()
openai_model_generic = "gpt-4o-mini"



### MAIN DOCUMENT VIEW ###
def main(request):
    if request.method == 'POST':
        try:
            if "file" in request.FILES:
                uploaded_file = request.FILES.get('file')
                source_material_name = request.POST.get('source')
                publication_date = request.POST.get('publication_date')

                if not uploaded_file:
                    return render(request, 'document/main.html', {'message': 'No file uploaded'})
                
                user = request.user
                file_name = uploaded_file.name
                file_extension = os.path.splitext(file_name)[1].lower()
                file_type = file_extension.replace('.', '').upper()

                new_document = Document.objects.create(
                    user=user,
                    file_name=file_name,
                    file_type=file_type,
                    source_name=source_material_name,
                    publication_date=publication_date,
                    status='pending'
                )

                process_document.delay(document_id=new_document.document_id, user_id=user.user_id)

                return render(request, 'document/main.html', {
                    "message": "File upload successfully. Processing has started.",
                    "document_id": new_document.document_id,
                })
        except Exception as e:
            print(f"Error while processing file: {str(e)}")
            return render(request, 'document/main.html', {"message": f"Error occurred while processing file: {str(e)}"})
    else:
        return render(request, 'document/main.html')

# @login_required(login_url='core:login')
# def main(request):
#     if request.method == 'POST':
#         print("POST request received.. Starting functions...")
#         source_material_name = request.POST.get('source')
#         print("Source material name:", source_material_name)
#         publication_date = request.POST.get('publication_date')
#         print("Publication date:", publication_date)

#         if isinstance(publication_date, datetime.date):
#             publication_date = publication_date.isoformat()

#         if "file" in request.FILES:
#             uploaded_file = request.FILES.get('file')
#             print(uploaded_file)

#             if not uploaded_file:
#                 return render(request, 'document/main.html', {'message': 'No file uploaded'})
            
#             try:
#                 user = request.user
#                 print("User:", user)

#                 file_namile.name
#                 file_extension = e = uploaded_fos.path.splitext(file_name)[1].lower()
#                 file_type = file_extension.replace('.', '').upper()

#                 new_document = Document.objects.create(
#                     user=user,
#                     file_name=file_name,
#                     file_type=file_type,
#                     source_name=source_material_name,
#                     publication_date=publication_date,
#                     status='pending'
#                 )
#                 print("New document created:", new_document)

#                 extracted_text = ""
#                 if file_extension == '.pdf':
#                     extracted_text = extract_text_from_pdf(uploaded_file)
#                 elif file_extension == '.docx':
#                     extracted_text = extract_text_from_docx(uploaded_file)
#                 elif file_extension == '.txt':
#                     extracted_text = extract_text_from_txt(uploaded_file)
#                 else:
#                     return render(request, 'document/main.html', {'message': 'Unsupported file format'})
                
#                 print("Extracted text length: ", len(extracted_text))
#                 print("chunking text...")
                
#                 chunks = chunk_text_with_context(extracted_text, model=openai_model_generic)

#                 print("Cleaning text with GPT...")
#                 cleaned_chunks = []
#                 for i, chunk in enumerate(chunks, start=1):
#                     start_time = time.time()
#                     cleaned_chunk = clean_text_with_GPT(chunk, model=openai_model_generic)
#                     cleaned_chunks.append(cleaned_chunk)
#                     end_time = time.time()

#                     duration = end_time - start_time
#                     print(f"Chunk {i}: completed in {duration:.2f} seconds")

#                 new_document.unstructured_data = json.dumps(cleaned_chunks)
#                 new_document.status = 'extracted'
#                 new_document.save()

#                 return render(request, 'document/main.html', {
#                     "message": "File uploaded successfully",
#                     "extracted_text": new_document.unstructured_data,
#                     "publication_date": publication_date,
#                     "source_name": source_material_name,
#                     "document_id": new_document.document_id,
#                 })
            
#             except Exception as e:
#                 print(f"Error while processing file: {str(e)}")
#                 return render(request, 'document/main.html', {"message": f"Error occurred while processing file: {str(e)}"})
        
#         elif "save" in request.POST:
#             try:
#                 edited_text = request.POST.get("extracted_text", "")
#                 document_id = request.POST.get("document_id")
#                 publication_date = request.POST.get("publication_date")

#                 if isinstance(publication_date, datetime.date):
#                     publication_date = publication_date.isoformat()

#                 source_material_name = request.POST.get("source_name")

#                 document = get_object_or_404(Document, document_id=document_id)
#                 document.unstructured_data = edited_text.replace("\r", "").replace("\n", " ")
#                 document.publication_date = publication_date
#                 document.source_name = source_material_name
#                 document.status = 'reviewed'
#                 document.save()

#                 return render(request, "document/main.html", {
#                     "message": "Text saved successfully",
#                     "extracted_text": edited_text,
#                     "document_id": document_id,
#                 })
#             except Exception as e:
#                 return render(request, 'document/main.html', {"message": f"An error occurred: {str(e)}"})
#     else:
#         return render(request, 'document/main.html')

            
@login_required(login_url='core:login')
def generate_q_and_a_view(request, document_id):
    print("Entered Generate Q and A View...")
    document = get_object_or_404(Document, document_id=document_id)
    processed_data, created = ProcessedData.objects.get_or_create(document=document)

    cleaned_chunks = document.unstructured_data.split(". ")

    if request.method == "POST":
        all_q_and_a_pairs = []
        window = 1

        for i, chunk in enumerate(cleaned_chunks):
            start_time = time.time()
            context_chunk = " ".join(cleaned_chunks[max(0, i - window): i])

            q_and_a_pairs = generate_q_and_a(chunk, context_chunk, document.source_name, document.publication_date, model=openai_model_generic)

            all_q_and_a_pairs.extend(q_and_a_pairs)
            end_time = time.time()
            duration = end_time - start_time
            print(f"Generated Q&A pairs for Chunk {i} in {duration:2f} seconds.")

        processed_data.structured_data = all_q_and_a_pairs
        processed_data.save()

        return redirect('document:edit-q-and-a', document_id=document_id)
    
    return render(request, 'document/generate_q_and_a.html', {
        "document": document,
        })

@login_required(login_url='core:login')
def edit_q_and_a_view(request, document_id):
    document = get_object_or_404(Document, document_id=document_id)
    processed_data = get_object_or_404(ProcessedData, document=document)

    q_and_a_pairs = processed_data.structured_data

    if request.method == "POST":
        updated_pairs = []
        for i, pair in enumerate(q_and_a_pairs):
            question = request.POST.get(f"question_{i}")
            answer = request.POST.get(f"answer_{i}")
            if question and answer:
                updated_pairs.append({
                    "question": question,
                    "answer": answer,
                    "source_name": pair['source_name'],
                    "publication_date": pair['publication_date']
                })
    
        processed_data.structured_data = updated_pairs
        processed_data.save()
        return redirect('document:edit-q-and-a', document_id=document_id)
    
    return render(request, 'document/edit_q_and_a.html', {
        "document": document,
        "q_and_a_pairs": q_and_a_pairs,
    })