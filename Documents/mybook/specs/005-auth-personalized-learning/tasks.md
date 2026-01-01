# Tasks: Authenticated Personalized Learning Module

**Feature**: 005-auth-personalized-learning
**Created**: 2025-12-31
**Input**: Design documents from `/specs/005-auth-personalized-learning/`

## Summary

Implementation of authentication (Better-Auth) and personalized learning features for the Physical AI & Humanoid Robotics book. Tasks organized by user story to enable independent implementation and testing.

- **Total Tasks**: 68
- **Backend Tasks**: 38
- **Frontend Tasks**: 22
- **Cross-cutting Tasks**: 8

## Quick Start (MVP)

The MVP is **User Story 1 (Registration) + User Story 2 (Sign-In)**. Complete Phase 1 + Phase 2 + Phase 3 (US1) + Phase 4 (US2) to get a minimal auth system.

---

## Phase 1: Project Setup

**Purpose**: Initialize project structure and dependencies

- [ ] T001 Create backend directory structure per plan.md: `backend/src/{models,services,middleware,lib}`
- [ ] T002 Create frontend directory structure: `frontend/src/{components/{auth,profile},services,hooks}`
- [ ] T003 Add Python dependencies to `backend/requirements.txt`: fastapi, uvicorn, sqlalchemy, pydantic, python-jose, passlib, bcrypt, aiohttp, alembic
- [ ] T004 Create `backend/.env.example` with all required environment variables
- [ ] T005 Create `backend/src/__init__.py` and all package `__init__.py` files
- [ ] T006 Create `backend/alembic.ini` and migration environment
- [ ] T007 Configure pytest in `backend/pyproject.toml` with pytest-asyncio, httpx

---

## Phase 2: Foundational Components

**Purpose**: Shared infrastructure required by all user stories

- [ ] T010 Create database configuration in `backend/src/lib/database.py`
- [ ] T011 Create JWT token utilities in `backend/src/lib/jwt.py`
- [ ] T012 Create encryption utilities in `backend/src/lib/encryption.py` for profile fields
- [ ] T013 Create audit logging module in `backend/src/lib/audit.py`
- [ ] T014 Create Better-Auth HTTP wrapper in `backend/src/lib/better_auth.py`
- [ ] T015 Create Pydantic schemas base in `backend/src/schemas/__init__.py`
- [ ] T016 Create auth middleware in `backend/src/middleware/auth.py` for JWT validation
- [ ] T017 Create rate limiting middleware in `backend/src/middleware/rate_limit.py`
- [ ] T018 Create error handlers in `backend/src/middleware/errors.py`

**Checkpoint**: All foundational components tested and integrated

---

## Phase 3: User Story 1 - New User Registration (P1)

**Goal**: Allow visitors to create accounts with email, password, and background info

**Independent Test**: Complete signup flow from anonymous state, verify account exists in database

### Backend Tasks

- [ ] T020 [US1] Create User SQLAlchemy model in `backend/src/models/user.py`
- [ ] T021 [US1] Create Session SQLAlchemy model in `backend/src/models/session.py`
- [ ] T022 [US1] Create Pydantic schemas for SignupRequest in `backend/src/schemas/auth.py`
- [ ] T023 [US1] Implement password hashing and validation in `backend/src/services/auth/password.py`
- [ ] T024 [US1] Implement UserService in `backend/src/services/auth/user_service.py`
- [ ] T025 [US1] Implement Better-Auth registration call in `backend/src/services/auth/better_auth_client.py`
- [ ] T026 [US1] Create JWT token generation in `backend/src/services/auth/tokens.py`
- [ ] T027 [US1] Implement auth router with POST /auth/signup endpoint in `backend/src/routers/auth.py`
- [ ] T028 [US1] Add signup validation (email format, password complexity) per NFR-005
- [ ] T029 [US1] Create database migration for User and Session tables

### Frontend Tasks

