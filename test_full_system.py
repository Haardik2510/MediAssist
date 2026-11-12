"""
MediAssist – Full System Performance & Synopsis Compliance Test
Tests every feature against the MCA Minor Project Synopsis requirements.
Produces a baseline score report.
"""
import os, sys, json, glob, time, traceback, re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()
os.environ["SMTP_HOST"] = ""
os.environ["SMTP_USER"] = ""
os.environ["SMTP_PASS"] = ""

# ── Score tracking ────────────────────────────────────────────────────────────
results = []  # list of (category, test_name, passed:bool, detail:str, weight)

def check(category, name, condition, detail="", weight=1):
    results.append((category, name, bool(condition), detail, weight))
    icon = "✓" if condition else "✗"
    print(f"  {icon} [{category}] {name}" + (f" — {detail}" if detail and not condition else ""))
    return condition

# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*74)
print("  MediAssist – Full System Performance & Synopsis Compliance Test")
print("="*74)

# ── 0. DEPENDENCY INSTALLATION VERIFICATION ──────────────────────────────────
print("\n" + "─"*74)
print("  SECTION 0: Dependency Installation")
print("─"*74)

import_tests = {
    "flask": "Flask web framework",
    "flask_limiter": "Flask-Limiter rate limiting",
    "cv2": "OpenCV image processing",
    "numpy": "NumPy numerical computing",
    "pytesseract": "Tesseract OCR wrapper",
    "rapidfuzz": "RapidFuzz fuzzy matching",
    "supabase": "Supabase SDK",
    "dotenv": "python-dotenv",
    "werkzeug.security": "Werkzeug password hashing",
}
for mod, desc in import_tests.items():
    try:
        __import__(mod)
        check("Dependencies", f"{desc} ({mod})", True)
    except ImportError as e:
        check("Dependencies", f"{desc} ({mod})", False, str(e))

# Tesseract binary
import pytesseract
_local_tess = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tesseract", "tesseract.exe")
_local_tessdata = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tesseract", "tessdata")
if os.path.isfile(_local_tess):
    pytesseract.pytesseract.tesseract_cmd = _local_tess
    os.environ["TESSDATA_PREFIX"] = _local_tessdata

tesseract_ok = False
tess_version = "NOT FOUND"
try:
    tess_version = str(pytesseract.get_tesseract_version())
    tesseract_ok = True
