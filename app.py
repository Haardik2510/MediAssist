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
        "/usr/bin/tesseract",
        "/usr/local/bin/tesseract",
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
# Deterministic persistent secret key prevents logout on Gunicorn worker switches or server restarts
_persistent_secret = "mediassist_persistent_session_key_production_2026_secured_v1"
app.secret_key = os.getenv("SECRET_KEY") or os.getenv("FLASK_SECRET_KEY") or _persistent_secret
app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE="Lax",
    SESSION_COOKIE_SECURE=False,
    PERMANENT_SESSION_LIFETIME=timedelta(days=30),
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
    """Wrapper that presents the data interface for Prescriptions,
    Medicines, and Doses in Supabase PostgreSQL."""

    def __init__(self, client):
        self.sb = client

    # -- Prescriptions --
    def save_prescription(self, uid, raw_text):
        r = self.sb.table("prescriptions").insert({
            "user_id": str(uid), "raw": raw_text[:5000],
            "created": datetime.utcnow().isoformat()
        }).execute()
        return r.data[0]["id"] if (r and getattr(r, "data", None)) else None

    def save_medicine(self, rx_id, uid, name, strength, freq, times_json, days, confidence=1.0):
        r = self.sb.table("medicines").insert({
            "rx_id": rx_id, "user_id": str(uid), "name": name, "strength": strength,
            "freq": freq, "times": times_json, "days": days, "confidence": confidence
        }).execute()
        return r.data[0]["id"] if (r and getattr(r, "data", None)) else None

    def save_dose(self, med_id, uid, due):
        self.sb.table("doses").insert({
            "med_id": med_id, "user_id": str(uid), "due": due, "status": "pending"
        }).execute()

    def get_medicines(self, uid):
        r = self.sb.table("medicines").select("id,name,strength,freq,times,days,confidence") \
            .eq("user_id", str(uid)).order("id", desc=True).execute()
        return r.data or []

    def get_due_doses(self, uid, now_str):
        r = self.sb.table("doses").select("id,due,med_id") \
            .eq("user_id", str(uid)).eq("status", "pending") \
            .lte("due", now_str).order("due").limit(20).execute()
        if not r or not getattr(r, "data", None):
            return []
        med_ids = list({d["med_id"] for d in r.data})
        if not med_ids:
            return []
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
            self.sb.table("doses").update({"due": new_due}).eq("id", dose_id).eq("user_id", str(uid)).execute()
        else:
            self.sb.table("doses").update({"status": status}).eq("id", dose_id).eq("user_id", str(uid)).execute()

    def delete_medicine(self, med_id, uid):
        self.sb.table("doses").delete().eq("med_id", med_id).eq("user_id", str(uid)).execute()
        self.sb.table("medicines").delete().eq("id", med_id).eq("user_id", str(uid)).execute()

    def batch_delete_medicines(self, med_ids, uid):
        self.sb.table("doses").delete().in_("med_id", med_ids).eq("user_id", str(uid)).execute()
        self.sb.table("medicines").delete().in_("id", med_ids).eq("user_id", str(uid)).execute()

    def get_timeline(self, uid, date_str):
        prefix = f"{date_str}%"
        r = self.sb.table("doses").select("id,due,status,med_id") \
            .eq("user_id", str(uid)).like("due", prefix).order("due").execute()
        doses_data = r.data or []
        if not doses_data:
            return []
        med_ids = list({d["med_id"] for d in doses_data})
        if not med_ids:
            return []
        mr = self.sb.table("medicines").select("id,name,strength").in_("id", med_ids).execute()
        med_map = {m["id"]: m for m in (mr.data or [])}
        res = []
        for d in doses_data:
            m = med_map.get(d["med_id"], {})
            res.append({
                "id": d["id"],
                "due": d["due"],
                "status": d.get("status", "pending"),
                "name": m.get("name", "Medicine"),
                "strength": m.get("strength", "")
            })
        return res

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
@limiter.limit("60/hour")
def register():
    e, p = creds()
    if not EMAIL_RE.match(e):
        return jsonify(error="Enter a valid email address."), 400
    if len(p) < 8:
        return jsonify(error="Password must be at least 8 characters."), 400

    if USE_SUPABASE:
        try:
            res = supabase_client.auth.sign_up({"email": e, "password": p})
            if not res or not res.user:
                return jsonify(error="Failed to create account with Supabase."), 400
            msg = "Account created! Check your email for the confirmation link, then log in."
            if res.user.confirmed_at or res.session:
                msg = "Account created successfully! You can now log in."
            return jsonify(ok=True, message=msg)
        except Exception as ex:
            err_msg = str(ex)
            if "already registered" in err_msg.lower():
                return jsonify(error="An account with this email already exists."), 409
            if "rate limit" in err_msg.lower():
                # Automatic bypass for Supabase email rate limits
                try:
                    admin_res = supabase_client.auth.admin.create_user({
                        "email": e,
                        "password": p,
                        "email_confirm": True
                    })
                    if admin_res and admin_res.user:
                        return jsonify(ok=True, message="Account created and verified! You can now log in directly.")
                except Exception as admin_ex:
                    if "already registered" in str(admin_ex).lower():
                        return jsonify(error="An account with this email already exists."), 409
                    return jsonify(error=f"Registration failed: {str(admin_ex)}"), 400
            return jsonify(error=err_msg), 400
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
    d = request.get_json(silent=True) or {}
    tok = d.get("token", "")
    if USE_SUPABASE:
        try:
            res = supabase_client.auth.verify_otp({"token_hash": tok, "type": "signup"})
            if res and res.user:
                return jsonify(ok=True)
        except Exception:
            pass
        return jsonify(ok=True)
    else:
        uid = take_token(tok, "verify")
        if not uid:
            return jsonify(error="This link is invalid or expired."), 400
        q("UPDATE users SET verified=1 WHERE id=?", (uid,))
        _sqlite().commit()
        return jsonify(ok=True)


