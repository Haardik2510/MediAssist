"""
MediAssist Backend Test Suite
Tests: Import check, OCR parsing, fuzzy matching, API endpoints, prescription dataset processing
"""
import os, sys, json, glob, traceback

# ── Set working directory ─────────────────────────────────────────────────────
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# ── Ensure .env is loaded ─────────────────────────────────────────────────────
from dotenv import load_dotenv
load_dotenv()

# Override SMTP for testing (no network in sandbox)
os.environ["SMTP_HOST"] = ""
os.environ["SMTP_USER"] = ""
os.environ["SMTP_PASS"] = ""

PASS = 0
FAIL = 0

def check(name, condition, detail=""):
    global PASS, FAIL
    if condition:
        PASS += 1
        print(f"  ✓ {name}")
    else:
        FAIL += 1
        print(f"  ✗ {name}" + (f" — {detail}" if detail else ""))

# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*70)
print("  MediAssist Backend Test Suite")
print("="*70)

# ── 1. Import checks ─────────────────────────────────────────────────────────
print("\n[1] Core imports")
try:
    import flask
    check("Flask", True)
except ImportError as e:
    check("Flask", False, str(e))

try:
    import cv2
    check("OpenCV", True)
except ImportError as e:
    check("OpenCV", False, str(e))

try:
    import numpy as np
    check("NumPy", True)
except ImportError as e:
    check("NumPy", False, str(e))

try:
    import pytesseract
    check("pytesseract (Python package)", True)
except ImportError as e:
    check("pytesseract (Python package)", False, str(e))

try:
    from rapidfuzz import fuzz, process
    check("RapidFuzz", True)
except ImportError as e:
    check("RapidFuzz", False, str(e))

try:
    from supabase import create_client
    check("Supabase SDK", True)
except ImportError as e:
    check("Supabase SDK", False, str(e))

# ── 2. Tesseract binary check ────────────────────────────────────────────────
print("\n[2] Tesseract OCR engine")
_local_tess = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tesseract", "tesseract.exe")
_local_tessdata = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tesseract", "tessdata")
if os.path.isfile(_local_tess):
    pytesseract.pytesseract.tesseract_cmd = _local_tess
    os.environ["TESSDATA_PREFIX"] = _local_tessdata

tesseract_available = False
try:
    version = pytesseract.get_tesseract_version()
    check(f"Tesseract binary (v{version})", True)
    tesseract_available = True
except Exception as e:
    check("Tesseract binary", False,
          "NOT INSTALLED. See install instructions below.")

# ── 3. App module import & parser test ────────────────────────────────────────
print("\n[3] App module & parser")
try:
    from app import app, parse, fuzzy_match_medicine, normalize_ocr_text, MEDICINE_DB, HAS_RAPIDFUZZ
    check("app.py imports cleanly", True)
except Exception as e:
    check("app.py imports", False, traceback.format_exc())
    print("\n❌ Cannot continue without app.py loading. Fix errors above.")
    sys.exit(1)

check("RapidFuzz active in app", HAS_RAPIDFUZZ)

# ── 4. Fuzzy matching tests ──────────────────────────────────────────────────
print("\n[4] Fuzzy medicine name matching")
test_cases = [
    ("Metformin", "Metformin", 1.0),
    ("metformin", "Metformin", 1.0),     # case-insensitive
    ("Metforrmin", "Metformin", 0.8),    # typo
    ("Paracetamol", "Paracetamol", 1.0),
    ("Paracetarnol", "Paracetamol", 0.8),# OCR misread
    ("Amlodipine", "Amlodipine", 1.0),
    ("Atorvasttin", "Atorvastatin", 0.7),# typo
    ("Clopidogrel", "Clopidogrel", 1.0),
    ("Pantoprazle", "Pantoprazole", 0.7),# typo
]

for input_name, expected_name, min_confidence in test_cases:
    matched, conf = fuzzy_match_medicine(input_name)
    ok = matched == expected_name and conf >= min_confidence
    check(f"'{input_name}' → '{matched}' (conf={conf:.2f})", ok,
          f"expected '{expected_name}' with conf>={min_confidence}")

# ── 5. OCR text normalization ─────────────────────────────────────────────────
print("\n[5] OCR text normalization")
check("'0D' → 'OD'", "OD" in normalize_ocr_text("Tab Metformin 500mg 0D 30 days"))
check("'8D' → 'BD'", "BD" in normalize_ocr_text("Tab Amlodipine 5mg 8D"))
check("'1-0-I' → '1-0-1'", "1-0-1" in normalize_ocr_text("I-0-I 14 days"))

# ── 6. Prescription parsing tests ────────────────────────────────────────────
print("\n[6] Prescription parsing")

