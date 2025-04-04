# Gym Management System (GMS)

The **Gym Management System (GMS)** is a backend API built with **Django** and **Django REST Framework (DRF)**. It provides a robust solution for managing gym operations, including user management, subscription plans, attendance tracking, and payment processing. The system is designed with scalability, security, and maintainability in mind.

---

## Features
### 1. User Management
- **Roles**: Users can have one of three roles:
  - **Admin**: Full access to manage users, subscriptions, payments, and attendance.
  - **Trainer**: Manage members, mark attendance, and record payments.
  - **Member**: View their profile, attendance, and payment history.
- **Authentication**: Secure JWT-based authentication with tokens stored in HTTP-only cookies.
- **Registration**:
  - Members can self-register.
  - Admins and Trainers can add new users.
- **Approval Workflow**:
  - Self-registered users require approval by Admins or Trainers.

### 2. Subscription Management
- **Plans**: Admins can create, update, and delete subscription plans (e.g., daily, monthly).
- **Subscriptions**: Members can subscribe to plans. Subscriptions are tracked with start and end dates.

### 3. Attendance Tracking
- Trainers or Admins can mark attendance for members.
- Prevents duplicate attendance records for the same day.

### 4. Payment Processing
- **Payment Methods**:
  - **M-Pesa**: Mobile payment integration using STK Push.
  - **Cash**: Manual payment recording.
  - **Other**: Easily extendable to support other payment methods.
- **Payment Records**: Tracks payment details including amount, method, and status.

### 5. Role-Based Access Control
- Permissions are enforced at both view and object levels.
- Ensures users can only access resources relevant to their roles.

### 6. Error Handling
- Provides standardized error responses.
- Custom exception handler and renderer used across the system.

---

## API Documentation

### Authentication
- **Register**: `POST /api/auth/register/`
- **Login**: `POST /api/auth/login/`
- **Logout**: `POST /api/auth/logout/`
- **Refresh Token**: `POST /api/auth/refresh/`

### User Management
- **List Users**: `GET /api/users/`
- **Create User**: `POST /api/users/`
- **Approve User**: `POST /api/users/<id>/approve/`
- **Update User**: `PUT /api/users/<id>/`
- **Delete User**: `DELETE /api/users/<id>/`

### Subscription Management
- **List Plans**: `GET /api/subscriptions/plans/`
- **Create Plan**: `POST /api/subscriptions/plans/`
- **Delete Plan**: `DELETE /api/subscriptions/plans/<id>/`
- **List Subscriptions**: `GET /api/subscriptions/`

### Attendance Tracking
- **Mark Attendance**: `POST /api/attendance/mark-member-attendance/`
- **Fetch Attendance**: `GET /api/attendance/fetch-attendance/`

### Payment Processing
- **Initiate Payment**: `POST /api/payments/initiate-payment/`

#### Payload Example:
```json
{
  "member": 3,
  "phone_number": "254798114462",
  "plan": 3,
  "payment_method": "M-Pesa",
  "description": "Payment of xx",
  "reference": "Test"
}
```

- **Fetch Payments**: `GET /api/payments/fetch-records/`

---

## Code Structure

```
users/           # Handles user management (registration, login, roles)
subscriptions/   # Manages subscription plans and member subscriptions
attendance/      # Tracks member attendance
payments/        # Handles payment processing and records
```

### Custom Utilities
- **Permissions**: Role-based access control - `api/utils/permissions.py`
- **Exception Handling**: Standardized error responses - `api/utils/exception_handler.py`
- **Custom Renderers**: JSON renderer for consistent API responses - `api/utils/renderers.py`

---
## [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
```
   ©2025 Copyright Samuel Juma

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
   ```


