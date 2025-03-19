# Gym Management System Database Schema

## Overview

This document outlines the database schema for a Gym Management System, detailing the tables, their attributes, and improvements for better efficiency, flexibility, and maintainability.

---

## 1. Users Table

| Column            | Type                          | Description                                                             |
| ----------------- | ----------------------------- | ----------------------------------------------------------------------- |
| `id`              | Primary Key                   | Unique identifier for each user                                         |
| `username`        | String (Unique)               | Used for login                                                          |
| `email`           | String (Unique)               | Email for communication                                                 |
| `phone_number`    | String (Unique)               | Used for M-Pesa transactions                                            |
| `role`            | Enum (Admin, Trainer, Member) | Defines user permissions                                                |
| `profile_picture` | String (Nullable)             | Profile image URL                                                       |
| `dob`             | Date (Nullable)               | Date of birth                                                           |
| `password`        | String (Hashed)               | Secure password storage                                                 |
| `created_at`      | DateTime                      | User registration timestamp                                             |
| `updated_at`      | DateTime                      | Last profile update                                                     |
| `added_by`        | Foreign Key (Users, Nullable) | ID of the user who added this user (Nullable for self-registered users) |
| `approved_by`     | Foreign Key (Users, Nullable) | ID of the user who approved this user                                   |
| `self_registered` | Boolean (Users, default=True) | Whether user is self-registered                                         |

---

## 2. Membership Table 

| Column       | Type                              | Description                   |
| ------------ | --------------------------------- | ----------------------------- |
| `id`         | Primary Key                       | Unique membership ID          |
| `member_id`  | Foreign Key (Users)               | Links to the gym member       |
| `plan_id`    | Foreign Key (Plans)               | Connects to a membership plan |
| `start_date` | Date                              | Subscription start date       |
| `end_date`   | Date                              | Subscription expiration date  |
| `status`     | Enum (Active, Expired, Cancelled) | Membership state              |
| `created_at` | DateTime                          | Record creation timestamp     |
| `updated_at` | DateTime                          | Last modification             |

---

## 3. Plans Table

| Column          | Type            | Description                              |
| --------------- | --------------- | ---------------------------------------- |
| `id`            | Primary Key     | Unique identifier                        |
| `name`          | String (Unique) | Plan name (Daily, Monthly, Yearly, etc.) |
| `price`         | Decimal(10,2)   | Cost of the plan                         |
| `duration_days` | Integer         | Number of days the plan lasts            |

---

## 4. Attendance Table

| Column           | Type                | Description                            |
| ---------------- | ------------------- | -------------------------------------- |
| `id`             | Primary Key         | Unique attendance record ID            |
| `member_id`      | Foreign Key (Users) | Links to the member                    |
| `date`           | Date                | The date of attendance                 |
| `status`         | Boolean             | `True` for present, `False` for absent |
| `checked_in_at`  | DateTime (Nullable) | Check-in timestamp (if present)        |
| `checked_out_at` | DateTime (Nullable) | Check-out timestamp (if present)       |
| `trainer_id`     | Foreign Key (Users) | Trainer who marked attendance          |

---

## 5. Payments Table

| Column           | Type                              | Description                            |
| ---------------- | --------------------------------- | -------------------------------------- |
| `id`             | Primary Key                       | Unique payment ID                      |
| `member_id`      | Foreign Key (Users)               | Member making the payment              |
| `amount`         | Decimal(10,2)                     | Payment amount                         |
| `payment_method` | Enum (Cash, M-Pesa)               | Payment type                           |
| `transaction_id` | String (Unique, Nullable)         | M-Pesa transaction ID (if applicable)  |
| `recorded_by`    | Foreign Key (Users)               | Admin/Trainer who recorded the payment |
| `status`         | Enum (Pending, Completed, Failed) | Payment state                          |
| `created_at`     | DateTime                          | Payment timestamp                      |

---

# Gym Management System API Endpoints

## 1. User Authentication & Registration

Handles user sign-up, login, and authentication.

### Endpoints:

- **POST** `/api/auth/register/` - Registers a new user (Member, Trainer, or Admin).
- **POST** `/api/auth/login/` - Logs in a user and returns an access token.
- **POST** `/api/auth/refresh/` - Refreshes the authentication token.
- **POST** `/api/auth/logout/` - Logs out the user by invalidating the token.
- **POST** `/api/auth/reset-password/` - Sends a password reset request.

## 2. User Management

Admins and trainers can manage users (Members and Trainers).

### Endpoints:

- **POST** `/api/users/` - Create a new user (Trainer or Member). (Admin/Trainer Only)
- **GET** `/api/users/` - Retrieve a list of all users. (Admin/Trainer Only)
- **GET** `/api/users/<int:pk>/` - Retrieve a specific user by ID. (Admin/Trainer Only)
- **PUT** `/api/users/<int:pk>/` - Update user details. (Admin/Trainer Only)
- **DELETE** `/api/users/<int:pk>/` - Delete a user. (Admin Only)

## 3. Membership Management

Handles gym subscription plans and renewals.

### Endpoints:

- **GET** `/api/subscriptions/plans/` - Retrieve available membership plans.
- **POST** `/api/subscriptions/subscribe/` - Subscribe a member to a plan
- **GET** `/api/subscriptions/<int:member_id>/` - Retrieve a user's subscription details.
- **PUT** `/api/subscriptions/<int:member_id>/renew/` - Renew a membership subscription.

## 4. Attendance Tracking

Records and tracks gym member attendance.

### Endpoints:

- **POST** `/api/attendance/check-in/` - Mark attendance when a member checks in. (Trainer/Admin Only)
- **GET** `/api/attendance/history/?member_id=<int>` - Retrieve attendance records for a specific member.
- **GET** `/api/attendance/summary/?start_date=<date>&end_date=<date>` - Get attendance reports.

## 5. Payment System

Handles manual and M-Pesa payments for subscriptions.

### Endpoints:

- **POST** `/api/payments/initiate/` - Initiate an M-Pesa payment via STK push.
- **POST** `/api/payments/verify/` - Verify M-Pesa payment status.
- **POST** `/api/payments/manual/` - Record a manual cash payment. (Trainer/Admin Only)
- **GET** `/api/payments/history/?member_id=<int>` - Retrieve payment history for a user.

## 6. Role-Based Access Control

- **Admins:** Manage users, trainers, payments, and gym data.
- **Trainers:** Manage attendance, schedules, add new members, record manual payments, and send STK push requests.
- **Members:** View their profiles, attendance, and payments.

## Authentication & Security

- All endpoints (except registration and login) require authentication.
- Role-based permissions determine access to certain routes.
- JWT tokens are used for authentication and must be passed in the request via `cookies` header.
