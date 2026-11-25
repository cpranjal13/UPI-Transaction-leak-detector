# UPI Leak Detector 💸🔍
> **Automated AI-Powered Financial Tracking & Spend Leak Detection System**

UPI Leak Detector is a personal finance web application built with Python and Flask. It helps users gain full visibility into their spending patterns, automatically flags hidden "money leaks" (such as recurring micro-transactions and anomalous large expenses), and provides personalized AI financial advice using Google Gemini.

---

## 🌟 Key Features

* **🤖 AI-Powered Statement Parsing**: Upload bank statements (PDFs) or receipts (PNG/JPG). Google Gemini intelligently extracts transaction details, debit amounts, dates, and account numbers.
* **⚡ Universal Regex Fallback**: Works completely offline without an API key using an advanced regex parsing engine compatible with major Indian banks (HDFC, ICICI, SBI, Axis, etc.).
* **🛡️ Spend Leak Detection Engine**: Automatically flags:
  * Repeated small spending habits (e.g. ₹50–₹200 micro-transactions repeating frequently at the same merchant).
  * High-frequency merchants.
  * Unusually large single expenses.
* **💬 AI Financial Advisor**: Built-in context-aware chatbot powered by Google Gemini that analyzes your recent 50 transactions to give actionable financial advice.
* **📊 Analytics Dashboard**: Interactive spend trend charts, category breakdowns (Food & Dining, Utilities, Shopping, Transport, etc.), and budget tracking.
* **📄 PDF Spending Reports**: Generate and download professional monthly spend summary reports with a single click.
* **🔒 Dual-Engine Database Support**: Automatically uses embedded SQLite for zero-config local development, or seamlessly connects to PostgreSQL if available.

---

## 🛠️ Tech Stack

* **Backend**: Python 3.10+, Flask
* **Authentication**: Flask-Login, Flask-Bcrypt
* **AI & NLP**: Google GenAI SDK (Gemini 2.5 Flash)
* **Data Processing**: Pandas, pdfplumber, Pillow
* **Database**: SQLite (default) / PostgreSQL (`psycopg2-binary`)
* **Frontend**: Bootstrap 5, Glassmorphism UI, Chart.js, Bootstrap Icons
* **Document Generation**: FPDF2

---

## 📁 Repository Structure

```text
upi_tracker/
├── app.py                              # Main Flask application and API routes
├── db.py                               # Database connector (SQLite & PostgreSQL auto-detect)
├── init_db.py                          # Database initialization script
├── schema.sql                          # Database table schemas
├── generate_report.py                  # Project documentation report generator
├── Project_Report_UPI_Leak_Detector.pdf # Compiled project report
├── requirements.txt                    # Python dependencies
├── run.bat                             # One-click Windows launcher
├── .env.example                        # Template for environment variables
├── .gitignore                          # Git ignore rules
├── templates/                          # HTML Jinja2 templates
│   ├── base.html
│   ├── dashboard.html
│   ├── login.html
│   ├── signup.html
│   ├── add_transaction.html
│   ├── transaction_details.html
│   ├── alerts.html
│   └── upload_csv.html
└── static/                             # Static assets (CSS, JS, images, icons)
    ├── css/style.css
    ├── img/logo.png
    ├── icons/
    ├── manifest.json
    └── sw.js
```

---

## 🚀 Quick Start Guide

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/upi-leak-detector.git
cd upi-leak-detector
```

### 2. Create and Activate a Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the `.env.example` file to `.env`:
```bash
# Windows (Command Prompt)
copy .env.example .env

# macOS / Linux / PowerShell
cp .env.example .env
```
Open `.env` and add your [Google Gemini API Key](https://aistudio.google.com/):
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

### 5. Initialize Database & Run
```bash
# Initialize database tables
python init_db.py

# Run application
python app.py
```
Open your browser and navigate to:
**`http://localhost:5000`** (or `http://127.0.0.1:5000`)

---

## 👥 Authors
* **Pranjal Chaudhary**
* **Pranav namdeo**

---

## 📜 License
This project is open-source and developed for educational and personal finance tracking purposes.
