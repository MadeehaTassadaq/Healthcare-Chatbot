# Data Model: Authenticated Personalized Learning Module

## Entities

### User

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Unique user identifier |
| email | VARCHAR(255) | UNIQUE, NOT NULL | User email (immutable after creation) |
| password_hash | VARCHAR(255) | NOT NULL | bcrypt hash of password |
| better_auth_id | VARCHAR(255) | UNIQUE | Reference to Better-Auth user |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Account creation time |
| last_login_at | TIMESTAMP | NULL | Last successful sign-in |
| deleted_at | TIMESTAMP | NULL | Soft delete timestamp |
| profile_data | JSONB | NOT NULL, DEFAULT '{}' | Structured profile (see below) |

**Indexes**:
- `idx_user_email` on email (unique constraint)
- `idx_user_better_auth_id` on better_auth_id
- `idx_user_deleted_at` on deleted_at (for GDPR queries)

---

### UserProfile (embedded in User.profile_data)

```json
{
  "software": {
    "languages": ["string"],
    "frameworks": ["string"],
    "tools": ["string"],
    "experienceLevel": "beginner" | "intermediate" | "advanced"
  },
  "hardware": {
    "platforms": ["string"],
    "sensors": ["string"],
    "actuators": ["string"],
    "experienceLevel": "beginner" | "intermediate" | "advanced"
  }
}
```

**Validation Rules**:
- experienceLevel must be one of: beginner, intermediate, advanced
- All arrays must have at least one element when set
- Null values allowed (user hasn't specified)

---

### Session

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Session identifier |
| user_id | UUID | NOT NULL, FK(user.id) | Reference to User |
| access_token | VARCHAR(500) | NOT NULL | JWT access token (hashed) |
| refresh_token_hash | VARCHAR(255) | NOT NULL | Hashed refresh token |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Session creation |
| expires_at | TIMESTAMP | NOT NULL | Access token expiration |
| last_used_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last activity |
| ip_address | INET | NULL | Client IP for audit |
| user_agent | VARCHAR(500) | NULL | Client user agent |

**Indexes**:
- `idx_session_user_id` on user_id
- `idx_session_access_token_hash` on access_token (hashed)
- `idx_session_expires_at` on expires_at (cleanup queries)

---

### ChapterPreference

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID | PRIMARY KEY | Preference identifier |
| user_id | UUID | NOT NULL, FK(user.id) | Reference to User |
| chapter_slug | VARCHAR(255) | NOT NULL | Docusaurus chapter ID |
| personalized | BOOLEAN | NOT NULL, DEFAULT FALSE | Personalization enabled |
| progress | VARCHAR(20) | NOT NULL, DEFAULT 'not-started' | not-started, in-progress, completed |
| last_position | INTEGER | NOT NULL, DEFAULT 0 | Scroll position / section index |
| completed_at | TIMESTAMP | NULL | Completion timestamp |
| created_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Preference creation |
| updated_at | TIMESTAMP | NOT NULL, DEFAULT NOW() | Last modification |

**Indexes**:
- `idx_chapter_pref_user_chapter` on (user_id, chapter_slug) UNIQUE
- `idx_chapter_pref_progress` on progress (for dashboard queries)

**Validation Rules**:
- progress must be one of: not-started, in-progress, completed
- chapter_slug must match existing Docusaurus chapter pattern

---

## State Transitions

### User Account Lifecycle

```
ACTIVE --(delete request)--> PENDING_DELETION --(24h)--> DELETED --(7d)--> PURGED
     |                             |
     |-- re-auth required          |-- soft delete (visible to user)
                                   |-- hard delete (permanent)
```

### Chapter Preference Lifecycle

```
not-started --(first visit)--> in-progress --(completion)--> completed
                   |                              |
                   |-- user navigates chapter     |-- auto-mark on scroll
                   |-- manual toggle              |-- manual toggle allowed
```

---

## Relationships Diagram

```
User (1) ────── (n) Session
  |
  └─ (n) ChapterPreference

Session: Each user can have multiple sessions (device/browser combinations)
ChapterPreference: Each user has independent preferences per chapter
```

---

## Audit Trail Schema

| Field | Type | Description |
|-------|------|-------------|
| id | UUID | Event identifier |
| user_id | UUID | Target user (nullable for anonymous) |
| event_type | VARCHAR(50) | signup, signin, signout, profile_update, delete, etc. |
| event_data | JSONB | Event-specific details (sanitized) |
| ip_address | INET | Client IP |
| user_agent | VARCHAR(500) | Client user agent |
| created_at | TIMESTAMP | Event timestamp |

**Retention**: 365 days for compliance
