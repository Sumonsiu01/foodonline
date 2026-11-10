# 🍔 FoodOnline - Multi-Vendor Food Marketplace Platform

A production-ready, feature-rich Multi-Vendor Food Marketplace built using **Django 5.x**, **Python 3.12+**, and **Bootstrap 5**. The platform enables food vendors to manage their restaurant profiles, menu offerings, and orders, while providing customers with a seamless food discovery, cart management, and checkout experience.

---

## 🌟 Key Features

### 🏢 Vendor Management
- **Vendor Onboarding & Dashboard**: Profile creation, logo/cover photo customization, and location mapping.
- **Menu Management**: Categorized menu items, custom pricing, and item availability toggles.
- **Real-Time Analytics**: Visual overview cards tracking Total Orders, Total Revenue, and Monthly Earnings.

### 🛍️ Customer Experience
- **Restaurant Discovery**: Search restaurants by location, category, or food item.
- **Cart & Dynamic Checkout**: Interactive cart management with tax, delivery fee, and discount calculations.
- **Order Tracking**: Order lifecycle status updates (Pending, Processing, Completed, Cancelled).

### 🛡️ Authentication & Authorization
- Multi-role user model (`Customer` vs. `Vendor` permissions).
- Custom middleware & signals for automatic profile generation upon registration.
- Global Context Processors for session-wide user/vendor data availability.

---

## 🛠️ Tech Stack & Dependencies

- **Backend Framework:** Django, Python
- **Database:** PostgreSQL / MySQL (MariaDB)
- **Frontend Framework:** HTML5, CSS3, JavaScript (ES6+), Bootstrap 5
- **Task Queue & Caching:** Redis, Celery (Optional for Async Notifications)
- **Asset Management:** Django Staticfiles, Pillow (Image Handling)

---

## 🚀 Quick Start Guide

### 1. Prerequisites
Ensure you have the following installed on your local system:
- Python 3.10+
- PostgreSQL or MySQL (XAMPP / MariaDB)
- Git

### 2. Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone [https://github.com/your-username/foodonline-django.git](https://github.com/your-username/foodonline-django.git)
   cd foodonline-django