- [ ] T030 [US1] Create API client in `frontend/src/services/api.ts`
- [ ] T031 [US1] Create auth state context in `frontend/src/contexts/AuthContext.tsx`
- [ ] T032 [US1] Create SignupForm React component in `frontend/src/components/auth/SignupForm.tsx`
- [ ] T033 [US1] Create background survey form in `frontend/src/components/auth/BackgroundSurvey.tsx`
- [ ] T034 [US1] Integrate signup flow into Docusaurus theme in `frontend/src/theme/index.ts`

### Test Tasks

- [ ] T035 [US1] Write unit tests for password hashing in `backend/tests/unit/test_password.py`
- [ ] T036 [US1] Write unit tests for JWT token generation in `backend/tests/unit/test_tokens.py`
- [ ] T037 [US1] Write integration test for POST /auth/signup in `backend/tests/integration/test_signup.py`
- [ ] T038 [US1] Write E2E test for signup flow in `frontend/tests/e2e/signup.spec.ts`

**Checkpoint**: Users can register with email/password/background and account exists in database

---

## Phase 4: User Story 2 - User Sign-In (P1)

**Goal**: Allow returning users to authenticate and access personalized content

**Independent Test**: Sign in with valid credentials, verify access to authenticated features

### Backend Tasks

- [ ] T040 [US2] Implement credentials validation in `backend/src/services/auth/credentials.py`
- [ ] T041 [US2] Implement session creation and storage in `backend/src/services/auth/session_service.py`
- [ ] T042 [US2] Implement token refresh flow in `backend/src/services/auth/refresh.py`
- [ ] T043 [US2] Add signin endpoint to auth router: POST /auth/signin in `backend/src/routers/auth.py`
- [ ] T044 [US2] Add signout endpoint to auth router: POST /auth/signout in `backend/src/routers/auth.py`
- [ ] T045 [US2] Add session endpoint: GET /auth/session in `backend/src/routers/auth.py`
- [ ] T046 [US2] Add token refresh endpoint: POST /auth/refresh in `backend/src/routers/auth.py`
- [ ] T047 [US2] Implement account lockout after failed attempts per Security Agent spec

### Frontend Tasks

- [ ] T050 [US2] Create SignInForm React component in `frontend/src/components/auth/SignInForm.tsx`
- [ ] T051 [US2] Create useAuth hook in `frontend/src/hooks/useAuth.ts`
- [ ] T052 [US2] Implement session persistence with localStorage in `frontend/src/services/auth/storage.ts`
- [ ] T053 [US2] Create AuthStatus indicator in `frontend/src/components/auth/AuthStatus.tsx`
- [ ] T054 [US2] Add auth state to Docusaurus navbar in `frontend/src/theme/Navbar/index.tsx`

### Test Tasks

- [ ] T055 [US2] Write integration tests for signin/signout in `backend/tests/integration/test_auth_flow.py`
- [ ] T056 [US2] Write unit tests for session service in `backend/tests/unit/test_session.py`
- [ ] T057 [US2] Write E2E test for signin flow in `frontend/tests/e2e/signin.spec.ts`
- [ ] T058 [US2] Write E2E test for session persistence in `frontend/tests/e2e/session.spec.ts`

**Checkpoint**: Users can sign in, stay authenticated across pages, and sign out

---

## Phase 5: User Story 3 - Profile Background Collection (P1)

**Goal**: Collect and store software/hardware background during and after registration

**Independent Test**: Verify background data is stored in profile and can be retrieved

### Backend Tasks

- [ ] T060 [US3] Extend User model with profile_data JSONB field validation
- [ ] T061 [US3] Create profile Pydantic schemas in `backend/src/schemas/profile.py`
- [ ] T062 [US3] Implement ProfileService in `backend/src/services/profile/profile_service.py`
- [ ] T063 [US3] Create profile router with GET/PUT /api/profile endpoints in `backend/src/routers/profile.py`
- [ ] T064 [US3] Add profile validation (experience levels, required arrays) per data-model.md

### Frontend Tasks

- [ ] T065 [US3] Create ProfileEditor component in `frontend/src/components/profile/ProfileEditor.tsx`
- [ ] T066 [US3] Create BackgroundSurvey update mode in `frontend/src/components/profile/BackgroundEditor.tsx`
- [ ] T067 [US3] Integrate profile display into user settings page

