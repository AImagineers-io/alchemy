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

def extract_text_from_pdf(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    text = " ".join([page.extract_text() for page in reader.pages])
    return text

def extract_text_from_docx(file):
    doc = DocxDocument(file)
    return "/n".join([para.text for para in doc.paragraphs])

def extract_text_from_txt(file):
    return file.read().decode('utf-8')

### Views ###


@login_required(login_url='core:login')
def main(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('file')

        if not uploaded_file:
            return render(request, 'document/main.html', {'message': 'No file uploaded'})
        
        try:
            user =  request.user

            file_name = uploaded_file.name
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
                extracted_text = extract_text_from_pdf(uploaded_file)
            elif file_extension == '.docx':
                extracted_text = extract_text_from_docx(uploaded_file)
            elif file_extension == '.txt':
                extracted_text = extract_text_from_txt(uploaded_file)
            else:
                return render(request, 'document/main.html', {"message": "Unsupported file format."})
            
            json_data = json.dumps({"content": extracted_text})

            new_document.unstructured_data = json_data
            new_document.status = 'text extracted'
            new_document.save()

            return render(request, "document/main.html", {
                "message": "File uploaded successfully.",
            })
        
        except Exception as e:
            return render(request, 'document/main.html', {"message": f"An error occurred: {str(e)}"})
    else:
        return render(request, 'document/main.html')

