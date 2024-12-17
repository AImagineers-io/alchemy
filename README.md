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
   ```

2. **Data Processing**:

   - Upload the documents or content you want to process.
   - The app will extract and transform the content into structured data.
   - The structured data can then be pushed to cloud storage or external services for further use.

3. **Future Updates**:
   - Alchemy will support additional features such as continuous data gathering from web sources and social media for AI systems.

# ERD for Project Alchemy - Variable Descriptions

![ERD_Design](./img/Alchemy_ERD.jpg)

## 1. User
### Attributes:
- **user_id (PK)**: The primary key for identifying each user. 
  - *Usage*: Unique identifier for each user within the system.
- **username**: The name used by the user to log in.
  - *Usage*: Acts as the primary handle for the user’s profile.
- **email**: The user’s email address.
  - *Usage*: For communication and login purposes.
- **password**: The hashed password for user authentication.
  - *Usage*: Secure authentication for accessing the system.
- **role**: The role assigned to the user (e.g., Admin, Regular User).
  - *Usage*: Controls access levels and permissions within the system.
- **created_at**: Timestamp for when the user account was created.
  - *Usage*: For tracking user registration and activity timelines.
- **updated_at**: Timestamp for the last update to the user account.
  - *Usage*: Helps manage and track changes to user information.

## 2. Document
### Attributes:
- **document_id (PK)**: The primary key for identifying each document.
  - *Usage*: Unique identifier for documents uploaded by users.
- **user_id (FK)**: Foreign key linking to the user who uploaded the document.
  - *Usage*: Associates documents with the user who owns them.
- **file_name**: The name of the file uploaded.
  - *Usage*: Used for referencing and managing files within the system.
- **file_type**: The type of the file (e.g., PDF, DOCX).
  - *Usage*: Helps in determining the appropriate method for processing the file.
- **upload_date**: The date the document was uploaded.
  - *Usage*: For tracking and organizing document uploads.
- **status**: The current processing status of the document (e.g., processed, pending).
  - *Usage*: Allows monitoring and updating the state of document processing.

## 3. ProcessedData
### Attributes:
- **data_id (PK)**: The primary key for identifying processed data entries.
  - *Usage*: Unique identifier for the processed data extracted from documents.
- **document_id (FK)**: Foreign key linking to the source document.
  - *Usage*: Connects processed data back to its original document for reference.
- **structured_data (JSON/BLOB)**: The transformed and structured data extracted from the document.
  - *Usage*: Stores the data in a format suitable for training LLMs or for integration with other systems.
- **processed_date**: Timestamp indicating when the document was processed.
  - *Usage*: For tracking processing times and managing document lifecycles.
- **storage_location**: The location where the processed data is stored (e.g., Local, Voiceflow, Cloud).
  - *Usage*: Indicates where the processed data is stored or transferred for further use.

## 4. TransformationLog
### Attributes:
- **log_id (PK)**: The primary key for identifying each transformation log entry.
  - *Usage*: Unique identifier for tracking individual transformation steps applied to documents.
- **document_id (FK)**: Foreign key linking to the document being processed.
  - *Usage*: Connects transformation logs to the corresponding document for traceability.
- **transformation_step**: A description or identifier of the specific transformation applied (e.g., text extraction, data cleaning).
  - *Usage*: Details the step applied to the document during processing.
- **status**: The outcome or status of the transformation step (e.g., successful, failed).
  - *Usage*: Helps in identifying the progress and issues during data processing.
- **timestamp**: The time the transformation step occurred.
  - *Usage*: Useful for tracking and auditing the document processing workflow.

## 5. APIRequestLog
### Attributes:
- **request_id (PK)**: The primary key for identifying each API request log entry.
  - *Usage*: Unique identifier for API call logs.
- **user_id (FK)**: Foreign key linking to the user who made the API request.
  - *Usage*: Tracks which user initiated the API call for monitoring and auditing.
- **api_endpoint**: The API endpoint that was called.
  - *Usage*: Useful for identifying which service or action was requested.
- **request_timestamp**: The time the API call was made.
  - *Usage*: Provides a timestamp for tracking when each API call occurred.
- **response_status**: The status code or outcome of the API request (e.g., 200 for success, 404 for not found).
  - *Usage*: Indicates the result of the API request, useful for debugging.

# App Flowchart
This flowchart outlines the process of document processing within the Project ALCHEMY application, focusing on how users interact with the system and how documents are managed. The flow includes document upload, text extraction, user verification, and storage in the database.

![alchemyflowchar](./img/Alchemy_AppFlowChart.jpg)
---

# Version History

## V.0.1.0
- added core app, this will store all shared models.
- added dashboard app, built a basic nav screen
- fixed the admin view not detecting static css

## V.0.2.0
- Implemented login, logout, and registration views using Django's default forms within the `core` app.
- Configured URL patterns and views to redirect users to the login page when accessing the root URL.
- Set up a conditional redirect to the dashboard if a user is already logged in.
- Modified the registration process to display a success message on the login page.
- Added a logout link and displayed the logged-in user's email on the dashboard.
- Fixed the logout functionality to use a custom template and redirected correctly to the login page after logging out.
- Updated the custom user model integration and confirmed that email-only registration and login were functional.

## V0.3.0
- Created a basic document processing interface (`main.html`) with a form to accept user-uploaded files (.pdf, .docx, .txt).
- Added logic to extract text content based on file type using `docx`, `PyPDF2`, and standard text reading methods.
- Replaced file path input with file upload field and refactored text extraction functions to handle file-like objects directly.
- Integrated Django’s `login_required` decorator to ensure user authentication before processing documents.
- Added a "Browse" button to facilitate file selection, allowing users to quickly choose files for processing without manually entering the file path.
- Added handling for double-escaped characters in `clean_text` function
- Text Cleaning Function with ChatGPT: Extended the clean_text function by integrating ChatGPT API capabilities. The updated function leverages natural language instructions to perform flexible and adaptive cleaning tasks, addressing unicode escapes, backslashes, escaped quotes, and more.
- added Publication date and Source Material - This is to enhance training material and RAG retrieval

## V0.4.0
- **Feature Added:** Enhanced Q&A Generation and Review Flow
  - Implemented an updated `generate_q_and_a` function to generate Q&A pairs from document content using GPT, now with strict JSON formatting for reliable parsing.
  - Updated the `generate_q_and_a_view` to handle unstructured text as a string rather than JSON, simplifying data management.
  - Added individual review fields for each Q&A pair in `edit_q_and_a_view`, allowing users to edit questions and answers directly.
  - Enhanced error handling to provide meaningful feedback when Q&A generation fails.
  - Improved user experience by redirecting to the Q&A review page upon generation success.

## V0.5.0
- Added `chunk_text_with_context` function to split extracted text into smaller chunks with overlapping tokens for better processing.
- Integrated `spacy` for sentence-based chunking and `tiktoken` for token counting, ensuring each chunk is within the specified token limit.
- Implemented context overlap in chunking logic to maintain coherence across chunk boundaries.
- Modified `main` view to handle different file formats and check for unsupported file types with a user-friendly error message.
- Adjusted view logic to handle and save `unstructured_data` consistently as plain text across processes.
- added print logs to trace what steps the app is taking
- Fixed issue on invalid JSON format on unstructed data
- **Enhanced Login and Registration Frontend:** Updated the UI for the login and registration screens with a modern, Bootstrap-based design, providing a more consistent and visually appealing user experience.
- **Integrated Django Widget Tweaks:** Added the `django-widget-tweaks` library to dynamically style form fields with Bootstrap classes, allowing for better control over form aesthetics and layout.

## V[0.7.0] - 2024-12-03
### Added
- Initial implementation of **Task Tracking** functionality:
  - Built an API endpoint (`/tasks/`) to fetch user-specific tasks using the `TaskLog` model.
  - Created a frontend view (`task_tracking.html`) to display real-time task progress using a progress bar.
  - Implemented `fetchUserTasks` in `theme.js` to fetch and display tasks dynamically on the Task Tracking page.
  - Introduced periodic polling with `setInterval` to update the task progress every 5 seconds.
- Added task deletion functionality:
  - Individual "Delete" buttons for each task in the Task Tracking view.
  - Backend API (`/tasks/<task_id>/delete/`) to handle individual task deletions.
  - JavaScript integration to call the delete API dynamically.
  - "Delete All" button to remove all tasks at once with a single click.
- Enhanced task logging:
  - Added `log_messages` to track detailed logs of task events (e.g., progress updates, task-specific messages).
  - Displayed logs dynamically under each task in the Task Tracking view.
- Updated **Document Upload** logic to integrate with Celery:
  - Triggered the `process_document` task asynchronously upon file upload.
  - Tracked the task progress and results using the `TaskLog` model.

### Fixed
- Resolved an issue where `theme.js` was not properly loaded into templates.
- Addressed the CSRF token error in delete requests by implementing a `getCookie` function.

### Changed
- Refactored frontend and backend logic to improve code readability and maintainability:
  - Moved reusable helper functions to `utils.js` and backend utility modules.
  - Optimized polling mechanism to minimize server load while maintaining real-time updates.

## V[0.8.0] - 2024-12-03
### **Added**
- **Enhanced Document Processing Logic:**
  - Integrated asynchronous Celery tasks for text cleaning and Q&A generation.
  - Handled multiple file types (`PDF`, `DOCX`, `TXT`) for text extraction.
  - Implemented dynamic progress tracking using the `TaskLog` model with real-time updates.
  - Added a cap on progress tracking to show a maximum of **90%** until task completion.

- **Q&A Pair Generation:**
  - Designed and implemented the `QAPair` model to store generated Q&A pairs with fields like:
    - `document`, `question`, `answer`, `source_name`, and `publication_date`.
  - Integrated `bulk_create` for efficient database persistence of Q&A pairs.

- **Task Logging Enhancements:**
  - Added `log_messages` field to the `TaskLog` model to record detailed step-by-step progress.
  - Updated task tracking frontend to dynamically display logs alongside task progress bars.

- **Frontend Improvements:**
  - Enhanced task tracking page to include:
    - Individual "Delete" buttons for each task.
    - A "Delete All" button for clearing all tasks at once.
  - Integrated `theme.js` for:
    - Periodic polling of the `/tasks/` API using `fetchUserTasks`.
    - Dynamic updates to task progress and logs.
    - Handling delete functionality through a dedicated API.

### **Fixed**
- **Serialization Issue:**
  - Resolved `InMemoryUploadedFile` JSON serialization error by moving text extraction logic out of Celery.
  
- **Bug in Q&A Saving Logic:**
  - Fixed `bulk_create` usage for `QAPair` model.
  - Added validation to ensure proper document linkage during Q&A generation.

- **JavaScript Integration:**
  - Corrected missing `fetchUserTasks` invocation on page load.
  - Fixed `getCookie` function for CSRF token handling.

- **Progress Calculation:**
  - Updated logic to dynamically calculate task progress without exceeding limits.

### **Future Considerations**
- Implement WebSocket support for instant updates in the Task Tracking view.
- Optimize the chunking and cleaning logic for handling larger documents.
- Add indexing to database tables for improved query performance.

---

### **Current Status**
- The application successfully processes documents, generates Q&A pairs, and tracks task progress dynamically with user-facing updates.

# Pending
- q and a pairs i think is not yet saved in a table... create new table for the q and a pairs (not json)
- i think the logic should be... q and a pair chunk created... save in db... then move to another one.
- the editing will happen later on... using the CRUD logic we'll create later.
- we probably need to demolish the document data table and instead use q and a pair db.
- documents needs to be saved as a table so that processing q and a will be entirely separate and the user can do this at a later time.
- then work on the main dashboard to show the metrics
- introduce redis and clelery
- sort out the source code... clean it up and make sure we are ready for expanding the app
- work on a CRUD system for q and a pairs
- work on a different document format - excel, xls, csv

# Journal

# Project Alchemy: Current Status and Next Steps

## **Current Status**
You are working on making Project Alchemy's dashboard more user-friendly by:
1. **Tracking Background Tasks**: Using Celery to process tasks asynchronously and showing task progress on the frontend.
2. **Toast Notifications**: Implementing a system to notify users of task updates in real time.
3. **Task Logs**: Adding a backend logging system to record task events and integrating it with the toast system.

---

## **Progress So Far**

### **Backend**
- Created a `LogEntry` model to store task logs (user messages for toast notifications).
- Tasks in `tasks.py` now log key events (e.g., "Task started," "Task 50% complete," "Task completed").

### **API**
- Created a `/logs/recent/` API endpoint to fetch recent log entries for the authenticated user.

### **Frontend**
- Built a basic toast notification system with:
  - **CSS for styling toasts**.
  - **JavaScript logic** to fetch logs from the API and display toasts dynamically.
- Discussed polling and real-time updates using WebSockets or Django Channels for future improvements.

---
## **What’s Next?**

Manage Q & A Pairs screen
- display table showing all pairs - with edit and delete buttons
- filter function
- search function
- add reviewed tick box - this means adding a reviewed field on QApairs model
- add category on the table - this means adding a category - need to build this in the logic of QA pair generation - maybe a separate logic or could be embedded
- pagination also
- need a way to filter un-reviewed questions (maybe a tickbox at the top)

checklist:
Done - Create a new view under the core app for managing Q&A pairs.
Done - Build the HTML template with a table, filters, and pagination.
Add "Edit" and "Delete" buttons for each Q&A pair.
Link "Add New Q&A Pair" to a form or separate page.
Update the QAPair model to include a status field (Pending, Reviewed, Edited).
Populate sample data for testing purposes.
Add logic to filter Q&A pairs by status and search query.
Implement pagination for large datasets.
Build a form to edit existing Q&A pairs.
Add logic to delete Q&A pairs with a confirmation prompt.
Create a form to add new Q&A pairs.
Display success/error messages for add, edit, and delete actions.
Test filtering, search, and pagination functionality.
Test adding, editing, and deleting Q&A pairs.

- Build CRUD, for reviewing Q and A Pairs --*current WIP*--
- Build metrics and graphs in the dashboard
- Add control panel function - send data to voiceflow knowledgebase end point
- Add control panel - export data through different formats (xls, csv, txt)

### **Further Enhancements**
- Implement WebSockets (optional) for real-time updates instead of polling.
- Consider adding a "View All Tasks" section or page for comprehensive task history.
- build a toast notifcation script to the dashboard
- test toast system
