# ADK FastAPI

A FastAPI application with authentication using SQLite database.

## Project Structure

```
ADK_FastAPI/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app instance
│   ├── models.py        # Pydantic models
│   ├── database.py      # Database configuration
│   ├── db_models.py     # SQLAlchemy models
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── ping.py
│   │   ├── google.py
│   │   └── auth.py
│   └── services/
│       ├── __init__.py
│       └── ping_service.py
├── config.py            # Application settings
├── seed_db.py           # Database seeding script
├── test_main.py         # Test suite
├── requirements.txt     # Dependencies
└── README.md
```

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set environment variables in `.env`:
   ```
   GOOGLE_API_KEY=your_key
   SECRET_KEY=your_secret_key
   ```

## Database Setup

The app uses SQLite for user authentication. The database file `auth.db` will be created automatically.

To seed the database with a test user:
```bash
python seed_db.py
```

## Logging

The application includes comprehensive logging:

- **Console logging**: Real-time logs in the terminal
- **File logging**: Detailed logs saved to `logs/app.log`
- **Error logging**: Errors saved to `logs/error.log`
- **Request logging**: All HTTP requests and responses are logged with timing
- **Authentication logging**: Login attempts, successes, and failures

Log levels: DEBUG, INFO, WARNING, ERROR

## Running

```bash
uvicorn app.main:app --reload
```

## Authentication

- Login at `/auth/token` with username `testuser` and password `password`.
- Use the token in Authorization header: `Bearer <token>` for protected routes.
- Password hashing uses SHA256 (compatible with all platforms).

## Endpoints

- `/ping`: Public ping
- `/auth/token`: Login
- `/auth/users/me`: Get current user (protected)
- `/google/status`: Google API status (protected)