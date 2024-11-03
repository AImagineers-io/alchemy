from django.shortcuts import render, get_object_or_404, redirect
import os
import json
from docx import Document as DocxDocument
import  PyPDF2
from django.http import JsonResponse
from core.models import Document, ProcessedData
from django.contrib.auth.decorators import login_required
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

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

def clean_text_with_GPT(text):
    prompt = f"""
    Clean the following text by:
    - Decoding any unicode escapes (such as \\n, \\t, and \\r) to their corresponding characters.
    - Removing unnecessary backlashes.
    - Replacing escaped quotes (\\\" and \\\') with regular quotes.
    - Stripping out any unicode sequences (e.g, \\uXXXX).
    
    Here is the text:
    {text}
    """
    clean_completions = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {
                "role": "system",
                "content": "Ypu are a text cleaner, you will receive an unfiltered text which you need to clean using the user instructions. Do not explain the text just share the output"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return clean_completions.choices[0].message.content

def generate_q_and_a(text, source_name, publication_date):
    prompt = f"""
    Generate as many Q&A pairs as possible from the following content. Format each pair as JSON object with fields 'question', 'answer', 'source_name', and 'publication_date'. Here is the content:
    {text}
    """

    response_format = {
        "type": "json_schema",
        "json_schema": {
            "name": "qa_schema",
            "schema": {
                "type": "object",
                "properties": {
                    "qa_pairs": { 
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "question": {
                                    "description": "The question generated from the input content",
                                    "type": "string"
                                },
                                "answer": {
                                    "description": "The answer generated from the input content",
                                    "type": "string"
                                },
                                "source_name": {
                                    "description": "The name of the source for the question and answer",
                                    "type": "string",
                                    "default": source_name
                                },
                                "publication_date": {
                                    "description": "The publication date of the source",
                                    "type": "string",
                                    "default": publication_date
                                }
                            },
                            "required": ["question", "answer", "source_name", "publication_date"],
                            "additionalProperties": False
                        }
                    }
                },
                "required": ["qa_pairs"],
                "additionalProperties": False
            }
        }
    }


    try:
        qa_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a Q&A generator, Generate questions and answers as per user's input. Strictly in JSON format according to the schema."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format=response_format
        )

        qa_content = json.loads(qa_response.choices[0].message.content)

        qa_pairs = qa_content['qa_pairs']

        return qa_pairs
    
    except json.JSONDecodeError as e:
        print("Error decoding JSON response:", str(e))
        raise ValueError("Failed to decode Q&A pairs as JSON")

    except Exception as e:
        print("Error during Q&A generation:", str(e))
        raise ValueError("Failed to generate Q&A pairs")

### Views

@login_required(login_url='core:login')
def main(request):
    if request.method == 'POST':
        source_material_name = request.POST.get('source')
        publication_date = request.POST.get('publication_date')
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
                    source_name=source_material_name,
                    publication_date=publication_date,
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
                
                cleaned_text = clean_text_with_GPT(extracted_text)

                new_document.unstructured_data = cleaned_text
                new_document.status = 'extracted'
                new_document.save()

                return render(request, "document/main.html", {
                    "message": "File uploaded successfully",
                    "extracted_text": extracted_text,
                    "publication_date": publication_date,
                    "source_name": source_material_name,
                    "document_id": new_document.document_id,
                })
            
            except Exception as e:
                return render(request, 'document/main.html', {"message": f"An error occurred: {str(e)}"})
            
        elif "save" in request.POST:
            try:
                edited_text = request.POST.get("extracted_text", "")
                document_id = request.POST.get("document_id")
                publication_date = request.POST.get("publication_date")
                source_material_name = request.POST.get("source_name")

                document = get_object_or_404(Document, document_id=document_id)
                document.unstructured_data = edited_text
                document.publication_date = publication_date
                document.source_name = source_material_name
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

@login_required(login_url='core:login')
def generate_q_and_a_view(request, document_id):
    document = get_object_or_404(Document, document_id=document_id)
    processed_data, created = ProcessedData.objects.get_or_create(document=document)

    unstructured_data = document.unstructured_data

    if request.method == "POST":
        q_and_a_pairs = generate_q_and_a(unstructured_data, document.source_name, document.publication_date)

        processed_data.structured_data = q_and_a_pairs
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
