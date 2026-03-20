🏥 CareSync – Hospital Management System
CareSync is a professional, light-themed administrative dashboard designed to manage hospital workflows—from patient registration and doctor scheduling to automated billing in Indian Rupees (₹).

✨ Features
📊 Smart Dashboard: Real-time stats for Patients, Doctors, and Today's Revenue.

🧑‍🤝‍🧑 Patient Management: Full CRUD (Create, Read, Update, Delete) with search functionality.

👨‍⚕️ Doctor Directory: Manage specialized doctors and their availability.

📅 Appointment System: Seamless booking flow with status tracking (Scheduled/Completed/Cancelled).

📄 Medical Records: Link diagnoses and clinical notes directly to patient profiles.

🧾 Automated Billing: Instant invoice generation with consultation, medicine, and test cost breakdown (Currency: ₹ INR).

🎨 UI/UX Design (The "Vibe")
Theme: Professional Light Theme (Clean & High Contrast).

Primary Color: #4A90E2 (Medical Blue).

Accent Color: #50C878 (Success Green).

Responsiveness: Fully responsive sidebar and data tables using Tailwind CSS.

🛠 Tech Stack
Backend: Python (Flask)

Database: SQLite (SQLAlchemy ORM)

Frontend: HTML5, Tailwind CSS, JavaScript

Icons: Lucide-React / FontAwesome

🚀 Getting Started
1. Clone & Extract
Extract the project zip file to your local machine.

2. Setup Virtual Environment (Recommended)
Bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
3. Install Dependencies
Bash
pip install -r requirements.txt
4. Run the Application
Bash
python app.py
Open http://127.0.0.1:5000 in your browser.

📂 Project Structure
Plaintext
CareSync/
├── static/          # CSS, JS, and Images
├── templates/       # HTML Pages (Base, Dashboard, Patients, etc.)
├── app.py           # Main Flask Application & Routes
├── models.py        # Database Schema (SQLAlchemy)
├── requirements.txt # Project Dependencies
└── README.md        # You are here!
💡 Viva Tips for CareSync
Database Integrity: All tables are linked using Foreign Keys (e.g., Appointments link to both Patients and Doctors).

State Management: Billing is only enabled once an appointment status is marked as "Completed".

Localization: The system is pre-configured for the Indian Healthcare market using ₹ (INR) formatting.