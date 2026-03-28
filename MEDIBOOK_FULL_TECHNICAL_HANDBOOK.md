# MediBook – Technical Implementation & Product Handbook (Deep Detail)

This document provides a low-level, granular specification of every file, function, UI component, and interaction within the MediBook system.

---

## 1. Full System Architecture & File Tree

### 1.1 Project Structure
```text
Doctor-Appointment-Management-System/
├── backend/
│   ├── app.py                      # Flask Application Entry Point & Configuration
│   ├── config.py                   # Environment-centric Application Settings
│   ├── models/
│   │   └── models.py               # SQLAlchemy Database Schemas (User, Doctor, Appt, etc.)
│   ├── routes/
│   │   ├── admin_routes.py         # Verification pipeline, user mgmt, platform stats
│   │   ├── auth_routes.py          # JWT logic, Login/Register/ChangePwd
│   │   ├── doctor_routes.py        # Schedule mgmt, RX upload, Dashboard stats
│   │   ├── message_routes.py       # P2P conversation logic, unread tracking
│   │   ├── notification_routes.py  # System alerts, polling, bulk-read updates
│   │   └── patient_routes.py       # Booking, record retrieval, profile updates
│   └── .env                       # Secrets, DB Credentials, Environment Flags
├── frontend/
│   ├── assets/                     # Professional medical photography and iconography
│   ├── admin-dashboard.html        # Platform metrics and system control center
│   ├── doctor-dashboard.html        # Clinical schedule and patient queue manager
│   ├── patient-dashboard.html       # Individual health portal and booking gateway
│   ├── index.html                  # High-conversion medical landing page
│   ├── login.html / register.html   # Authenticated entry points
│   ├── doctors.html                # Multi-parameter doctor search and discovery
│   ├── prescriptions.html          # Immutable record retrieval for patients
│   ├── shared_navbar.js            # Modularized Central Interface Logic
│   └── ...                         # Feature-specific pages (Apps, Records, Settings)
├── SYSTEM_MASTER_SPEC.md           # Master Product Specification
└── MEDIBOOK_FULL_HANDBOOK.md       # (This Document)
```

---

## 2. Granular Frontend Specifications

### 2.1 The Global `shared_navbar.js` (System Brain)
This file is the single source of truth for navigation across every page.
*   **Initials Generator:** Uses `.split(' ')` and `.map(n => n[0])` to derive a 2-character avatar if no image is present.
*   **Event Propagation Control:** All dropdown click handlers (`onclick`) use `e.stopPropagation()` to prevent the document-level "click outside to close" logic from firing prematurely.
*   **Real-time Polling (`setInterval`):** Synchronizes badge counts every 30 seconds for local notifications and messages.
*   **Search Intercept (`Ctrl + K`):** Global event listener focuses search input, overriding browser default shortcuts.
*   **Micro-States:**
    *   **Loading:** SVG CSS Spinner shows during async fetch.
    *   **Error:** Orange "Circle Exclamation" icon if API is unreachable.
    *   **Empty:** Standardized icons (`fa-comment-slash`, `fa-bell-slash`) for 0-result states.

### 2.2 Landing Page (`index.html`) Detailed Sections
*   **Hero Unit:** Uses a search-first design philosophy. Input triggers results on `doctors.html`.
*   **Department Carousel:** Displays 6 cardiology, pediatrics, etc. categories with distinct icons.
*   **Doctor Cards:** Dynamically rendered based on verification status (`verified` only).
*   **CTA logic:** "Get Started" buttons contextually redirect based on whether a `token` exists in LocalStorage.

### 2.3 Dashboard UI Modular specs
*   **Patient Dashboard:**
    *   **Stats Grid:** Total Appointments, Active Prescriptions, Health History Count.
    *   **Doctor Finder Widget:** Top-rated specialists based on platform ranking.
*   **Doctor Dashboard:**
    *   **Appointment Queue:** List view with "Accept" and "Join" actions.
    *   **Clinical Summary:** Real-time patient count and today's schedule summary.

---

## 3. Detailed Backend Logic & Data Integrity

### 3.1 Advanced Database Interaction
*   **Conversation Logic:** Messages don't just store IDs. The `GET /api/messages/` endpoint groups results by `other_id` to build a "Thread" view from a flat table.
*   **Soft Deletion Safeguard:** The verification system uses a `verification_status` ENUM (`pending`, `verified`, `rejected`) rather than deleting doctor rows to maintain historical appointment records.
*   **Prescription Integrity:** When a prescription is uploaded, the system validates that the `doctor_id` matches the appointment being completed (Role Validation).

### 3.2 Secure API Routing Logic
*   **JWT Handshake:** 
    *   Front-end: `localStorage.getItem('token')`
    *   Back-end: `@jwt_required()` decorator extracts identity payload from Header.
*   **CORS Policy:** Explicitly allows cross-origin requests from the browser while maintaining credential security.

---

## 4. "Small Things" - Edge Case & UI Excellence

### 4.1 UI Component Behaviors
*   **Button States:** All buttons use `:active` transform scale (`0.98`) to provide tactile feedback.
*   **Dropdown Alignment:**
    *   `profileDropdown`: Aligned to right: `20px` to match avatar edge.
    *   `notificationsDropdown`: Width: `340px` to accommodate long message titles.
*   **Badge Redundancy:** If the unread count is `0`, the `badge-notify` span is set to `display: none` rather than showing a '0'.

### 4.2 State Transitions
*   **Login → Dashboard:** Smooth redirect using `window.location.href`. Profile initials are pre-calculated and cached to avoid flicker during the first fetch.
*   **Mark Read Logic:** Notification `is_read` updates in the DB immediately on click, then triggers a local UI refresh without reloading the page.

---

## 5. Security & Technical Safeguards

*   **Input Cleansing:** Flask's `request.get_json()` coupled with ORM models ensures no raw strings hit the DB.
*   **Token Expiry Handle:** If a 401 is received from any fetch call, the user is redirected to `login.html` automatically within the catch block of `shared_navbar.js`.

---

## 6. Detailed Dashboard Function Overviews

### 6.1 Administrator Panel Metrics
*   **User Management:** Admins see full email-list for audit, but passwords remain salted/hashed and inaccessible (Zero Knowledge principle).
*   **Analytics Engine:** Calculations for revenue share are performed at the DB level (`db.func.sum`) to ensure speed and accuracy.

### 6.2 Doctor Verification Pipeline
*   Doctor uploads credentials (simulated via registration city/fee).
*   Admin reviews. Verification unlocks the doctor's visibility in the Patient Discovery (Landing) area.

---

## 7. Performance & Optimization Specs

*   **Custom Scrollbars:** Optimized CSS for the Message/Notification lists to provide a "Mobile App" feel on desktop.
*   **Polling Health:** Badge polling stops when the tab is inactive (Visibility API suggestion) for battery and bandwidth efficiency.
