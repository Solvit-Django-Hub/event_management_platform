# 🎫 Event Management Platform

A Django REST Framework backend that allows users to discover events, purchase tickets, register for events, and manage their bookings.

**Author:** Adolphe Uwayo

---

## 📖 Overview

The Event Management Platform is a REST API built with Django and Django REST Framework (DRF). It enables:

- Event organizers to create and manage events
- Users to browse, search, and filter available events
- Users to register/purchase tickets for events
- Users to view and manage their bookings
- Secure JWT-based authentication and role-based permissions

---

## 🚀 Features

### 1. Authentication

- User registration
- Login (JWT access & refresh tokens)
- Token refresh
- Logout (token blacklisting)

### 2. User Management

- Create profile
- View profile
- Update profile
- Change password

### 3. Database

- Django ORM
- SQLite (development) — easily swappable for PostgreSQL/MySQL in production
- 5+ related models (e.g. `User`, `Event`, `Category`, `Ticket`, `Booking`)

### 4. REST API

Full CRUD support where applicable:

- `GET` — list & retrieve
- `POST` — create
- `PUT` / `PATCH` — update
- `DELETE` — remove

### 5. Serializers

- Create, retrieve, update serializers
- Field-level and object-level validation
- Nested relationships (e.g. bookings include event & ticket details)

### 6. API Views

Demonstrates multiple DRF view styles:

- Function-Based Views (FBVs)
- `APIView`
- Generic Views
- Mixins
- ViewSets (with routers)

### 7. Validation

- Unique email enforcement
- Non-negative ticket price
- Valid phone number format
- Required field checks
- Date validation (e.g. event date cannot be in the past)
- Business rules (e.g. cannot book more tickets than available)

### 8. Permissions

Role-based access control:

- **Admin** — full access to all resources
- **Staff/Organizer** — manage their own events
- **Customer/User** — browse events, manage own bookings

### 9. Search & Filtering

Example endpoints:

```
GET /api/events/?search=music
GET /api/events/?category=concert
GET /api/events/?ordering=-date
```

### 10. Pagination

All list endpoints are paginated for performance.

### 11. API Documentation

Interactive API docs via Swagger/OpenAPI:

```
/api/docs/       -> Swagger UI
/api/schema/     -> Raw OpenAPI schema
```

### 12. Testing

- Model tests
- Serializer tests
- API endpoint tests
- Authentication tests
- Permission tests

---

## 🛠️ Tech Stack

- Python 3
- Django
- Django REST Framework
- Simple JWT (`djangorestframework-simplejwt`)
- drf-yasg / drf-spectacular (Swagger/OpenAPI docs)
- SQLite (default) / PostgreSQL (optional)
- django-filter (search & filtering)

---

## 📂 Project Structure

```
backend/
├── event_management_platform/   # Project settings, URLs, WSGI/ASGI
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── apps/                        # Django apps (accounts, events, tickets, bookings, etc.)
├── manage.py
├── requirements.txt
└── db.sqlite3
```

---

## ⚙️ Setup & Installation

1. **Clone the repository**

   ```bash
   git clone event_management_hub
   cd backend
   ```

2. **Create and activate a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Apply migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**

   ```bash
   python manage.py runserver
   ```

7. **Access the API**
   - API root: `http://127.0.0.1:8000/api/`
   - Swagger docs: `http://127.0.0.1:8000/api/docs/`
   - Admin panel: `http://127.0.0.1:8000/admin/`

---

## 🔑 Authentication Flow

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/auth/register/` | POST | Register a new user |
| `/api/auth/login/` | POST | Obtain JWT access & refresh tokens |
| `/api/auth/refresh/` | POST | Refresh access token |
| `/api/auth/logout/` | POST | Blacklist refresh token |

Include the access token in subsequent requests:

```
Authorization: Bearer <access_token>
```

---

## 🧪 Running Tests

```bash
python manage.py test
```

---

## 📌 Notes

This project was built as part of a Django REST Framework learning exercise, demonstrating authentication, permissions, serializers, viewsets, filtering, pagination, API documentation, and testing best practices.
