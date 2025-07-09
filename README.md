# 🧪 Testcase Management System

A web-based system for managing and organizing test cases, built with **Django** and **MySQL**. This system enables users to upload standardized Excel files for test cases, store metadata, track execution statuses (Pass, Fail, Ongoing), and categorize tests by group (e.g., Mastercard, Visacard, etc.).

## 🚀 Features

- ✅ Upload and parse Excel files for test cases
<img width="1076" alt="upload" src="https://github.com/user-attachments/assets/9259384b-1b76-4ef9-855c-c2b4c180ab1a" />

- 📂 Save uploaded files to project directory (`Testcases/`)
- 🗂 Group test cases by category (`testcase_group`)
  <img width="1078" alt="projects" src="https://github.com/user-attachments/assets/fba15659-785c-4d94-a821-292dfb50abfa" />

- 📊 View summary statistics (e.g., count of Pass, Fail, Ongoing per group)
  <img width="1079" alt="Dashboard" src="https://github.com/user-attachments/assets/0b21c1e7-1f42-4657-91c8-64d398e0a8df" />
- 🔍 Django admin for CRUD operations
- 🛡 CSRF protection and form validation
- 🗑 Delete old files after upload

---

## 📁 Folder Structure

