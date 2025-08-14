# Leave Management System

 **GitHub Repository:**  
[github.com/NiketNannavare/Leave_Management_System](https://github.com/NiketNannavare/Leave_Management_System)

## 📌 Overview

A Mini Leave Management System (MVP) built for assignment purposes.

**Tech Stack:**
- **Backend:** Flask (Python) + SQLite (SQLAlchemy)
- **Frontend:** Static HTML + JavaScript (served from Flask’s `static/` folder)

**Features for HR:**
- Add employees
- Apply for leave
- Approve or reject leave requests
- Track leave balances
- View pending, approved, and rejected applications

---

## ⚙️ Setup Instructions

### 🔹 Backend (Flask)

1. **Install dependencies:**
    ```bash
    pip install flask flask_sqlalchemy flask-cors
    ```

2. **Run the backend:**
    ```bash
    python app.py
    ```

3. **Backend URL:**  
   [http://127.0.0.1:5000](http://127.0.0.1:5000)

### 🔹 Frontend (HTML)

- Frontend files are in the `/static/` folder.
- Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.
- Flask serves `index.html` from the static directory.

**UI Features:**
- Add employees
- Apply for leave
- Approve/Reject leave
- View leave balances
- View Pending, Approved, Rejected applications

---

## 🚦 Edge Cases Handled

- Cannot apply leave before joining date
- Cannot apply with end date before start date
- Cannot apply for more days than available leave balance
- Cannot apply overlapping leave dates
- Cannot approve/reject a leave twice
- Employee not found

---

## 🚀 Potential Improvements

- Add authentication
- Email notifications on approval/rejection
- Support for different leave types (Casual, Sick, etc.)

---

## 📡 API Endpoints

### 🔹 Add Employee

**POST** `/employees`
```json
{
  "name": "test",
  "email": "tst@example.com",
  "department": "IT",
  "joining_date": "2025-01-09"
}
```
**Response:**
```json
{ "message": "Employee added successfully" }
```

---

### 🔹 Apply for Leave

**POST** `/leave/apply`
```json
{
  "employee_id": 1,
  "start_date": "2025-02-10",
  "end_date": "2025-02-12",
  "reason": "Family event"
}
```
**Response (success):**
```json
{ "message": "Leave request submitted" }
```
**Response (failure):**
```json
{ "message": "Leave overlaps with existing request" }
```

---

### 🔹 Approve/Reject Leave

**PUT** `/leave/<leave_id>`
```json
{ "status": "approved" }
```
**Response:**
```json
{ "message": "Leave approved" }
```

---

### 🔹 Check Leave Balance

**GET** `/leave/balance/<employee_id>`
```json
{ "message": "Leave balance: 17" }
```

---

### 🔹 Get Applications by Status

- **GET** `/leave/applications/pending`
- **GET** `/leave/applications/approved`
- **GET** `/leave/applications/rejected`

**Response:**
```json
[
  {
    "leave_id": 4,
    "employee_id": 6,
    "employee_name": "test",
    "department": "IT",
    "start_date": "2025-02-10",
    "end_date": "2025-02-12",
    "reason": "Family event",
    "status": "pending"
  }
]

```