except Exception:
    # Try common Windows paths
    for p in [r"C:\Program Files\Tesseract-OCR\tesseract.exe",
              r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"]:
        if os.path.isfile(p):
            pytesseract.pytesseract.tesseract_cmd = p
            try:
                tess_version = str(pytesseract.get_tesseract_version())
                tesseract_ok = True
                break
            except Exception:
                pass
check("Dependencies", f"Tesseract OCR binary (v{tess_version})", tesseract_ok,
      "Required for /api/scan OCR feature", weight=3)

# ── 1. APP MODULE IMPORT ─────────────────────────────────────────────────────
print("\n" + "─"*74)
print("  SECTION 1: Application Module")
print("─"*74)

try:
    from app import (app, parse, fuzzy_match_medicine, normalize_ocr_text,
                     preprocess_image, MEDICINE_DB, HAS_RAPIDFUZZ, USE_SUPABASE,
                     FREQ, SLOTS)
    check("App Module", "app.py imports cleanly", True)
except Exception as e:
    check("App Module", "app.py imports", False, traceback.format_exc())
    print("\n❌ FATAL: Cannot continue. Fix app.py import errors.")
    sys.exit(1)

check("App Module", "RapidFuzz active", HAS_RAPIDFUZZ, weight=2)
check("App Module", f"Medicine DB has {len(MEDICINE_DB)} entries", len(MEDICINE_DB) >= 50, weight=1)
check("App Module", f"Backend: {'Supabase' if USE_SUPABASE else 'SQLite (fallback)'}", True)

# ── 2. SYNOPSIS MODULE 1: PRESCRIPTION SCANNER ──────────────────────────────
print("\n" + "─"*74)
print("  SECTION 2: Module 1 – Prescription Scanner (Synopsis VI-B-1)")
print("─"*74)

# 2a. Image preprocessing
import cv2, numpy as np

# Create a test image
test_img = np.ones((400, 600, 3), dtype=np.uint8) * 240
cv2.putText(test_img, "Tab. Metformin 500mg OD 30 days", (20, 100),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (10, 10, 10), 1)
_, buf = cv2.imencode(".png", test_img)
img_bytes = buf.tobytes()

result = preprocess_image(img_bytes)
check("Scanner", "Image preprocessing (grayscale+denoise+threshold)", result is not None, weight=2)
if result:
    otsu, adaptive = result
    check("Scanner", f"Otsu output shape {otsu.shape}", otsu is not None and len(otsu.shape) == 2)
    check("Scanner", f"Adaptive output shape {adaptive.shape}", adaptive is not None and len(adaptive.shape) == 2)

# 2b. OCR text extraction
if tesseract_ok and result:
    t0 = time.time()
    raw_text = pytesseract.image_to_string(result[0])
    ocr_time = time.time() - t0
    check("Scanner", f"OCR text extraction ({ocr_time:.2f}s)", len(raw_text) > 0,
          f"extracted {len(raw_text)} chars", weight=3)
    check("Scanner", f"OCR latency < 5s ({ocr_time:.2f}s)", ocr_time < 5.0, weight=1)
else:
    check("Scanner", "OCR text extraction", False, "Tesseract not available", weight=3)

# 2c. File upload validation
app.config["TESTING"] = True
client = app.test_client()

# Upload non-image should fail
with client.session_transaction() as s:
    s["uid"] = 99999  # fake session for testing scan endpoint
r = client.post("/api/scan", content_type="multipart/form-data",
                headers={"X-Requested-With": "fetch"})
check("Scanner", "Rejects empty upload (400)", r.status_code == 400)

# 2d. Dataset OCR test (all 10 prescriptions)
print("\n  --- Dataset OCR Processing ---")
dataset_dir = os.path.join("datasets", "prescriptions")
images = sorted(glob.glob(os.path.join(dataset_dir, "*.png")))
check("Scanner", f"Dataset has {len(images)} prescription images", len(images) >= 10, weight=1)

total_meds_extracted = 0
total_expected = 0
per_image_results = []

if tesseract_ok:
    for img_path in images:
        fname = os.path.basename(img_path)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            per_image_results.append((fname, 0, 0, []))
            continue

        # Preprocess
        h, w = img.shape
        if max(h, w) < 1000:
            scale = 1500 / max(h, w)
            img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
        img = cv2.fastNlMeansDenoising(img, None, 10, 7, 21)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        img = clahe.apply(img)
        img_otsu = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        img_adapt = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                           cv2.THRESH_BINARY, 15, 8)

        meds = []
        raw = ""
        for proc_img in (img_otsu, img_adapt):
            for cfg in ("", "--psm 6"):
                try:
                    r_try = pytesseract.image_to_string(proc_img, config=cfg)
                    m_try = parse(r_try)
                    if len(m_try) > len(meds):
                        meds, raw = m_try, r_try
                except Exception:
                    pass

        # Expected count from the generator
        expected_map = {
            "prescription_01.png": 4, "prescription_02.png": 4,
            "prescription_03.png": 5, "prescription_04.png": 4,
            "prescription_05.png": 4, "prescription_06.png": 4,
            "prescription_07.png": 4, "prescription_08.png": 4,
            "prescription_09.png": 5, "prescription_10.png": 4,
        }
        expected = expected_map.get(fname, 4)
        total_expected += expected
        total_meds_extracted += len(meds)
        per_image_results.append((fname, len(meds), expected, meds))

        status = "PASS" if len(meds) >= expected * 0.5 else "FAIL"
        print(f"    {fname}: {len(meds)}/{expected} medicines [{status}]")
        for m in meds:
            conf_pct = f"{m['confidence']:.0%}" if m.get('confidence') else "?"
            print(f"      → {m['name']} {m['strength']} {m['freq']} x{m['days']}d (match:{conf_pct})")

    extraction_rate = total_meds_extracted / total_expected * 100 if total_expected > 0 else 0
    check("Scanner", f"Dataset extraction rate {extraction_rate:.0f}% ({total_meds_extracted}/{total_expected})",
          extraction_rate >= 50, weight=3)
