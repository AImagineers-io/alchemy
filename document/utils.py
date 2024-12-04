import tiktoken
import time
import spacy
import PyPDF2
import datetime
import json

from openai import OpenAI
from dotenv import load_dotenv
from docx import Document as DocxDocument

load_dotenv()
client = OpenAI()
nlp = spacy.load("en_core_web_sm")

### CHUNK TEXT WITH CONTEXT ###
def chunk_text_with_context(text, model, max_tokens=1500, overlap=200):
    start_time = time.time()
    encoding = tiktoken.encoding_for_model(model)
    chunks = []
    current_chunk = []
    current_token_count = 0

    doc = nlp(text)
    sentences = [sent.text for sent in doc.sents]

    for sentence in sentences:
        token_count = len(encoding.encode(sentence))

        if current_token_count + token_count > max_tokens:
            chunks.append(" ".join(current_chunk))

            trimmed_chunk = []
            trimmed_token_count = 0

            for sent in reversed(current_chunk):
                sentence_token_count = len(encoding.encode(sent))
                if trimmed_token_count + sentence_token_count <= overlap:
                    trimmed_chunk.insert(0, sent)
                    trimmed_token_count += sentence_token_count
                else:
                    break

            current_chunk = trimmed_chunk
            current_token_count = trimmed_token_count

        current_chunk.append(sentence)
        current_token_count += token_count

        print(f"chunks: {len(chunks)}, current_token_count: {current_token_count}")

    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    end_time = time.time()
    duration = end_time - start_time
        
    print(f"Chunk logic completed in {duration:.2f} seconds,  Number of chunks: ", len(chunks))
    return chunks

### EXTRACT TEXT FROM FILES ###
def extract_text_from_pdf(file):
    text = ""
    reader = PyPDF2.PdfReader(file)
    text = " ".join([page.extract_text() for page in reader.pages])
    return text

### EXTRACT TEXT FROM DOCX FILES ###
def extract_text_from_docx(file):
    doc = DocxDocument(file)
    return "\n".join([para.text for para in doc.paragraphs])

### EXTRACT TEXT FROM TXT FILES ###
def extract_text_from_txt(file):
    return file.read().decode('utf-8')

### CLEAN TEXT WITH GPT ###
def clean_text_with_GPT(text, model):
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
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a text cleaner, you will receive an unfiltered text which you need to clean using the user instructions. Do not explain the text just share the output"
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return clean_completions.choices[0].message.content

### GENERATE Q AND A FUNCTION ###
def generate_q_and_a(chunk, context, source_name, publication_date, model):

    if isinstance(publication_date, datetime.date):
        publication_date = publication_date.isoformat()

    prompt = f"""
    Based on the following content, generate as many Q&A pairs as possible. Use both the main content and context to maintain coherence. Format each pair as a JSON object with fields 'question', 'answer', 'source_name', and 'publication_date'. 
    
    Context:
    {context}

    Main Content:
    {chunk}

    Source Name:
    {source_name}

    Publication Date:
    {publication_date}
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
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a Q&A generator. Generate questions and answers in JSON format according to the schema using the content and context provided."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            response_format=response_format,
        )

        qa_content = json.loads(qa_response.choices[0].message.content)
        qa_pairs = qa_content["qa_pairs"]
        return qa_pairs
    
    except json.JSONDecodeError as e:
        print("Error decoding JSON response:", str(e))
        raise ValueError("Failed to decode Q&A pairs as JSON")
    
    except Exception as e:
        print("Error during Q&A generation:", str(e))
        raise ValueError("Failed to generate Q&A pairs")
    