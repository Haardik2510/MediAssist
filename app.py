"""
MediAssist – AI-Powered Prescription Scanner & Medicine Reminder System
Backend: Flask + Supabase (Auth + PostgreSQL) + Tesseract OCR + NLP parsing
"""
import os, re, json, secrets, smtplib, traceback
from datetime import datetime, timedelta
from email.message import EmailMessage
from functools import wraps

import cv2, numpy as np, pytesseract
from dotenv import load_dotenv

# Auto-detect Tesseract binary path on Windows if not already in PATH
_local_tess = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tesseract", "tesseract.exe")
_local_tessdata = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tesseract", "tessdata")
if os.path.isfile(_local_tess):
    pytesseract.pytesseract.tesseract_cmd = _local_tess
    os.environ["TESSDATA_PREFIX"] = _local_tessdata
else:
    for _p in [
        os.getenv("TESSERACT_CMD", ""),
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        os.path.expanduser(r"~\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"),
    ]:
        if _p and os.path.isfile(_p):
            pytesseract.pytesseract.tesseract_cmd = _p
            break
from flask import Flask, request, jsonify, session, g, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

# ─── Optional Sentry monitoring ──────────────────────────────────────────────
if os.getenv("SENTRY_DSN"):
    import sentry_sdk; sentry_sdk.init(dsn=os.environ["SENTRY_DSN"])

# ─── Supabase client ─────────────────────────────────────────────────────────
SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip().strip('"').strip("'")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "").strip().strip('"').strip("'")
USE_SUPABASE = bool(SUPABASE_URL and SUPABASE_KEY and SUPABASE_URL.startswith("http"))

supabase_client = None
if USE_SUPABASE:
    try:
        from supabase import create_client
        supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("[MediAssist] Supabase connected")
    except Exception as _e:
        print(f"[MediAssist] Supabase connection failed ({_e}) - falling back to SQLite")
        USE_SUPABASE = False
        supabase_client = None
else:
    print("[MediAssist] Supabase not configured or invalid URL - falling back to SQLite")

# ─── Optional NLP libraries ──────────────────────────────────────────────────
try:
    from rapidfuzz import fuzz as rf_fuzz, process as rf_process
    HAS_RAPIDFUZZ = True
except ImportError:
    HAS_RAPIDFUZZ = False

try:
    import spacy
    nlp = spacy.load("en_core_web_sm")
    HAS_SPACY = True
except Exception:
    HAS_SPACY = False

# ─── Flask setup ──────────────────────────────────────────────────────────────
app = Flask(__name__, static_folder="static", static_url_path="")
app.secret_key = os.getenv("SECRET_KEY") or os.getenv("FLASK_SECRET_KEY") or secrets.token_hex(32)
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=os.getenv("PROD") == "1",
    MAX_CONTENT_LENGTH=8 * 1024 * 1024,
)
limiter = Limiter(get_remote_address, app=app, default_limits=["300/hour"])

# ─── Medicine reference database for fuzzy matching ──────────────────────────
MEDICINE_DB = [
    "Metformin", "Amlodipine", "Omeprazole", "Aspirin", "Paracetamol",
    "Amoxicillin", "Cetirizine", "Atorvastatin", "Clopidogrel", "Metoprolol",
    "Ramipril", "Ecosprin", "Levothyroxine", "Vitamin D3", "Iron Folic Acid",
    "Calcium", "Diclofenac", "Pantoprazole", "Pregabalin", "Thiocolchicoside",
    "Doxycycline", "Isotretinoin", "Biotin", "Levocetirizine", "Montelukast",
    "Doxofylline", "Prednisolone", "Deriphyllin", "Multivitamin",
    "Glimepiride", "Telmisartan", "Rosuvastatin", "Insulin Glargine",
    "Escitalopram", "Clonazepam", "Propranolol", "Methylcobalamin",
    "Azithromycin", "Ciprofloxacin", "Ibuprofen", "Ranitidine",
    "Losartan", "Lisinopril", "Gabapentin", "Duloxetine", "Sertraline",
    "Fluoxetine", "Venlafaxine", "Olanzapine", "Risperidone",
    "Domperidone", "Ondansetron", "Rabeprazole", "Lansoprazole",
    "Cefixime", "Cephalexin", "Ofloxacin", "Norfloxacin",
    "Hydroxychloroquine", "Methotrexate", "Acyclovir", "Valacyclovir",
    "Atenolol", "Bisoprolol", "Diltiazem", "Verapamil",
    "Furosemide", "Spironolactone", "Hydrochlorothiazide",
    "Sitagliptin", "Vildagliptin", "Pioglitazone", "Glibenclamide",
    "Warfarin", "Rivaroxaban", "Apixaban", "Enoxaparin",
    "Salbutamol", "Budesonide", "Formoterol", "Tiotropium",
    "Amitriptyline", "Nortriptyline", "Carbamazepine", "Phenytoin",
    "Levetiracetam", "Sodium Valproate", "Clobazam", "Topiramate",
    "Fexofenadine", "Loratadine", "Chlorpheniramine", "Dexamethasone",
    "Betamethasone", "Mometasone", "Fluticasone", "Beclometasone",
    "Tramadol", "Morphine", "Fentanyl", "Codeine",
    "Cough Linctus", "Multivitamin Syrup",
]