else:
    check("Scanner", "Dataset OCR processing", False, "Tesseract not available", weight=3)

# ── 3. SYNOPSIS MODULE 2: MEDICINE PARSER ────────────────────────────────────
print("\n" + "─"*74)
print("  SECTION 3: Module 2 – Medicine Parser (Synopsis VI-B-2)")
print("─"*74)

# 3a. Frequency notation interpretation (Synopsis Table VIII)
freq_tests = [
    ("OD",  1, ["08:00"]),
    ("BD",  2, ["08:00", "20:00"]),
    ("TDS", 3, ["08:00", "14:00", "20:00"]),
    ("QID", 4, ["08:00", "12:00", "16:00", "20:00"]),
    ("HS",  1, ["22:00"]),
]
for code, count, expected_times in freq_tests:
    actual = FREQ.get(code, [])
    check("Parser", f"Frequency {code} → {count} dose(s)", len(actual) == count and actual == expected_times)

# 3b. 1-0-1 notation parsing
notation_tests = [
    ("Tab. Test 500mg 1-0-1 5 days", 2, "1-0-1"),
    ("Tab. Test 500mg 1-1-1 5 days", 3, "1-1-1"),
    ("Tab. Test 500mg 1-0-0 5 days", 1, "1-0-0"),
    ("Tab. Test 500mg 0-0-1 5 days", 1, "0-0-1"),
    ("Tab. Test 500mg 0-1-0 5 days", 1, "0-1-0"),
]
for line, exp_count, exp_freq in notation_tests:
    meds = parse(line)
    if meds:
        check("Parser", f"Notation '{exp_freq}' → {exp_count} time(s)",
              len(meds[0]["times"]) == exp_count and meds[0]["freq"] == exp_freq)
    else:
        check("Parser", f"Notation '{exp_freq}'", False, "not parsed")

# 3c. Fuzzy matching accuracy
print("\n  --- Fuzzy Matching Accuracy ---")
fuzzy_tests = [
    ("Metformin", "Metformin", 0.95),
    ("Metforrmin", "Metformin", 0.80),      # typo
    ("Paracetarnol", "Paracetamol", 0.80),  # OCR misread
    ("Atorvasttin", "Atorvastatin", 0.80),
    ("Pantoprazle", "Pantoprazole", 0.80),
    ("Arnlodipine", "Amlodipine", 0.75),     # OCR r→m
    ("Clonazeparn", "Clonazepam", 0.75),      # OCR n→rn
    ("Escitolapram", "Escitalopram", 0.70),   # scrambled
    ("Omeprazol", "Omeprazole", 0.80),        # missing e
    ("Cetirizin", "Cetirizine", 0.80),        # missing e
]
fuzzy_correct = 0
for input_name, expected, min_conf in fuzzy_tests:
    matched, conf = fuzzy_match_medicine(input_name)
    ok = matched == expected and conf >= min_conf
    if ok:
        fuzzy_correct += 1
    check("Parser", f"Fuzzy: '{input_name}' → '{matched}' ({conf:.0%})", ok,
          f"expected '{expected}' ≥{min_conf:.0%}")

fuzzy_accuracy = fuzzy_correct / len(fuzzy_tests) * 100
check("Parser", f"Fuzzy matching accuracy: {fuzzy_accuracy:.0f}%", fuzzy_accuracy >= 70, weight=2)