### Test Tasks

- [ ] T068 [US3] Write integration tests for profile CRUD in `backend/tests/integration/test_profile.py`
- [ ] T069 [US3] Write unit tests for profile validation in `backend/tests/unit/test_profile_validation.py`
- [ ] T070 [US3] Write E2E test for profile update in `frontend/tests/e2e/profile.spec.ts`

**Checkpoint**: Background info saved to profile, can be updated, persists across sessions

---

## Phase 6: User Story 4 - Chapter Personalization (P2)

**Goal**: Allow users to toggle personalization per chapter based on their background

**Independent Test**: Toggle personalization on chapter, verify content adapts

### Backend Tasks

- [ ] T080 [US4] Create ChapterPreference SQLAlchemy model in `backend/src/models/preference.py`
- [ ] T081 [US4] Create preferences Pydantic schemas in `backend/src/schemas/preferences.py`
- [ ] T082 [US4] Implement PreferenceService in `backend/src/services/personalization/preference_service.py`
- [ ] T083 [US4] Create preferences router with GET/PUT endpoints in `backend/src/routers/preferences.py`
- [ ] T084 [US4] Extend RAG chatbot integration to accept userBackground parameter in `backend/src/services/personalization/rag_integration.py`
- [ ] T085 [US4] Implement personalized response caching per research.md findings

### Frontend Tasks

- [ ] T090 [US4] Create ChapterPreferences component in `frontend/src/components/profile/ChapterPreferences.tsx`
- [ ] T091 [US4] Create personalization toggle in `frontend/src/components/chapter/PersonalizationToggle.tsx`
- [ ] T092 [US4] Implement preference-aware content rendering in chapter view
- [ ] T093 [US4] Create RAG context provider in `frontend/src/contexts/RAGContext.tsx`

### Test Tasks

- [ ] T094 [US4] Write integration tests for preferences API in `backend/tests/integration/test_preferences.py`
- [ ] T095 [US4] Write unit tests for preference service in `backend/tests/unit/test_preferences.py`
- [ ] T096 [US4] Write E2E test for personalization toggle in `frontend/tests/e2e/personalization.spec.ts`

**Checkpoint**: Personalization toggles work, content differs based on user background

---

## Phase 7: User Story 5 - Profile Management (P2)

**Goal**: Allow users to view, update, and delete their account with GDPR compliance

**Independent Test**: Access profile settings, modify data, verify changes persist, delete account

### Backend Tasks

- [ ] T100 [US5] Implement GDPR deletion workflow (soft delete + hard delete) in `backend/src/services/profile/gdpr_service.py`
- [ ] T101 [US5] Create profile export endpoint: GET /api/profile/export in `backend/src/routers/profile.py`
- [ ] T102 [US5] Implement re-authentication for account deletion per FR-014
- [ ] T103 [US5] Add audit logging for all profile operations per NFR-004

### Frontend Tasks

- [ ] T105 [US5] Create ProfileSettings page in `frontend/src/pages/profile/settings.tsx`
- [ ] T106 [US5] Create AccountDeleteConfirm dialog in `frontend/src/components/profile/AccountDeleteConfirm.tsx`
- [ ] T107 [US5] Create ProfileExport component for data download in `frontend/src/components/profile/ProfileExport.tsx`

### Test Tasks

- [ ] T108 [US5] Write integration tests for GDPR deletion in `backend/tests/integration/test_gdpr.py`
- [ ] T109 [US5] Write integration tests for profile export in `backend/tests/integration/test_export.py`
- [ ] T110 [US5] Write E2E test for account deletion in `frontend/tests/e2e/delete-account.spec.ts`

**Checkpoint**: Profile management works, GDPR deletion completes per timeline

---

## Phase 8: User Story 6 - Learning Progress Tracking (P3)

**Goal**: Track and display reading progress across chapters

**Independent Test**: Read chapters, verify progress indicators show correctly, persists after logout/login

