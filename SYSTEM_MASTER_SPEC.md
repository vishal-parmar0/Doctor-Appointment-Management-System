# MediBook – Doctor Appointment Management System: Master Specification

**Project Name:** MediBook  
**Version:** 1.0.0 (Production Core)  
**Status:** Engineering Ready  
**Document Type:** Master System Specification (MSS)

---

## 1. Product Definition

### Business Objective
To provide a high-performance, compliant, and scalable SaaS platform that digitizes the entire lifecycle of medical consultations—from discovery and booking to prescription management and history tracking.

### Healthcare Use Case
A three-tier ecosystem (Patient, Doctor, Admin) designed to reduce operational friction in clinic-based and tele-consultation environments. It ensures that patients can find verified specialists, doctors can manage their practice efficiently, and administrators can maintain platform integrity.

### Primary Users
*   **Patients:** Individuals seeking medical advice, booking, and history access.
*   **Doctors:** Verified medical practitioners managing schedules and patients.
*   **Administrators:** Platform regulators managing user lifecycles and system health.

### Operational Goals
*   **Availability:** 99.9% uptime for appointment booking.
*   **Integrity:** Immutable record-keeping of medical history and prescriptions.
*   **Trust:** 100% verification rate for practitioner profiles.

---

## 2. Full User Journey

### 2.1 Public Discovery (Landing)
*   **First Visit:** User lands on `index.html`. System loads featured specialists and specialization categories.
*   **Search/Filter:** User filters by specialty or search term. Results update dynamically (State Transition: Public → Browsing).

### 2.2 Identity & Access (Auth)
*   **Registration:** User selects role (Patient/Doctor). System persists `User` and `RoleProfile` (Patient/Doctor).
*   **Login:** Handshake with `/api/auth/login`. Returns JWT (24h expiry) and user object.
*   **Role Routing:** Middleware redirects based on `user.role` to `patient-dashboard.html`, `doctor-dashboard.html`, or `admin-dashboard.html`.

### 2.3 Feature Operations
*   **Patient:** Finds doctor → Books Slot → Receives Notification → Attends → Receives Prescription.
*   **Doctor:** Approves Appointment → Consults → Uploads Prescription (Completes Flow).
*   **Admin:** Reviews Doctor Document → Verifies Profile → Monitors Platform Analytics.

### 2.4 Terminal State (Logout)
*   User clicks Logout. System purges LocalStorage (`user`, `token`). Redirects to `login.html`.

---

## 3. Full Information Architecture

| Page | Purpose | Data Dependencies | Actions |
| :--- | :--- | :--- | :--- |
| `index.html` | Hero/Discovery | featured doctors, specialty list | Search, Filter, CTA to Login |
| `login.html` / `register.html` | Identity Management | - | Auth, Password Recovery |
| `patient-dashboard.html` | Patient Home | User profile, recent apps, notifications | Access widgets (apps, rx, search) |
| `doctor-dashboard.html` | Doctor Home | Schedule summary, current status | Manage queue, mark status |
| `admin-dashboard.html` | Control Center | Aggregate system metrics | Verification pipeline access |
| `appointments.html` | History/Management | Appointment list (patient) | Cancel, View Details |
| `prescriptions.html` | Medical Records | Prescription list | Download, Share |
| `doctors.html` | Specialist Search | Filtered doctor list | Book Appointment |
| `profile.html` | Settings | User/Doctor/Patient table | Update Bio, Avatar, Contact |

---

## 4. Full Role System (RBAC)

### 4.1 Patient
*   **Readable:** Doctors (Verified), Own Appointments, Own Prescriptions, Own Medical Records.
*   **Writable:** Own Profile, New Appointments, Messages (to booked doctors).
*   **Restricted:** Cannot view other patients, cannot verify doctors, cannot delete records.