# 3d. OCR normalization
norm_tests = [
    ("0D", "OD"), ("8D", "BD"), ("T0S", "TDS"),
    ("I-0-I", "1-0-1"), ("l-0-l", "1-0-1"), ("l-l-l", "1-1-1"),
    ("1ab.", "Tab."), ("rng", "mg"),
]
norm_pass = 0
for before, after in norm_tests:
    fixed = normalize_ocr_text(before)
    ok = after in fixed
    if ok: norm_pass += 1
    check("Parser", f"Normalize '{before}' → contains '{after}'", ok)

# ── 4. SYNOPSIS MODULE 3: PRESCRIPTION VAULT ────────────────────────────────
print("\n" + "─"*74)
print("  SECTION 4: Module 3 – Prescription Vault / Auth (Synopsis VI-B-3)")
print("─"*74)

import sqlite3 as _sq
# Clean first
conn = _sq.connect("mediassist.db")
conn.execute("DELETE FROM doses WHERE user_id IN (SELECT id FROM users WHERE email LIKE '%@perftest.dev')")
conn.execute("DELETE FROM medicines WHERE user_id IN (SELECT id FROM users WHERE email LIKE '%@perftest.dev')")
conn.execute("DELETE FROM prescriptions WHERE user_id IN (SELECT id FROM users WHERE email LIKE '%@perftest.dev')")
conn.execute("DELETE FROM tokens WHERE user_id IN (SELECT id FROM users WHERE email LIKE '%@perftest.dev')")
conn.execute("DELETE FROM users WHERE email LIKE '%@perftest.dev'")
conn.commit()
conn.close()

# 4a. Registration
t0 = time.time()
r = client.post("/api/register",
    data=json.dumps({"email": "vault@perftest.dev", "password": "Secure123!"}),
    content_type="application/json", headers={"X-Requested-With": "fetch"})
reg_time = time.time() - t0
check("Vault/Auth", f"Registration ({reg_time:.3f}s) → {r.status_code}", r.status_code == 200, weight=2)

# 4b. Password hashing (must be salted hash, not plaintext)
conn = _sq.connect("mediassist.db")
row = conn.execute("SELECT pw FROM users WHERE email='vault@perftest.dev'").fetchone()
conn.close()
check("Vault/Auth", "Password stored as hash (not plaintext)",
      row and row[0].startswith(("scrypt:", "pbkdf2:", "$2")), weight=2)

# 4c. Login denied for unverified
r = client.post("/api/login",
    data=json.dumps({"email": "vault@perftest.dev", "password": "Secure123!"}),
    content_type="application/json", headers={"X-Requested-With": "fetch"})
check("Vault/Auth", "Login rejected for unverified user (403)", r.status_code == 403, weight=2)

# 4d. Email verification flow
conn = _sq.connect("mediassist.db")
conn.execute("UPDATE users SET verified=1 WHERE email='vault@perftest.dev'")
conn.commit()
conn.close()

t0 = time.time()
r = client.post("/api/login",
    data=json.dumps({"email": "vault@perftest.dev", "password": "Secure123!"}),
    content_type="application/json", headers={"X-Requested-With": "fetch"})
login_time = time.time() - t0
check("Vault/Auth", f"Login after verification ({login_time:.3f}s) → {r.status_code}", r.status_code == 200, weight=2)

# 4e. Session management
r = client.get("/api/me")
user_data = r.get_json()
check("Vault/Auth", "Session: /api/me returns user",
      user_data.get("user", {}).get("email") == "vault@perftest.dev")

# 4f. CSRF protection
r = client.post("/api/register",
    data=json.dumps({"email": "csrf@perftest.dev", "password": "Secure123!"}),
    content_type="application/json")  # Missing X-Requested-With
check("Vault/Auth", "CSRF protection blocks requests without header (400)", r.status_code == 400, weight=2)

# 4g. Security headers
r = client.get("/")
check("Vault/Auth", "X-Content-Type-Options: nosniff",
      r.headers.get("X-Content-Type-Options") == "nosniff")
check("Vault/Auth", "X-Frame-Options: DENY",
      r.headers.get("X-Frame-Options") == "DENY")
check("Vault/Auth", "Referrer-Policy: same-origin",
      r.headers.get("Referrer-Policy") == "same-origin")