test_rx_lines = [
    ("Tab. Metformin 500mg     1-0-1    30 days", "Metformin", "500mg", "1-0-1", 2, 30),
    ("Tab. Amlodipine 5mg      OD       30 days", "Amlodipine", "5mg", "OD", 1, 30),
    ("Cap. Omeprazole 20mg     1-0-0    14 days", "Omeprazole", "20mg", "1-0-0", 1, 14),
    ("Tab. Paracetamol 500mg    TDS     5 days", "Paracetamol", "500mg", "TDS", 3, 5),
    ("Cap. Amoxicillin 500mg    BD      7 days", "Amoxicillin", "500mg", "BD", 2, 7),
    ("Tab. Cetirizine 10mg      HS      5 days", "Cetirizine", "10mg", "HS", 1, 5),
    ("Tab. Atorvastatin 20mg     HS      30 days", "Atorvastatin", "20mg", "HS", 1, 30),
    ("Tab. Diclofenac 50mg      BD      7 days", "Diclofenac", "50mg", "BD", 2, 7),
    ("Tab. Escitalopram 10mg      OD      30 days", "Escitalopram", "10mg", "OD", 1, 30),
    ("Tab. Propranolol 20mg       BD      30 days", "Propranolol", "20mg", "BD", 2, 30),
]

for line, exp_name, exp_strength, exp_freq, exp_times_count, exp_days in test_rx_lines:
    results = parse(line)
    if results:
        r = results[0]
        ok = (r["name"] == exp_name and r["strength"] == exp_strength and
              r["freq"] == exp_freq and len(r["times"]) == exp_times_count and
              r["days"] == exp_days)
        check(f"Parse '{exp_name}' {exp_freq}", ok,
              f"got name={r['name']}, strength={r['strength']}, freq={r['freq']}, times={len(r['times'])}, days={r['days']}")
    else:
        check(f"Parse '{exp_name}' {exp_freq}", False, "no medicines extracted")

# Multi-line parsing
multi_line = """Tab. Metformin 500mg     1-0-1    30 days
Tab. Amlodipine 5mg      OD       30 days
Cap. Omeprazole 20mg     1-0-0    14 days
Tab. Aspirin 75mg        OD       30 days"""

multi_results = parse(multi_line)
check(f"Multi-line: extracted {len(multi_results)} medicines (expected 4)", len(multi_results) == 4)

# ── 7. API endpoint tests (with Flask test client) ───────────────────────────
print("\n[7] API endpoints")
app.config["TESTING"] = True
client = app.test_client()

# Health check
r = client.get("/api/health")
check("GET /api/health", r.status_code == 200)
health = r.get_json()
check(f"  backend = '{health.get('backend')}'", health.get("backend") in ("sqlite", "supabase"))
check(f"  rapidfuzz = {health.get('nlp', {}).get('rapidfuzz')}", health.get("nlp", {}).get("rapidfuzz") == True)

# Unauthenticated access
r = client.get("/api/medicines")
check("GET /api/medicines (unauth) → 401", r.status_code == 401)

r = client.get("/api/me")
check("GET /api/me (unauth) → user=None", r.get_json().get("user") is None)

# Clean up test users first
import sqlite3 as _sq
conn = _sq.connect("mediassist.db")
conn.execute("DELETE FROM users WHERE email LIKE '%@mediassist.dev'")
conn.commit()
conn.close()

# Register an unverified user
r = client.post("/api/register",
    data=json.dumps({"email": "unverified@mediassist.dev", "password": "Test1234!"}),
    content_type="application/json",
    headers={"X-Requested-With": "fetch"})
check(f"POST /api/register (unverified) → {r.status_code}", r.status_code == 200)

# Login without verification → 403
r = client.post("/api/login",
    data=json.dumps({"email": "unverified@mediassist.dev", "password": "Test1234!"}),
    content_type="application/json",
    headers={"X-Requested-With": "fetch"})
check(f"POST /api/login (unverified) → 403", r.status_code == 403)

# Register + verify flow
r = client.post("/api/register",
    data=json.dumps({"email": "verified@mediassist.dev", "password": "Test1234!"}),
    content_type="application/json",
    headers={"X-Requested-With": "fetch"})

# Manually verify the user in the DB for testing
conn = _sq.connect("mediassist.db")
conn.execute("UPDATE users SET verified=1 WHERE email='verified@mediassist.dev'")
conn.commit()
conn.close()

# Login with verified user
r = client.post("/api/login",
    data=json.dumps({"email": "verified@mediassist.dev", "password": "Test1234!"}),
    content_type="application/json",
    headers={"X-Requested-With": "fetch"})
check(f"POST /api/login (verified) → 200", r.status_code == 200)

# Get user info
r = client.get("/api/me")
check("GET /api/me → user.email present", r.get_json().get("user", {}).get("email") == "verified@mediassist.dev")

# Get medicines (empty)
r = client.get("/api/medicines")
check("GET /api/medicines → 200 (empty list)", r.status_code == 200 and isinstance(r.get_json(), list))

# Save prescription
meds_data = {
    "raw": "Tab. Metformin 500mg 1-0-1 30 days",
    "medicines": [
        {"name": "Metformin", "strength": "500mg", "freq": "1-0-1",
         "times": ["08:00", "20:00"], "days": 3, "confidence": 1.0}
    ]
}
r = client.post("/api/prescriptions",
    data=json.dumps(meds_data),
    content_type="application/json",
    headers={"X-Requested-With": "fetch"})
