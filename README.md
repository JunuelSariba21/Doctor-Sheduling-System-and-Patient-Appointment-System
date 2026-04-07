# 🏥 Doctor Scheduling System (DSS)
**Project Status — [APRIL 7, 2026]**

A web-based **Doctor Scheduling System** built with **Flask, SQLite, Bootstrap, and JavaScript**.

The system allows administrators to manage doctors, assign availability schedules, edit schedules through modal forms, delete doctors or individual slots, and support patient booking synchronization.

---

# 🚀 Features

## ✅ Doctor Management
- Add new doctors
- View all doctors in table format
- Edit doctor names
- Delete doctors with all associated schedules

## ✅ Availability Management
- Add doctor availability by **date and time**
- Prevent duplicate schedule entries using SQLite unique constraints
- View all schedules in a clean dashboard table
- Edit existing schedule slots
- Delete individual schedule slots

## ✅ Booking Support
- Book available doctor slots
- Release booked slots
- Prevent double booking
- Synchronize slot updates with Patient Appointment System (PAS)

## ✅ User Interface
- Clean **Bootstrap 5 dashboard**
- Modal-based editing form
- Bootstrap icon buttons for actions
- Auto-refresh doctor table after CRUD operations
- Responsive layout for desktop and mobile

## ✅ Backend API Routes
### Doctor Routes
- `POST /doctor` → Add doctor
- `GET /doctors` → Get all doctors
- `PUT /doctor/<id>` → Edit doctor
- `DELETE /doctor/<id>` → Delete doctor

### Availability Routes
- `POST /availability` → Add availability
- `GET /doctors/full` → Get doctors with schedules
- `PUT /edit-schedule` → Edit doctor + slot
- `POST /delete-slot` → Delete specific slot

### Booking Routes
- `POST /book-slot`
- `POST /release-slot`

---

# 🛠️ Tech Stack
- **Backend:** Flask (Python)
- **Database:** SQLite
- **Frontend:** HTML, Bootstrap 5, JavaScript
- **Icons:** Bootstrap Icons

---

# 📂 Project Structure
```bash
project/
│
├── app.py
├── doctor.db
├── templates/
   └── index.html


# 🧑‍⚕️ Patient Appointment System (PAS)
**Project Status — [APRIL 7, 2026]**

A web-based **Patient Appointment System** built with **Flask, SQLite, Bootstrap, JavaScript, and REST API integration**.

The system allows patients or staff to book doctor appointments by selecting available schedules from the **Doctor Scheduling System (DSS)**.  
It supports real-time slot synchronization, cancellation, and automatic release of doctor availability.

---

# 🚀 Features

## ✅ Appointment Booking
- Enter patient name
- Select doctor from DSS
- View only available doctor slots
- Book appointments in real time
- Prevent booking already reserved slots

## ✅ Appointment Management
- View all booked appointments
- Refresh appointment table
- Cancel appointments
- Automatically release cancelled slots back to DSS

## ✅ DSS Integration
- Fetch doctors directly from DSS API
- Fetch doctor schedules from DSS
- Synchronize slot booking with DSS
- Synchronize cancellation with DSS
- Prevent double booking across systems

## ✅ User Interface
- Bootstrap 5 clean responsive UI
- Doctor dropdown selection
- Dynamic slot dropdown
- Appointment table view
- Instant refresh after booking/cancellation

---

# 🔗 API Integration Flow
The PAS communicates with DSS through REST APIs.

## 📥 Fetch Data
- `GET /doctors`
- `GET /doctor/<id>`

## 📤 Sync Booking
- `POST /book-slot`

## 🔄 Sync Cancellation
- `POST /release-slot`

This ensures both systems always stay synchronized.

---

# 🛠️ Tech Stack
- **Backend:** Flask (Python)
- **Database:** SQLite
- **Frontend:** HTML, Bootstrap 5, JavaScript
- **External API:** DSS Flask REST API
- **HTTP Client:** Python Requests

---

# 📂 Project Structure
```bash
PAS/
│
├── app.py
├── appointment.db
├── templates/
    └── index.html
