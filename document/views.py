from django.shortcuts import render, get_object_or_404
import os
import json
from docx import Document as DocxDocument
import PyPDF2
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from core.models import Document, User
from django.contrib.auth.decorators import login_required


### Support Functions ###

def extract_text_from_pdf(file_path):
    text =  ""
    with open(file_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = " ".join([page.extract_text() for page in reader.pages])
    return text

def extract_text_from_docx(file_path):
    doc = DocxDocument(file_path)
    return "/n".join([para.text for para in doc.paragraphs])

def extract_text_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as txt_file:
        return txt_file.read()

### Views ###


@login_required(login_url='core:login')
def main(request):
    if request.method == 'POST':
        file_path = request.POST.get("file_path")

        if not file_path:
            return render(request, "document/main.html", {"message": "File path is required."})
        
        if not os.path.isfile(file_path):
            return render(request, "document/main.html", {"message": "File not found."})
        
        try:
            user = request.user

            file_name = os.path.basename(file_path)
            file_extension = os.path.splitext(file_name)[1].lower()
            file_type = file_extension.replace('.', '').upper()

            new_document = Document.objects.create(
                user=user,
                file_name=file_name,
                file_type=file_type,
                status='pending',
            )

            extracted_text = ""
            if file_extension == '.pdf':
                extracted_text = extract_text_from_pdf(file_path)
            elif file_extension == '.docx':
                extracted_text = extract_text_from_docx(file_path)
            elif file_extension == '.txt':
                extracted_text = extract_text_from_txt(file_path)
            else:
                return render(request, 'document/main.html', {"message": "Unsupported file format."})
            
            json_data = json.dumps({"content": extracted_text})

            new_document.unstructured_data = json_data
            new_document.status = 'captured'
            new_document.save()

            return render(request, "document/main.html", {
                "message": f"Document processed successfully with ID {new_document.document_id}."
            })
    
        except Exception as e:
            return render(request, 'document/main.html', {"message": f"An error occurred: {str(e)}"})
    
    else:
        return render(request, 'document/main.html')