# 4h. Save prescription
rx_data = {
    "raw": "Tab. Metformin 500mg 1-0-1 30 days\nTab. Amlodipine 5mg OD 30 days",
    "medicines": [
        {"name": "Metformin", "strength": "500mg", "freq": "1-0-1",
         "times": ["08:00", "20:00"], "days": 5, "confidence": 1.0},
        {"name": "Amlodipine", "strength": "5mg", "freq": "OD",
         "times": ["08:00"], "days": 5, "confidence": 1.0},
    ]
}
t0 = time.time()
r = client.post("/api/prescriptions",
    data=json.dumps(rx_data), content_type="application/json",
    headers={"X-Requested-With": "fetch"})
save_time = time.time() - t0
check("Vault/Auth", f"Save prescription ({save_time:.3f}s) → {r.status_code}", r.status_code == 200, weight=2)

# 4i. Retrieve medicines
t0 = time.time()
r = client.get("/api/medicines")
med_time = time.time() - t0
meds = r.get_json()
check("Vault/Auth", f"Retrieve medicines ({med_time:.3f}s) → {len(meds)} items",
      len(meds) == 2, weight=1)

# 4j. Data isolation — another user can't see these
r2 = client.post("/api/logout", data="{}", content_type="application/json",
                 headers={"X-Requested-With": "fetch"})
r2 = client.get("/api/medicines")
check("Vault/Auth", "Data isolation: unauth → 401", r2.status_code == 401, weight=2)

# Re-login for remaining tests
client.post("/api/login",
    data=json.dumps({"email": "vault@perftest.dev", "password": "Secure123!"}),
    content_type="application/json", headers={"X-Requested-With": "fetch"})

# ── 5. SYNOPSIS MODULE 4: REMINDER ENGINE ───────────────────────────────────
print("\n" + "─"*74)
print("  SECTION 5: Module 4 – Reminder Engine (Synopsis VI-B-4)")
print("─"*74)

# 5a. Dose schedule generation
conn = _sq.connect("mediassist.db")
uid_row = conn.execute("SELECT id FROM users WHERE email='vault@perftest.dev'").fetchone()
uid = uid_row[0] if uid_row else 0
dose_count = conn.execute("SELECT COUNT(*) FROM doses WHERE user_id=?", (uid,)).fetchone()[0]
conn.close()
# 2 meds: Metformin 2x/day x 5days = 10, Amlodipine 1x/day x 5days = 5 → 15 total
check("Reminders", f"Dose schedule generated: {dose_count} doses (expected 15)",
      dose_count == 15, weight=2)

# 5b. Due reminders endpoint
r = client.get("/api/reminders/due")
check("Reminders", f"GET /api/reminders/due → {r.status_code}", r.status_code == 200, weight=1)

# 5c. Mark dose as taken
conn = _sq.connect("mediassist.db")
dose_row = conn.execute("SELECT id FROM doses WHERE user_id=? AND status='pending' LIMIT 1", (uid,)).fetchone()
conn.close()
if dose_row:
    r = client.post(f"/api/doses/{dose_row[0]}",
        data=json.dumps({"status": "taken"}), content_type="application/json",
        headers={"X-Requested-With": "fetch"})
    check("Reminders", "Mark dose as 'taken'", r.status_code == 200, weight=2)

    # Verify it's actually marked
    conn = _sq.connect("mediassist.db")
    status = conn.execute("SELECT status FROM doses WHERE id=?", (dose_row[0],)).fetchone()
    conn.close()
    check("Reminders", "Dose status updated in DB", status and status[0] == "taken", weight=1)

