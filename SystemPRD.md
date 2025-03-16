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

---

## 3. Plans Table (NEW for Managing Subscription Plans)

| Column          | Type            | Description                              |
| --------------- | --------------- | ---------------------------------------- |
| `id`            | Primary Key     | Unique identifier                        |
| `name`          | String (Unique) | Plan name (Daily, Monthly, Yearly, etc.) |
| `price`         | Decimal(10,2)   | Cost of the plan                         |
| `duration_days` | Integer         | Number of days the plan lasts            |


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

---
