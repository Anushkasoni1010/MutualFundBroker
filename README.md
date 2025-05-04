# 📊 Mutual Fund Broker API

*** IMPORTANT NOTE: Please replace the rapid api's API KEY before starting the app ***


This is a backend service built using **FastAPI** that allows users to:

- Sign up and log in securely.
- Add and View their portfolio
- Track current value of the investments hourly.
- Fetch mutual fund houses and schemes.
- Select a fund family house, fetch open-ended schemes for that family to fetch mutual fund data.
- Automatically update NAVs using the RapidAPI data source.

---

## 🚀 Features

- User authentication via JWT.
- Mutual fund investment tracking.
- Auto NAV updates via RapidAPI.
- SQLite database with SQLAlchemy ORM.
- Database migrations using Alembic.
- Full API documentation with Swagger UI on the root (`/`).
- Docker support for containerized deployment.

---

## 🛠️ Tech Stack

- **FastAPI** — high-performance async web framework
- **SQLite** — lightweight relational database
- **SQLAlchemy** — ORM for interacting with the database
- **Alembic** — for managing database migrations
- **JWT (via PyJWT)** — for user authentication
- **Uvicorn** — ASGI server to run FastAPI
- **Docker** — for containerization
- **Requests** — for external API calls
- **APScheduler** — background task scheduling

---

## 📂 Project Structure

```bash
app/
├── db.py
├── main.py
├── routes/
│   ├── auth.py
│   ├── fund.py
│   └── portfolio.py
├── services/
│   └── rapidapi.py
├── token/
│   └── token.py
alembic/
migrations/
models.py
Dockerfile
requirements.txt
.env
```

---

## ⚙️ Environment Setup

### 📄 1. Create a .env file and add these Env Variables
```bash 

DATABASE_URL = "sqlite:///./sqlite.db"
SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
RAPIDAPI_KEY
RAPIDAPI_HOST = "latest-mutual-fund-nav.p.rapidapi.com"
RAPIDAPI_URL = "https://latest-mutual-fund-nav.p.rapidapi.com/latest"
```

### 2. Get values for these Variables

SECRET_KEY - Create a strong secret key for password encryption
RAPIDAPI_KEY - To obtain rapid api key:
- Sign up for an account on RapidAPI.
- Go To "https://rapidapi.com/suneetk92/api/latest-mutual-fund-nav" and obtain the required API key.


##  💻 Run Without Docker
### 🔧 1. Clone the Repository

```bash
git clone https://github.com/yourusername/portfolio-tracker.git
cd portfolio-tracker
```

### 📦 2. Install Dependencies (without Docker)

```bash
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 🛠 3. Set Up the Database Tables
```bash
alembic upgrade head
```

### ▶️ 4. Run the App Locally
```bash
uvicorn app.main:app --reload
```

## 🐳 Run with Docker

### 📄 1. Build the Docker Image
```bash
docker build -t mutual-fund-broker .
```

### 🚀 2. Run the Docker Container
```bash
docker run -p 8000:8000 mutual-fund-broker
```
```
This will:
	•	Run alembic upgrade head to apply DB migrations
	•	Start the FastAPI app with uvicorn

Swagger UI will be available at http://localhost:8000
```

## 🔐 Authentication
You must first /signup/ and then /login/ to get a JWT token.

Use this token in Postman or Swagger UI as:

```bash
Bearer <your_token_here>
```

## 📬 API Endpoints Overview
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST   |     /auth/signup/     |     Register a new user        |
| POST   |/auth/login/  |Log in and receive access token |
| POST   | /portfolio/add  |Add an investment   |
| GET    | /portfolio/   | Get current portfolio value|
| GET    |fund/houses|Fetch all mutual fund houses|
| GET    |/fund/schemes|Fetch schemes for a fund family|

## 🙋‍♂️ Author

Anushka Soni
Feel free to reach out with feedback or feature requests!