# ─── SQLite fallback layer ────────────────────────────────────────────────────
import sqlite3
DB = os.getenv("DB_PATH", "mediassist.db")
SCHEMA = """
CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, email TEXT UNIQUE, pw TEXT, verified INT DEFAULT 0, onboarded INT DEFAULT 0, created TEXT);
CREATE TABLE IF NOT EXISTS tokens(token TEXT PRIMARY KEY, user_id INT, kind TEXT, expires TEXT);
CREATE TABLE IF NOT EXISTS prescriptions(id INTEGER PRIMARY KEY, user_id INT, raw TEXT, created TEXT);
CREATE TABLE IF NOT EXISTS medicines(id INTEGER PRIMARY KEY, rx_id INT, user_id INT, name TEXT, strength TEXT, freq TEXT, times TEXT, days INT, confidence REAL DEFAULT 1.0);
CREATE TABLE IF NOT EXISTS doses(id INTEGER PRIMARY KEY, med_id INT, user_id INT, due TEXT, status TEXT DEFAULT 'pending');
"""

def _sqlite():
    if "db" not in g:
        g.db = sqlite3.connect(DB)
        g.db.row_factory = sqlite3.Row
        g.db.executescript(SCHEMA)
        try:
            g.db.execute("ALTER TABLE medicines ADD COLUMN confidence REAL DEFAULT 1.0")
            g.db.commit()
        except sqlite3.OperationalError:
            pass
    return g.db

@app.teardown_appcontext
def close(_):
    d = g.pop("db", None)
    if d:
        d.close()

def q(sql, a=()):
    return _sqlite().execute(sql, a)

