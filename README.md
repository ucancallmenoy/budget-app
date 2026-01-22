# Budget App

A comprehensive budget tracking web application built with Flask and SQLite. Track your income and expenses, view financial summaries, and manage your transactions with ease.

## Features

- **User Authentication**: Secure registration and login with password hashing
- **Dashboard**: Overview of total income, expenses, and current balance
- **Add Transactions**: Log income and expense transactions with description, amount, category, and date
- **View Transactions**: Paginated list of all transactions with filtering options
- **Filter & Search**: Filter transactions by category, date range
- **Edit Transactions**: Update existing transaction details
- **Delete Transactions**: Remove transactions from the database
- **Responsive Design**: Works on desktop and mobile devices

## Technology Stack

- **Backend**: Flask 3.0
- **Database**: SQLite
- **Authentication**: Flask-Login with Werkzeug password hashing
- **Forms**: Flask-WTF with WTForms validation
- **Frontend**: HTML, CSS, Jinja2 templates

## Project Structure

```
budget_app/
│
├── app/
│   ├── __init__.py              # Application factory
│   ├── config.py                # Configuration settings
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── database.py          # Database connection
│   │   ├── user.py              # User model
│   │   └── transaction.py       # Transaction model
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py              # Authentication routes
│   │   ├── main.py              # Dashboard routes
│   │   ├── transactions.py      # Transaction routes
│   │   └── errors.py            # Error handlers
│   │
│   ├── forms/
│   │   ├── __init__.py
│   │   ├── auth_forms.py        # Login & registration forms
│   │   └── transaction_forms.py # Transaction forms
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── main/
│   │   │   └── dashboard.html
│   │   ├── transactions/
│   │   │   ├── list.html
│   │   │   └── form.html
│   │   └── errors/
│   │       ├── 404.html
│   │       └── 500.html
│   │
│   ├── static/
│   │   └── css/
│   │       └── style.css
│   │
│   └── utils/
│       └── __init__.py
│
├── instance/                    # Created automatically
│   └── budget.db               # SQLite database
│
├── .env                        # Environment variables (create from .env.example)
├── .env.example                # Example environment variables
├── .gitignore
├── requirements.txt
├── run.py                      # Development server entry point
├── wsgi.py                     # Production server entry point
└── README.md
```

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone or download the project**

2. **Create a virtual environment**

```bash
python -m venv venv
```

3. **Activate the virtual environment**

On Windows:
```bash
venv\Scripts\activate
```

On macOS/Linux:
```bash
source venv/bin/activate
```

4. **Install dependencies**

```bash
pip install -r requirements.txt
```

5. **Create environment file**

Copy `.env.example` to `.env` and update the values:

```bash
cp .env.example .env
```

Edit `.env` and set a strong secret key:
```
SECRET_KEY=your-very-secret-random-key-here
FLASK_ENV=development
DATABASE_NAME=budget.db
```

6. **Run the application**

```bash
python run.py
```

The application will be available at `http://localhost:5000`

## Usage

### First Time Setup

1. Navigate to `http://localhost:5000`
2. Click "Register" to create a new account
3. Fill in username, email, and password (minimum 8 characters)
4. After registration, log in with your credentials

### Using the App

1. **Dashboard**: View your financial summary and recent transactions
2. **Add Transaction**: Click "Add Transaction" to log income or expenses
3. **View All Transactions**: Browse all transactions with pagination
4. **Filter**: Use filters to find specific transactions by category or date
5. **Edit**: Click "Edit" on any transaction to modify it
6. **Delete**: Click "Delete" to remove a transaction (confirmation required)

## Security Features

- Passwords are hashed using Werkzeug's security module
- CSRF protection on all forms via Flask-WTF
- Session cookies are HTTP-only
- SQL injection protection through parameterized queries
- User authentication required for all transaction operations

## Configuration

Key configuration options in `app/config.py`:

- `SECRET_KEY`: Used for session encryption and CSRF tokens
- `DATABASE_PATH`: Location of SQLite database file
- `TRANSACTIONS_PER_PAGE`: Number of transactions per page (default: 10)
- `SESSION_COOKIE_SECURE`: Set to True in production with HTTPS

## Production Deployment

For production deployment:

1. Set `FLASK_ENV=production` in `.env`
2. Generate a strong `SECRET_KEY`
3. Use a production WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
```

4. Configure a reverse proxy (nginx/Apache)
5. Enable HTTPS
6. Set up proper database backups

## Database Schema

### Users Table
- id (PRIMARY KEY)
- username (UNIQUE)
- email (UNIQUE)
- password_hash
- created_at

### Transactions Table
- id (PRIMARY KEY)
- user_id (FOREIGN KEY)
- description
- amount
- transaction_type (income/expense)
- category
- date
- created_at

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, please create an issue in the project repository.