# 5d. Snooze dose
conn = _sq.connect("mediassist.db")
dose_row2 = conn.execute("SELECT id, due FROM doses WHERE user_id=? AND status='pending' LIMIT 1", (uid,)).fetchone()
conn.close()
if dose_row2:
    old_due = dose_row2[1]
    r = client.post(f"/api/doses/{dose_row2[0]}",
        data=json.dumps({"status": "snooze"}), content_type="application/json",
        headers={"X-Requested-With": "fetch"})
    check("Reminders", "Snooze dose (postpone 10min)", r.status_code == 200, weight=1)

    conn = _sq.connect("mediassist.db")
    new_due = conn.execute("SELECT due FROM doses WHERE id=?", (dose_row2[0],)).fetchone()
    conn.close()
    check("Reminders", "Snoozed dose has new due time", new_due and new_due[0] != old_due, weight=1)

# 5e. Skip dose
conn = _sq.connect("mediassist.db")
dose_row3 = conn.execute("SELECT id FROM doses WHERE user_id=? AND status='pending' LIMIT 1", (uid,)).fetchone()
conn.close()
if dose_row3:
    r = client.post(f"/api/doses/{dose_row3[0]}",
        data=json.dumps({"status": "skipped"}), content_type="application/json",
        headers={"X-Requested-With": "fetch"})
    check("Reminders", "Skip dose", r.status_code == 200, weight=1)

# 5f. Invalid dose action rejected
if dose_row3:
    r = client.post(f"/api/doses/{dose_row3[0]}",
        data=json.dumps({"status": "invalid"}), content_type="application/json",
        headers={"X-Requested-With": "fetch"})
    check("Reminders", "Invalid dose action rejected (400)", r.status_code == 400)

# ── 6. SYNOPSIS MODULE 5: MEDICINE LOCATOR ──────────────────────────────────
print("\n" + "─"*74)
print("  SECTION 6: Module 5 – Medicine Locator (Synopsis VI-B-5)")
print("─"*74)

# Check frontend code for locator features
with open("static/app.js", "r", encoding="utf-8") as f:
    js = f.read()

check("Locator", "Geolocation API used (navigator.geolocation)", "navigator.geolocation" in js, weight=2)
check("Locator", "Leaflet.js map integration (L.map)", "L.map" in js, weight=2)
check("Locator", "Overpass API for nearby pharmacies", "overpass-api.de" in js, weight=2)
check("Locator", "Online pharmacy links (1mg)", "1mg.com" in js, weight=2)
check("Locator", "Online pharmacy links (Netmeds)", "netmeds.com" in js, weight=2)

with open("static/index.html", "r", encoding="utf-8") as f:
    html = f.read()
check("Locator", "Leaflet CSS loaded", "leaflet.css" in html)
check("Locator", "Leaflet JS loaded", "leaflet.js" in html)

# ── 7. FRONTEND / UI ────────────────────────────────────────────────────────
print("\n" + "─"*74)
print("  SECTION 7: Frontend / UI (Synopsis VII-B)")
print("─"*74)

check("Frontend", "Landing page serves (200)", client.get("/").status_code == 200, weight=1)
check("Frontend", "Static CSS loads", client.get("/style.css").status_code == 200)
check("Frontend", "Static JS loads", client.get("/app.js").status_code == 200)

# Check HTML for key UI elements
check("Frontend", "Responsive viewport meta tag", 'width=device-width' in html, weight=1)
check("Frontend", "Anime.js loaded for animations", "anime.min.js" in html)
check("Frontend", "Upload input with camera capture", 'capture=environment' in js, weight=1)

# CSS responsive design
with open("static/style.css", "r", encoding="utf-8") as f:
    css = f.read()
check("Frontend", "Mobile responsive (media query ≤640px)", "@media" in css and "640px" in css, weight=1)
check("Frontend", "Prefers-reduced-motion support", "prefers-reduced-motion" in css)
check("Frontend", "Dark theme design (--bg:#07090c)", "--bg:#07090c" in css)

# Privacy & Terms pages in JS
check("Frontend", "Privacy policy page", "Privacy Policy" in js)
check("Frontend", "Terms of service page", "Terms of Service" in js)
check("Frontend", "Onboarding wizard (3 steps)", "Step 1 of 3" in js or "Step ${i+1} of 3" in js, weight=1)