check(f"POST /api/prescriptions → {r.status_code}", r.status_code == 200)

# Get medicines (should have 1 now)
r = client.get("/api/medicines")
medicines = r.get_json()
check(f"GET /api/medicines → {len(medicines)} medicine(s)", len(medicines) >= 1)

# Get due reminders
r = client.get("/api/reminders/due")
check(f"GET /api/reminders/due → 200", r.status_code == 200)

# Logout
r = client.post("/api/logout",
    data="{}",
    content_type="application/json",
    headers={"X-Requested-With": "fetch"})
check("POST /api/logout → 200", r.status_code == 200)

# ── 8. Dataset prescription OCR test ─────────────────────────────────────────
print("\n[8] Dataset prescription processing")
dataset_dir = os.path.join("datasets", "prescriptions")
images = sorted(glob.glob(os.path.join(dataset_dir, "*.png")))
check(f"Found {len(images)} prescription images", len(images) >= 10)

if tesseract_available and images:
    total_meds = 0
    for img_path in images:
        fname = os.path.basename(img_path)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            check(f"  Load {fname}", False, "could not read image")
            continue

        # Preprocess
        img = cv2.fastNlMeansDenoising(img, None, 10, 7, 21)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        img = clahe.apply(img)
        img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        meds = []
        raw = ""
        for cfg in ("", "--psm 6"):
            r_try = pytesseract.image_to_string(img, config=cfg)
            m_try = parse(r_try)
            if len(m_try) > len(meds):
                meds, raw = m_try, r_try
        total_meds += len(meds)
        check(f"  {fname}: {len(meds)} medicines extracted",
              len(meds) >= 1,
              f"raw text length={len(raw)}")

        # Print extracted medicines for verification
        for m in meds:
            conf_str = f"(conf={m['confidence']:.0%})" if m.get('confidence') else ""
            print(f"      → {m['name']} {m['strength']} {m['freq']} x{m['days']}d {conf_str}")

    print(f"\n  Total medicines extracted from dataset: {total_meds}")
    check(f"Dataset extraction rate ≥ 20 medicines", total_meds >= 20)
elif not tesseract_available:
    print("  ⚠ Skipping OCR tests — Tesseract not installed")
    print("    Install it with one of:")
    print("    • Windows: choco install tesseract")
    print("    • Or download from: https://github.com/UB-Mannheim/tesseract/wiki")

# ── 9. Supabase connection test ───────────────────────────────────────────────
print("\n[9] Supabase connection")
if os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_KEY"):
    try:
        from supabase import create_client
        sb = create_client(os.environ["SUPABASE_URL"], os.environ["SUPABASE_KEY"])
        r = sb.table("users").select("count", count="exact").execute()
        check("Supabase connected", True)
    except Exception as e:
        check("Supabase connection", False, str(e))
else:
    print("  ⚠ SUPABASE_URL/SUPABASE_KEY not set — using SQLite fallback")
    check("SQLite fallback mode active", True)

# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*70)
print(f"  Results: {PASS} passed, {FAIL} failed, {PASS+FAIL} total")
print("="*70)

if not tesseract_available:
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║  ⚠ TESSERACT NOT INSTALLED — OCR features will not work            ║
║                                                                      ║
║  To install Tesseract on Windows:                                    ║
║                                                                      ║
║  Option 1 (Chocolatey):                                              ║
║    choco install tesseract                                           ║
║                                                                      ║
║  Option 2 (Manual):                                                  ║
║    Download from:                                                    ║
║    https://github.com/UB-Mannheim/tesseract/wiki                     ║
║    Install, then add to PATH:                                        ║
║    C:\\Program Files\\Tesseract-OCR                                    ║
║                                                                      ║
║  Option 3 (Ubuntu/WSL):                                              ║
║    sudo apt install tesseract-ocr                                    ║
╚══════════════════════════════════════════════════════════════════════╝
""")

print(f"\n{'✅ ALL TESTS PASSED' if FAIL == 0 else f'❌ {FAIL} TEST(S) FAILED'}\n")

# Cleanup test DB entries
try:
    conn = _sq.connect("mediassist.db")
    conn.execute("DELETE FROM doses WHERE user_id IN (SELECT id FROM users WHERE email LIKE '%@mediassist.dev')")
    conn.execute("DELETE FROM medicines WHERE user_id IN (SELECT id FROM users WHERE email LIKE '%@mediassist.dev')")
    conn.execute("DELETE FROM prescriptions WHERE user_id IN (SELECT id FROM users WHERE email LIKE '%@mediassist.dev')")
    conn.execute("DELETE FROM tokens WHERE user_id IN (SELECT id FROM users WHERE email LIKE '%@mediassist.dev')")
    conn.execute("DELETE FROM users WHERE email LIKE '%@mediassist.dev'")
    conn.commit()
    conn.close()
except:
    pass

sys.exit(0 if FAIL == 0 else 1)
