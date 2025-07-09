# 🧪 Testcase Management System

A web-based system for managing and organizing test cases, built with **Django** and **MySQL**. This system enables users to upload standardized Excel files for test cases, store metadata, track execution statuses (Pass, Fail, Ongoing), and categorize tests by group (e.g., Mastercard, Visacard, etc.).

## 🚀 Features

- ✅ Upload and parse Excel files for test cases
![alt text](upload.png)
- 📂 Save uploaded files to project directory (`Testcases/`)
- 🗂 Group test cases by category (`testcase_group`)
- 📊 View summary statistics (e.g., count of Pass, Fail, Ongoing per group)
- 🔍 Django admin for CRUD operations
- 🛡 CSRF protection and form validation
- 🗑 Delete old files after upload

---

## 📁 Folder Structure