@app.post("/api/login")
@limiter.limit("60/minute")
def login():
    e, p = creds()
    if USE_SUPABASE:
        try:
            res = supabase_client.auth.sign_in_with_password({"email": e, "password": p})
            if not res or not res.user:
                return jsonify(error="Incorrect email or password."), 401
            session.clear()
            session.permanent = True
            uid = str(res.user.id)
            session["uid"] = uid
            session["email"] = res.user.email
            onb = 0
            try:
                pr = supabase_client.table("profiles").select("onboarded").eq("id", uid).maybe_single().execute()
                if pr and getattr(pr, "data", None):
                    onb = int(pr.data.get("onboarded", 0))
            except Exception:
                pass
            session["onboarded"] = onb
            return jsonify(ok=True)
        except Exception as ex:
            err_msg = str(ex).lower()
            if "invalid login credentials" in err_msg:
                return jsonify(error="Incorrect email or password."), 401
            if "email not confirmed" in err_msg:
                return jsonify(error="Please confirm your email first. Check your inbox for the Supabase confirmation link."), 403
            return jsonify(error=str(ex)), 400
    else:
        row = q("SELECT * FROM users WHERE email=?", (e,)).fetchone()
        u = dict(row) if row else None
        if not u or not check_password_hash(u["pw"], p):
            return jsonify(error="Incorrect email or password."), 401
        if not u["verified"]:
            return jsonify(error="Verify your email first. Check your inbox."), 403
        session.clear()
        session.permanent = True
        session["uid"] = u["id"]
        session["email"] = u["email"]
        return jsonify(ok=True)


@app.post("/api/logout")
def logout():
    if USE_SUPABASE:
        try:
            supabase_client.auth.sign_out()
        except Exception:
            pass
    session.clear()
    return jsonify(ok=True)


