# CallerID
 
## Requirements

- Python 3.12+
- Django 5.1+
- Django Rest Framework 3.15+
- Simple JWT 5.3+

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/prasad0819/CallerID.git
cd CallerID
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations & Seed Data

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata caller_id/api/fixtures/dummy.json
```

### 5. Start the Development Server

```bash
python manage.py runserver
```

Test the API using Postman at http://127.0.0.1:8000/api/_endpoint_

## Schema

- User
    - Name
    - Phone Number
    - Email Address (optional)
    - Contacts (0 to many)

- Contact
    - Name
    - Phone number
    - Owner (User)

- Spam Report
    - Phone number
    - Reported By (User)

## APIs

### Registration & Authentication

- POST /api/register
    - full_name (string)
    - phone_number (string)
    - email (string, optional)
    - password (string, write-only)

- POST /api/token
    - phone_number (string)
    - password (string)

- POST /api/token/refresh
    - refresh (string)

### CallerID

- POST /api/add-contact
    - name (string)
    - phone_number (string)
    - owner (Current User)

- POST /api/report-spam
    - phone_number (string)
    - reported_by (Current User)

- GET /api/search-by-name
    - full_name (string)

- GET /api/search-by-phone-number
    - phone_number (string)


