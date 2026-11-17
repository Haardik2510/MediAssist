"""
build_screenshots.py
Generates clean component demo pages and captures high-resolution
figure screenshots for the MediAssist Minor Project Final Report.
"""

import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'report_assets')
STATIC_DIR = os.path.join(BASE_DIR, 'static')
os.makedirs(ASSETS_DIR, exist_ok=True)

edge_exe = r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'

def wrap_html(body_content, title="MediAssist Demonstration"):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="file:///{os.path.abspath(os.path.join(STATIC_DIR, 'style.css')).replace(os.sep, '/')}">
<style>
  body {{ background: #ffffff; color: #0f172a; margin: 0; padding: 24px; font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif; }}
  .frame-box {{ max-width: 1040px; margin: 0 auto; background: #ffffff; }}
</style>
</head>
<body>
<div class="frame-box">
{body_content}
</div>
</body>
</html>"""

views = {
    'fig5_landing.png': {
        'html': wrap_html("""
<nav style="margin-bottom:24px;border-radius:12px;box-shadow:0 2px 10px rgba(0,0,0,0.05)">
  <b>MediAssist</b>
  <div style="display:flex;gap:14px;align-items:center">
    <a href="#" style="color:#0f172a;font-weight:600">Home</a>
    <a href="#" style="color:#ea580c;font-weight:600">Dashboard</a>
    <a class="btn sm" href="#" style="color:#fff">Get Started</a>
  </div>
</nav>
<section class="hero" style="min-height:auto;padding:30px 20px 40px;text-align:left">
  <span class="badge" style="background:rgba(234,88,12,0.12);color:#ea580c;font-weight:700;margin-bottom:12px;display:inline-block;padding:6px 12px;border-radius:20px">Smart Healthcare &bull; Clinical Adherence Platform</span>
  <h1 style="font-size:44px;line-height:1.15;margin:8px 0 16px;color:#09090b;letter-spacing:-0.02em">Never misread a prescription<br>or miss a dose again.</h1>
  <p style="max-width:680px;color:#64748b;font-size:18px;line-height:1.6;margin-bottom:24px">
    MediAssist scans your handwritten or printed prescription, interprets doctor shorthand into clear daily dose times, reminds you with audible voice guidance, and connects you with nearby pharmacies.
  </p>
  <div style="display:flex;gap:14px;align-items:center;flex-wrap:wrap">
    <button class="btn" style="padding:13px 28px;font-size:16px">Create Free Account</button>
    <button class="btn ghost" style="padding:13px 24px;font-size:16px">Explore Live Demo</button>
  </div>
</section>
<footer>
  <div class="footer-top">
    <div style="display:flex;gap:16px;align-items:center;flex-wrap:wrap">
      <a href="#">Privacy Policy</a>
      <a href="#">Terms</a>
      <span>Assistive tool only. Not a substitute for a doctor or pharmacist.</span>
    </div>
  </div>
  <div class="footer-credits">
    <div class="mentor"><span style="color:var(--mut)">Faculty Mentor:</span> <strong>Cosmena Mahapatra</strong></div>
    <div class="student"><span style="color:var(--mut)">Made by:</span> <strong style="color:var(--ac)">Haardik Goel</strong> <span style="color:var(--mut)">(VIPS TC, MCA &bull; 09415504426)</span></div>
  </div>
</footer>
"""),
        'height': 680
    },

    'fig6_slider.png': {
        'html': wrap_html("""
<h2 style="font-size:26px;margin:10px 0 16px">How MediAssist Works: 5-Stage Patient Flow</h2>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px;margin-bottom:24px">
  <div class="card" style="padding:18px">
    <small style="color:#ea580c;font-weight:700">STAGE 1</small>
    <h3 style="margin:6px 0 8px;font-size:17px">Prescription Scan</h3>
    <p style="font-size:13.5px;color:#64748b;margin:0">Upload a photograph or capture directly via camera. OpenCV removes noise and binarizes text.</p>
  </div>
  <div class="card" style="padding:18px">
    <small style="color:#ea580c;font-weight:700">STAGE 2</small>
    <h3 style="margin:6px 0 8px;font-size:17px">Clinical NLP Parsing</h3>
    <p style="font-size:13.5px;color:#64748b;margin:0">RapidFuzz matches 113+ medicines. Notations like 1-0-1, OD, and TDS become scheduled hours.</p>
  </div>
  <div class="card" style="padding:18px">
    <small style="color:#ea580c;font-weight:700">STAGE 3</small>
    <h3 style="margin:6px 0 8px;font-size:17px">Human Verification</h3>
    <p style="font-size:13.5px;color:#64748b;margin:0">Mandatory editable gateway. Patient audits and adjusts every extracted dose before saving.</p>
  </div>
  <div class="card" style="padding:18px">
    <small style="color:#ea580c;font-weight:700">STAGE 4</small>
    <h3 style="margin:6px 0 8px;font-size:17px">Audible Reminders</h3>
    <p style="font-size:13.5px;color:#64748b;margin:0">Browser push notifications with spoken voice alerts and one-tap Taken/Snooze/Skip tracking.</p>
  </div>
  <div class="card" style="padding:18px">
    <small style="color:#ea580c;font-weight:700">STAGE 5</small>
    <h3 style="margin:6px 0 8px;font-size:17px">Medicine Locator</h3>
    <p style="font-size:13.5px;color:#64748b;margin:0">One-click Tata 1mg online orders and Google Maps store finder for local emergency stock.</p>
  </div>
</div>
"""),
        'height': 360
    },

    'fig7_dashboard.png': {
        'html': wrap_html("""
<h1 style="font-size:28px;margin-bottom:14px">Your Medicines & Ingestion Hub</h1>
<div class="card" style="margin-bottom:20px;border-left:4px solid #ea580c">
  <h3 style="margin:0 0 6px;font-size:18px">Prescription Ingestion Interface</h3>
  <p style="color:#64748b;font-size:14px;margin:0 0 16px">Upload a prescription photo from your mobile gallery or take a high-resolution snapshot using your device camera.</p>
  <div style="display:flex;gap:12px;flex-wrap:wrap;align-items:center">
    <label class="btn" style="cursor:pointer;margin:0;display:inline-flex;align-items:center;gap:8px;padding:12px 22px">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
      Choose from Gallery / Files
    </label>
    <label class="btn ghost" style="cursor:pointer;margin:0;display:inline-flex;align-items:center;gap:8px;padding:12px 22px">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>
      Take Photo with Camera
    </label>
    <span style="font-size:13px;color:#64748b;margin-left:8px">Supports JPEG, PNG, WEBP (Max 8MB &bull; Compressed to 1200px)</span>
  </div>
</div>
"""),
        'height': 290
    },

    'fig8_ai_guidance.png': {
        'html': wrap_html("""
<h2 style="font-size:22px;margin-bottom:12px">AI Consumption & Timing Summary</h2>
<div class="card" id="ai-summary-box">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;flex-wrap:wrap;gap:8px">
    <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap">
      <span class="badge" style="background:#c2410c;color:#fff;padding:5px 12px;font-size:12.5px;box-shadow:0 2px 6px rgba(194,65,12,0.3)">Google Gemini 1.5 Flash (Live AI)</span>
      <button class="btn sm btn-voice" style="background:#0f172a;color:#fff;display:inline-flex;align-items:center;gap:6px;padding:6px 14px">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon><path d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path></svg>
        🔊 Listen to Regimen (Voice Read-Aloud)
      </button>
    </div>
    <button class="btn ghost sm">Refresh Summary</button>
  </div>

  <p style="font-size:14.5px;line-height:1.6;margin-bottom:16px">
    <b>Regimen Overview:</b> You have 4 active medications coordinated for maximum therapeutic absorption and minimum gastrointestinal irritation. Pantoprazole is taken on an empty stomach first thing in the morning. Metformin is divided twice daily with meals. Atorvastatin is scheduled at bedtime for optimal nighttime cholesterol synthesis.
  </p>

  <div class="grid" style="grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-bottom:16px">
    <div class="slot-card" style="border-left:4px solid #ea580c">
      <b style="color:#ea580c;display:block;margin-bottom:6px">Morning (Breakfast / Empty Stomach)</b>
      <div style="font-size:13.5px;margin-bottom:6px"><b>Pantoprazole 40mg</b> <span style="font-family:monospace;color:var(--mut)">(08:00)</span><br><span style="color:var(--mut);font-size:12px">Take 30 mins before food on empty stomach</span></div>
      <div style="font-size:13.5px;margin-bottom:6px"><b>Metformin 500mg</b> <span style="font-family:monospace;color:var(--mut)">(08:30)</span><br><span style="color:var(--mut);font-size:12px">Take with or immediately after breakfast</span></div>
    </div>
    <div class="slot-card" style="border-left:4px solid #f97316">
      <b style="color:#f97316;display:block;margin-bottom:6px">Afternoon (Lunch)</b>
      <div style="font-size:13.5px;margin-bottom:6px"><b>Paracetamol 650mg</b> <span style="font-family:monospace;color:var(--mut)">(13:00)</span><br><span style="color:var(--mut);font-size:12px">Take after lunch only if fever or headache persists</span></div>
    </div>
    <div class="slot-card" style="border-left:4px solid #c2410c">
      <b style="color:#c2410c;display:block;margin-bottom:6px">Evening (Dinner)</b>
      <div style="font-size:13.5px;margin-bottom:6px"><b>Metformin 500mg</b> <span style="font-family:monospace;color:var(--mut)">(20:00)</span><br><span style="color:var(--mut);font-size:12px">Take with evening dinner</span></div>
    </div>
    <div class="slot-card" style="border-left:4px solid #18181b">
      <b style="color:#18181b;display:block;margin-bottom:6px">Night (Bedtime)</b>
      <div style="font-size:13.5px;margin-bottom:6px"><b>Atorvastatin 20mg</b> <span style="font-family:monospace;color:var(--mut)">(22:00)</span><br><span style="color:var(--mut);font-size:12px">Take at bedtime with water</span></div>
    </div>
  </div>

  <div style="margin-top:14px">
    <b style="font-size:13px;color:var(--mut);text-transform:uppercase;letter-spacing:.05em">Doctor Instructions & Precautions</b>
    <div style="margin-top:8px;display:grid;gap:8px">
      <div style="padding:10px 12px;background:#f8fafc;border:1px solid var(--bd);border-radius:8px;box-shadow:0 1px 3px rgba(0,0,0,0.03);font-size:13.5px">
        <b>Pantoprazole:</b> <span style="color:#ea580c;font-weight:600">Morning 08:00</span> &mdash; Swallow whole with water; do not crush or chew.
      </div>
      <div style="padding:10px 12px;background:#f8fafc;border:1px solid var(--bd);border-radius:8px;box-shadow:0 1px 3px rgba(0,0,0,0.03);font-size:13.5px">
        <b>Metformin:</b> <span style="color:#ea580c;font-weight:600">With Food (08:30 & 20:00)</span> &mdash; Maintain steady hydration to prevent gastrointestinal upset.
      </div>
    </div>
  </div>
</div>
"""),
        'height': 560
    },

    'fig9_timeline.png': {
        'html': wrap_html("""
<h2 style="font-size:22px;margin-bottom:12px">Timeline & History Calendar</h2>
<div class="card">
  <div style="display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:16px">
    <button class="btn ghost sm">&lt; Previous</button>
    <input type="date" value="2026-11-17" style="width:auto;min-width:160px;padding:8px 12px;border:1px solid var(--bd);border-radius:8px;font-weight:600">
    <button class="btn ghost sm">Next &gt;</button>
    <button class="btn sm">Today</button>
  </div>

  <div id="timeline-items">
    <div class="timeline-item">
      <div>
        <span class="badge" style="background:#18181b;color:#f4f4f5;margin-right:8px;font-family:monospace;padding:4px 8px">08:00 AM</span>
        <b style="font-size:15px">Pantoprazole</b> <span style="color:var(--mut)">40mg</span>
      </div>
      <div><span class="badge taken" style="padding:4px 10px;font-size:13px">Taken</span></div>
    </div>
    <div class="timeline-item">
      <div>
        <span class="badge" style="background:#18181b;color:#f4f4f5;margin-right:8px;font-family:monospace;padding:4px 8px">08:30 AM</span>
        <b style="font-size:15px">Metformin</b> <span style="color:var(--mut)">500mg</span>
      </div>
      <div><span class="badge taken" style="padding:4px 10px;font-size:13px">Taken</span></div>
    </div>
    <div class="timeline-item">
      <div>
        <span class="badge" style="background:#18181b;color:#f4f4f5;margin-right:8px;font-family:monospace;padding:4px 8px">01:00 PM</span>
        <b style="font-size:15px">Paracetamol</b> <span style="color:var(--mut)">650mg</span>
      </div>
      <div><span class="badge skipped" style="padding:4px 10px;font-size:13px">Skipped</span></div>
    </div>
    <div class="timeline-item">
      <div>
        <span class="badge" style="background:#18181b;color:#f4f4f5;margin-right:8px;font-family:monospace;padding:4px 8px">08:00 PM</span>
        <b style="font-size:15px">Metformin</b> <span style="color:var(--mut)">500mg</span>
      </div>
      <div style="display:flex;gap:6px">
        <button class="btn sm" style="padding:6px 14px">Take Dose</button>
        <button class="btn ghost sm" style="padding:6px 14px">Skip</button>
      </div>
    </div>
    <div class="timeline-item">
      <div>
        <span class="badge" style="background:#18181b;color:#f4f4f5;margin-right:8px;font-family:monospace;padding:4px 8px">10:00 PM</span>
        <b style="font-size:15px">Atorvastatin</b> <span style="color:var(--mut)">20mg</span>
      </div>
      <div><span class="badge pending" style="padding:4px 10px;font-size:13px">Pending</span></div>
    </div>
  </div>
</div>
"""),
        'height': 460
    },

    'fig10_batch_delete.png': {
        'html': wrap_html("""
<h2 style="font-size:22px;margin-bottom:12px">Medication Schedule & Multi-Delete Management</h2>
<div id="batch-bar" style="display:flex;margin-bottom:12px;padding:12px 16px;background:rgba(239,68,68,0.1);border:1px solid rgba(239,68,68,0.3);border-radius:10px;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px">
  <span style="font-weight:700;color:#dc2626;font-size:15px">&bull; 2 medicines selected</span>
  <button class="btn danger sm" style="padding:8px 18px">Delete Selected Medicines</button>
</div>
<div class="card" style="overflow-x:auto;padding:16px">
  <table style="width:100%;border-collapse:collapse;font-size:14px">
    <thead>
      <tr style="border-bottom:2px solid var(--bd)">
        <th style="width:36px;text-align:center;padding:10px"><input type="checkbox" checked style="width:18px;height:18px"></th>
        <th style="padding:10px">Medicine</th>
        <th style="padding:10px">Frequency</th>
        <th style="padding:10px">Times</th>
        <th style="padding:10px">Duration</th>
        <th style="padding:10px">Buy Online</th>
        <th style="padding:10px">Action</th>
      </tr>
    </thead>
    <tbody>
      <tr style="border-bottom:1px solid var(--bd)">
        <td style="text-align:center;padding:12px"><input type="checkbox" checked style="width:18px;height:18px"></td>
        <td><b>Pantoprazole</b> 40mg</td>
        <td>OD (Once Daily)</td>
        <td>08:00</td>
        <td>14 days</td>
        <td><a href="https://www.1mg.com/search/all?name=Pantoprazole" target="_blank" style="color:#ea580c;font-weight:600">Tata 1mg &nearr;</a></td>
        <td><button class="btn danger sm">Delete</button></td>
      </tr>
      <tr style="border-bottom:1px solid var(--bd)">
        <td style="text-align:center;padding:12px"><input type="checkbox" checked style="width:18px;height:18px"></td>
        <td><b>Metformin</b> 500mg</td>
        <td>1-0-1 (Twice Daily)</td>
        <td>08:30, 20:00</td>
        <td>30 days</td>
        <td><a href="https://www.1mg.com/search/all?name=Metformin" target="_blank" style="color:#ea580c;font-weight:600">Tata 1mg &nearr;</a></td>
        <td><button class="btn danger sm">Delete</button></td>
      </tr>
      <tr>
        <td style="text-align:center;padding:12px"><input type="checkbox" style="width:18px;height:18px"></td>
        <td><b>Atorvastatin</b> 20mg</td>
        <td>HS (At Bedtime)</td>
        <td>22:00</td>
        <td>30 days</td>
        <td><a href="https://www.1mg.com/search/all?name=Atorvastatin" target="_blank" style="color:#ea580c;font-weight:600">Tata 1mg &nearr;</a></td>
        <td><button class="btn danger sm">Delete</button></td>
      </tr>
    </tbody>
  </table>
</div>
"""),
        'height': 380
    },

    'fig11_voice_assistant.png': {
        'html': wrap_html("""
<h2 style="font-size:22px;margin-bottom:12px">Real-Time MediAssist Voice Assistant Dialog</h2>
<div class="card" style="max-width:540px;margin:0 auto;box-shadow:0 25px 50px -12px rgba(0,0,0,0.25);border:1px solid #cbd5e1;padding:24px">
  <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;border-bottom:1px solid var(--bd);padding-bottom:12px">
    <div style="display:flex;align-items:center;gap:10px">
      <span style="font-size:26px">🎙️</span>
      <div>
        <h3 style="margin:0;font-size:18px;color:#09090b">MediAssist Voice Assistant</h3>
        <small style="color:#64748b">Hands-free clinical speech recognition & synthesis</small>
      </div>
    </div>
    <span class="badge" style="background:#16a34a;color:#fff;font-size:11px;padding:4px 8px">● Engine Active</span>
  </div>

  <div class="voice-wave" style="display:flex;margin:16px 0">
    <div class="vbar"></div><div class="vbar"></div><div class="vbar"></div><div class="vbar"></div><div class="vbar"></div>
  </div>

  <div style="font-size:14px;color:#ea580c;text-align:center;margin:6px 0 12px;font-weight:700">
    ● Listening for your spoken medical command...
  </div>

  <div style="min-height:50px;background:#f8fafc;border:1px solid var(--bd);border-radius:10px;padding:12px;margin:10px 0;font-size:14px;color:#0f172a;line-height:1.5">
    <b>You said:</b> &ldquo;What are my medicines today?&rdquo;
  </div>

  <div style="background:#fff7ed;border-left:4px solid #ea580c;border-radius:6px;padding:12px;margin:10px 0;font-size:14px;color:#7c2d12;line-height:1.5">
    <b>MediAssist Audio:</b> &ldquo;You have 4 medications scheduled: Pantoprazole 40 milligrams once daily, Metformin 500 milligrams twice daily with meals, and Atorvastatin 20 milligrams at bedtime.&rdquo;
  </div>

  <div style="display:flex;gap:10px;justify-content:center;align-items:center;margin:14px 0">
    <button class="btn danger sm" style="padding:8px 18px">🛑 Stop Listening</button>
    <button class="btn ghost sm" style="padding:8px 18px">⏹ Stop Audio Playback</button>
  </div>

  <div style="font-size:12px;color:#64748b;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:6px">Sample Voice Commands:</div>
  <div style="display:flex;flex-wrap:wrap;gap:6px">
    <span class="cmd-pill">What are my medicines today?</span>
    <span class="cmd-pill">Read AI clinical guidance</span>
    <span class="cmd-pill">Mark Metformin as taken</span>
    <span class="cmd-pill">Find nearby pharmacy</span>
    <span class="cmd-pill">Go to dashboard</span>
  </div>

  <form style="display:flex;gap:8px;margin-top:14px;width:100%">
    <input placeholder="Or type a voice command..." style="flex:1;padding:8px 12px;font-size:13.5px;border:1px solid var(--bd);border-radius:8px" value="What are my medicines today?">
    <button class="btn sm" type="button">Send</button>
  </form>
</div>
"""),
        'height': 630
    },

    'fig12_locator.png': {
        'html': wrap_html("""
<h2 style="font-size:22px;margin-bottom:12px">Medicine Locator & Online Pharmacy Procurement</h2>
<div class="card" style="padding:22px">
  <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:10px;margin-bottom:16px">
    <div>
      <b style="font-size:16px">Nearby Pharmacy Discovery & Radar</b>
      <p style="margin:2px 0 0;font-size:13.5px;color:var(--mut)">Interactive map showing verified dispensaries, hospitals, and medical stores within 3.5 km.</p>
    </div>
    <a class="btn" href="https://www.google.com/maps/search/pharmacy+near+me" target="_blank" style="display:inline-flex;align-items:center;gap:6px;padding:10px 20px">
      Open in Google Maps &nearr;
    </a>
  </div>
  <div id="map" style="background:#f1f5f9;display:flex;align-items:center;justify-content:center;color:#475569;font-weight:500;border:1px solid var(--bd);height:260px;border-radius:12px;box-shadow:inset 0 2px 4px rgba(0,0,0,0.04)">
    <div style="text-align:center">
      <div style="font-size:36px;margin-bottom:6px">📍 🏥 💊</div>
      <b style="font-size:16px;color:#0f172a">Pitampura &bull; Rohini &bull; New Delhi</b><br>
      <span style="color:#ea580c;font-weight:700;font-size:14px">12 Verified Pharmacies Detected via OpenStreetMap / Google Places API</span><br>
      <span style="font-size:12.5px;color:#64748b">Apollo Pharmacy (0.4 km) &bull; Fortis Chemist (1.1 km) &bull; MedPlus (1.4 km)</span>
    </div>
  </div>
</div>
"""),
        'height': 380
    }
}

for fname, data in views.items():
    tmp_html = os.path.join(STATIC_DIR, f'temp_{fname}.html')
    with open(tmp_html, 'w', encoding='utf-8') as f:
        f.write(data['html'])
    
    out_png = os.path.join(ASSETS_DIR, fname)
    url = 'file:///' + tmp_html.replace(os.sep, '/')
    cmd = [
        edge_exe,
        '--headless',
        '--disable-gpu',
        '--run-all-compositor-stages-before-draw',
        f'--window-size=1200,{data["height"]}',
        f'--screenshot={out_png}',
        url
    ]
    subprocess.run(cmd, capture_output=True, timeout=15)
    if os.path.exists(out_png):
        print(f"Generated screenshot: {fname} ({os.path.getsize(out_png):,} bytes)")
    else:
        print(f"FAILED: {fname}")
    
    try: os.remove(tmp_html)
    except: pass

print("Figure snapshot generation complete.")
