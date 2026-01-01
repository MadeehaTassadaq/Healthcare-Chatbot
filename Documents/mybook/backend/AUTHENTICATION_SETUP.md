# Authentication Setup Guide

## Environment Configuration

Your backend uses **two separate secrets** for authentication:

### 1. BETTER_AUTH_SECRET
- **Purpose**: Authenticates your FastAPI backend when calling Better-Auth API
- **Value**: `RqKUAVTFY9xdhxBdBZBk3U9kTQV83EQV`
- **Usage**: Sent as `Authorization: Bearer {BETTER_AUTH_SECRET}` header when your backend makes HTTP calls to Better-Auth
- **Source**: This is the same secret configured in your Better-Auth instance (often called `AUTH_SECRET` in Better-Auth docs)

### 2. JWT_SECRET
- **Purpose**: Signs JWT tokens created by YOUR FastAPI backend
- **Value**: `LLkUQH7IEbo8HSMieTn85SXG5UPx0x9FmO6rUZUYs8k`
- **Usage**: Your backend creates its own JWT access/refresh tokens using this secret
- **Source**: Generated independently for your backend (not related to Better-Auth)

## Why Two Secrets?

This is a **hybrid authentication approach**:

1. **Better-Auth** handles user authentication (signup/signin/password verification)
2. **Your Backend** creates its own JWT tokens for API authorization
3. This gives you control over session management while leveraging Better-Auth's authentication features

## Production URLs

- **Frontend (Azure)**: https://agreeable-sand-0efbb301e.4.azurestaticapps.net
- **Backend (Render)**: https://rag-chatbot-4-1bvx.onrender.com
- **Database**: Neon PostgreSQL (already configured)

## CORS Configuration

Your backend accepts requests from:
- Production frontend: `https://agreeable-sand-0efbb301e.4.azurestaticapps.net`
- Local development: `http://localhost:3000` and `http://localhost:3001`

## Security Keys Generated

### ENCRYPTION_KEY
- **Purpose**: Encrypts sensitive profile data (software/hardware background) at rest
- **Value**: `90d8364805f9e06fe21c192d596aadc3a17572e5d2465893b7152fdd9ff2dfc7`
- **Algorithm**: AES-256 via Fernet

## Next Steps

1. Ensure Better-Auth is running and configured with `BETTER_AUTH_SECRET`
2. Continue with Phase 3 implementation (User Registration services and routes)
3. Run database migrations to create User and Session tables
4. Test signup/signin flow with Better-Auth integration

## Token Flow

```
User Signup/Signin
    ↓
Frontend → Better-Auth (validates credentials)
    ↓
Better-Auth → Your Backend (with BETTER_AUTH_SECRET)
    ↓
Your Backend creates JWT tokens (with JWT_SECRET)
    ↓
JWT tokens returned to frontend in httpOnly cookies
    ↓
Frontend uses JWT tokens for API requests
```
