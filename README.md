# FastAPI Task Management API

A modern, RESTful task management API built with FastAPI, Pydantic, and SQLModel. This project demonstrates best practices for building scalable Python web APIs with comprehensive data validation, database operations, and clean code architecture.

## Features

- **Full CRUD Operations** - Create, Read, Update, Delete tasks
- **Data Validation** - Comprehensive input validation using Pydantic
- **Database Integration** - SQLModel/SQLAlchemy with SQLite
- **RESTful API Design** - Proper HTTP methods and status codes
- **Pagination Support** - Skip/limit query parameters
- **Filtering** - Filter tasks by status and priority
- **Auto-generated Documentation** - OpenAPI/Swagger UI
- **Error Handling** - Proper error responses with meaningful messages

## Tech Stack

- **FastAPI** - Modern, fast web framework for building APIs
- **Pydantic** - Data validation and serialization
- **SQLModel** - ORM for database operations (built on SQLAlchemy)
- **SQLite** - Lightweight database (easily replaceable with PostgreSQL/MySQL)
- **Uvicorn** - ASGI server for running the application

## Project Structure

```
├── main.py          # FastAPI application and routes
├── models.py        # Pydantic models and database schema
├── database.py      # Database configuration and session management
├── crud.py          # Database operations (CRUD functions)
├── requirements.txt # Python dependencies
└── README.md        # This file
```

## Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)

### Setup

1. **Clone or download the project files**

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**

   ```bash
   python main.py
   ```

   Or using uvicorn directly:

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

4. **Access the API**
   - API Base URL: http://localhost:8000
   - Interactive Documentation: http://localhost:8000/docs
   - Alternative Documentation: http://localhost:8000/redoc

## API Documentation

### Base URL

```
http://localhost:8000
```

### Endpoints

#### Root Endpoint

- **GET /** - Return API information and available endpoints

#### Health Check

- **GET /health** - Return API health status

#### Task Management

##### Create Task

- **POST /tasks**
- **Status Code:** 201 (Created)
- **Request Body:**
  ```json
  {
  	"title": "Complete project documentation",
  	"description": "Write comprehensive documentation for the new feature",
  	"status": "pending",
  	"priority": "high",
  	"due_date": "2024-01-15T18:00:00",
  	"assigned_to": "Zeina Zayed"
  }
  ```

##### List Tasks

- **GET /tasks**
- **Query Parameters:**
  - `skip` (optional): Number of tasks to skip (default: 0)
  - `limit` (optional): Maximum number of tasks to return (default: 100, max: 1000)

##### Get Task by ID

- **GET /tasks/{task_id}**
- **Status Code:** 200 (OK) or 404 (Not Found)

##### Update Task

- **PUT /tasks/{task_id}**
- **Status Code:** 200 (OK) or 404 (Not Found)
- **Request Body:** (all fields optional)
  ```json
  {
  	"title": "Updated task title",
  	"status": "in_progress",
  	"priority": "urgent"
  }
  ```

##### Delete Task

- **DELETE /tasks/{task_id}**
- **Status Code:** 200 (OK) or 404 (Not Found)

#### Filtering Endpoints

##### Get Tasks by Status

- **GET /tasks/status/{status}**
- **Valid Status Values:** `pending`, `in_progress`, `completed`, `cancelled`

##### Get Tasks by Priority

- **GET /tasks/priority/{priority}**
- **Valid Priority Values:** `low`, `medium`, `high`, `urgent`

## Data Models

### Task Status Enum

- `pending` - Task is waiting to be started
- `in_progress` - Task is currently being worked on
- `completed` - Task has been finished
- `cancelled` - Task has been cancelled

### Task Priority Enum

- `low` - Low priority task
- `medium` - Medium priority task (default)
- `high` - High priority task
- `urgent` - Urgent task requiring immediate attention

### Task Fields

| Field       | Type     | Required | Description                       |
| ----------- | -------- | -------- | --------------------------------- |
| id          | Integer  | Auto     | Unique task identifier            |
| title       | String   | Yes      | Task title (max 200 chars)        |
| description | String   | No       | Task description (max 1000 chars) |
| status      | Enum     | Yes      | Task status (default: pending)    |
| priority    | Enum     | Yes      | Task priority (default: medium)   |
| created_at  | DateTime | Auto     | Creation timestamp                |
| updated_at  | DateTime | Auto     | Last update timestamp             |
| due_date    | DateTime | No       | Task deadline                     |
| assigned_to | String   | No       | Assignee name (max 100 chars)     |

## Validation Rules

1. **Title Validation:**

   - Cannot be empty or whitespace only
   - Must be trimmed of leading/trailing spaces
   - Maximum 200 characters

2. **Due Date Validation:**

   - Must be in the future (if provided)

3. **HTTP Status Codes:**
   - 200: Successful retrieval/update
   - 201: Successful creation
   - 404: Resource not found
   - 422: Validation errors
   - 400: Other client errors

## Example API Calls

### Create a Task

```bash
curl -X POST "http://localhost:8000/tasks" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Learn FastAPI",
       "description": "Complete the FastAPI tutorial and build a sample project",
       "priority": "high",
       "due_date": "2024-01-20T18:00:00",
       "assigned_to": "Zeina Zayed"
     }'
```

### List All Tasks

```bash
curl -X GET "http://localhost:8000/tasks"
```

### Get Tasks with Pagination

```bash
curl -X GET "http://localhost:8000/tasks?skip=0&limit=10"
```

### Get Tasks by Status

```bash
curl -X GET "http://localhost:8000/tasks/status/pending"
```

### Update a Task

```bash
curl -X PUT "http://localhost:8000/tasks/1" \
     -H "Content-Type: application/json" \
     -d '{
       "status": "in_progress",
       "priority": "urgent"
     }'
```

### Delete a Task

```bash
curl -X DELETE "http://localhost:8000/tasks/1"
```

## Error Handling

The API provides comprehensive error handling with meaningful error messages:

- **404 Not Found:** When trying to access a non-existent task
- **422 Validation Error:** When request data doesn't meet validation requirements
- **400 Bad Request:** For other client-side errors

Example error response:

```json
{
	"detail": "Task not found"
}
```

## Database

The application uses SQLite as the database for simplicity. The database file (`tasks.db`) will be created automatically when you first run the application.

### Database Schema

The Task table is created with the following structure:

- Primary key with auto-increment
- Proper field constraints and relationships
- Automatic timestamp management

## Development

### Running in Development Mode

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The `--reload` flag enables auto-reload when code changes are detected.

### Accessing Documentation

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc
- **OpenAPI Schema:** http://localhost:8000/openapi.json

## Testing the API

1. **Start the server** using the instructions above
2. **Visit http://localhost:8000/docs** for interactive API documentation
3. **Use the Swagger UI** to test all endpoints directly in your browser
4. **Use curl or Postman** for programmatic testing
