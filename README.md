# MediAssist: AI-Powered Prescription Scanner and Medicine Reminder System

MediAssist is an assistive web platform designed to simplify medication management for patients, elderly individuals, and caregivers. The system digitizes handwritten and printed prescriptions using Optical Character Recognition (OCR), interprets clinical dosage frequencies (`OD`, `BD`, `TDS`, `1-0-1`) into concrete daily schedules, triggers scheduled reminders, and helps patients locate medicines online and at nearby pharmacies.

---

## Key Features

- **Prescription Scanner & OCR**:
  - Image acquisition via camera capture or file upload (PNG/JPG up to 8MB).
  - OpenCV preprocessing pipeline: Bilateral NlMeans denoising, CLAHE contrast enhancement, and dual Otsu + Adaptive Gaussian thresholding.
  - Optical Character Recognition powered by Tesseract OCR.
- **Medicine Parser & NLP Matching**:
  - Regex-based dosage parsing and frequency slot mapping (`OD`, `BD`, `TDS`, `QID`, `HS`, `1-0-1`, `1-1-1`, etc.).
  - RapidFuzz approximate string matching against a built-in 100+ medicine reference database.
  - OCR error normalization (e.g., `0D` -> `OD`, `8D` -> `BD`, `I-0-I` -> `1-0-1`, `rng` -> `mg`).
- **Human-in-the-Loop Verification**:
  - Mandatory confirmation screen allowing users to edit medicine names, strengths, timings, and durations before anything is saved.
- **Authentication & Secure Vault**:
  - Real user authentication with session management and HTTP-only cookies.
  - Salted password hashing via Werkzeug (scrypt/pbkdf2).
  - Password reset flow via time-limited, cryptographically secure tokens.
  - Dual storage: Supabase PostgreSQL (with Row Level Security) and local SQLite fallback.
  - Per-user data isolation: every query is scoped to the authenticated user ID.
  - Full data deletion: one-click permanent account and prescription wipe.
- **Reminder Engine & Dose Lifecycle**:
  - Automated schedule generator calculating all dose instances across prescribed durations.
  - One-tap dose logging: `Taken`, `Snooze 10m`, and `Skip`.
  - Browser notifications via MDN Notifications API.
- **Medicine Locator**:
  - Direct 1-click **Open Google Maps Nearby** button visible from the start.
  - Live GPS store discovery using HTML5 Geolocation.
  - Manual area/city/pincode search powered by OpenStreetMap Nominatim and Overpass API mirrors.
  - One-click online pharmacy deep search links for 1mg, Netmeds, and Apollo Pharmacy.
- **Security & Reliability**:
  - Rate limiting via Flask-Limiter (`5/hr` registrations, `10/min` logins, `20/hr` scans).
  - CSRF header verification (`X-Requested-With: fetch`).
  - Security headers (`X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: same-origin`).
  - Error tracking integration with Sentry SDK and client-side error beacons.
  - Custom 404 page and clean loading/empty states throughout.
  - Mobile-responsive layout (supports viewports down to 320px).
  - 3-step first-time user onboarding wizard.

---

## Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend** | HTML5, CSS3 (Custom Dark Theme), JavaScript (ES6+), Leaflet.js, Anime.js |
| **Backend** | Python 3.12, Flask, Flask-Limiter, Werkzeug |
| **OCR & Vision** | Tesseract OCR (v4.1.1/v5.x), OpenCV (cv2), NumPy |
| **NLP & Matching**| RapidFuzz, Regular Expressions |
| **Database & Auth**| Supabase (PostgreSQL with RLS) / SQLite3 (local fallback) |
| **Maps & Places** | Leaflet.js, OpenStreetMap Nominatim & Overpass API, Google Maps |

---

## Getting Started

### 1. Prerequisites
- Python 3.10+
- Tesseract OCR (included as a portable binary in `tesseract/` on Windows, or `sudo apt install tesseract-ocr` on Linux)

### 2. Installation
```bash
git clone https://github.com/Haardik2510/MediAssist.git
cd MediAssist

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Environment Configuration
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Fill in your configuration:
```ini
SECRET_KEY=generate-a-secure-random-key-here
BASE_URL=http://localhost:5000
PROD=0

# Supabase (Leave empty to use local SQLite)
SUPABASE_URL=
SUPABASE_KEY=

# Optional SMTP (leave empty to output verification links to terminal)
SMTP_HOST=
SMTP_PORT=587
SMTP_USER=
SMTP_PASS=
MAIL_FROM=no-reply@mediassist.local
```

### 4. Run the Application
```bash
python app.py
```
Open `http://localhost:5000` in your web browser.

---

## Running Automated Tests

Run the backend verification suite (59 tests):
```bash
python test_backend.py
```

Run the full system compliance and benchmark suite (112 tests, 100% score):
```bash
python test_full_system.py
```

---

## Testing with Sample Prescriptions

Sample doctor prescriptions are included in `datasets/prescriptions/` (`prescription_01.png` through `prescription_10.png`).
You can upload any of these directly on the Dashboard to test the end-to-end OCR and schedule generation.

---

## Free Cloud Deployment Guide

### Deploying on Render (Free Web Service)
1. Push this repository to your GitHub account (`https://github.com/Haardik2510/MediAssist`).
2. Sign up at [render.com](https://render.com) and click **New ➔ Web Service**.
3. Select your `MediAssist` repository.
4. Set the following settings:
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Under **Environment Variables**, add:
   - `SECRET_KEY`: (any long random string)
   - `PROD`: `1`
   - `SUPABASE_URL`: (your Supabase project URL)
   - `SUPABASE_KEY`: (your Supabase service/anon key)
6. Click **Deploy Web Service**. Your app is live at `https://your-app.onrender.com`.

### Setting Up Free Supabase PostgreSQL
1. Create a free account at [supabase.com](https://supabase.com).
2. Create a new project.
3. Open the **SQL Editor**, paste the contents of `supabase_schema.sql`, and click **Run**.
4. Copy the Project URL and API Key into Render's Environment Variables.

---

## Academic Information

- **Project**: MediAssist – AI-Powered Prescription Scanner and Medicine Reminder System
- **Student**: Haardik Goel (Enrollment No. 09417704426)
- **Programme**: Master of Computer Applications (MCA 1B)
- **Institution**: Vivekananda School of Information Technology, VIPS-TC, affiliated with Guru Gobind Singh Indraprastha University (GGSIPU), Delhi.
- **Mentor**: Dr. Cosmina

---

## License & Disclaimer
This project is an assistive tool and does not provide medical advice or diagnosis. Always consult a qualified medical professional for health decisions.
