---
description: How to run the MediBook Doctor Appointment System
---

### Prerequisites
1.  **MySQL Server**: Ensure MySQL is running on `localhost`.
2.  **Database**: Create a database named `medibook`.
    ```bash
    mysql -u root -pentersql -e "CREATE DATABASE IF NOT EXISTS medibook;"
    mysql -u root -pentersql medibook < backend/database/schema.sql
    ```

### Step 1: Start the Backend
// turbo-all
1. Navigate to the project root and start the Flask server:
   ```bash
   export PYTHONPATH=$PYTHONPATH:$(pwd)/backend && python3 backend/app.py
   ```
   *The backend will run on http://localhost:5000*

### Step 2: Open the Frontend
2. Serve the frontend using Python's http.server. Go to the `frontend` folder and run this:
   ```bash
   cd frontend
   python3 -m http.server 5500
   ```
3. Open `http://localhost:5500/index.html` in your web browser.

### Step 3: Test the Flow
- **Register** a new Patient and a new Doctor.
- **Admin Verification**:
  - Go to `login.html` and use the admin credentials from `schema.sql`.
  - Navigate to **Verification Desk** and approve the new Doctor.
- **Booking**:
  - Login as the Patient.
  - Go to **Find Doctors** and book a slot with the verified Doctor.
- **Doctor Confirmation**:
  - Login as the Doctor.
  - Go to **Appointments** and accept the booking.
