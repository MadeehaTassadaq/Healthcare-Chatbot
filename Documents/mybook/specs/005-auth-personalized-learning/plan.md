# Implementation Plan: Authenticated Personalized Learning Module

**Branch**: `005-auth-personalized-learning` | **Date**: 2025-12-31 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/005-auth-personalized-learning/spec.md`

## Summary

Implement authentication (Better-Auth) and personalized learning features for the Physical AI & Humanoid Robotics book. The system will allow users to register/sign in, store structured profiles (software/hardware background), and optionally personalize chapter content via the existing RAG chatbot. Frontend runs on Azure Static Web App (Docusaurus), backend on Render with PostgreSQL.

## Technical Context

**Language/Version**: Python 3.12 (existing backend stack)
**Primary Dependencies**: Better-Auth, FastAPI, Pydantic, SQLAlchemy, aiohttp
**Storage**: PostgreSQL (via existing backend infrastructure on Render)
**Testing**: pytest, pytest-asyncio, httpx for API tests
**Target Platform**: Linux server (Render), Web browser (Docusaurus/React)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: 1,000 concurrent users, 500ms API p95, 2s auth operations
**Constraints**: <200ms perceived latency for personalization toggle, GDPR-compliant deletion
**Scale/Scope**: 1,000-10,000 registered users, 1,000 concurrent sessions

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

*   [x] **Technical Accuracy:** Plan uses established auth patterns (JWT sessions, bcrypt, OAuth2-derived flows) and verified libraries.
*   [x] **Co-design Focus:** Personalization explicitly maps user hardware/software background to relevant chapter content.
*   [x] **Applicability:** Real-world robotics use cases integrated via RAG (e.g., Jetson for CUDA, ROS 2 for Python users).
*   [x] **Safety & Ethics:** GDPR-compliant deletion, encrypted profiles, audit logging, no data sharing.
*   [x] **Content Structure:** Profile schema supports chapter-level preferences aligned with modular chapter structure.
*   [x] **Sourcing:** Using official Better-Auth docs, FastAPI best practices, OWASP auth guidelines.
*   [x] **Technical Standards:** Docusaurus frontend, Mermaid.js for architecture diagrams, Python backend.

## Project Structure

### Documentation (this feature)

```text
specs/005-auth-personalized-learning/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (below)
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   ├── openapi.yaml     # OpenAPI 3.0 specification
│   └── schemas.yaml     # JSON Schema for requests/responses
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/              # SQLAlchemy models
│   │   ├── user.py          # User entity
│   │   ├── session.py       # Session entity
│   │   └── preference.py    # ChapterPreference entity
│   ├── services/
│   │   ├── auth/
│   │   │   ├── router.py    # Auth endpoints (signup, signin, signout)
│   │   │   └── service.py   # Auth business logic
│   │   ├── profile/
│   │   │   ├── router.py    # Profile endpoints
│   │   │   └── service.py   # Profile CRUD + GDPR deletion
│   │   └── personalization/
│   │       ├── router.py    # Preferences endpoints
│   │       └── service.py   # Preference management + RAG context
│   ├── middleware/
│   │   ├── auth.py          # JWT validation middleware
│   │   └── rate_limit.py    # Rate limiting for auth endpoints
│   └── lib/
│       ├── better_auth.py   # Better-Auth integration
│       ├── encryption.py    # Profile field encryption
│       └── audit.py         # Audit logging
└── tests/
    ├── unit/
    ├── integration/
    └── contract/            # API contract tests

frontend/
├── src/
│   ├── components/
│   │   ├── auth/            # SignupForm, SignInForm, AuthStatus
│   │   └── profile/         # BackgroundSurvey, ProfileEditor, ChapterPreferences
│   ├── services/
│   │   ├── api.ts           # API client
│   │   └── auth.ts          # Auth state management
│   └── hooks/
│       └── useAuth.ts       # React hook for auth state
└── tests/
    └── e2e/
        └── auth.spec.ts     # Playwright tests

