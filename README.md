# 💰 Smart Expense Tracker

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python) ![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi) ![MySQL](https://img.shields.io/badge/MySQL-8.0+-4479A1?style=for-the-badge&logo=mysql) ![TailwindCSS](https://img.shields.io/badge/Tailwind-CSS-38B2AC?style=for-the-badge&logo=tailwind-css)

**Smart Expense Tracker** is a full-stack web application designed to help users manage their finances efficiently. It features a secure authentication system, role-based access control (Admin/User), interactive charts for analysis, and detailed reporting.

---

## 🌟 Key Features

### 🔐 Security & Authentication
- **Secure Login/Signup:** Passwords are hashed using **Bcrypt**.
- **Forgot Password:** OTP-based password reset system via Email.
- **RBAC (Role-Based Access Control):** Separate dashboards for **Admins** and **Users**.

### 💸 Expense Management
- **Track Finances:** Add Income and Expenses with categories.
- **Smart Validation:** Prevents expenses if the balance is insufficient.
- **Pagination:** Efficiently browse large transaction histories.
- **Date Filters:** Filter transactions by Today, Last 7 Days, This Month, etc.

### 📊 Visual Analytics
- **Dashboard:** Real-time updates of Net Balance, Total Income, and Expense.
- **Interactive Charts:** - **Doughnut Chart:** Breakdown of expenses by category.
  - **Bar Chart:** Income vs. Expense comparison.

### ⚙️ Advanced Features
- **Profile Management:** Upload Profile Picture and update details.
- **Export Data:** Download transaction history as **CSV/Excel**.
- **Admin Panel:** Admins can manage users (Promote/Demote) and monitor global transactions.

---

## 📸 Project Screenshots

| **Dashboard** | **Admin Panel** |
| :---: | :---: |
| ![Dashboard](./screenshots/dashboard.png) | ![Admin](./screenshots/admin.png) |

| **Add Transaction** | **Profile Settings** |
| :---: | :---: |
| ![Transaction](./screenshots/transaction.png) | ![Settings](./screenshots/settings.png) |

---

## 🛠️ Tech Stack

* **Backend:** Python, FastAPI, SQLAlchemy
* **Database:** MySQL (PyMySQL)
* **Frontend:** HTML5, Jinja2 Templates, Tailwind CSS, JavaScript
* **Visualization:** Chart.js
* **Tools:** Uvicorn, FastAPI-Mail, Python-Multipart

---

## 🚀 Installation & Setup Guide

Follow these steps to run the project on your local machine.

### 1. Navigate to Project Directory
Open your terminal and navigate to the project folder:
```powershell
cd "C:\Users\91993\OneDrive\Desktop\expanse tracker project"
```

### 2. Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

### 3. Set Up the Database
- Ensure MySQL is installed and running.
- Create a database named `expense_tracker`.
- Update the database connection details in `app/core/config.py`.

### 4. Run Database Migrations
Use Alembic to set up the database schema:
```bash
alembic upgrade head
```

### 5. Set Up Roles
Run the setup script for roles:
```bash
python setup_roles.py
```

### 6. Run the Application
Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The application will be available at `http://localhost:8000`.

---

## 📖 Usage

- **Register/Login:** Create an account or log in with existing credentials.
- **Dashboard:** View your financial summary and charts.
- **Add Transactions:** Record income and expenses.
- **Admin Features:** If you have admin privileges, manage users and view global data.

---

## 🤝 Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

---

## 📄 License

This project is licensed under the MIT License.
