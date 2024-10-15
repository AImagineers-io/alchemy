# Alchemy

### Overview

**Alchemy** is a document processing application designed to transform content from multiple formats and mediums (e.g., PDFs, DOCX, web pages, etc.) into a format suitable for training large language models (LLMs). The goal is to ensure that this data is structured in a way that makes it easy to integrate with LLMs, enabling intelligent systems to access and deliver accurate, relevant information.

The app runs locally but also has the ability to:
- Push processed data to **cloud storage** or **Voiceflow** to support **retrieval-augmented generation (RAG)**.
- Connect to the internet for backend API calls to ensure seamless data handling and integration with external services.

Built using **Docker** and the **Django REST framework**, Alchemy ensures modularity, scalability, and ease of deployment, making it adaptable for various use cases, including future upgrades.

### Features

- **Content Ingestion**: Supports various file formats such as PDFs, DOCX, and potentially web pages for extracting content.
- **Data Transformation**: Processes content into structured data that can be used for training or fine-tuning LLMs.
- **Cloud Integration**: Pushes processed data to cloud storage or third-party systems such as Voiceflow for enhanced AI-driven responses.
- **Internet Connectivity**: Handles backend API calls to interact with external systems for data integration or updates.

### Future Expansion

Alchemy has the potential to evolve into a full-fledged data-gathering app, allowing it to:
- **Scrub webpages and social media** platforms to collect relevant data and continuously update its knowledge base.
- Provide automated, real-time data extraction to keep AI systems updated with the latest information from online sources.

### Technology Stack

- **Docker**: For containerized and portable deployments.
- **Django REST Framework**: Backend for API calls and handling data processing.
- **Python Libraries**: Tools for document parsing and transformation (e.g., PyPDF2, python-docx).

### Usage

1. **Local Deployment**:
   - Clone the repository and ensure Docker is installed on your system.
   - Build and run the Docker container to start the application.
   
   ```bash
   docker-compose up --build