docs/
├── auth-architecture.md     # Architecture diagram (Mermaid)
└── api-reference.md         # Generated from OpenAPI
```

**Structure Decision**: Two-package structure with backend (FastAPI) and frontend (Docusaurus/React) per existing project patterns. Backend at `backend/`, frontend components integrated into Docusaurus at `frontend/` or within the Docusaurus plugins directory.

## Complexity Tracking

*No constitution violations requiring justification.*

---

# Phase 0: Research & Discovery

## Unknowns to Resolve

| # | Unknown | Impact | Research Task |
|---|---------|--------|---------------|
| 1 | Better-Auth Python client capabilities | HIGH | Verify Better-Auth provides Python SDK for backend integration or requires HTTP wrapper |
| 2 | Docusaurus auth integration pattern | HIGH | Determine how to integrate auth state with Docusaurus React components |
| 3 | RAG personalization context injection | MEDIUM | Research how to pass user background as context to existing RAG chatbot |
| 4 | Session management strategy | MEDIUM | JWT vs session cookies - choose optimal pattern for Static Web App + Render |

## Research Findings

### Finding 1: Better-Auth Integration

**Decision**: Use Better-Auth's REST API from Python backend rather than waiting for official SDK.

**Rationale**: Better-Auth is primarily a JavaScript/TypeScript library. For Python backend, we'll:
- Call Better-Auth's HTTP endpoints for signup/signin operations
- Manage sessions via our own JWT tokens synchronized with Better-Auth
- Store user profiles in PostgreSQL, reference Better-Auth user IDs

**Alternatives considered**:
- Wait for Better-Auth Python SDK (not available, delays project)
- Proxy all auth through separate JS service (adds latency, complexity)

### Finding 2: Docusaurus Authentication

**Decision**: Create custom Docusaurus plugin with React hooks for auth state.

**Rationale**: Docusaurus supports custom plugins and React frontend. We'll:
- Create `plugin-auth` plugin with AuthProvider context
- Use localStorage + JWT for persistent sessions
- Sync with backend on page load

**Alternatives considered**:
- Modify Docusaurus source (complex, upgrade-resistant)
- External auth iframe (poor UX, CORS issues)

### Finding 3: RAG Context Injection

**Decision**: Extend existing RAG chatbot to accept user context parameter.

**Rationale**: The existing RAG chatbot already queries chapter content. We'll:
- Add optional `userBackground` field to RAG request payload
- Include user's software/hardware preferences in prompt context
- Cache personalized responses separately from standard

**Alternatives considered**:
- Separate personalized index (duplicates storage)
- Query-time filtering only (less accurate)

### Finding 4: Session Management

**Decision**: JWT access tokens + refresh token cookies.

**Rationale**: Best balance for SPA + API architecture:
- Access token (15 min) in memory for API calls
- Refresh token (30 days) in httpOnly cookie
- Server validates on each protected request

**Alternatives considered**:
- Session cookies only (good but less portable)
- Pure JWT without refresh (security risk on token theft)

---

# Phase 1: Design & Contracts

## Data Model

See `data-model.md` for detailed entity definitions.

## API Contracts

See `contracts/openapi.yaml` for OpenAPI 3.0 specification.

## Quickstart Guide

See `quickstart.md` for development setup instructions.

---

# Phase 2: Implementation (not in scope for /sp.plan)

See `/sp.tasks` command output.

---

## Implementation Phases

### Phase 1: Backend Foundation (Week 1)

**Goal**: Core authentication and profile storage

| Task | Duration | Dependencies |
|------|----------|--------------|
| Set up SQLAlchemy models (User, Session, ChapterPreference) | 2 days | None |
| Implement JWT token generation and validation | 2 days | Models |
| Create Better-Auth HTTP wrapper service | 2 days | JWT, Better-Auth docs |
| Build signup/signin API endpoints | 2 days | Auth service |
| Add rate limiting middleware | 1 day | None |
| Write unit tests for auth service | 2 days | All above |

**Gate**: All auth endpoints return 401 for invalid tokens

### Phase 2: Profile Management (Week 2)

**Goal**: Structured profile CRUD and GDPR deletion

| Task | Duration | Dependencies |
|------|----------|--------------|
| Implement profile CRUD endpoints | 2 days | Phase 1 complete |
| Add encryption for sensitive profile fields | 1 day | Profile endpoints |
| Build GDPR deletion workflow (soft + hard delete) | 2 days | Profile, audit logging |
| Create profile export API (JSON download) | 1 day | Profile read |
| Write integration tests for profile | 2 days | All above |

**Gate**: Profile data persists encrypted, exports correctly, deletes per GDPR timeline

### Phase 3: Frontend Authentication (Week 2-3)

**Goal**: Docusaurus auth UI and state management

| Task | Duration | Dependencies |
|------|----------|--------------|
| Create Docusaurus auth plugin | 2 days | None |
| Build signup/signin React components | 2 days | Auth plugin |
| Implement session persistence (localStorage + cookies) | 1 day | Components |
| Add auth state hook (useAuth) | 1 day | Plugin |
| Write E2E auth tests (Playwright) | 2 days | All above |

**Gate**: Users can sign up, sign in, and sign out from Docusaurus UI

### Phase 4: Personalization Engine (Week 3-4)

**Goal**: Chapter preferences and RAG integration

| Task | Duration | Dependencies |
|------|----------|--------------|
| Build preferences API (get/set per chapter) | 2 days | Phase 2 complete |
| Create background survey component | 2 days | Phase 3 complete |
| Extend RAG chatbot to accept user context | 3 days | Existing RAG code |
| Implement preference-aware content rendering | 2 days | Preferences API |
| Write E2E personalization tests | 2 days | All above |

**Gate**: Personalized content differs based on user background, toggles instantly

### Phase 5: Progress Tracking (Week 4)

**Goal**: Reading progress persistence

| Task | Duration | Dependencies |
|------|----------|--------------|
| Add progress tracking to preferences | 1 day | Phase 4 complete |
| Create dashboard progress view | 2 days | Preferences read |
| Add progress indicators to chapter nav | 1 day | Dashboard |
| Write progress tracking tests | 1 day | All above |

**Gate**: Progress persists across sessions, shows in dashboard

### Phase 6: Security Hardening (Week 5)

**Goal**: Audit logging and compliance verification

| Task | Duration | Dependencies |
|------|----------|--------------|
| Implement audit logging for all auth events | 1 day | Phase 1-4 complete |
| Add security headers middleware | 0.5 day | None |
| Perform security review (OWASP checklist) | 1 day | All above |
| Document incident response procedures | 0.5 day | Audit logs |

**Gate**: All auth events logged, no security vulnerabilities found

---

## Dependencies Graph

```
Phase 1 (Backend Foundation)
    │
    ├─► Phase 2 (Profile Management)
    │           │
    │           └─► Phase 4 (Personalization Engine)
    │                       │
    │                       └─► Phase 5 (Progress Tracking)
    │
    └─► Phase 3 (Frontend Auth)
                │
                └─► Phase 4 (Personalization Engine)
                            │
                            └─► Phase 6 (Security Hardening)
