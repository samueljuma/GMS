# Gym Management System Database Schema

## Overview

This document outlines the database schema for a Gym Management System, detailing the tables, their attributes, and improvements for better efficiency, flexibility, and maintainability.

---

## 1. Users Table (Enhanced for Scalability & Role Management)

| Column            | Type                          | Description                     |
| ----------------- | ----------------------------- | ------------------------------- |
| `id`              | Primary Key                   | Unique identifier for each user |
| `username`        | String (Unique)               | Used for login                  |
| `email`           | String (Unique)               | Email for communication         |
| `phone_number`    | String (Unique)               | Used for M-Pesa transactions    |
| `role`            | Enum (Admin, Trainer, Member) | Defines user permissions        |
| `profile_picture` | String (Nullable)             | Profile image URL               |
| `dob`             | Date (Nullable)               | Date of birth                   |
| `password`        | String (Hashed)               | Secure password storage         |
| `created_at`      | DateTime                      | User registration timestamp     |
| `updated_at`      | DateTime                      | Last profile update             |

### Improvements:

- **Added `phone_number`** (Essential for M-Pesa transactions)
- **Used Enum for `role`** instead of a string to prevent invalid values
- **Added `created_at` & `updated_at`** to track user account changes

---

## 2. Membership Table (Improved for Plan Flexibility)

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

### Improvements:

- **Replaced `plan` column with `plan_id`** (Linked to a new `Plans` table for easy management)
- **Added `status` column** to indicate active/expired/cancelled memberships
- **Timestamps (`created_at`, `updated_at`)** for tracking changes

---

## 3. Plans Table (NEW for Managing Subscription Plans)

| Column          | Type            | Description                              |
| --------------- | --------------- | ---------------------------------------- |
| `id`            | Primary Key     | Unique identifier                        |
| `name`          | String (Unique) | Plan name (Daily, Monthly, Yearly, etc.) |
| `price`         | Decimal(10,2)   | Cost of the plan                         |
| `duration_days` | Integer         | Number of days the plan lasts            |

### Why This is Better?

- **Flexible** – You can easily add new plans (e.g., Weekly, Quarterly, etc.)
- **No duplicate values** – Instead of storing "Daily" or "Monthly" in multiple rows, you store them once in `Plans`

---

## 4. Attendance Table (Optimized for Daily Presence Tracking)

| Column           | Type                | Description                            |
| ---------------- | ------------------- | -------------------------------------- |
| `id`             | Primary Key         | Unique attendance record ID            |
| `member_id`      | Foreign Key (Users) | Links to the member                    |
| `date`           | Date                | The date of attendance                 |
| `status`         | Boolean             | `True` for present, `False` for absent |
| `checked_in_at`  | DateTime (Nullable) | Check-in timestamp (if present)        |
| `checked_out_at` | DateTime (Nullable) | Check-out timestamp (if present)       |
| `trainer_id`     | Foreign Key (Users) | Trainer who marked attendance          |

### Improvements:

- **Added `trainer_id`** to track which trainer marked attendance
- **Optimized for reports** – Now you can quickly check total present/absent days

---

## 5. Payments Table (Enhanced for Payment Tracking & Verification)

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

### Improvements:

- **Added `status` column** to track if a payment was successful or failed
- **`recorded_by` field** ensures accountability when trainers manually record payments
- **Supports reconciliation** with `transaction_id` for M-Pesa payments

---
