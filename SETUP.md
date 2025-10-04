# WakaFine Setup Guide

This guide provides instructions on how to set up and run the WakaFine bus ticketing system.

## 1. Installation

First, install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

Next, install the required Node.js packages using npm:

```bash
npm install
```

## 2. Database Setup

Once the dependencies are installed, apply the database migrations:

```bash
python manage.py migrate
```

## 3. Create Admin User

To create an admin user, run the following script:

```bash
python create_admin.py
```

## 4. Seed the Database

To populate the database with sample data, including routes, buses, and users, run the following script:

```bash
python seed_data.py
```

## 5. Run the Development Server

To run the development server, use the following command:

```bash
python manage.py runserver
```

The application will be accessible at `http://127.0.0.1:8000`.

## 6. User Credentials

Here are the credentials for the default users:

*   **Admin:**
    *   **Username:** `admin`
    *   **Password:** `admin@1234`

*   **Staff:**
    *   **Username:** `staff`
    *   **Password:** `staff123`

*   **Customer:**
    *   **Username:** `customer`
    *   **Password:** `customer123`
