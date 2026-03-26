# image-tagger

A Django REST API that uses OpenAI's vision capabilities to automatically generate tags for uploaded images.

## Features

- Upload images via REST API
- Automatic AI-powered tag generation using OpenAI
- PostgreSQL database backend
- Django REST Framework for API endpoints

## Setup

1. **Clone the repository**

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and fill in your values:
   - `OPENAI_API_KEY` — your OpenAI API key
   - `DATABASE_URL` — your PostgreSQL connection string

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

## Project Structure

```
image-tagger/
├── core/          # Django project settings and URLs
├── images/        # Images app (models, views, serializers)
├── manage.py
├── requirements.txt
├── .env.example
└── .gitignore
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | /api/images/ | List all images |
| POST   | /api/images/ | Upload an image |
| GET    | /api/images/<id>/ | Retrieve an image and its tags |
| DELETE | /api/images/<id>/ | Delete an image |
