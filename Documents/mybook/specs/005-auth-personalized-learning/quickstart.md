# Quickstart: Authenticated Personalized Learning Module

## Prerequisites

- Python 3.12+
- PostgreSQL 14+
- Node.js 18+ (for Docusaurus frontend)
- Better-Auth instance (self-hosted or cloud)

## Environment Setup

```bash
# Clone and enter project
cd /home/madeeha/Documents/mybook

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Set environment variables
export BETTER_AUTH_URL="https://your-better-auth-instance.com"
export DATABASE_URL="postgresql://user:pass@localhost:5432/physical_ai_book"
export JWT_SECRET="your-jwt-secret-min-32-chars"
export ENCRYPTION_KEY="your-32-byte-encryption-key"

# Frontend setup
cd ../frontend  # or Docusaurus root
npm install
```

## Development Workflow

### 1. Start Backend

```bash
cd backend
uvicorn src.main:app --reload --port 8000
```

API docs available at: http://localhost:8000/docs

### 2. Start Frontend (Docusaurus)

```bash
npm start
```

Site available at: http://localhost:3000

### 3. Run Tests

```bash
# Backend tests
cd backend
pytest -v

# Frontend tests
npm test
```

## Key Configuration

### Better-Auth Setup

Configure Better-Auth with the following endpoints:
- Signup: `POST /api/auth/signup`
- Signin: `POST /api/auth/signin`
- Session: `GET /api/auth/session`

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes |
| `JWT_SECRET` | Secret for JWT signing (32+ chars) | Yes |
| `BETTER_AUTH_URL` | Better-Auth instance URL | Yes |
| `ENCRYPTION_KEY` | 32-byte key for profile encryption | Yes |
| `CORS_ORIGINS` | Comma-separated allowed origins | Yes |

## First-Time Setup

```bash
# Run migrations
cd backend
alembic upgrade head

# Seed initial data (if needed)
python -m scripts.seed_initial_chapters
```

## Deployment

### Backend (Render)

1. Create new web service on Render
2. Connect GitHub repository
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn src.main:app`
5. Add environment variables from `.env.production`

### Frontend (Azure Static Web App)

1. Create Azure Static Web App
2. Configure build: `npm run build`
3. Output directory: `build`
4. Add API proxy configuration for auth endpoints

## Verification Checklist

- [ ] Backend starts without errors on port 8000
- [ ] Frontend loads without errors on port 3000
- [ ] Signup creates user in PostgreSQL
- [ ] Signin returns valid JWT tokens
- [ ] Profile CRUD operations work
- [ ] Chapter preferences save and load
- [ ] E2E tests pass

## Common Issues

### CORS Errors

Add frontend origin to `CORS_ORIGINS` environment variable.

### Database Connection

Verify `DATABASE_URL` format: `postgresql://user:pass@host:port/dbname`

### JWT Validation Fails

Ensure `JWT_SECRET` is consistent across all services.