@app.post("/api/forgot")
@limiter.limit("30/hour")
def forgot():
    e, _ = creds()
    if not EMAIL_RE.match(e):
        return jsonify(error="Enter a valid email address."), 400
    if USE_SUPABASE:
        try:
            base = os.getenv("BASE_URL", "").rstrip("/")
            opts = {"redirect_to": f"{base}/#/reset"} if base else {}
            supabase_client.auth.reset_password_for_email(e, opts)
        except Exception as ex:
            print("[MediAssist] Supabase reset password email error:", ex)
        return jsonify(ok=True)
    else:
        row = q("SELECT id FROM users WHERE email=?", (e,)).fetchone()
        if row:
            mail(e, "Reset your MediAssist password",
                 f"Reset: {os.getenv('BASE_URL')}/#/reset/{make_token(row['id'], 'reset', 1)}")
        return jsonify(ok=True)


@app.post("/api/reset")
@limiter.limit("10/hour")
def reset():
    d = request.get_json(silent=True) or {}
    p = d.get("password", "")
    if len(p) < 8:
        return jsonify(error="Password must be at least 8 characters."), 400

    if USE_SUPABASE:
        uid = session.get("uid")
        if uid:
            try:
                supabase_client.auth.admin.update_user_by_id(str(uid), {"password": p})
                return jsonify(ok=True)
            except Exception as ex:
                return jsonify(error=str(ex)), 400
        tok = d.get("token", "")
        if tok:
            try:
                res = supabase_client.auth.verify_otp({"token_hash": tok, "type": "recovery"})
                if res and res.user:
                    supabase_client.auth.admin.update_user_by_id(str(res.user.id), {"password": p})
                    return jsonify(ok=True)
            except Exception:
                pass
        return jsonify(error="This reset link is invalid or expired."), 400
    else:
        uid = take_token(d.get("token", ""), "reset")
        if not uid:
            return jsonify(error="This reset link is invalid or expired."), 400
        q("UPDATE users SET pw=? WHERE id=?", (generate_password_hash(p), uid))
        _sqlite().commit()
        return jsonify(ok=True)


@app.get("/api/me")
def me():
    if "uid" not in session:
        return jsonify(user=None)
    if USE_SUPABASE:
        uid = str(session["uid"])
        email = session.get("email", "")
        onboarded_val = session.get("onboarded", 0)
        try:
            pr = supabase_client.table("profiles").select("onboarded,email").eq("id", uid).maybe_single().execute()
            if pr and getattr(pr, "data", None):
                email = pr.data.get("email") or email
                onboarded_val = pr.data.get("onboarded", onboarded_val)
        except Exception:
            pass
        return jsonify(user={"email": email, "onboarded": int(onboarded_val)})
    else:
        u = q("SELECT email,onboarded FROM users WHERE id=?", (session["uid"],)).fetchone()
        return jsonify(user=dict(u) if u else None)


@app.post("/api/onboarded")
@auth
def onboarded():
    uid = str(session["uid"])
    if USE_SUPABASE:
        try:
            supabase_client.table("profiles").update({"onboarded": 1}).eq("id", uid).execute()
        except Exception as ex:
            print("[MediAssist] update onboarded error:", ex)
        session["onboarded"] = 1
    else:
        q("UPDATE users SET onboarded=1 WHERE id=?", (session["uid"],))
        _sqlite().commit()
    return jsonify(ok=True)


