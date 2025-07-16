# AICPR_MSE SERVER

This is a FastAPI backend project using PostgreSQL, Alembic for database migrations, and Docker for environment management.

---

## 🛠 Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- Python 3.9+ (optional for local development without Docker)

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/AICPR_MSE.git
cd AICPR_MSE
```

### 2. Set up Environement Variables
```bash
cp .env.sample .env
```

### 3. Install Dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4. Run with Docker Compose
```bash
docker compose up --build
```
Visit the FastAPI docs at http://localhost:8000/docs

### Database Migrations
```bash
make makemigrations m="your message"   # Create new migration
make migrate                           # Apply migrations
```

#### Refer to Makefile for commands