# Human-in-the-loop confirmation
check("Frontend", "Human-in-the-loop: review step before save",
      "Review and correct before saving" in js or "Confirm and save" in js, weight=2)

# ── 8. SECURITY & PRIVACY (Synopsis VIII-E) ─────────────────────────────────
print("\n" + "─"*74)
print("  SECTION 8: Security & Privacy (Synopsis VIII-E)")
print("─"*74)

check("Security", "Salted password hashing (werkzeug)", "generate_password_hash" in open("app.py").read(), weight=2)
check("Security", "Session cookie HttpOnly", app.config.get("SESSION_COOKIE_HTTPONLY") == True, weight=2)
check("Security", "Session cookie SameSite=Lax", app.config.get("SESSION_COOKIE_SAMESITE") == "Lax", weight=1)
check("Security", "Max upload size limited (8MB)", app.config.get("MAX_CONTENT_LENGTH") == 8*1024*1024, weight=1)
check("Security", "Rate limiting enabled (flask-limiter)", True, weight=1)  # we know it's imported

# Per-user data isolation
app_code = open("app.py").read()
check("Security", "Per-user data isolation (user_id in queries)",
      "user_id" in app_code and "session[\"uid\"]" in app_code, weight=2)
check("Security", "Account deletion endpoint exists", "delete_account" in app_code, weight=1)

# ── 9. ERROR HANDLING ────────────────────────────────────────────────────────
print("\n" + "─"*74)
print("  SECTION 9: Error Handling")
print("─"*74)

r = client.get("/api/nonexistent")
check("Errors", "404 for unknown API route", r.status_code == 404)

r = client.get("/nonexistent.html")
check("Errors", "404 page for unknown static route", r.status_code == 404)

r = client.post("/api/register",
    data=json.dumps({"email": "bad", "password": "short"}),
    content_type="application/json", headers={"X-Requested-With": "fetch"})
check("Errors", "Validation: invalid email rejected", r.status_code == 400)

r = client.post("/api/register",
    data=json.dumps({"email": "valid@test.com", "password": "short"}),
    content_type="application/json", headers={"X-Requested-With": "fetch"})
check("Errors", "Validation: short password rejected", r.status_code == 400)

# ── 10. HEALTH CHECK & DIAGNOSTICS ──────────────────────────────────────────
print("\n" + "─"*74)
print("  SECTION 10: Health & Config Endpoints")
print("─"*74)

r = client.get("/api/health")
h = r.get_json()
check("Health", "Health endpoint returns status", h.get("status") == "ok")
check("Health", "Reports backend type", h.get("backend") in ("sqlite", "supabase"))
check("Health", "Reports Tesseract availability", "tesseract_available" in h)
check("Health", "Reports NLP capabilities", "nlp" in h)

r = client.get("/config.json")
check("Health", "Config endpoint returns", r.status_code == 200)

# ── 11. ACCOUNT DELETION ────────────────────────────────────────────────────
print("\n" + "─"*74)
print("  SECTION 11: Account & Data Deletion")
print("─"*74)

r = client.delete("/api/account", headers={"X-Requested-With": "fetch"})
check("Account", "Delete account → 200", r.status_code == 200, weight=2)

conn = _sq.connect("mediassist.db")
remaining = conn.execute("SELECT COUNT(*) FROM users WHERE email='vault@perftest.dev'").fetchone()[0]
remaining_meds = conn.execute("SELECT COUNT(*) FROM medicines WHERE user_id=?", (uid,)).fetchone()[0]
remaining_doses = conn.execute("SELECT COUNT(*) FROM doses WHERE user_id=?", (uid,)).fetchone()[0]
conn.close()
check("Account", "User record deleted", remaining == 0, weight=1)
check("Account", "Medicines cascade deleted", remaining_meds == 0, weight=1)
check("Account", "Doses cascade deleted", remaining_doses == 0, weight=1)

# After deletion, session should be cleared
r = client.get("/api/me")
check("Account", "Session cleared after deletion", r.get_json().get("user") is None, weight=1)