@app.delete("/api/account")
@auth
def delete_account():
    uid = str(session["uid"])
    if USE_SUPABASE:
        for t in ("doses", "medicines", "prescriptions"):
            try:
                supabase_client.table(t).delete().eq("user_id", uid).execute()
            except Exception:
                pass
        try:
            supabase_client.table("profiles").delete().eq("id", uid).execute()
        except Exception:
            pass
        try:
            supabase_client.auth.admin.delete_user(uid)
        except Exception as ex:
            print("[MediAssist] delete user error:", ex)
    else:
        for t in ("doses", "medicines", "prescriptions", "tokens"):
            q(f"DELETE FROM {t} WHERE user_id=?", (uid,))
        q("DELETE FROM users WHERE id=?", (uid,))
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
    """Advanced high-speed image preprocessing for accurate OCR results."""
    # Decode image
    img = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None

    # Normalize dimensions: cap max size at 1600px for speed, floor at 1000px for clarity
    h, w = img.shape
    max_dim = max(h, w)
    if max_dim > 1600:
        scale = 1600.0 / max_dim
        img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
    elif max_dim < 1000:
        scale = 1500.0 / max_dim
        img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

    # Fast Gaussian noise reduction (instantaneous vs slow non-local means)
    blurred = cv2.GaussianBlur(img, (3, 3), 0)

    # Increase contrast with CLAHE
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    img_contrasted = clahe.apply(blurred)

    # 1. Otsu thresholding
    img_otsu = cv2.threshold(img_contrasted, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # 2. Adaptive thresholding
    img_adaptive = cv2.adaptiveThreshold(
        img_contrasted, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 15, 8
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
@limiter.limit("60/hour")
def scan():
    f = request.files.get("image")
    if not f:
        return jsonify(error="Upload a valid prescription image (JPG or PNG)."), 400

    img_bytes = f.read()
    result = preprocess_image(img_bytes)
    if result is None:
        return jsonify(error="Upload a valid prescription image (JPG or PNG)."), 400

    img_otsu, img_adaptive = result

    # Fast first pass (Otsu thresholding, ~0.3s)
    raw = ""
    meds = []
    try:
        raw = pytesseract.image_to_string(img_otsu)
        meds = parse(raw)
    except Exception:
        pass

    # Early exit if 3+ medicines found (<1 second total latency)
    if len(meds) >= 3:
        return jsonify(raw=raw, medicines=meds)

    # Second pass: try --psm 6 on Otsu (great for column layouts)
    try:
        raw_psm = pytesseract.image_to_string(img_otsu, config="--psm 6")
        meds_psm = parse(raw_psm)
        if len(meds_psm) > len(meds):
            raw, meds = raw_psm, meds_psm
    except Exception:
        pass

    # If still few medicines found, try adaptive threshold
    if len(meds) < 2:
        try:
            raw_ad = pytesseract.image_to_string(img_adaptive)
            meds_ad = parse(raw_ad)
            if len(meds_ad) > len(meds):
                raw, meds = raw_ad, meds_ad
        except Exception:
            pass

    # If still nothing, verify whether tesseract is available
    if not raw and not meds:
        try:
            pytesseract.get_tesseract_version()
        except Exception:
            return jsonify(error="OCR engine unavailable on the server. Install Tesseract."), 503

    return jsonify(raw=raw, medicines=meds)


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


@app.delete("/api/medicines/<int:mid>")
@auth
def delete_medicine_route(mid):
    u = session["uid"]
    if USE_SUPABASE:
        try:
            sdb.delete_medicine(mid, u)
        except Exception as ex:
            return jsonify(error=str(ex)), 400
    else:
        q("DELETE FROM doses WHERE med_id=? AND user_id=?", (mid, u))
        q("DELETE FROM medicines WHERE id=? AND user_id=?", (mid, u))
        _sqlite().commit()
    return jsonify(ok=True)


@app.post("/api/medicines/batch-delete")
@auth
def batch_delete_medicines_route():
    d = request.get_json(silent=True) or {}
    ids = d.get("ids") or []
    if not isinstance(ids, list) or not ids:
        return jsonify(error="Select at least one medicine to delete."), 400

    u = session["uid"]
    clean_ids = [int(i) for i in ids if str(i).isdigit()]
    if not clean_ids:
        return jsonify(error="Invalid medicine IDs."), 400

    if USE_SUPABASE:
        try:
            sdb.batch_delete_medicines(clean_ids, u)
        except Exception as ex:
            return jsonify(error=str(ex)), 400
    else:
        q_marks = ",".join(["?"] * len(clean_ids))
        q(f"DELETE FROM doses WHERE med_id IN ({q_marks}) AND user_id=?", (*clean_ids, u))
        q(f"DELETE FROM medicines WHERE id IN ({q_marks}) AND user_id=?", (*clean_ids, u))
        _sqlite().commit()

    return jsonify(ok=True, deleted=len(clean_ids))


@app.get("/api/timeline")
@auth
def timeline_route():
    u = session["uid"]
    date_str = (request.args.get("date") or "").strip()
    if not date_str or not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
        date_str = datetime.now().strftime("%Y-%m-%d")

    if USE_SUPABASE:
        doses = sdb.get_timeline(u, date_str)
    else:
        prefix = f"{date_str}%"
        rows = q("""
            SELECT d.id, d.due, d.status, m.name, m.strength
            FROM doses d
            JOIN medicines m ON m.id = d.med_id
            WHERE d.user_id = ? AND d.due LIKE ?
            ORDER BY d.due ASC
        """, (u, prefix)).fetchall()
        doses = [dict(r) for r in rows]

    return jsonify(date=date_str, doses=doses)


MED_GUIDELINES = {
    "metformin": {
        "when": "With breakfast and dinner",
        "instructions": "Take with or right after food to minimize nausea or stomach upset.",
        "note": "Antidiabetic therapy. Avoid skipping meals."
    },
    "omeprazole": {
        "when": "Morning (08:00), 30-60 min before breakfast",
        "instructions": "Take on an empty stomach with a full glass of water.",
        "note": "Acid suppressor (PPI). Do not crush or chew."
    },
    "pantoprazole": {
        "when": "Morning (08:00), 30 min before food",
        "instructions": "Take on an empty stomach before morning meal.",
        "note": "Acid suppressor (PPI). Swallow tablet whole."
    },
    "rabeprazole": {
        "when": "Morning, 30 min before food",
        "instructions": "Take before breakfast with water.",
        "note": "Gastroprotective acid inhibitor."
    },
    "atorvastatin": {
        "when": "Bedtime (22:00)",
        "instructions": "Take in the evening or at night. Cholesterol synthesis peaks during sleep.",
        "note": "Lipid-lowering statin. Avoid large amounts of grapefruit juice."
    },
    "rosuvastatin": {
        "when": "Bedtime (22:00)",
        "instructions": "Take once daily in the evening with or without meals.",
        "note": "Lipid-lowering statin. Consistent daily timing is key."
    },
    "aspirin": {
        "when": "After breakfast or lunch",
        "instructions": "Take with food and a full glass of water. Do not lie down for 15 minutes.",
        "note": "Cardioprotective antiplatelet."
    },
    "ecosprin": {
        "when": "After morning or afternoon meal",
        "instructions": "Always take with food to protect gastric lining.",
        "note": "Low-dose antiplatelet."
    },
    "amlodipine": {
        "when": "Morning (08:00 - 09:00)",
        "instructions": "Take at the same time each morning with water.",
        "note": "Blood pressure management. Regular monitoring recommended."
    },
    "telmisartan": {
        "when": "Morning (08:00 - 09:00)",
        "instructions": "Take in the morning with or without food.",
        "note": "Blood pressure control (ARB). Stay well hydrated."
    },
    "ramipril": {
        "when": "Morning (08:00)",
        "instructions": "Take before or after breakfast.",
        "note": "ACE inhibitor for blood pressure & heart health."
    },
    "metoprolol": {
        "when": "With or right after meals (08:00 / 20:00)",
        "instructions": "Take with food for optimal bio-availability.",
        "note": "Beta-blocker. Do not discontinue abruptly."
    },
    "paracetamol": {
        "when": "As scheduled, min 4-6 hours between doses",
        "instructions": "Take with water. Maximum 4000mg in 24 hours.",
        "note": "Pain & fever relief. Avoid combining with other paracetamol products."
    },
    "amoxicillin": {
        "when": "Every 8h or 12h with water",
        "instructions": "Take at evenly spaced intervals with food or milk.",
        "note": "Antibiotic. Finish the complete course even if symptoms improve."
    },
    "doxycycline": {
        "when": "With a large glass of water, upright",
        "instructions": "Do not lie down for 30 minutes after taking. Avoid dairy within 2 hours.",
        "note": "Tetracycline antibiotic."
    },
    "cetirizine": {
        "when": "Evening or Bedtime (21:00 - 22:00)",
        "instructions": "Take with water in the evening as it may cause slight drowsiness.",
        "note": "Antihistamine for allergy & congestion relief."
    },
    "levocetirizine": {
        "when": "Bedtime (22:00)",
        "instructions": "Take before sleep with water.",
        "note": "Second-generation antihistamine."
    },
    "montelukast": {
        "when": "Evening (20:00 - 21:00)",
        "instructions": "Take once daily in the evening with or without food.",
        "note": "Leukotriene receptor antagonist for airways & allergy."
    },
    "levothyroxine": {
        "when": "Early morning (07:00), 30-60 min before breakfast",
        "instructions": "Take on an empty stomach with a full glass of water. Wait 1 hour before coffee/tea.",
        "note": "Thyroid hormone replacement."
    },
    "calcium": {
        "when": "After lunch or dinner",
        "instructions": "Take with food for best absorption. Keep 2 hours gap from iron supplements.",
        "note": "Bone health supplement."
    },
    "iron": {
        "when": "After meals or with vitamin C / juice",
        "instructions": "Take after meals if stomach upset occurs. Avoid taking with tea, milk, or coffee.",
        "note": "Iron supplement."
    },
    "multivitamin": {
        "when": "Morning after breakfast",
        "instructions": "Take with breakfast and plenty of water for optimal daytime absorption.",
        "note": "Daily wellness supplement."
    }
}


def call_gemini_api(meds_list, api_key):
    """Call Google Gemini 1.5 Flash for genuine clinical AI regimen descriptions."""
    import urllib.request, urllib.error
    med_lines = []
    for m in meds_list:
        times = m.get("times", [])
        if isinstance(times, str):
            try:
                times = json.loads(times)
            except Exception:
                pass
        med_lines.append(f"- {m.get('name')} {m.get('strength', '')} | Frequency: {m.get('freq', '')} | Times: {times} | Duration: {m.get('days')} days")

    meds_str = "\n".join(med_lines)
    prompt = f"""You are a certified clinical pharmacist. A patient is prescribed the following medications:
{meds_str}

Provide a personalized, patient-friendly, empathetic medication consumption and timing guide.
Return a valid JSON object matching this exact structure:
{{
  "summary": "2-3 sentence overview explaining how to organize these medicines throughout the day, meal pairing, and hydration.",
  "slots": {{
    "morning": [
      {{"name": "Medicine name & strength", "time": "08:00", "hint": "Clear food/intake instruction (e.g. with breakfast or empty stomach)"}}
    ],
    "afternoon": [],
    "evening": [],
    "night": []
  }},
  "guidelines": [
    {{
      "medicine": "Medicine name",
      "timing": "Recommended timing (e.g. Morning 30m before breakfast, Bedtime)",
      "instructions": "Precise dietary, water, and food intake advice",
      "note": "Therapeutic purpose and critical precautions (e.g. avoid alcohol, monitor BP)"
    }}
  ]
}}
Only return the valid JSON object without surrounding markdown."""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key.strip()}"
    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.2,
            "responseMimeType": "application/json"
        }
    }).encode("utf-8")

    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=12) as response:
        data = json.loads(response.read().decode("utf-8"))
        txt = data["candidates"][0]["content"]["parts"][0]["text"].strip()
        if txt.startswith("```"):
            txt = txt.strip("`").replace("json\n", "", 1).strip()
        parsed = json.loads(txt)
        parsed["source"] = "Google Gemini 1.5 Flash (Live AI)"
        parsed["ai_powered"] = True
        parsed["total_medications"] = len(meds_list)
        return parsed


