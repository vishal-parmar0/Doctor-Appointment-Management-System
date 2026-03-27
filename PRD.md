# Product Requirements Document (PRD): MediBook

## 1. Product Overview
**Project Name**: MediBook - Doctor Appointment Management System  
**Tagline**: "Your Personal Health Assistant"  
**Project Version**: 1.0 (Static UI Prototype)

MediBook is a comprehensive, role-based healthcare management platform designed to bridge the gap between patients, healthcare providers (doctors), and administrators. It provides a seamless, high-fidelity user interface for scheduling appointments, managing medical records, and platform oversight.

---

## 2. Core Value Proposition
- **For Patients**: Easy access to top-tier medical specialists with a built-in AI assistant for health tracking.
- **For Doctors**: A streamlined "Virtual Practice" to manage patient loads, schedules, and clinical notes.
- **For Admins**: A bird's-eye view of platform health, security, and doctor verification.

---

## 3. Targeted User Roles
| Role | Primary Objective |
| :--- | :--- |
| **Patient** | Book and track appointments, manage personal medical data, and use MediAI. |
| **Doctor** | Manage daily consultation schedules, view patient histories, and track earnings. |
| **Admin** | Oversight of platform users, doctor credential verification, and system health. |

---

## 4. Key Functional Features

### 🟢 Patient Module
- **Dashboard**: Unified view of health vitals (Heart rate, Sleep, BMI) and active treatments.
- **Find Doctors**: Search by city, name, or specialization with category-based filtering.
- **Appointment Booking**: Multi-step booking modal for selecting time slots and consultation types.
- **MediAI Console**: An interactive, AI-driven panel for quick medical advice and health insights.
- **Medicine Tracker**: Timeline-based tracker for daily drug adherence.
- **Digital Health Folder**: Secure access to past prescriptions and medical reports.

### 🔵 Doctor Module
- **Practice Analytics**: Visual charts showing patient growth and consultation recovery rates.
- **Schedule Planner**: Granular control over daily time slots (Video vs. In-Person).
- **Patient Vault**: Secure database of patients with slide-out clinical history panels.
- **Consultation Management**: Real-time tools to accept/reject or join video consultation meets.
- **Practice Settings**: Customizable consultation fees, slot durations, and "Vacation Mode" toggles.

### 🔴 Admin Module
- **Command Center**: Real-time server performance (CPU/Memory/Latency) and revenue visualizations.
- **Doctor Verification Desk**: A dedicated desk to review uploaded licenses and approve/deny doctors.
- **Registry Management**: Global tables for managing both Doctor and Patient accounts (Block/View/Audit).
- **Core Config**: Platform-wide settings for commission rates and maintenance modes.

---

## 5. Technology Stack
- **Languages**: HTML5, CSS3, JavaScript (ES6+).
- **UI Frameworks**: Bootstrap 5.3.0 (Responsive layouts and standard components).
- **Icons**: Font Awesome 6.4.0 (Professional medical iconography).
- **Fonts**: Google Fonts (Poppins & Montserrat).
- **Interactive Graphs**: Chart.js (Data visualization across all roles).
- **Animations**: AOS (Animate On Scroll) for high-end aesthetic feedback.
- **Graphics**: HTML5 Canvas (Visualizer Orb).

---

## 6. Design System & Aesthetics
- **Primary Color Palette**: 
  - `Royal Blue (#0066FF)` - Core brand color.
  - `Indigo Purple (#7C3AED)` - Secondary/AI intelligence color.
  - `Teal (#06B6D4)` - Health/Eco-system color.
- **Modern UI Elements**: 
  - Glassmorphic panels with `backdrop-filter`.
  - Soft-shadow card layouts for focus.
  - Sub-pixel micro-animations on hover interactions.

---

## 7. Future Roadmap (Backend Implementation)
1. **Database Integration**: Implementation of SQL/NoSQL schemas for persistent User and Appointment data.
2. **Real-time Auth**: JWT-based or Session-based secure authentication.
3. **LLM Integration**: Connecting MediAI to a real Gen-AI API (e.g., OpenAI/Gemini) for true intelligence.
4. **Video API**: Integration of a real WebRTC or Zoom SDK for tele-consultations.
5. **PDF Engine**: Dynamic generation of prescriptions and medical reports on the server side.

---

## 8. Conclusion
MediBook is positioned as a "One-Stop Healthcare Solution" that provides a professional and intuitive experience across all healthcare stakeholders, ensuring medical management is simpler, faster, and more accessible.
