# Research: Authenticated Personalized Learning Module

**Feature**: 005-auth-personalized-learning
**Date**: 2025-12-31

## Better-Auth Python Integration

**Decision**: Use Better-Auth REST API via HTTP wrapper.

**Rationale**: Better-Auth is JavaScript-native. For Python backend:
- Call Better-Auth HTTP endpoints for signup/signin
- Manage JWT sessions synchronously with Better-Auth
- Store user profiles in PostgreSQL, reference Better-Auth user IDs

**Sources**:
- Better-Auth official documentation (better-auth.dev)
- REST API patterns for auth services

---

## Docusaurus Authentication Pattern

**Decision**: Create custom Docusaurus plugin with React Context.

**Rationale**:
- Docusaurus supports custom plugins and React frontend
- AuthProvider wraps app with session state
- localStorage + JWT for persistent sessions
- Sync with backend on page load

**Sources**:
- Docusaurus plugin documentation
- React Context patterns for auth state

---

## RAG Context Injection

**Decision**: Extend existing RAG chatbot with user context parameter.

**Implementation**:
- Add optional `userBackground` field to RAG request
- Include software/hardware preferences in prompt
- Cache personalized responses separately

**Sources**:
- Existing RAG chatbot implementation
- Prompt engineering best practices

---

## Session Management Strategy

**Decision**: JWT access tokens + refresh token cookies.

**Rationale**:
- Access token (15 min) in memory for API calls
- Refresh token (30 days) in httpOnly cookie
- Server validates on each protected request

**Security**:
- Token rotation on refresh
- Short-lived access tokens limit exposure
- httpOnly cookies prevent XSS theft
