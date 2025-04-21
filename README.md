# 🔗 Project Name

A backend service built with Django and integrated with Supabase for storage for PUP-BARK, a lost-and-found platform for constituents of the Polytechnic University of the Philippines.

---

## 📚 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment Variables](#environment-variables)
  - [Running the Project](#running-the-project)
- [API Reference](#api-reference)
- [License](#license)

---

## 📝 Overview

The project’s goal is to create a web platform wherein concerned personnel of the Polytechnic University of the Philippines (PUP) - Manila can facilitate the management of lost and found items of constituents of the university in two months' time. 

Specifically, the project aims to: 
- Allow constituents concerned with the project to view the lost items listing and create a 
request form to claim an item. 
- Provide a claim form detailing information about the claimant for communication purposes 
with the personnel. 
- Allow creation of lost item posts by the assigned administrators detailing the name and 
category of the lost item, the status of the item, a detailed description of the lost item for 
verification, last seen location and time when the item was found, and a photo detailing the 
item. 
- Authorize the administrators to view the claim forms provided by claimants on the platform. 
- Provide administrators the authority to update or edit the details of a post and to delete a lost 
item post if the need arises.

---

## ✨ Features

- Django-based REST API
- Supabase integration for file uploads
- Claim and lost item management
- Custom admin panel

---

## ⚙️ Tech Stack

- **Framework**: Django 5.2
- **Database**: PostgreSQL (Supabase-hosted)
- **Cloud Storage**: Supabase Storage Buckets
- **API Testing**: Postman

---

## 🚀 Getting Started

### 🧰 Prerequisites

- Python 3.10+
- Pipenv
- PostgreSQL
- Supabase account

### 📦 Installation

```bash
git clone https://github.com/zeegma/bark-backend.git
cd bark-backend
pip install -r requirements.txt
```
And you're good to go!

### 🎄 Environment Variables
Create a .env file in the root directory. Fill up the details with your specific secret credentials.

```.env
DB_NAME=name
DB_USER=user
DB_PASSWORD=password
DB_HOST=host
DB_PORT=port

SUPABASE_URL=supabase_url
SUPABASE_KEY=supabase_key
```

### 🏁 Running the Project
To run the project and test its APIs, one can run the following commands:

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

#### Running Scripts
We provided scripts to allow easy manipulation and seeding of our database. Use the following format when running a script:

```bash
python manage.py runscript <script_name>
```

Here are the scripts that you could use:
- flush_admin (drop data from admin table)
- flush_claim (drop data from claim forms table)
- flush_items (drop data from lost items table)
- migrate_and_seed (migrate changes, and seeds all tables)
- migrate_auth (hashes the passwords in the table)
- seed_admin (seed the admin table)
- seed_claim (seed the claim table)
- seed_items (seed the items table)

---

## 🔌 API Reference
Here is the API endpoint guide if you will use these APIs for specific frontend requirements or just for testing.
### 📦 Lost Items

| Method | Endpoint                             | Description                    |
|--------|--------------------------------------|--------------------------------|
| GET    | `/`                                  | Retrieve all lost items        |
| GET    | `/lost-items/`                       | Retrieve all lost items        |
| GET    | `/lost-items/<item_id>/`             | Retrieve a single lost item    |
| POST   | `/lost-items/create/`                | Create a new lost item         |
| PUT    | `/lost-items/<item_id>/edit/`        | Edit a lost item               |
| DELETE | `/lost-items/<item_id>/delete/`      | Delete a lost item             |

---

### 🛡️ Admin

| Method | Endpoint                             | Description                    |
|--------|--------------------------------------|--------------------------------|
| GET    | `/admins/`                           | Get all admins                 |
| GET    | `/admins/<admin_id>/`                | Get details of an admin        |
| POST   | `/admins/register/`                  | Register a new admin           |
| POST   | `/admins/login/`                     | Login an admin                 |
| POST   | `/admins/logout/`                    | Logout the current admin       |
| DELETE | `/admins/<admin_id>/delete/`         | Delete an admin                |

---

### 📋 Claim Form

| Method | Endpoint                             | Description                          |
|--------|--------------------------------------|--------------------------------------|
| GET    | `/claim-forms/`                      | Get all claim forms                  |
| POST   | `/claim-form/create/`                | Create a new claim form              |
| DELETE | `/claimants/delete/`                 | Delete multiple claimants by ID list |

---

### 📊 Admin Dashboard Stats

| Method | Endpoint                             | Description                    |
|--------|--------------------------------------|--------------------------------|
| GET    | `/admin/dashboard/`                  | Get overall dashboard stats    |
| GET    | `/admin/stats/total/`                | Total number of lost items     |
| GET    | `/admin/stats/lost/`                 | Number of unclaimed items      |
| GET    | `/admin/stats/claimed/`              | Number of claimed items        |
| GET    | `/admin/stats/expired/`              | Number of expired items        |
