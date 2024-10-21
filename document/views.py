from django.shortcuts import render, get_object_or_404
import os
import json
from docx import Document as DocxDocument
import  PyPDF2
from django.http import JsonResponse
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
    return "\n".join([para.text for para in doc.paragraphs])

def extract_text_from_txt(file):
    return file.read().decode('utf-8')

### Views ###

@login_required(login_url='core:login')
def main(request):
    if request.method == 'POST':
        if "file" in request.FILES:
            uploaded_file = request.FILES.get('file')

            if not uploaded_file:
                return render(request, 'document/main.html', {'message': 'No file uploaded'})
            
            try:
                user = request.user

                file_name = uploaded_file.name
                file_extension = os.path.splitext(file_name)[1].lower()
                file_type = file_extension.replace('.', '').upper()

                new_document = Document.objects.create(
                    user=user,
                    file_name=file_name,
                    file_type=file_type,
                    status='pending'
                )

                extracted_text = ""
                if file_extension == '.pdf':
                    extracted_text = extract_text_from_pdf(uploaded_file)
                elif file_extension == '.docx':
                    extracted_text = extract_text_from_docx(uploaded_file)
                elif file_extension == '.txt':
                    extracted_text = extract_text_from_txt(uploaded_file)
                else:
                    return render(request, 'document/main.html', {'message': 'Unsupported file format'})
                
                json_data = json.dumps({"content": extracted_text})

                new_document.unstructured_data = json_data
                new_document.status = 'extracted'
                new_document.save()

                return render(request, "document/main.html", {
                    "message": "File uploaded successfully",
                    "extracted_text": extracted_text,
                    "document_id": new_document.document_id,
                })
            
            except Exception as e:
                return render(request, 'document/main.html', {"message": f"An error occurred: {str(e)}"})
            
        elif "save" in request.POST:
            try:
                edited_text = request.POST.get("extracted_text", "")
                document_id = request.POST.get("document_id")

                document = get_object_or_404(Document, document_id=document_id)
                document.unstructured_data = json.dumps({"content": edited_text})
                document.status = 'reviewed'
                document.save()

                return render(request, "document/main.html", {
                    "message": "Text saved successfully",
                    "extracted_text": edited_text,
                    "document_id": document_id,
                })
            except Exception as e:
                return render(request, 'document/main.html', {"message": f"An error occurred: {str(e)}"})
    else:
        return render(request, 'document/main.html')