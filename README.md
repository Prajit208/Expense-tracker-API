# Expense Tracker

A full-stack expense tracker. The backend is a REST API built with FastAPI and PostgreSQL, and the frontend is plain HTML, CSS and JavaScript.

**Live demo:** https://expense-tracker-frontend-lac-chi.vercel.app
**API docs:** https://expense-tracker-backend-bice-five.vercel.app/docs

## Features

- Sign up and log in with JWT authentication
- Add, edit and delete expenses
- Total spent summary
- Filter by title, category, amount range and date range
- Sort by date or amount, ascending or descending
- Each user sees only their own expenses

## Tech stack

| Part | Technology |
| --- | --- |
| Backend | FastAPI, SQLAlchemy, Alembic |
| Database | PostgreSQL (Supabase) |
| Auth | OAuth2 password flow with JWT, hashed passwords |
| Frontend | HTML, CSS, vanilla JavaScript |
| Tests | pytest |
| Hosting | Vercel |

## Project structure

```
expense-tracker-api/
├── backend/
│   ├── app/
│   │   ├── routers/        auth.py, expenses.py, users.py
│   │   ├── main.py         app setup and CORS
│   │   ├── database.py     engine and session
│   │   ├── models.py       SQLAlchemy models
│   │   ├── schemas.py      Pydantic schemas
│   │   ├── oauth2.py       token creation and verification
│   │   └── utils.py        password hashing
│   ├── alembic/            database migrations
│   ├── tests/              pytest tests
│   └── requirements.txt
└── frontend/
    ├── index.html
    ├── login.html
    ├── signup.html
    ├── dashboard.html
    ├── css/style.css
    └── js/
```

## API overview

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | `/users/` | Create an account |
| POST | `/login` | Log in (form data: `username` is the email, plus `password`), returns a token |
| GET | `/expenses/` | List your expenses, with optional filters |
| POST | `/expenses/` | Create an expense |
| PUT | `/expenses/{id}` | Update an expense |
| DELETE | `/expenses/{id}` | Delete an expense |

`GET /expenses/` accepts these optional query parameters: `category`, `min_amount`, `max_amount`, `date_from`, `date_to`, `search`, `sort_by` (`date` or `amount`) and `order` (`asc` or `desc`).

All expense endpoints need an `Authorization: Bearer <token>` header.

## Running locally

### Backend

1. Create a virtual environment and install the dependencies:
   ```bash
   cd backend
   python -m venv venv
   venv\Scripts\activate        # Windows
   source venv/bin/activate     # macOS / Linux
   pip install -r requirements.txt
   ```
2. Create a `.env` file in `backend/`:
   ```
   DATABASE_URL=postgresql://user:password@host:5432/dbname
   SECRET_KEY=a-long-random-string
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```
   If the database password contains special characters, percent-encode them.
3. Create the tables and start the server:
   ```bash
   alembic upgrade head
   uvicorn app.main:app --reload
   ```

The API runs at `http://127.0.0.1:8000` and the docs at `http://127.0.0.1:8000/docs`.

### Frontend

1. Serve the `frontend/` folder with a local server, for example the VS Code Live Server extension. 
2. In `frontend/js/api.js`, set `API` to `http://127.0.0.1:8000`.
3. Make sure the frontend address is listed in `allow_origins` in `backend/app/main.py`.

### Tests

```bash
cd backend
pytest
```

Point the tests at a separate test database (see `tests/conftest.py`), never at your real data.

## Deployment

The backend and frontend are separate Vercel projects, with Root Directory set to `backend` and `frontend`. The backend's environment variables are set in its project settings, and the deployed frontend address is added to `allow_origins` in `backend/app/main.py`.