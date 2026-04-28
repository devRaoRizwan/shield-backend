# Shield House Backend API

A Django REST Framework API for the Shield House e-commerce platform with PostgreSQL database via Supabase.

## Tech Stack

- **Framework:** Django 5.2.5
- **REST API:** Django REST Framework 3.14.0
- **Database:** PostgreSQL (via Supabase)
- **Authentication:** Token Authentication
- **Server:** Gunicorn
- **Static Files:** WhiteNoise
- **CORS:** django-cors-headers
- **Python:** 3.8+

## Features

- RESTful API endpoints for products and inquiries
- Token-based authentication
- CORS support for frontend integration
- PostgreSQL with Supabase
- Static file management with WhiteNoise
- Admin panel for content management

## Architecture

```
Shield Backend/
├── catalog/              # Main app
│   ├── models.py        # Product, Inquiry models
│   ├── views.py         # API views
│   ├── serializers.py   # DRF serializers
│   ├── urls.py          # App URLs
│   └── management/      # Custom seed_products command
├── config/              # Project settings
│   ├── settings.py      # Django & database settings
│   ├── urls.py          # Main URL routing
│   ├── wsgi.py          # WSGI config (production)
│   └── asgi.py          # ASGI config
├── manage.py            # Django CLI
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (DO NOT COMMIT)
├── .gitignore          # Git ignore rules
└── Procfile            # Render deployment config
```

## API Endpoints

```
GET   /api/products/           # List all products
GET   /api/products/<id>/      # Get product details
POST  /api/inquiries/          # Create inquiry
GET   /api/admin/login/        # Admin login (if implemented)
```

## Prerequisites

- Python 3.8 or higher
- PostgreSQL or Supabase account
- Virtual environment (venv)
- Git

## Local Development Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/shield-backend.git
cd shield-backend
```

### 2. Create and activate virtual environment

**Windows (PowerShell):**
```powershell
python -m venv env
.\env\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory (copy from `.env.example` if available):

```env
# Django Configuration
DJANGO_SECRET_KEY=your-secret-key-here-change-in-production
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,your-domain.onrender.com,your-frontend.vercel.app

# CORS Configuration (for frontend access)
CORS_ALLOWED_ORIGINS=http://localhost:5173,https://your-frontend.vercel.app

# Production Database (Supabase)
DATABASE_URL=postgresql://user:password@host:port/database

# Local Development Database (PostgreSQL)
POSTGRES_DB=shieldbackend
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-password
POSTGRES_HOST=127.0.0.1
POSTGRES_PORT=5432
```

### 5. Run database migrations

```powershell
# Make sure virtual environment is activated
.\env\Scripts\Activate.ps1

# Run migrations
python manage.py migrate
```

### 6. Create superuser for admin panel

```bash
python manage.py createsuperuser
```

Follow the prompts to set username, email, and password.

### 7. Seed sample products (optional)

```bash
python manage.py seed_products
```

### 8. Run development server

```bash
python manage.py runserver
```

Server will be available at:
- **API:** http://localhost:8000/api/
- **Admin Panel:** http://localhost:8000/admin/
- **Browsable API:** http://localhost:8000/api/products/

## Deployment on Render

### Prerequisites

1. Code pushed to GitHub
2. Supabase database created with connection string
3. Render account (https://render.com)

### Step 1: Create Web Service on Render

1. Log in to Render dashboard
2. Click **New** → **Web Service**
3. Connect GitHub and select `shield-backend` repository
4. Configure settings:
   - **Name:** `shield-backend` (customize if desired)
   - **Region:** Choose closest to your users
   - **Branch:** `main`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn config.wsgi:application`

### Step 2: Add Environment Variables

In Render dashboard → **Environment** → Add the following:

```
DJANGO_SECRET_KEY=<generate-a-strong-random-secret-key>
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=your-api.onrender.com,your-frontend.vercel.app
DATABASE_URL=<your-supabase-connection-string>
CORS_ALLOWED_ORIGINS=https://your-frontend.vercel.app
```

**To generate SECRET_KEY:**
```python
# Run this in Python REPL
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

### Step 3: Deploy

1. Click **Create Web Service**
2. Wait for build to complete (2-5 minutes)
3. Once deployed, note your URL: `https://your-api.onrender.com`

### Step 4: Run migrations on Render

Once deployed:
1. Go to your service dashboard
2. Click **Shell** (top right)
3. Run: `python manage.py migrate`
4. Create superuser: `python manage.py createsuperuser`

Your API is now live! Update your frontend's `VITE_API_URL` to use this URL.

## Database Setup (Supabase)

### Create Supabase Project

1. Visit https://supabase.com
2. Sign up and create new project
3. Wait for project to be ready
4. Go to **Project Settings** → **Database**
5. Copy the connection string: `postgresql://[user]:[password]@[host]:[port]/[database]`
6. Add to `.env` as `DATABASE_URL`

**Note:** Database migrations run automatically when you deploy to Render.

## Production Checklist

- [x] `.env` file created with production secrets
- [x] `DEBUG=False` in production
- [x] `ALLOWED_HOSTS` includes all domains
- [x] `CORS_ALLOWED_ORIGINS` configured for frontend
- [x] Database migrations run on Render
- [x] Superuser created on Render
- [x] Static files collected (WhiteNoise)
- [x] Gunicorn configured in Procfile

## Troubleshooting

### Django Check Fails
```bash
python manage.py check
```
If errors appear, check:
- Virtual environment is activated
- All required packages installed: `pip install -r requirements.txt`
- `.env` file exists with required variables

### Database Connection Errors
- Verify `DATABASE_URL` is correct in `.env`
- Ensure Supabase project is running
- Check that your IP is whitelisted (if using IP restrictions)
- Test locally first with `python manage.py migrate`

### CORS Errors (Frontend can't reach API)
- Verify `CORS_ALLOWED_ORIGINS` includes your frontend URL
- Format must be: `https://yourdomain.vercel.app` (no trailing slash)
- Make requests from frontend to `VITE_API_URL` environment variable

### Static Files Not Serving
- WhiteNoise handles static file serving automatically
- If issues persist, run: `python manage.py collectstatic --noinput`

## Important Files

- **`requirements.txt`** - All Python dependencies
- **`Procfile`** - Render deployment instructions
- **`.env`** - Environment variables (NEVER commit)
- **`.gitignore`** - Files to exclude from Git
- **`config/settings.py`** - Django configuration
- **`config/wsgi.py`** - Production WSGI application

## Helpful Commands

```bash
# Check Django installation
python manage.py check

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Load seed data
python manage.py seed_products

# Run tests
python manage.py test

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Access Django shell
python manage.py shell
```

## Learning Resources

- [Django Official Documentation](https://docs.djangoproject.com)
- [Django REST Framework](https://www.django-rest-framework.org)
- [Supabase Database Guide](https://supabase.com/docs/guides/database)
- [Render Deployment](https://render.com/docs/deploy-django)
- [WhiteNoise Documentation](http://whitenoise.evans.io/)

## License

MIT License

5. Start the server:

```powershell
python manage.py runserver
```

## Frontend Mapping

- `/shop` should call `GET /api/products/`
- `/shop/:slug` should call `GET /api/products/<slug>/`
- `image` is returned as a usable media URL for rendering product images from the backend
- Invalid slugs correctly return `404 Not Found`

## PostgreSQL Notes

- The project now uses PostgreSQL as the default database backend.
- Database credentials are read from environment variables instead of being hardcoded.
- `psycopg2-binary` is already available in this environment, so Django can connect to PostgreSQL once your database is running.
