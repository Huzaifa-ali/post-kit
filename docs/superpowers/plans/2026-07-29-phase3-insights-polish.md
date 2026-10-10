# Post-Kit Desktop UI — Phase 3 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add Analytics (CSV import, dashboard, export), Credits (plan/usage), Notifications (activity feed), and Settings page to complete the app.

**Architecture:** Same patterns as Phase 1-2. Each module: router + service + models. SQLite for analytics storage. Event bus for notification triggers.

**Spec:** `docs/superpowers/specs/2026-07-29-post-kit-ui-design.md`
**Depends on:** Phase 1 + Phase 2 complete

---

## Tasks

1. Analytics Module — Backend (CSV/Excel import, dashboard data, export)
2. Credits Module — Backend (plan display, usage tracking, reset logic)
3. Notifications Module — Backend (CRUD, event-driven creation)
4. Settings Module — Backend (config management, rebuild trigger)
5. Frontend — Analytics, Settings pages + notification dropdown JS
6. Final wiring — Update main.py nav, run all tests, verify full app