### Backend Tasks

- [ ] T120 [US6] Add progress tracking methods to PreferenceService
- [ ] T121 [US6] Create progress endpoint: GET /api/progress in `backend/src/routers/progress.py`
- [ ] T122 [US6] Add progress auto-update on chapter completion

### Frontend Tasks

- [ ] T125 [US6] Create ProgressDashboard in `frontend/src/components/profile/ProgressDashboard.tsx`
- [ ] T126 [US6] Add progress indicators to chapter navigation sidebar
- [ ] T127 [US6] Implement scroll position tracking per chapter

### Test Tasks

- [ ] T128 [US6] Write integration tests for progress API in `backend/tests/integration/test_progress.py`
- [ ] T129 [US6] Write E2E test for progress tracking in `frontend/tests/e2e/progress.spec.ts`

**Checkpoint**: Progress persists, shows in dashboard, tracks last position

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Security hardening, documentation, final integration

- [ ] T130 Add security headers middleware (CORS, HSTS, X-Frame-Options)
- [ ] T131 Implement rate limiting for all auth endpoints per plan.md
- [ ] T132 Create API documentation from OpenAPI spec in `docs/api-reference.md`
- [ ] T133 Generate architecture diagram in Mermaid.js per plan.md
- [ ] T134 Write SECURITY.md with incident response procedures
- [ ] T135 Create docker-compose.yml for local development
- [ ] T136 Configure CI/CD pipeline for backend tests
- [ ] T137 Configure CI/CD pipeline for frontend E2E tests

---

## Dependencies

```
Phase 1 (Setup)
    │
    └─ Phase 2 (Foundational)
            │
            ├─ Phase 3 (US1 - Registration)
            │       └─ Phase 4 (US2 - Sign-In)
            │               └─ Phase 5 (US3 - Background Collection)
            │
            ├─ Phase 6 (US4 - Personalization) [depends on Phase 5]
            │       └─ Phase 7 (US5 - Profile Management)
            │               └─ Phase 8 (US6 - Progress Tracking)
            │
            └─ Phase 9 (Polish)
```

---

## Parallel Execution Examples

Within each phase, the following can run in parallel:

- **Phase 2**: T010-T013 (lib utilities) can run before T015-T018 (middleware)
- **Phase 3**: Backend tasks (T020-T029) can run alongside frontend tasks (T030-T034)
- **Phase 4**: Backend auth endpoints (T040-T047) can run alongside frontend components (T050-T054)
- **Phase 5-8**: Each user story's backend and frontend tasks can run in parallel

---

## Implementation Strategy

### MVP Scope (Weeks 1-2)
Complete: Phase 1 + Phase 2 + Phase 3 (US1) + Phase 4 (US2)
- Users can register and sign in
- Basic session management
- Profile storage for background info

### Increment 1 (Week 3)
Complete: Phase 5 (US3) + Phase 6 (US4)
- Background collection at signup
- Chapter personalization toggle
- RAG integration for personalized content

### Increment 2 (Week 4)
Complete: Phase 7 (US5) + Phase 8 (US6)
- Full profile management
- GDPR account deletion
- Progress tracking dashboard

### Final (Week 5)
Complete: Phase 9 (Polish)
- Security hardening
- Documentation
- CI/CD setup

---

## File Paths Reference

| Component | Path |
|-----------|------|
| User Model | `backend/src/models/user.py` |
| Session Model | `backend/src/models/session.py` |
| ChapterPreference Model | `backend/src/models/preference.py` |
| Auth Router | `backend/src/routers/auth.py` |
| Profile Router | `backend/src/routers/profile.py` |
| Preferences Router | `backend/src/routers/preferences.py` |
| Auth Middleware | `backend/src/middleware/auth.py` |
| SignupForm | `frontend/src/components/auth/SignupForm.tsx` |
| SignInForm | `frontend/src/components/auth/SignInForm.tsx` |
| AuthContext | `frontend/src/contexts/AuthContext.tsx` |
| useAuth Hook | `frontend/src/hooks/useAuth.ts` |