### 4.2 Doctor
*   **Readable:** Own Schedule, Assigned Patients' Medical History.
*   **Writable:** Own Profile (Bio/Fees), Prescriptions, Slot Availability.
*   **Restricted:** Cannot view other doctors' revenue, cannot delete appointments (only cancel).

### 4.3 Administrator
*   **Readable:** System-wide Users, Audit Logs, Analytics, Verification Queue.
*   **Writable:** Verification Status, User Deletion (System Hygiene).
*   **Restricted:** Cannot view private message content (Privacy Safeguard).

---

## 5. Landing Page Production Spec

### 5.1 Hero Section
*   **Input:** Dynamic keyword search.
*   **CTA:** "Book Now" (Routes to Auth if not logged in).
*   **Animation:** AOS (Animate On Scroll) for value proposition cards.

### 5.2 Filters (Advanced Search)
*   **City Filter:** Dropdown filtering `Doctor` table by `city`.
*   **Specialization Cards:** Trigger fetch to `/api/doctor/search?specialty=X`.

### 5.3 CTA Analytics
*   Every CTA click triggers a frontend event (State Log) before navigation.

---

## 6. Full Dashboard Specification

### 6.1 Patient Dashboard
*   **Health Cards:** Real-time summary of upcoming appointments and new prescriptions.
*   **Medicine Tracker:** Frontend-managed schedule of current Rx course.
*   **Search Shortcut:** `Ctrl + K` global focus on doctor search.
*   **Polling Engine:** 30s interval for `/api/notifications/unread-count`.

### 6.2 Doctor Dashboard
*   **Queue Management:** Priority list of 'Pending' and 'Today's' appointments.
*   **Patient Record Access:** One-click retrieval of patient history before consultation.
*   **Prescription Portal:** Standardized form for ICD-10/Generic-Medicine entry.

### 6.3 Admin Dashboard
*   **Verification Waterfall:** List of doctors awaiting credential review.
*   **Platform Revenue:** Calculated via `SUM(consultation_fee * commission_rate)`.
*   **User Traffic:** Daily Active Users (DAU) and New Signups monitoring.

---

## 7. Full Button Inventory

| Button Label | Page | Trigger Event | Backend Endpoint | DB Interaction |
| :--- | :--- | :--- | :--- | :--- |
| `Accept` | Doctor Dashboard | click | `PUT /api/doctor/appointments/accept/{id}` | Update `Appointment.status` |
| `Upload Prescription` | Doctor Apps | submit | `POST /api/doctor/prescriptions` | Create `Prescription`, Complete `Appointment` |
| `Book Appointment` | Doctor Detail | submit | `POST /api/patient/appointments` | Create `Appointment`, Notify Doctor |
| `Verify` | Admin Verif | click | `PUT /api/admin/verify-doctor/{id}` | Update `Doctor.verification_status` |
| `Mark All Read` | Navbar DD | click | `PUT /api/notifications/read-all` | Update `Notification.is_read` |
| `Update Profile` | Profile | submit | `PUT /api/patient/profile/update` | Update `User` table |

---

## 8. Full Icon Behavior Specification

### 8.1 Search Icon (`fa-search`)
*   **Hover:** Changes color to `--primary`.
*   **Click:** Focuses `#globalSearch`.

### 8.2 Message/Notification Icons
*   **Badge Logic:** Display `absolute` red pill if unread count > 0.
*   **Dropdown State:** `toggleMessagesDropdown(event)` stops propagation to document levels.
*   **Empty State:** Custom CSS placeholder (`fa-bell-slash`) with centered text.

### 8.3 Profile Avatar
*   **Initials Logic:** Automated initials generation if `avatar_url` is null.
*   **Dropdown:** Contains Settings, Profile, and Logout.

---

## 9. Full API Contract

### Authentication Domain
*   **POST** `/api/auth/register`
    *   **Body:** `{email, password, full_name, role, ...}`
    *   **Success:** 201 Created
*   **POST** `/api/auth/login`
    *   **Success:** 200 OK + `{"token": "JWT_TOKEN", "user": {}}`