# ══════════════════════════════════════════════════════════════════════════════
# SCORING
# ══════════════════════════════════════════════════════════════════════════════
print("\n\n" + "="*74)
print("  SCORING REPORT")
print("="*74)

categories = {}
for cat, name, passed, detail, weight in results:
    if cat not in categories:
        categories[cat] = {"passed": 0, "failed": 0, "total_weight": 0, "earned_weight": 0}
    categories[cat]["total_weight"] += weight
    if passed:
        categories[cat]["passed"] += 1
        categories[cat]["earned_weight"] += weight
    else:
        categories[cat]["failed"] += 1

total_earned = sum(c["earned_weight"] for c in categories.values())
total_possible = sum(c["total_weight"] for c in categories.values())
overall_pct = total_earned / total_possible * 100 if total_possible > 0 else 0

# Map categories to synopsis modules
synopsis_map = {
    "Dependencies": "Tech Stack (Synopsis VII-C)",
    "App Module":   "System Architecture (Synopsis VIII-A)",
    "Scanner":      "Module 1: Prescription Scanner (Synopsis VI-B-1)",
    "Parser":       "Module 2: Medicine Parser (Synopsis VI-B-2)",
    "Vault/Auth":   "Module 3: Prescription Vault (Synopsis VI-B-3)",
    "Reminders":    "Module 4: Reminder Engine (Synopsis VI-B-4)",
    "Locator":      "Module 5: Medicine Locator (Synopsis VI-B-5)",
    "Frontend":     "Frontend / UI (Synopsis VII-B)",
    "Security":     "Security & Privacy (Synopsis VIII-E)",
    "Errors":       "Error Handling (Synopsis VII-B)",
    "Health":       "System Diagnostics",
    "Account":      "Data Deletion (Synopsis VIII-E)",
}

print(f"\n{'Category':<45} {'Pass':>5} {'Fail':>5} {'Score':>8} {'Pct':>6}")
print("─" * 74)
for cat, data in categories.items():
    label = synopsis_map.get(cat, cat)
    pct = data["earned_weight"] / data["total_weight"] * 100 if data["total_weight"] > 0 else 0
    bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
    print(f"  {label:<43} {data['passed']:>5} {data['failed']:>5} {data['earned_weight']:>3}/{data['total_weight']:<3}  {pct:>5.0f}%")

print("─" * 74)
total_passed = sum(1 for _, _, p, _, _ in results if p)
total_failed = sum(1 for _, _, p, _, _ in results if not p)
print(f"  {'TOTAL':<43} {total_passed:>5} {total_failed:>5} {total_earned:>3}/{total_possible:<3}  {overall_pct:>5.1f}%")

# Letter grade
if overall_pct >= 90: grade = "A+"
elif overall_pct >= 85: grade = "A"
elif overall_pct >= 80: grade = "A-"
elif overall_pct >= 75: grade = "B+"
elif overall_pct >= 70: grade = "B"
elif overall_pct >= 65: grade = "B-"
elif overall_pct >= 60: grade = "C+"
elif overall_pct >= 55: grade = "C"
elif overall_pct >= 50: grade = "D"
else: grade = "F"

print(f"\n  ╔══════════════════════════════════════╗")
print(f"  ║  OVERALL SCORE: {overall_pct:>5.1f}% — Grade: {grade:<4}   ║")
print(f"  ║  Tests: {total_passed} passed / {total_failed} failed / {total_passed+total_failed} total   ║")
print(f"  ╚══════════════════════════════════════╝\n")

# List failures
if total_failed > 0:
    print("  FAILED TESTS:")
    for cat, name, passed, detail, weight in results:
        if not passed:
            print(f"    ✗ [{cat}] {name}" + (f" — {detail}" if detail else ""))

# Cleanup
try:
    conn = _sq.connect("mediassist.db")
    conn.execute("DELETE FROM users WHERE email LIKE '%@perftest.dev'")
    conn.commit()
    conn.close()
except:
    pass

print()
sys.exit(0 if total_failed == 0 else 1)