# ─── Supabase data-access layer ──────────────────────────────────────────────
class SupabaseDB:
    """Wrapper that presents the same interface as the SQLite layer
    but stores everything in Supabase PostgreSQL via the PostgREST API."""

    def __init__(self, client):
        self.sb = client

    # -- Users --
    def get_user_by_email(self, email):
        r = self.sb.table("users").select("*").eq("email", email).maybe_single().execute()
        return dict(r.data) if (r and getattr(r, "data", None)) else None

    def get_user_by_id(self, uid):
        r = self.sb.table("users").select("*").eq("id", uid).maybe_single().execute()
        return dict(r.data) if (r and getattr(r, "data", None)) else None

    def create_user(self, email, pw_hash):
        r = self.sb.table("users").insert({
            "email": email, "pw": pw_hash, "verified": 0, "onboarded": 0,
            "created": datetime.utcnow().isoformat()
        }).execute()
        return r.data[0]["id"] if (r and getattr(r, "data", None)) else None

    def verify_user(self, uid):
        self.sb.table("users").update({"verified": 1}).eq("id", uid).execute()

    def set_password(self, uid, pw_hash):
        self.sb.table("users").update({"pw": pw_hash}).eq("id", uid).execute()

    def set_onboarded(self, uid):
        self.sb.table("users").update({"onboarded": 1}).eq("id", uid).execute()

    def delete_user(self, uid):
        for t in ("doses", "medicines", "prescriptions", "tokens"):
            self.sb.table(t).delete().eq("user_id", uid).execute()
        self.sb.table("users").delete().eq("id", uid).execute()

    # -- Tokens --
    def create_token(self, tok, uid, kind, expires):
        self.sb.table("tokens").insert({
            "token": tok, "user_id": uid, "kind": kind, "expires": expires
        }).execute()

    def take_token(self, tok, kind):
        r = self.sb.table("tokens").select("*").eq("token", tok).eq("kind", kind).maybe_single().execute()
        if not r or not getattr(r, "data", None) or r.data.get("expires", "") < datetime.utcnow().isoformat():
            return None
        uid = r.data["user_id"]
        self.sb.table("tokens").delete().eq("token", tok).execute()
        return uid

    # -- Prescriptions --
    def save_prescription(self, uid, raw_text):
        r = self.sb.table("prescriptions").insert({
            "user_id": uid, "raw": raw_text[:5000],
            "created": datetime.utcnow().isoformat()
        }).execute()
        return r.data[0]["id"] if r.data else None

    def save_medicine(self, rx_id, uid, name, strength, freq, times_json, days, confidence=1.0):
        r = self.sb.table("medicines").insert({
            "rx_id": rx_id, "user_id": uid, "name": name, "strength": strength,
            "freq": freq, "times": times_json, "days": days, "confidence": confidence
        }).execute()
        return r.data[0]["id"] if r.data else None

    def save_dose(self, med_id, uid, due):
        self.sb.table("doses").insert({
            "med_id": med_id, "user_id": uid, "due": due, "status": "pending"
        }).execute()

    def get_medicines(self, uid):
        r = self.sb.table("medicines").select("id,name,strength,freq,times,days,confidence") \
            .eq("user_id", uid).order("id", desc=True).execute()
        return r.data or []

    def get_due_doses(self, uid, now_str):
        r = self.sb.table("doses").select("id,due,med_id") \
            .eq("user_id", uid).eq("status", "pending") \
            .lte("due", now_str).order("due").limit(20).execute()
        if not r.data:
            return []
        # join with medicine names
        med_ids = list({d["med_id"] for d in r.data})
        mr = self.sb.table("medicines").select("id,name,strength").in_("id", med_ids).execute()
        med_map = {m["id"]: m for m in (mr.data or [])}
        result = []
        for d in r.data:
            m = med_map.get(d["med_id"], {})
            result.append({"id": d["id"], "due": d["due"], "name": m.get("name", ""), "strength": m.get("strength", "")})
        return result

    def update_dose(self, dose_id, uid, status):
        if status == "snooze":
            new_due = (datetime.now() + timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M")
            self.sb.table("doses").update({"due": new_due}).eq("id", dose_id).eq("user_id", uid).execute()
        else:
            self.sb.table("doses").update({"status": status}).eq("id", dose_id).eq("user_id", uid).execute()

sdb = SupabaseDB(supabase_client) if USE_SUPABASE else None

# ─── Email helper ─────────────────────────────────────────────────────────────
def mail(to, subject, body):
    host = os.getenv("SMTP_HOST", "").strip()
    if not host:
        print(f"\n[MAIL to {to}] {subject}\n{body}\n")
        return
    try:
        m = EmailMessage()
        m["To"], m["From"], m["Subject"] = to, os.getenv("MAIL_FROM"), subject
        m.set_content(body)
        with smtplib.SMTP(host, int(os.getenv("SMTP_PORT", 587))) as s:
            s.starttls()
            s.login(os.environ["SMTP_USER"], os.environ["SMTP_PASS"])
            s.send_message(m)
    except Exception as e:
        print(f"\n[MAIL FAILED to {to}] {subject}\n{body}\nError: {e}\n")

# ─── Token helpers (unified for both backends) ───────────────────────────────
def make_token(uid, kind, hours):
    t = secrets.token_urlsafe(32)
    expires = (datetime.utcnow() + timedelta(hours=hours)).isoformat()
    if USE_SUPABASE:
        sdb.create_token(t, uid, kind, expires)
    else:
        q("INSERT INTO tokens VALUES(?,?,?,?)", (t, uid, kind, expires))
        _sqlite().commit()
    return t

def take_token(tok, kind):
    if USE_SUPABASE:
        return sdb.take_token(tok, kind)
    r = q("SELECT * FROM tokens WHERE token=? AND kind=?", (tok, kind)).fetchone()
    if not r or r["expires"] < datetime.utcnow().isoformat():
        return None
    q("DELETE FROM tokens WHERE token=?", (tok,))
    _sqlite().commit()
    return r["user_id"]

# ─── Auth decorator ───────────────────────────────────────────────────────────
def auth(f):
    @wraps(f)
    def w(*a, **k):
        if "uid" not in session:
            return jsonify(error="Please log in to continue."), 401
        return f(*a, **k)
    return w

# ─── Middleware ───────────────────────────────────────────────────────────────
@app.before_request
def csrf():
    if request.method in ("POST", "PUT", "DELETE") and request.path != "/api/log" \
            and request.headers.get("X-Requested-With") != "fetch":
        return jsonify(error="Invalid request."), 400

@app.after_request
def headers(r):
    r.headers.update({
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "Referrer-Policy": "same-origin",
    })
    return r

# ─── Auth routes ──────────────────────────────────────────────────────────────
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def creds():
    d = request.get_json(silent=True) or {}
    return (d.get("email") or "").strip().lower(), d.get("password") or ""


@app.post("/api/register")
@limiter.limit("5/hour")
def register():
    e, p = creds()
    if not EMAIL_RE.match(e):
        return jsonify(error="Enter a valid email address."), 400
    if len(p) < 8:
        return jsonify(error="Password must be at least 8 characters."), 400

    if USE_SUPABASE:
        if sdb.get_user_by_email(e):
            return jsonify(error="An account with this email already exists."), 409
        uid = sdb.create_user(e, generate_password_hash(p))
    else:
        if q("SELECT 1 FROM users WHERE email=?", (e,)).fetchone():
            return jsonify(error="An account with this email already exists."), 409
        uid = q("INSERT INTO users(email,pw,created) VALUES(?,?,?)",
                (e, generate_password_hash(p), datetime.utcnow().isoformat())).lastrowid
        _sqlite().commit()

    mail(e, "Verify your MediAssist email",
         f"Verify: {os.getenv('BASE_URL')}/#/verify/{make_token(uid, 'verify', 48)}")
    return jsonify(ok=True)


@app.post("/api/verify")
def verify():
    uid = take_token((request.get_json(silent=True) or {}).get("token", ""), "verify")
    if not uid:
        return jsonify(error="This link is invalid or expired."), 400
    if USE_SUPABASE:
        sdb.verify_user(uid)
    else:
        q("UPDATE users SET verified=1 WHERE id=?", (uid,))
        _sqlite().commit()
    return jsonify(ok=True)


@app.post("/api/login")
@limiter.limit("10/minute")
def login():
    e, p = creds()
    if USE_SUPABASE:
        u = sdb.get_user_by_email(e)
    else:
        row = q("SELECT * FROM users WHERE email=?", (e,)).fetchone()
        u = dict(row) if row else None

    if not u or not check_password_hash(u["pw"], p):
        return jsonify(error="Incorrect email or password."), 401
    if not u["verified"]:
        return jsonify(error="Verify your email first. Check your inbox."), 403
    session.clear()
    session["uid"] = u["id"]
    return jsonify(ok=True)


@app.post("/api/logout")
def logout():
    session.clear()
    return jsonify(ok=True)


@app.post("/api/forgot")
@limiter.limit("5/hour")
def forgot():
    e, _ = creds()
    if USE_SUPABASE:
        u = sdb.get_user_by_email(e)
        uid = u["id"] if u else None
    else:
        row = q("SELECT id FROM users WHERE email=?", (e,)).fetchone()
        uid = row["id"] if row else None
    if uid:
        mail(e, "Reset your MediAssist password",
             f"Reset: {os.getenv('BASE_URL')}/#/reset/{make_token(uid, 'reset', 1)}")
    return jsonify(ok=True)


@app.post("/api/reset")
@limiter.limit("10/hour")
def reset():
    d = request.get_json(silent=True) or {}
    if len(d.get("password", "")) < 8:
        return jsonify(error="Password must be at least 8 characters."), 400
    uid = take_token(d.get("token", ""), "reset")
    if not uid:
        return jsonify(error="This link is invalid or expired."), 400
    if USE_SUPABASE:
        sdb.set_password(uid, generate_password_hash(d["password"]))
    else:
        q("UPDATE users SET pw=? WHERE id=?", (generate_password_hash(d["password"]), uid))
        _sqlite().commit()
    return jsonify(ok=True)


@app.get("/api/me")
def me():
    if "uid" not in session:
        return jsonify(user=None)
    if USE_SUPABASE:
        u = sdb.get_user_by_id(session["uid"])
        if u:
            return jsonify(user={"email": u["email"], "onboarded": u["onboarded"]})
        return jsonify(user=None)
    else:
        u = q("SELECT email,onboarded FROM users WHERE id=?", (session["uid"],)).fetchone()
        return jsonify(user=dict(u) if u else None)


@app.post("/api/onboarded")
@auth
def onboarded():
    if USE_SUPABASE:
        sdb.set_onboarded(session["uid"])
    else:
        q("UPDATE users SET onboarded=1 WHERE id=?", (session["uid"],))
        _sqlite().commit()
    return jsonify(ok=True)


@app.delete("/api/account")
@auth
def delete_account():
    u = session["uid"]
    if USE_SUPABASE:
        sdb.delete_user(u)
    else:
        for t in ("doses", "medicines", "prescriptions", "tokens"):
            q(f"DELETE FROM {t} WHERE user_id=?", (u,))
        q("DELETE FROM users WHERE id=?", (u,))
        _sqlite().commit()
    session.clear()
    return jsonify(ok=True)


# ─── OCR + Enhanced NLP-based Parsing ─────────────────────────────────────────
FREQ = {
    "OD":  ["08:00"],
    "QD":  ["08:00"],
    "BD":  ["08:00", "20:00"],
    "BID": ["08:00", "20:00"],
    "TDS": ["08:00", "14:00", "20:00"],
    "TID": ["08:00", "14:00", "20:00"],
    "QID": ["08:00", "12:00", "16:00", "20:00"],
    "HS":  ["22:00"],
}
SLOTS = ["08:00", "14:00", "20:00"]


def fuzzy_match_medicine(name):
    """Match extracted medicine name against the reference database.
    Returns (matched_name, confidence_score)."""
    if not name or not name.strip():
        return name, 0.0

    cleaned = name.strip().title()

    # Direct match first
    for med in MEDICINE_DB:
        if med.lower() == cleaned.lower():
            return med, 1.0

    # Fuzzy match with RapidFuzz
    if HAS_RAPIDFUZZ and MEDICINE_DB:
        result = rf_process.extractOne(cleaned, MEDICINE_DB, scorer=rf_fuzz.WRatio, score_cutoff=60)
        if result:
            matched, score, _ = result
            return matched, round(score / 100.0, 2)

    # Fallback: return as-is
    return cleaned, 0.5


def preprocess_image(img_bytes):
    """Advanced image preprocessing for better OCR results."""
    # Decode image
    img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None

    # Resize if too small (improves OCR on small images)
    h, w = img.shape
    if max(h, w) < 1000:
        scale = 1500 / max(h, w)
        img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    # Denoise
    img = cv2.fastNlMeansDenoising(img, None, 10, 7, 21)

    # Increase contrast with CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    img = clahe.apply(img)

    # Adaptive thresholding for uneven lighting
    img_otsu = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # Also try adaptive thresholding
    img_adaptive = cv2.adaptiveThreshold(
        img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 8
    )

    return img_otsu, img_adaptive


def normalize_ocr_text(text):
    """Clean up common OCR artifacts and normalize text."""
    if not text:
        return ""
    # Fix common OCR misreads
    replacements = {
        "|": "l", "0D": "OD", "8D": "BD", "T0S": "TDS", "oD": "OD", "oD.": "OD",
        "HS.": "HS", "OD.": "OD", "BD.": "BD", "TDS.": "TDS", "Smg": "5mg",
        "I-0-I": "1-0-1", "l-0-l": "1-0-1", "I-I-I": "1-1-1",
        "l-l-l": "1-1-1", "l-0-0": "1-0-0", "0-0-l": "0-0-1",
        "1ab.": "Tab.", "1ab ": "Tab ", "Cap.": "Cap.",
        "tab.": "Tab.", "cap.": "Cap.", "syp.": "Syp.",
        "inj.": "Inj.",
        "rng": "mg", "rncg": "mcg",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    # Normalize multiple spaces/tabs
    text = re.sub(r"[ \t]+", " ", text)
    return text


def parse(text):
    """Enhanced prescription parser with NLP and fuzzy matching."""
    text = normalize_ocr_text(text)
    out = []

    for ln in text.splitlines():
        ln = ln.strip()
        if not ln or len(ln) < 5:
            continue

        # Match prescription line patterns:
        # Tab/Cap/Syp/Inj. MedicineName Strength Frequency Duration
        m = re.match(
            r"^[\W]*(?:tab(?:let)?|cap(?:sule)?|syp(?:rup)?|inj(?:ection)?)?"
            r"\.?\s*"
            r"([A-Za-z][A-Za-z\- ]{2,40}?)"    # medicine name
            r"\s*"
            r"(\d+\s*(?:mg|mcg|g|ml|IU|units?))?"  # strength (optional)
            r"\b(.*?)$",                          # rest of line
            ln, re.I
        )
        if not m or not m.group(1).strip():
            continue

        raw_name = m.group(1).strip()
        strength = (m.group(2) or "").replace(" ", "")
        rest = m.group(3)
        times, label = None, None

        # Pattern 1: 1-0-1 notation
        p = re.search(r"\b([01])\s*[-–]\s*([01])\s*[-–]\s*([01])\b", rest)
        if p:
            times = [SLOTS[i] for i in range(3) if p.group(i + 1) == "1"]
            label = f"{p.group(1)}-{p.group(2)}-{p.group(3)}"
        else:
            # Pattern 2: Frequency abbreviation (OD, BD, TDS, etc.)
            w = re.search(r"\b(OD|QD|BD|BID|TDS|TID|QID|HS)\b", rest, re.I)
            if w:
                label = w.group(1).upper()
                times = FREQ[label]

        if not times:
            continue

        # Duration: look for "X days" or "X d"
        d = re.search(r"(\d+)\s*(?:days?|d)\b", rest, re.I)
        days = int(d.group(1)) if d else 5

        # Fuzzy-match medicine name
        matched_name, confidence = fuzzy_match_medicine(raw_name)

        out.append({
            "name": matched_name,
            "raw_name": raw_name,
            "strength": strength,
            "freq": label,
            "times": times,
            "days": days,
            "confidence": confidence,
        })

    return out


@app.post("/api/scan")
@auth
@limiter.limit("20/hour")
def scan():
    f = request.files.get("image")
    if not f:
        return jsonify(error="Upload a valid prescription image (JPG or PNG)."), 400

    img_bytes = f.read()
    result = preprocess_image(img_bytes)
    if result is None:
        return jsonify(error="Upload a valid prescription image (JPG or PNG)."), 400

    img_otsu, img_adaptive = result

    # Try OCR with both preprocessing styles and PSM modes, picking the highest medicine yield
    candidates = []
    for img in (img_otsu, img_adaptive):
        for cfg in ("", "--psm 6"):
            try:
                raw_cand = pytesseract.image_to_string(img, config=cfg)
                meds_cand = parse(raw_cand)
                candidates.append((len(meds_cand), raw_cand, meds_cand))
            except Exception:
                pass

    if not candidates:
        return jsonify(error="OCR engine unavailable on the server. Install Tesseract."), 503

    candidates.sort(key=lambda c: c[0], reverse=True)
    raw, medicines = candidates[0][1], candidates[0][2]

    return jsonify(raw=raw, medicines=medicines)


@app.post("/api/prescriptions")
@auth
def save_rx():
    d = request.get_json(silent=True) or {}
    meds = d.get("medicines") or []
    u = session["uid"]
    if not meds:
        return jsonify(error="Add at least one medicine before saving."), 400

    if USE_SUPABASE:
        rx_id = sdb.save_prescription(u, d.get("raw", ""))
        for m in meds:
            name = str(m.get("name", "")).strip()[:60]
            times = [t for t in m.get("times", []) if re.match(r"^\d\d:\d\d$", str(t))]
            if not name or not times:
                return jsonify(error="Every medicine needs a name and at least one valid time."), 400
            days = max(1, min(int(m.get("days") or 5), 365))
            confidence = float(m.get("confidence", 1.0))
            mid = sdb.save_medicine(rx_id, u, name, str(m.get("strength", ""))[:20],
                                     str(m.get("freq", ""))[:10], json.dumps(times), days, confidence)
            for n in range(days):
                for t in times:
                    sdb.save_dose(mid, u, (datetime.now() + timedelta(days=n)).strftime("%Y-%m-%d ") + t)
    else:
        rx = q("INSERT INTO prescriptions(user_id,raw,created) VALUES(?,?,?)",
               (u, d.get("raw", "")[:5000], datetime.utcnow().isoformat())).lastrowid
        for m in meds:
            name = str(m.get("name", "")).strip()[:60]
            times = [t for t in m.get("times", []) if re.match(r"^\d\d:\d\d$", str(t))]
            if not name or not times:
                return jsonify(error="Every medicine needs a name and at least one valid time."), 400
            days = max(1, min(int(m.get("days") or 5), 365))
            confidence = float(m.get("confidence", 1.0))
            mid = q("INSERT INTO medicines(rx_id,user_id,name,strength,freq,times,days,confidence) VALUES(?,?,?,?,?,?,?,?)",
                     (rx, u, name, str(m.get("strength", ""))[:20],
                      str(m.get("freq", ""))[:10], json.dumps(times), days, confidence)).lastrowid
            for n in range(days):
                for t in times:
                    q("INSERT INTO doses(med_id,user_id,due) VALUES(?,?,?)",
                      (mid, u, (datetime.now() + timedelta(days=n)).strftime("%Y-%m-%d ") + t))
        _sqlite().commit()
    return jsonify(ok=True)


@app.get("/api/medicines")
@auth
def meds():
    if USE_SUPABASE:
        rows = sdb.get_medicines(session["uid"])
        return jsonify([{**x, "times": json.loads(x["times"]) if isinstance(x["times"], str) else x["times"]}
                        for x in rows])
    else:
        r = q("SELECT m.id,m.name,m.strength,m.freq,m.times,m.days,m.confidence FROM medicines m WHERE m.user_id=? ORDER BY m.id DESC",
              (session["uid"],)).fetchall()
        return jsonify([dict(x, times=json.loads(x["times"])) for x in r])


@app.get("/api/reminders/due")
@auth
def due():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    if USE_SUPABASE:
        return jsonify(sdb.get_due_doses(session["uid"], now))
    else:
        r = q("SELECT d.id,d.due,m.name,m.strength FROM doses d JOIN medicines m ON m.id=d.med_id "
              "WHERE d.user_id=? AND d.status='pending' AND d.due<=? ORDER BY d.due LIMIT 20",
              (session["uid"], now)).fetchall()
        return jsonify([dict(x) for x in r])


@app.post("/api/doses/<int:i>")
@auth
def dose(i):
    s = (request.get_json(silent=True) or {}).get("status")
    if s not in ("taken", "skipped", "snooze"):
        return jsonify(error="Invalid action."), 400
    if USE_SUPABASE:
        sdb.update_dose(i, session["uid"], s)
    else:
        if s == "snooze":
            q("UPDATE doses SET due=? WHERE id=? AND user_id=?",
              ((datetime.now() + timedelta(minutes=10)).strftime("%Y-%m-%d %H:%M"), i, session["uid"]))
        else:
            q("UPDATE doses SET status=? WHERE id=? AND user_id=?", (s, i, session["uid"]))
        _sqlite().commit()
    return jsonify(ok=True)


# ─── Static / Config / Error handlers ────────────────────────────────────────
@app.errorhandler(404)
def nf(_):
    if request.path.startswith("/api/"):
        return jsonify(error="Not found."), 404
    return send_from_directory("static", "404.html"), 404

@app.errorhandler(429)
def rl(_):
    return jsonify(error="Too many attempts. Wait a few minutes and try again."), 429

@app.errorhandler(Exception)
def handle_exception(e):
    traceback.print_exc()
    if request.path.startswith("/api/"):
        code = getattr(e, "code", 500)
        return jsonify(error=getattr(e, "description", None) or str(e) or "Internal server error"), code
    return send_from_directory("static", "404.html"), 500

@app.get("/config.json")
def cfg():
    return jsonify(
        plausible=os.getenv("PLAUSIBLE_DOMAIN") or None,
        google_maps_key=os.getenv("GOOGLE_MAPS_KEY") or None,
        geoapify_key=os.getenv("GEOAPIFY_KEY") or None,
    )

@app.post("/api/log")
def clientlog():
    app.logger.error("client error: %s", request.get_data(as_text=True)[:300])
    return "", 204

@app.get("/")
def home():
    return send_from_directory("static", "index.html")

# ─── Health check & status ────────────────────────────────────────────────────
@app.get("/api/health")
def health():
    status = {
        "status": "ok",
        "backend": "supabase" if USE_SUPABASE else "sqlite",
        "ocr_engine": "tesseract",
        "nlp": {
            "rapidfuzz": HAS_RAPIDFUZZ,
            "spacy": HAS_SPACY,
        },
        "timestamp": datetime.utcnow().isoformat(),
    }
    # Check Tesseract
    try:
        pytesseract.get_tesseract_version()
        status["tesseract_available"] = True
    except Exception:
        status["tesseract_available"] = False
    return jsonify(status)


if __name__ == "__main__":
    app.run(debug=os.getenv("PROD") != "1")
