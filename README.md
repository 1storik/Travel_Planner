# Travel Planner API

Travel Planner is a Django REST API for managing travel projects and the places a traveller wants to visit. Places are validated against the Art Institute of Chicago API before they are stored locally.

This project covers the core assessment requirements:

- create, list, retrieve, update, and delete travel projects
- create a project together with places in one request
- add places to an existing project
- update place notes
- mark places as visited
- expose OpenAPI and Swagger documentation
- enforce project and place validation rules

## Tech Stack

- Python 3.12
- Django 6
- Django REST Framework
- drf-spectacular for OpenAPI/Swagger
- SQLite
- `requests` for third-party API validation

## Project Structure

```text
Travel_Planner/
├── Travel_Planner/        # Django project settings and root URLs
├── trips/                 # Travel project/place models, serializers, views
├── db.sqlite3             # SQLite database
├── manage.py
├── requirements.txt
└── README.md
```

## Features

### Validation rules

- A project must contain at least 1 place on creation
- A project cannot contain more than 10 places
- The same external Art Institute artwork cannot be added twice to the same project
- A place must exist in the Art Institute of Chicago API before it is saved
- A project cannot be deleted if any place in it has already been visited

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/1storik/Travel_Planner.git
cd Travel_Planner
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Start the server

```bash
python manage.py runserver
```

The API will be available at:

- `http://127.0.0.1:8000/api/`
- Swagger UI: `http://127.0.0.1:8000/api/docs/`
- OpenAPI schema: `http://127.0.0.1:8000/api/schema/`

## Environment Variables

No custom environment variables are required in the current implementation.

## API Documentation

Swagger/OpenAPI is included and can be used instead of a Postman collection:

- Swagger UI: <http://127.0.0.1:8000/api/docs/>
- OpenAPI schema: <http://127.0.0.1:8000/api/schema/>

## Endpoints

Base path: `/api`

### Projects

- `GET /projects/` - list projects
- `POST /projects/` - create a project with places
- `GET /projects/{id}/` - get a single project
- `PUT /projects/{id}/` - update project fields
- `PATCH /projects/{id}/` - partially update project fields
- `DELETE /projects/{id}/` - delete project if no place is visited

### Places

- `GET /projects/{project_id}/places/` - list places for a project
- `POST /projects/{project_id}/places/` - add a place to a project
- `GET /projects/{project_id}/places/{place_id}/` - get one place
- `PUT /projects/{project_id}/places/{place_id}/` - update `notes` and `visited`
- `PATCH /projects/{project_id}/places/{place_id}/` - partially update `notes` and `visited`

## Example Requests

### Create a project with places

```bash
curl -X POST http://127.0.0.1:8000/api/projects/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Chicago Art Weekend",
    "description": "Shortlist of artworks to see",
    "start_date": "2026-05-01",
    "places": [
      {
        "external_id": 129884,
        "notes": "Start here"
      },
      {
        "external_id": 111628,
        "notes": "Check gallery schedule"
      }
    ]
  }'
```

### Add a place to an existing project

```bash
curl -X POST http://127.0.0.1:8000/api/projects/1/places/ \
  -H "Content-Type: application/json" \
  -d '{
    "external_id": 16568,
    "notes": "Look up nearby exhibits too"
  }'
```

### Update notes or mark a place as visited

```bash
curl -X PATCH http://127.0.0.1:8000/api/projects/1/places/2/ \
  -H "Content-Type: application/json" \
  -d '{
    "notes": "Visited in the afternoon",
    "visited": true
  }'
```

### List all projects

```bash
curl http://127.0.0.1:8000/api/projects/
```