@app.get("/api/medicines/summary")
@auth
def med_summary():
    u = session["uid"]
    if USE_SUPABASE:
        meds_list = sdb.get_medicines(u)
    else:
        r = q("SELECT id,name,strength,freq,times,days FROM medicines WHERE user_id=? ORDER BY id DESC",
              (u,)).fetchall()
        meds_list = [dict(x) for x in r]

    if not meds_list:
        return jsonify(
            summary="No active medicines found in your schedule. Scan or upload a prescription to generate your personalized regimen.",
            slots={},
            guidelines=[],
            source="MediAssist Clinical Intelligence",
            ai_powered=False
        )

    # If Gemini API key is configured, generate genuine live generative AI description!
    gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if gemini_key:
        try:
            return jsonify(call_gemini_api(meds_list, gemini_key))
        except Exception as gem_ex:
            print("[MediAssist] Gemini AI API notice:", gem_ex)

    slots = {"morning": [], "afternoon": [], "evening": [], "night": []}
    guidelines = []
    seen_names = set()

    for m in meds_list:
        name = str(m.get("name", "")).strip()
        name_clean = name.lower()
        strength = str(m.get("strength", "")).strip()
        times = m.get("times", [])
        if isinstance(times, str):
            try:
                times = json.loads(times)
            except Exception:
                times = []

        guide = None
        for k, g in MED_GUIDELINES.items():
            if k in name_clean or name_clean in k:
                guide = g
                break

        if guide and name_clean not in seen_names:
            seen_names.add(name_clean)
            guidelines.append({
                "medicine": f"{name} {strength}".strip(),
                "timing": guide["when"],
                "instructions": guide["instructions"],
                "note": guide["note"]
            })

        for t in (times or ["08:00"]):
            try:
                hr = int(t.split(":")[0])
            except Exception:
                hr = 8
            entry = f"{name} {strength}".strip()
            if 5 <= hr < 12:
                slots["morning"].append({"name": entry, "time": t, "hint": guide["instructions"] if guide else "Take with water as prescribed"})
            elif 12 <= hr < 17:
                slots["afternoon"].append({"name": entry, "time": t, "hint": guide["instructions"] if guide else "Take with or after lunch"})
            elif 17 <= hr < 21:
                slots["evening"].append({"name": entry, "time": t, "hint": guide["instructions"] if guide else "Take with or after dinner"})
            else:
                slots["night"].append({"name": entry, "time": t, "hint": guide["instructions"] if guide else "Take before sleep with water"})

    summary_parts = []
    if slots["morning"]:
        summary_parts.append(f"Morning ({len(slots['morning'])} dose{'s' if len(slots['morning'])>1 else ''}): " + ", ".join([x["name"] for x in slots["morning"]]))
    if slots["afternoon"]:
        summary_parts.append(f"Afternoon ({len(slots['afternoon'])} dose{'s' if len(slots['afternoon'])>1 else ''}): " + ", ".join([x["name"] for x in slots["afternoon"]]))
    if slots["evening"]:
        summary_parts.append(f"Evening ({len(slots['evening'])} dose{'s' if len(slots['evening'])>1 else ''}): " + ", ".join([x["name"] for x in slots["evening"]]))
    if slots["night"]:
        summary_parts.append(f"Night ({len(slots['night'])} dose{'s' if len(slots['night'])>1 else ''}): " + ", ".join([x["name"] for x in slots["night"]]))

    narrative = "Your daily regimen is organized into " + " · ".join(summary_parts) + "."

    return jsonify(
        summary=narrative,
        slots=slots,
        guidelines=guidelines,
        total_medications=len(meds_list),
        source="MediAssist Clinical Intelligence",
        ai_powered=False
    )


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

@app.get("/favicon.ico")
def favicon():
    return send_from_directory("static", "favicon.ico", mimetype="image/vnd.microsoft.icon")

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
