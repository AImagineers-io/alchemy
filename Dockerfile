FROM python:3.12.5-slim

# Copy requirements and project files
COPY ./requirements.txt /requirements.txt
COPY . /app
WORKDIR /app

# Install dependencies
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /requirements.txt && \
    adduser --disabled-password --no-create-home django-user

ENV PATH="/py/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#Ensure the non-root user has access to the app directory
RUN chown -R django-user /app

# Use a non-root user
USER django-user

EXPOSE 8000

# Run Gunicorn with the correct path to your project
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 30 project_alchemy.wsgi:application