```

---

## Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Better-Auth API changes break integration | LOW | HIGH | Version-lock Better-Auth, abstract auth operations behind interface |
| Docusaurus upgrade breaks auth plugin | MEDIUM | MEDIUM | Use official plugin APIs, minimize monkey-patching, test on Docusaurus upgrades |
| RAG personalization degrades quality | MEDIUM | MEDIUM | A/B test personalized vs standard, collect user feedback, allow toggle |
| GDPR deletion timeline missed | LOW | HIGH | Automated deletion jobs with monitoring alerts, weekly compliance audit |
| Session hijacking / token theft | MEDIUM | HIGH | httpOnly cookies, short access token lifetime, refresh token rotation |
| Scalability: 1,000 concurrent users | LOW | MEDIUM | Load test at 2x target, add connection pooling, consider Redis for sessions |
| User abandonment during signup | MEDIUM | LOW | Track drop-off points, optimize form (progressive disclosure), A/B test |

---

## Rollback Plan

| Scenario | Rollback Action |
|----------|-----------------|
| Auth bug locks users out | Revert to previous deployment, disable Better-Auth calls |
| Profile data corruption | Restore from daily PostgreSQL backup, replay audit log |
| RAG personalization degrades | Disable personalization flag, serve standard content only |
| Security breach | Revoke all sessions, force password reset, enable enhanced logging |

---

## Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Registration completion rate | >90% | /api/auth/signup success / total starts |
| Sign-in latency (p95) | <2s | API endpoint timing |
| Profile API latency (p95) | <500ms | API endpoint timing |
| Personalization toggle latency | <200ms | Frontend UX measurement |
| GDPR deletion compliance | 100% | Automated compliance check |
| Auth-related support tickets | <5/week | Support dashboard |