### Patient Domain
*   **GET** `/api/patient/appointments` - Fetch history.
*   **POST** `/api/patient/appointments` - Book new.

### Notification/Message Domain
*   **PUT** `/api/notifications/read-all` - Bulk update status.
*   **PUT** `/api/messages/read-all` - Bulk update inbox.

---

## 10. Full Database Specification (MySQL)

### Table: `users`
*   **Primary Key:** `id` (INT, AI)
*   **Fields:** `email` (Unique), `password_hash`, `full_name`, `role`, `created_at`.
*   **Indexes:** `idx_email` (BTREE).

### Table: `appointments`
*   **FKs:** `patient_id` → `users.id`, `doctor_id` → `users.id`.
*   **Constraints:** Cascade on delete to maintain history cleanup.
*   **Status Enum:** `pending`, `confirmed`, `completed`, `cancelled`.

### Table: `notifications`
*   **Fields:** `patient_id`, `title`, `message`, `type`, `is_read`.
*   **Persistence:** Notifications expire after 90 days (Auto-cleanup query).

---

## 11. State Management Rules

### Appointment Lifecycle
1.  **Pending:** Created by patient.
2.  **Confirmed/Cancelled:** Updated by doctor.
3.  **Completed:** Transitioned automatically upon Prescription upload.

### Message State
*   **Sent:** Initial entry in DB.
*   **Read:** Status update triggered by `GET /thread/{id}`.

---

## 12. Full Alert Engine Logic

*   **Generation:** Triggered by DB hooks on appointment status change.
*   **Persistence:** All alerts stored in `notifications` table; local badges updated via polling.
*   **Priority:** `appointment_cancelled` triggers high-visibility red badge.

---

## 13. Full Messaging Logic

*   **Security:** Patients can only message a doctor if an active/past appointment link exists (`Appointment.id` found).
*   **Ordering:** Messages grouped by conversation ID and ordered by `timestamp` ASC.

---

## 14. Security Architecture

*   **JWT Handshake:** Bearer token required in `Authorization` header for all `/api/` calls (except login/register).
*   **Password Entropy:** Bcrypt hashing with salt rounds.
*   **Sanitization:** SQL Alchemy ORM prevents SQL injection.
*   **Role Middleware:** Server-side verification of `get_jwt_identity()['role']` for every protected route.

---

## 15. Failure Handling

*   **401 Unauthorized:** Purge LocalStorage and force redirect to login.
*   **500 Internal Error:** Standardized JSON response with error mask.
*   **Empty State:** Consistent icon-based UI for 0 results (Standardized in `shared_navbar.js`).

---

## 16. Performance Rules

*   **Pagination:** 20 records per page for `doctors.html`.
*   **Lazy Loading:** Avatars and heavy assets load on viewport entry.
*   **DB Optimization:** Indexed `patient_id` and `doctor_id` on appointments table.

---

## 17. Deployment & DevOps

*   **Environment:** Production requires `.env` with `FLASK_DEBUG=0`.
*   **Secrets:** `SECRET_KEY` and `JWT_SECRET_KEY` must be rotated bi-annually.
*   **Concurrency:** Gunicorn/Nginx setup for production scale.

---

## 18. Future Scalability (Engineering Roadmap)

*   **Video Module:** Integration with WebRTC for real-time video consults.
*   **Payment Gateway:** Stripe/Razorpay integration for consultation fee processing.
*   **AI Triage:** Pre-consultation symptom checker for patient priority.

---

## 19. System Intelligence (Logic Not in Prompt)

*   **Automatic Slate Cleanup:** System reconciles "Pending" appointments older than 24h as "Expired".
*   **Initials Engine:** Advanced regex-based initials generation handled in JS to save server compute.
*   **Event Propagation Guard:** Universal click-interceptor for dropdown persistence.
*   **Soft Delete:** User deletion is a "soft" flag to maintain medical history logs for legal compliance.
