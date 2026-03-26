# image-tagger

A REST API that accepts image uploads, runs them through OpenAI GPT-4o Vision to extract semantic tags and a natural-language description, and stores the results in PostgreSQL for full-text search — all containerized with Docker.

## Built With

- **Python 3** — core language
- **Django** — web framework and ORM
- **Django REST Framework** — API layer
- **OpenAI GPT-4o** — vision model for tag and description generation
- **PostgreSQL** — relational database with native JSON support
- **Docker / Docker Compose** — containerized local development and deployment

## How It Works

```
POST /api/images/upload/
        │
        ▼
  Image saved to disk
        │
        ▼
  File read and base64-encoded
        │
        ▼
  OpenAI GPT-4o Vision API called
  → returns { "tags": [...], "description": "..." }
        │
        ▼
  Tags (JSONField) + description stored in PostgreSQL
        │
        ▼
  GET /api/images/search/?q=keyword
  → PostgreSQL JSONField contains-query returns matching images
```

Each upload is fully processed synchronously — by the time the API responds, the image has been analyzed and its tags are indexed and searchable.

## API Reference

### List all images

```
GET /api/images/
```

**Response**
```json
[
  {
    "id": 1,
    "filename": "sunset.jpg",
    "uploaded_at": "2026-03-26T14:22:10Z",
    "tags": ["sunset", "ocean", "golden hour", "horizon", "clouds"],
    "description": "A vibrant sunset over the ocean with warm golden tones reflecting off the water.",
    "is_processed": true
  }
]
```

---

### Upload an image

```
POST /api/images/upload/
Content-Type: multipart/form-data

file=<image file>
```

**Response** `201 Created`
```json
{
  "id": 2,
  "filename": "dog.jpg",
  "uploaded_at": "2026-03-26T14:25:03Z",
  "tags": ["dog", "golden retriever", "park", "grass", "outdoor"],
  "description": "A golden retriever playing fetch in a sunny park.",
  "is_processed": true
}
```

---

### Search images by tag or keyword

```
GET /api/images/search/?q=keyword
```

**Response**
```json
[
  {
    "id": 2,
    "filename": "dog.jpg",
    "uploaded_at": "2026-03-26T14:25:03Z",
    "tags": ["dog", "golden retriever", "park", "grass", "outdoor"],
    "description": "A golden retriever playing fetch in a sunny park.",
    "is_processed": true
  }
]
```

## Running with Docker

```bash
git clone https://github.com/your-username/image-tagger.git
cd image-tagger
cp .env.example .env   # add your OPENAI_API_KEY and DATABASE_URL
docker-compose up --build
```

The API will be available at `http://localhost:8000`.

## Key Engineering Decisions

**Django was chosen for the ORM.**
Django's ORM handles migrations, model validation, and query-building out of the box, which kept the data layer clean and schema changes low-friction. For a project centered on a well-defined data model (image + tags + description), the productivity gains of a batteries-included framework outweigh the overhead.

**PostgreSQL `JSONField` was used for flexible tag storage.**
Tags are a variable-length list of strings — a normalized many-to-many join table would add schema complexity for no benefit here. PostgreSQL's native `jsonb` column (exposed via Django's `JSONField`) stores the tag array directly and supports containment queries (`tags__contains=query`) without any extra indexing setup, keeping both the model and the search logic simple.

**Docker was used for containerization.**
Wrapping the Django app and PostgreSQL in Docker Compose means the entire stack — including the correct Python version, database, and environment config — can be reproduced with a single command. This eliminates "works on my machine" issues and makes the project straightforward to evaluate or deploy.
