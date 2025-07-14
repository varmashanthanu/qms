# 🏦 Queue Management System (QMS)

A secure, scalable, and modular queue management system built with **Django**, **Django REST Framework**, **PostgreSQL
**, and **Docker**. Designed for use in **bank branches** with support for **multi-role access**, real-time ticket
updates, and dashboard APIs.

---

## 🚀 Features

- 🔐 **Role-Based Access Control**  
  Supports Admin and Staff roles with JWT authentication.

- 🧾 **Ticket Issuance via Kiosk Interface**  
  Customers can generate service tickets through kiosk endpoints (to be implemented).

- 🧑‍💼 **Service & Queue Management**  
  Admins can manage service categories, queues, and staff assignments.

- 📊 **Real-Time Dashboard API**  
  Staff dashboards display live queue states and average wait times (to be implemented).

- 🌐 **RESTful API**  
  All backend features are exposed via a secure, versioned REST API.

- 🐳 **Dockerized Development Setup**  
  Use Docker Compose for isolated development environments.

---

## 📁 Project Structure

qms/
├── qms/ # Django project root
├── users/ # User app (authentication & roles)
├── Dockerfile.dev # Dev Dockerfile
├── docker-compose.dev.yml# Dev Compose file
├── requirements.txt
├── .env
└── README.md

---

## ⚙️ Requirements

- Docker & Docker Compose
- Git
- Python 3.11+ (for local development only)

---

## 🛠️ Development Setup

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/qms.git
cd qms
```

### 2. Create the .env File

Create an `.env-dev` file in the project root with the following content:

```env-dev
POSTGRES_DB=qms_db
POSTGRES_USER=qms_user
POSTGRES_PASSWORD=qms_pass
DB_HOST=db
DB_PORT=5432
SECRET_KEY=replace-this-with-a-secret
DEBUG=1
```

### 3. Build and Run with Docker Compose

```bash
docker-compose -f docker-compose.dev.yml build
docker-compose -f docker-compose.dev.yml up -d
```

### 4. Initialize the Database and Project (db migrations + superuser)

```bash
docker-compose -f docker-compose.dev.yml exec web python manage.py migrate
docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser  # Follow prompts to create an admin user
```

Access the admin interface at `http://localhost:8000/admin` with the superuser credentials you created.
Health check the API at `http://localhost:8000/api/v1/health`.

## 📡 API Endpoints

Access the API documentation at `http://localhost:8000/api/v1/docs` (Swagger UI).

| Method | Endpoint                   | Description                   | Auth Required |
|--------|----------------------------|-------------------------------|---------------|
| POST   | /api/v1/auth/login/        | Obtain JWT access & refresh   | ❌ No          |
| POST   | /api/v1/auth/refresh/      | Refresh JWT token             | ✅ Yes         |
| POST   | /api/v1/auth/create-staff/ | Admin-only: create staff user | ✅ Yes (admin) |
| GET    | /api/v1/auth/health/       | Healthcheck                   | ❌ No          |


## 📝 Future Work
- [ ] Celery integration for background tasks (re-assignment etc.)
- [ ] Auditing & logging for ticket operations
- [ ] Staff notifications for ticket updates

## 🔒 License

© 2025 Shanthanu Varma. All rights reserved.
Unauthorized use, distribution, or modification of this code is prohibited.

## 📬 Contact

For questions, licensing, or deployment support:
📧 varma [DOT] shanthanu [ AT ] gmail.com