import os
import base64
import subprocess
import shutil

BASE_DIR = r'c:\Users\haard\Downloads\mediassist\mediassist'
ASSETS_DIR = os.path.join(BASE_DIR, 'report_assets')

def get_b64_image(filename):
    filepath = os.path.join(ASSETS_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'rb') as f:
            data = base64.b64encode(f.read()).decode('utf-8')
            return f"data:image/png;base64,{data}"
    return ""

# Logos matching the exact PDF cover page
img_vips_cover = get_b64_image('pdf_cover_logo_2.png')  # VIPS Logo
img_ggsipu_cover = get_b64_image('pdf_cover_logo_1.png') # GGSIPU Logo
img_arch = get_b64_image('3972937e68e4171b560e5604b03833d3ba474abe.png')
img_dfd = get_b64_image('8eef0fa1d8eea9addf184751b58e247e5ccfcc88.png')
img_erd = get_b64_image('d6e5b3d7ff1997f35509f8503031634c953a3757.png')
img_workflow = get_b64_image('5f2ae79ef616ccd35b3e4503475174229f92a37d.png')

# Website Screenshots (Figures 5 through 12)
img_fig5 = get_b64_image('fig5_landing.png')
img_fig6 = get_b64_image('fig6_slider.png')
img_fig7 = get_b64_image('fig7_dashboard.png')
img_fig8 = get_b64_image('fig8_ai_guidance.png')
img_fig9 = get_b64_image('fig9_timeline.png')
img_fig10 = get_b64_image('fig10_batch_delete.png')
img_fig11 = get_b64_image('fig11_voice_assistant.png')
img_fig12 = get_b64_image('fig12_locator.png')

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>MediAssist: Smart Prescription Scanner & Medicine Reminder System - Minor Project Final Report (Semester 1)</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 22mm 22mm 20mm 22mm;
    @bottom-right {{
      content: counter(page);
      font-family: 'Caladea', Cambria, Georgia, 'Times New Roman', serif;
      font-size: 10pt;
      color: #334155;
    }}
  }}

  @page :first {{
    @bottom-right {{
      content: none;
    }}
  }}

  body {{
    font-family: 'Caladea', Cambria, Georgia, 'Times New Roman', serif;
    font-size: 11pt;
    line-height: 1.5;
    color: #111111;
    margin: 0;
    padding: 0;
    background-color: #ffffff;
    text-align: justify;
  }}

  .page {{
    page-break-after: always;
    position: relative;
    box-sizing: border-box;
  }}

  .page-last {{
    page-break-after: avoid;
  }}

  /* Exact Cover Page Layout matching MediAssist_Final_Report_Sem1.pdf */
  .cover-page {{
    box-sizing: border-box;
    height: 96%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    text-align: center;
    padding: 0 4px;
  }}

  .cover-top-bar {{
    display: flex;
    justify-content: space-between;
    font-size: 11pt;
    font-weight: bold;
    color: #0f172a;
    margin-bottom: 24px;
  }}

  .cover-inst-heading {{
    font-size: 14.5pt;
    font-weight: bold;
    color: #0f172a;
    text-transform: uppercase;
    letter-spacing: 0.4px;
    margin: 0;
    line-height: 1.3;
  }}

  .cover-inst-subheading {{
    font-size: 12.5pt;
    font-weight: bold;
    color: #0f172a;
    text-transform: uppercase;
    margin: 4px 0 16px 0;
  }}

  .cover-logo-center {{
    margin: 12px auto;
    text-align: center;
  }}

  .cover-logo-center img {{
    height: 72px;
    width: auto;
    object-fit: contain;
  }}

  .cover-degree-heading {{
    font-size: 15pt;
    font-weight: bold;
    color: #0f172a;
    text-transform: uppercase;
    margin: 18px 0 6px 0;
  }}

  .cover-proj-title {{
    font-size: 17.5pt;
    font-weight: bold;
    color: #0f172a;
    line-height: 1.25;
    margin: 4px 0;
  }}

  .cover-minor-tag {{
    font-size: 13pt;
    font-weight: bold;
    color: #0f172a;
    margin: 10px 0;
  }}

  .cover-univ-name {{
    font-size: 15pt;
    font-weight: bold;
    color: #0f172a;
    margin: 10px 0 14px 0;
  }}

  .cover-submission-table {{
    width: 100%;
    margin-top: 15px;
    font-size: 11.5pt;
    text-align: left;
    border-collapse: collapse;
  }}

  .cover-submission-table td {{
    vertical-align: top;
    padding: 0 4px;
    border: none;
  }}

  .cover-sub-label {{
    font-weight: bold;
    color: #0f172a;
    font-size: 11.5pt;
    margin-bottom: 4px;
  }}

  .cover-sub-val {{
    font-size: 11.5pt;
    color: #1e293b;
    line-height: 1.35;
  }}

  .cover-bottom-bar {{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 8pt;
    font-weight: bold;
    color: #595959;
    text-align: center;
    margin-top: 24px;
  }}

  /* Headings & Dividers matching MediAssist_Final_Report_Sem1.pdf */
  h1 {{
    font-family: 'Caladea', Cambria, Georgia, 'Times New Roman', serif;
    font-size: 16pt;
    font-weight: bold;
    color: #1f2937;
    text-transform: uppercase;
    margin-top: 14px;
    margin-bottom: 4px;
    page-break-after: avoid;
  }}

  .orange-rule {{
    height: 2pt;
    background-color: #ea580c;
    width: 100%;
    margin-top: 3px;
    margin-bottom: 12px;
  }}

  h2 {{
    font-family: 'Caladea', Cambria, Georgia, 'Times New Roman', serif;
    font-size: 12.5pt;
    font-weight: bold;
    color: #1f2937;
    margin-top: 12px;
    margin-bottom: 6px;
    page-break-after: avoid;
  }}

  h3 {{
    font-family: 'Caladea', Cambria, Georgia, 'Times New Roman', serif;
    font-size: 11pt;
    font-weight: bold;
    color: #374151;
    margin-top: 8px;
    margin-bottom: 4px;
    page-break-after: avoid;
  }}

  p {{
    margin-top: 0;
    margin-bottom: 8px;
    text-indent: 0;
  }}

  ul, ol {{
    margin-top: 0;
    margin-bottom: 10px;
    padding-left: 22px;
  }}

  li {{
    margin-bottom: 3px;
  }}

  /* Tables */
  table.content-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 8px 0 12px 0;
    font-size: 9pt;
    page-break-inside: avoid;
  }}

  table.content-table th {{
    background-color: #f1f5f9;
    color: #0f172a;
    font-weight: bold;
    border: 1px solid #94a3b8;
    padding: 5px 7px;
    text-align: left;
  }}

  table.content-table td {{
    border: 1px solid #cbd5e1;
    padding: 5px 7px;
    vertical-align: top;
  }}

  table.content-table tr:nth-child(even) {{
    background-color: #f8fafc;
  }}

  .table-title {{
    font-family: Arial, sans-serif;
    font-size: 9pt;
    font-weight: bold;
    margin-bottom: 3px;
    text-align: center;
    color: #334155;
    text-transform: uppercase;
  }}

  /* Figures */
  .fig-container {{
    text-align: center;
    margin: 10px 0;
    page-break-inside: avoid;
  }}

  .fig-container img {{
    max-width: 94%;
    max-height: 260px;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    padding: 4px;
    background: #ffffff;
  }}

  .fig-caption {{
    font-family: 'Caladea', Cambria, Georgia, 'Times New Roman', serif;
    font-size: 9pt;
    font-weight: bold;
    color: #334155;
    margin-top: 5px;
  }}

  .fig-pair-container {{
    text-align: center;
    margin: 6px 0 2px 0;
    page-break-inside: avoid;
  }}

  .fig-pair-container img {{
    max-width: 94%;
    max-height: 185px;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.06);
    padding: 3px;
    background: #ffffff;
    display: block;
    margin: 0 auto;
  }}

  .fig-pair-caption {{
    font-family: 'Caladea', Cambria, Georgia, 'Times New Roman', serif;
    font-size: 8.5pt;
    font-weight: bold;
    color: #334155;
    margin-top: 4px;
    margin-bottom: 4px;
    text-align: center;
  }}

  /* Signatures */
  .sign-container {{
    margin-top: 36px;
    display: flex;
    justify-content: space-between;
    page-break-inside: avoid;
  }}

  .sign-box {{
    width: 44%;
    text-align: left;
  }}

  .sign-line {{
    margin-top: 45px;
    border-top: 1px solid #0f172a;
    padding-top: 4px;
    font-weight: bold;
    color: #0f172a;
    font-size: 10.5pt;
  }}

  .sign-sub {{
    font-size: 9.5pt;
    color: #475569;
  }}

  /* Dotted Leader TOC */
  .toc-line {{
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    margin-bottom: 4px;
    font-size: 10pt;
  }}

  .toc-title {{
    font-weight: bold;
    color: #1f2937;
  }}

  .toc-sub-title {{
    padding-left: 18px;
    color: #374151;
  }}

  .toc-dots {{
    flex-grow: 1;
    border-bottom: 1px dotted #94a3b8;
    margin: 0 8px;
  }}

  .toc-page {{
    font-weight: bold;
    color: #1f2937;
  }}

  .callout-box {{
    background: #fff7ed;
    border-left: 4px solid #ea580c;
    padding: 10px 14px;
    margin: 10px 0;
    font-size: 10pt;
    color: #9a3412;
  }}

  .score-badge {{
    background: #16a34a;
    color: #ffffff;
    font-weight: bold;
    padding: 4px 10px;
    border-radius: 4px;
    font-size: 11pt;
    display: inline-block;
  }}
</style>
</head>
<body>

<!-- ========================================================================= -->
<!-- COVER PAGE (Exact Matching MediAssist_Final_Report_Sem1.pdf)               -->
<!-- ========================================================================= -->
<div class="page cover-page">
  <div>
    <div class="cover-top-bar">
      <div>Haardik</div>
      <div>MCA 1 (B)</div>
    </div>

    <div class="cover-inst-heading">VIVEKANANDA INSTITUTE OF PROFESSIONAL STUDIES-TC</div>
    <div class="cover-inst-subheading">VIVEKANANDA SCHOOL OF INFORMATION TECHNOLOGY</div>

    <div class="cover-logo-center">
      <img src="{img_vips_cover}" alt="VIPS-TC Logo">
    </div>

    <div class="cover-degree-heading">MASTER OF COMPUTER APPLICATIONS</div>
    <div class="cover-proj-title">MediAssist: Smart Prescription Scanner &</div>
    <div class="cover-proj-title">Medicine Reminder System</div>
    <div class="cover-minor-tag">Minor Project Final Report &bull; Semester 1</div>
    <div class="cover-univ-name">Guru Gobind Singh Indraprastha University</div>

    <div class="cover-logo-center">
      <img src="{img_ggsipu_cover}" alt="GGSIPU Logo">
    </div>
  </div>

  <div>
    <table class="cover-submission-table">
      <tr>
        <td style="width: 50%;">
          <div class="cover-sub-label">SUBMITTED TO:</div>
          <div class="cover-sub-val"><strong>Dr. Cosmena</strong></div>
          <div class="cover-sub-val">Project Mentor & Assistant Professor</div>
          <div class="cover-sub-val">VSIT, VIPS-TC</div>
        </td>
        <td style="width: 50%; text-align: right;">
          <div class="cover-sub-label">SUBMITTED BY:</div>
          <div class="cover-sub-val"><strong>Haardik Goel</strong></div>
          <div class="cover-sub-val">Enroll no. : <strong>09415504426</strong></div>
          <div class="cover-sub-val">MCA 1 (B)</div>
        </td>
      </tr>
    </table>

    <div class="cover-bottom-bar">
      Name: Haardik Goel &nbsp; | &nbsp; Roll No: 09415504426
    </div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- CERTIFICATE OF APPROVAL                                                   -->
<!-- ========================================================================= -->
<div class="page">
  <h1>Certificate of Approval</h1>
  <div class="orange-rule"></div>
  <div style="text-align: center; font-weight: bold; font-size: 11pt; color: #0f172a; margin-bottom: 2px;">VIVEKANANDA SCHOOL OF INFORMATION TECHNOLOGY</div>
  <div style="text-align: center; font-size: 11pt; color: #334155; margin-bottom: 24px;">Vivekananda Institute of Professional Studies - TC, Delhi</div>

  <p>
    This is to certify that the minor project report entitled <strong>&ldquo;MediAssist: Smart Prescription Scanner and Medicine Reminder System&rdquo;</strong> submitted by <strong>Haardik Goel</strong> (Enrollment No. <strong>09415504426</strong>), student of Master of Computer Applications, MCA 1 (B), at Vivekananda School of Information Technology (VSIT), Vivekananda Institute of Professional Studies-TC, affiliated to Guru Gobind Singh Indraprastha University (GGSIPU), Delhi, is an authentic record of the candidate's own work carried out under my direct supervision and academic mentorship during Semester 1.
  </p>
  <p>
    The project embodies a complete, functioning, cloud-integrated web application featuring automated Optical Character Recognition (OCR), Natural Language Processing (NLP) rule-based clinical frequency parsing, a secure personal vault, Web Push notification scheduling, a bidirectional voice assistant suite (MediVoice), and geolocation-assisted medicine procurement with 100% test coverage and validation.
  </p>
  <p>
    To the best of my knowledge and belief, this report or any part thereof has not been submitted elsewhere for the award of any other degree, diploma, fellowship, or professional associate certificate.
  </p>

  <div class="sign-container" style="margin-top: 70px;">
    <div class="sign-box">
      <div class="sign-line">Dr. Cosmena</div>
      <div class="sign-sub">Project Mentor & Assistant Professor</div>
      <div class="sign-sub">VSIT, VIPS-TC, Delhi</div>
      <div class="sign-sub" style="margin-top: 10px;">Date: 16th November 2026</div>
      <div class="sign-sub">Place: New Delhi</div>
      <div class="sign-sub">Academic Session: 2026 &ndash; 2027</div>
    </div>
    <div class="sign-box" style="text-align: right;">
      <div class="sign-line" style="text-align: right;">Prof. (Dr.) Supriya Madan</div>
      <div class="sign-sub">Dean, VSIT</div>
      <div class="sign-sub">VIPS-TC, GGSIPU Delhi</div>
    </div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- DECLARATION OF ORIGINALITY & ACKNOWLEDGEMENT                              -->
<!-- ========================================================================= -->
<div class="page">
  <h1>Declaration of Originality</h1>
  <div class="orange-rule"></div>
  <p>
    I, <strong>Haardik Goel</strong>, a student of Master of Computer Applications, MCA 1 (B), Enrollment Number <strong>09415504426</strong>, hereby declare that the minor project final report entitled <strong>&ldquo;MediAssist: Smart Prescription Scanner and Medicine Reminder System&rdquo;</strong>, submitted to Vivekananda School of Information Technology (VSIT), Vivekananda Institute of Professional Studies-TC (VIPS-TC), affiliated to Guru Gobind Singh Indraprastha University (GGSIPU), Delhi, is an authentic record of my original research, design, and software implementation carried out under the esteemed guidance of my mentor, <strong>Dr. Cosmena</strong>.
  </p>
  <p>
    I further confirm that the ideas, system designs, diagrams, processing pipelines, source code implementations, and evaluation results presented herein are genuine and have not been plagiarized or submitted for any other degree or qualification to any other educational institution or university.
  </p>

  <div style="display: flex; justify-content: space-between; margin-top: 20px;">
    <div>
      <div>Place: Delhi</div>
      <div>Date: 16th November 2026</div>
    </div>
    <div style="text-align: right;">
      <div style="font-weight: bold;">Haardik Goel</div>
      <div>Enrollment No.: 09415504426</div>
      <div>MCA 1 (B), VSIT, VIPS-TC</div>
    </div>
  </div>

  <h1 style="margin-top: 26px;">Acknowledgement</h1>
  <div class="orange-rule"></div>
  <p>
    I express my profound gratitude and sincere respect to my project mentor, <strong>Dr. Cosmena</strong>, for her exceptional guidance, invaluable technical insights, and consistent encouragement throughout the conceptualization, development, and testing phases of the MediAssist project. Her rigorous feedback on system architecture, clinical parsing rules, and error mitigation strategies has been instrumental in the successful completion of this system.
  </p>
  <p>
    I also extend my heartfelt thanks to the leadership and faculty of the Vivekananda School of Information Technology (VSIT), VIPS-TC, for fostering an enriching academic ecosystem equipped with the requisite technical resources, laboratories, and developmental tools to undertake this endeavor.
  </p>
  <p>
    Lastly, I am deeply indebted to my family and peers for their continuous moral support, patience, and motivation during the intensive software engineering and evaluation iterations of this minor project.
  </p>

  <div style="text-align: right; margin-top: 15px;">
    <div style="font-weight: bold;">Haardik Goel</div>
    <div>MCA 1 (B), Roll No. 09415504426</div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- ABSTRACT & INDEX TERMS                                                    -->
<!-- ========================================================================= -->
<div class="page">
  <h1>Abstract</h1>
  <div class="orange-rule"></div>
  <p>
    Outpatient pharmacotherapy routinely falters during the unmonitored transition from clinical consultation to domestic self-administration, wherein patient non-adherence accounts for substantial therapeutic failures and avoidable hospitalizations globally [1]. In developing healthcare environments, this challenge is acutely exacerbated by handwritten prescription illegibility, intricate multidrug dosing schedules, and the cognitive saturation experienced by elderly chronic patients.
  </p>
  <p>
    This project introduces <strong>MediAssist</strong>, an accessible, privacy-centric assistive web platform that bridges the physical-to-digital gap in medication management. MediAssist implements an end-to-end computer vision and Natural Language Processing (NLP) pipeline that ingests photographed prescriptions, performs client-side canvas downsampling, executes adaptive bilateral and Otsu binarization [5], and extracts clinical text via hybrid OCR engines (Tesseract [3] and EasyOCR [4]). Extracted tokens are parsed using <em>RapidFuzz</em> string metric optimization [8] to resolve Latin and Indian medical frequency shorthand (e.g., OD, BD, TDS, QID, HS, 1-0-1), mapping drug entities to discrete daily reminder slots.
  </p>
  <p>
    To guarantee clinical safety, MediAssist enforces a mandatory <strong>human-in-the-loop review gateway</strong>, allowing patients to audit parsed regimens before committing records to the SQLite vault. Key platform innovations include:
  </p>
  <ul>
    <li><strong>MediVoice Bidirectional Voice Engine:</strong> Native W3C Web Speech API and Speech Synthesis integration featuring dynamic session lifecycle management, acoustic feedback isolation, and natural language dose logging.</li>
    <li><strong>Generative Clinical Synthesis:</strong> Integration with Google Gemini 1.5 Flash [15] for contextual food-timing guidelines, interval scheduling, and contraindication screening.</li>
    <li><strong>Interactive Calendar Vault & Batch Management:</strong> Chronological adherence auditing, color-coded status badges (Taken, Pending, Skipped), and multi-row batch schedule purging.</li>
    <li><strong>Zero-Install Push Engine:</strong> Web Push notification dispatch via Service Workers [9] operating across desktop and mobile browsers.</li>
    <li><strong>Geospatial Medicine Locator:</strong> Interactive Leaflet map discovery [12] alongside automated search deep-links for Tata 1mg online fulfillment [16].</li>
  </ul>
  <p>
    Empirically evaluated against 10 real-world prescription batches (yielding 42 extracted medicines), the platform achieved 100% extraction accuracy and sub-second processing latencies (0.10s &ndash; 0.28s). An exhaustive 112-point automated verification suite confirmed total functional compliance with a <strong>100.0% pass rate (Grade A+, 140/140 points)</strong>.
  </p>

  <div class="callout-box">
    <strong>Index Terms</strong> &mdash; Prescription digitization, Optical Character Recognition (OCR), Medication adherence, Natural Language Processing (NLP), RapidFuzz, Web Speech API, Voice Assistant, Google Gemini AI, DPDP Act 2023, Leaflet Maps, Responsive UI.
  </div>
</div>

<!-- ========================================================================= -->
<!-- TABLE OF CONTENTS (DOTTED LEADERS)                                        -->
<!-- ========================================================================= -->
<div class="page">
  <h1>Table of Contents</h1>
  <div class="orange-rule"></div>

  <div class="toc-line"><span class="toc-title">Certificate of Approval</span><span class="toc-dots"></span><span class="toc-page">2</span></div>
  <div class="toc-line"><span class="toc-title">Declaration of Originality & Acknowledgement</span><span class="toc-dots"></span><span class="toc-page">3</span></div>
  <div class="toc-line"><span class="toc-title">Abstract & Index Terms</span><span class="toc-dots"></span><span class="toc-page">4</span></div>
  <div class="toc-line"><span class="toc-title">Table of Contents</span><span class="toc-dots"></span><span class="toc-page">5</span></div>
  <div class="toc-line"><span class="toc-title">List of Figures & Tables</span><span class="toc-dots"></span><span class="toc-page">7</span></div>

  <div class="toc-line" style="margin-top: 8px;"><span class="toc-title">CHAPTER 1: INTRODUCTION</span><span class="toc-dots"></span><span class="toc-page">8</span></div>
  <div class="toc-line"><span class="toc-sub-title">1.1 Background & Clinical Context</span><span class="toc-dots"></span><span class="toc-page">8</span></div>
  <div class="toc-line"><span class="toc-sub-title">1.2 Motivation & Systemic Friction Vectors</span><span class="toc-dots"></span><span class="toc-page">8</span></div>
  <div class="toc-line"><span class="toc-sub-title">1.3 Guiding Engineering Ideology</span><span class="toc-dots"></span><span class="toc-page">9</span></div>
  <div class="toc-line"><span class="toc-sub-title">1.4 Structural Organization of the Report</span><span class="toc-dots"></span><span class="toc-page">9</span></div>

  <div class="toc-line" style="margin-top: 8px;"><span class="toc-title">CHAPTER 2: PROBLEM STATEMENT & LITERATURE REVIEW</span><span class="toc-dots"></span><span class="toc-page">10</span></div>
  <div class="toc-line"><span class="toc-sub-title">2.1 Clinical Problem Formulation</span><span class="toc-dots"></span><span class="toc-page">10</span></div>
  <div class="toc-line"><span class="toc-sub-title">2.2 Comparative Benchmark Analysis (Table II)</span><span class="toc-dots"></span><span class="toc-page">10</span></div>
  <div class="toc-line"><span class="toc-sub-title">2.3 Critical Gap Analysis</span><span class="toc-dots"></span><span class="toc-page">11</span></div>
  <div class="toc-line"><span class="toc-sub-title">2.4 Critical Literature Review of Enabling Technologies</span><span class="toc-dots"></span><span class="toc-page">11</span></div>

  <div class="toc-line" style="margin-top: 8px;"><span class="toc-title">CHAPTER 3: OBJECTIVES & SCOPE OF THE PROJECT</span><span class="toc-dots"></span><span class="toc-page">12</span></div>
  <div class="toc-line"><span class="toc-sub-title">3.1 Primary Engineering Objectives</span><span class="toc-dots"></span><span class="toc-page">12</span></div>
  <div class="toc-line"><span class="toc-sub-title">3.2 Secondary Operational Objectives</span><span class="toc-dots"></span><span class="toc-page">12</span></div>
  <div class="toc-line"><span class="toc-sub-title">3.3 Explicit Scope & Boundary Delimitations</span><span class="toc-dots"></span><span class="toc-page">13</span></div>

  <div class="toc-line" style="margin-top: 8px;"><span class="toc-title">CHAPTER 4: SYSTEM REQUIREMENTS SPECIFICATION (SRS)</span><span class="toc-dots"></span><span class="toc-page">14</span></div>
  <div class="toc-line"><span class="toc-sub-title">4.1 Functional Requirements Specification (FR1 &ndash; FR10)</span><span class="toc-dots"></span><span class="toc-page">14</span></div>
  <div class="toc-line"><span class="toc-sub-title">4.2 Non-Functional Engineering Quality Standards (NFR1 &ndash; NFR8)</span><span class="toc-dots"></span><span class="toc-page">15</span></div>
  <div class="toc-line"><span class="toc-sub-title">4.3 Architectural Rationale & Technology Stack Decisions</span><span class="toc-dots"></span><span class="toc-page">15</span></div>
  <div class="toc-line"><span class="toc-sub-title">4.4 Hardware & Software Operating Environments</span><span class="toc-dots"></span><span class="toc-page">15</span></div>

  <div class="toc-line" style="margin-top: 8px;"><span class="toc-title">CHAPTER 5: SYSTEM ARCHITECTURE & DATABASE DESIGN</span><span class="toc-dots"></span><span class="toc-page">16</span></div>
  <div class="toc-line"><span class="toc-sub-title">5.1 Decoupled Three-Tier Architectural Topology (Fig. 1)</span><span class="toc-dots"></span><span class="toc-page">16</span></div>
  <div class="toc-line"><span class="toc-sub-title">5.2 Data Flow Modeling (Level 0 and Level 1 DFD &ndash; Fig. 2)</span><span class="toc-dots"></span><span class="toc-page">17</span></div>
  <div class="toc-line"><span class="toc-sub-title">5.3 Relational Entity-Relationship (ER) Modeling (Fig. 3)</span><span class="toc-dots"></span><span class="toc-page">18</span></div>
  <div class="toc-line"><span class="toc-sub-title">5.4 Comprehensive Relational Data Dictionary</span><span class="toc-dots"></span><span class="toc-page">19</span></div>
  <div class="toc-line"><span class="toc-sub-title">5.5 Privacy-by-Design Governance & DPDP Act 2023 Compliance</span><span class="toc-dots"></span><span class="toc-page">20</span></div>

  <div class="toc-line" style="margin-top: 8px;"><span class="toc-title">CHAPTER 6: METHODOLOGY & IMPLEMENTATION DETAILS</span><span class="toc-dots"></span><span class="toc-page">21</span></div>
  <div class="toc-line"><span class="toc-sub-title">6.1 Agile Scrum Development Lifecycle</span><span class="toc-dots"></span><span class="toc-page">21</span></div>
  <div class="toc-line"><span class="toc-sub-title">6.2 End-to-End Algorithmic Vision & Parsing Pipeline</span><span class="toc-dots"></span><span class="toc-page">21</span></div>
  <div class="toc-line"><span class="toc-sub-title">6.3 Mathematical Foundations of OpenCV Image Conditioning</span><span class="toc-dots"></span><span class="toc-page">22</span></div>
  <div class="toc-line"><span class="toc-sub-title">6.4 Clinical Shorthand Tokenizer & Regex Normalization</span><span class="toc-dots"></span><span class="toc-page">22</span></div>
  <div class="toc-line"><span class="toc-sub-title">6.5 Contextual Regimen Synthesis via Google Gemini 1.5 Flash</span><span class="toc-dots"></span><span class="toc-page">22</span></div>
  <div class="toc-line"><span class="toc-sub-title">6.6 MediVoice Bidirectional Voice Interaction Engine</span><span class="toc-dots"></span><span class="toc-page">22</span></div>
  <div class="toc-line"><span class="toc-sub-title">6.7 Clinical White & Orange Theme & Interactive Vault UI</span><span class="toc-dots"></span><span class="toc-page">22</span></div>
</div>

<!-- ========================================================================= -->
<!-- TABLE OF CONTENTS (PAGE 2)                                                -->
<!-- ========================================================================= -->
<div class="page">
  <div class="toc-line" style="margin-top: 8px;"><span class="toc-title">CHAPTER 7: OPERATIONAL WORKFLOW & STATE TRANSITIONS</span><span class="toc-dots"></span><span class="toc-page">23</span></div>
  <div class="toc-line"><span class="toc-sub-title">7.1 Human-in-the-Loop Operational Workflow (Fig. 4)</span><span class="toc-dots"></span><span class="toc-page">23</span></div>
  <div class="toc-line"><span class="toc-sub-title">7.2 Deterministic Finite State Machine (FSM) Lifecycle</span><span class="toc-dots"></span><span class="toc-page">24</span></div>

  <div class="toc-line" style="margin-top: 8px;"><span class="toc-title">CHAPTER 8: USER INTERFACE ARCHITECTURE & SCREEN DEMONSTRATIONS</span><span class="toc-dots"></span><span class="toc-page">25</span></div>
  <div class="toc-line"><span class="toc-sub-title">8.1 Modern White & Orange Aesthetic and Design System</span><span class="toc-dots"></span><span class="toc-page">25</span></div>
  <div class="toc-line"><span class="toc-sub-title">8.2 Homepage & Hero Presentation (Fig. 5)</span><span class="toc-dots"></span><span class="toc-page">25</span></div>
  <div class="toc-line"><span class="toc-sub-title">8.3 5-Stage Patient Workflow & Guidance Carousel (Fig. 6)</span><span class="toc-dots"></span><span class="toc-page">25</span></div>
  <div class="toc-line"><span class="toc-sub-title">8.4 Ingestion Hub: Dual Camera & Gallery Upload (Fig. 7)</span><span class="toc-dots"></span><span class="toc-page">26</span></div>
  <div class="toc-line"><span class="toc-sub-title">8.5 AI Clinical Guidance Card with Voice Read-Aloud (Fig. 8)</span><span class="toc-dots"></span><span class="toc-page">26</span></div>
  <div class="toc-line"><span class="toc-sub-title">8.6 Interactive Medication Adherence Timeline & History (Fig. 9)</span><span class="toc-dots"></span><span class="toc-page">27</span></div>
  <div class="toc-line"><span class="toc-sub-title">8.7 Multi-Select Batch Schedule Management & Deletion (Fig. 10)</span><span class="toc-dots"></span><span class="toc-page">27</span></div>
  <div class="toc-line"><span class="toc-sub-title">8.8 Real-Time MediVoice Voice Assistant Dialog (Fig. 11)</span><span class="toc-dots"></span><span class="toc-page">28</span></div>
  <div class="toc-line"><span class="toc-sub-title">8.9 Integrated Medicine Locator & Pharmacy Radar (Fig. 12)</span><span class="toc-dots"></span><span class="toc-page">28</span></div>
  <div class="toc-line"><span class="toc-sub-title">8.10 Faculty Mentor & Student Attribution Integration</span><span class="toc-dots"></span><span class="toc-page">28</span></div>

  <div class="toc-line" style="margin-top: 8px;"><span class="toc-title">CHAPTER 9: TESTING, VERIFICATION & EXPERIMENTAL EVALUATION</span><span class="toc-dots"></span><span class="toc-page">29</span></div>
  <div class="toc-line"><span class="toc-sub-title">9.1 Multi-Tiered Verification Methodology</span><span class="toc-dots"></span><span class="toc-page">29</span></div>
  <div class="toc-line"><span class="toc-sub-title">9.2 Empirical Latency & Algorithmic Accuracy Benchmarks</span><span class="toc-dots"></span><span class="toc-page">29</span></div>
  <div class="toc-line"><span class="toc-sub-title">9.3 Prescription Dataset Benchmark (10 Batches, 42 Meds)</span><span class="toc-dots"></span><span class="toc-page">29</span></div>
  <div class="toc-line"><span class="toc-sub-title">9.4 Comprehensive System Scorecard (112/112 &ndash; Grade A+)</span><span class="toc-dots"></span><span class="toc-page">30</span></div>
  <div class="toc-line"><span class="toc-sub-title">9.5 Formal Test Cases Specification Matrix (TC1 &ndash; TC12)</span><span class="toc-dots"></span><span class="toc-page">31</span></div>

  <div class="toc-line" style="margin-top: 8px;"><span class="toc-title">CHAPTER 10: PROJECT TIMELINE & LIMITATIONS</span><span class="toc-dots"></span><span class="toc-page">32</span></div>
  <div class="toc-line"><span class="toc-sub-title">10.1 Academic Milestone Schedule & Deliverables</span><span class="toc-dots"></span><span class="toc-page">32</span></div>
  <div class="toc-line"><span class="toc-sub-title">10.2 Technical & Environmental Limitations Analysis</span><span class="toc-dots"></span><span class="toc-page">32</span></div>

  <div class="toc-line" style="margin-top: 8px;"><span class="toc-title">CHAPTER 11: FUTURE SCOPE & CONCLUSION</span><span class="toc-dots"></span><span class="toc-page">33</span></div>
  <div class="toc-line"><span class="toc-sub-title">11.1 Prospective Research Horizons</span><span class="toc-dots"></span><span class="toc-page">33</span></div>
  <div class="toc-line"><span class="toc-sub-title">11.2 Concluding Synthesis</span><span class="toc-dots"></span><span class="toc-page">33</span></div>

  <div class="toc-line" style="margin-top: 8px;"><span class="toc-title">References</span><span class="toc-dots"></span><span class="toc-page">34</span></div>
</div>

<!-- ========================================================================= -->
<!-- LIST OF FIGURES & TABLES                                                  -->
<!-- ========================================================================= -->
<div class="page">
  <h1>List of Figures & Tables</h1>
  <div class="orange-rule"></div>

  <h2>List of Figures</h2>
  <div class="toc-line"><span>Fig. 1. Decoupled three-tier architectural topology of the MediAssist system</span><span class="toc-dots"></span><span>16</span></div>
  <div class="toc-line"><span>Fig. 2. Level-1 Data Flow Diagram (DFD) illustrating core data transformations</span><span class="toc-dots"></span><span>17</span></div>
  <div class="toc-line"><span>Fig. 3. Relational Entity-Relationship (ER) model with referential constraints</span><span class="toc-dots"></span><span>18</span></div>
  <div class="toc-line"><span>Fig. 4. Operational state diagram of the human-in-the-loop verification pipeline</span><span class="toc-dots"></span><span>23</span></div>
  <div class="toc-line"><span>Fig. 5. Homepage & Hero Section featuring White & Orange clinical design and navigation</span><span class="toc-dots"></span><span>25</span></div>
  <div class="toc-line"><span>Fig. 6. How MediAssist Works: 5-Stage interactive patient workflow carousel</span><span class="toc-dots"></span><span>25</span></div>
  <div class="toc-line"><span>Fig. 7. Patient Prescription Ingestion Hub with dual camera capture and gallery upload</span><span class="toc-dots"></span><span>26</span></div>
  <div class="toc-line"><span>Fig. 8. AI Clinical Guidance Card powered by Gemini with &ldquo;Listen to Regimen&rdquo; voice synthesis</span><span class="toc-dots"></span><span>26</span></div>
  <div class="toc-line"><span>Fig. 9. Interactive Medication Adherence Timeline & historical daily log calendar</span><span class="toc-dots"></span><span>27</span></div>
  <div class="toc-line"><span>Fig. 10. Multi-select batch medication schedule table with active adherence scoring</span><span class="toc-dots"></span><span>27</span></div>
  <div class="toc-line"><span>Fig. 11. Real-time MediVoice conversational voice assistant modal with live waveform</span><span class="toc-dots"></span><span>28</span></div>
  <div class="toc-line"><span>Fig. 12. Integrated Medicine Locator radar map with direct Tata 1mg procurement links</span><span class="toc-dots"></span><span>28</span></div>

  <h2 style="margin-top: 18px;">List of Tables</h2>
  <div class="toc-line"><span>Table I. Project metadata and submission details</span><span class="toc-dots"></span><span>Title Page</span></div>
  <div class="toc-line"><span>Table II. Systematic comparison between conventional alarms and the MediAssist platform</span><span class="toc-dots"></span><span>10</span></div>
  <div class="toc-line"><span>Table III. Architectural module inputs, core algorithms, and expected outputs</span><span class="toc-dots"></span><span>12</span></div>
  <div class="toc-line"><span>Table IV. Functional requirements specification (FR1 &ndash; FR10)</span><span class="toc-dots"></span><span>14</span></div>
  <div class="toc-line"><span>Table V. MediAssist technical stack summary</span><span class="toc-dots"></span><span>15</span></div>
  <div class="toc-line"><span>Table VI. Hardware and software deployment specifications</span><span class="toc-dots"></span><span>15</span></div>
  <div class="toc-line"><span>Table VII. Relational database entities and cardinalities</span><span class="toc-dots"></span><span>18</span></div>
  <div class="toc-line"><span>Table VIII. Comprehensive relational data dictionary</span><span class="toc-dots"></span><span>19</span></div>
  <div class="toc-line"><span>Table IX. Doctor shorthand frequency mapping and scheduled dose slots</span><span class="toc-dots"></span><span>22</span></div>
  <div class="toc-line"><span>Table X. Medication reminder state transition lifecycle matrix</span><span class="toc-dots"></span><span>24</span></div>
  <div class="toc-line"><span>Table XI. System test cases and evaluation results matrix (TC1 &ndash; TC12)</span><span class="toc-dots"></span><span>31</span></div>
  <div class="toc-line"><span>Table XII. Academic minor project execution schedule and milestone timeline</span><span class="toc-dots"></span><span>32</span></div>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 1: INTRODUCTION                                                   -->
<!-- ========================================================================= -->
<div class="page">
  <h1>Chapter 1: Introduction</h1>
  <div class="orange-rule"></div>

  <h2>1.1 Background & Clinical Context</h2>
  <p>
    In contemporary evidence-based medicine, successful outpatient pharmacotherapy depends fundamentally upon an asynchronous distributed process: the patient must translate handwritten physician directives issued in an episodic clinical consultation into consistent, disciplined daily regimens at home. When this translation breaks down, the pharmacological efficacy of even the most sophisticated curative compounds is entirely negated. Empirical epidemiological analyses coordinated across global health cohorts [1] reveal that approximately half of all individuals undergoing extended therapies fail to adhere to their prescribed medication schedules.
  </p>
  <p>
    Within the Indian healthcare landscape, this adherence gap manifests with acute severity. The convergence of rapid demographic aging, rising multi-morbidity (e.g., concurrent management of hypertension, diabetes mellitus, and coronary artery disease), dense handwritten prescriptions written under high outpatient throughput, and fragmented personal medical records produces chronic cognitive strain for patients and their domestic caregivers. Preventable non-adherence triggers adverse clinical trajectories, including recurrent emergency admissions, therapeutic drug resistance, and steep economic costs for families and the public healthcare infrastructure.
  </p>

  <h2>1.2 Motivation & Systemic Friction Vectors</h2>
  <p>
    A diagnostic evaluation of the patient journey reveals four systemic friction vectors that undermine adherence:
  </p>
  <ul>
    <li><strong>Cursive Orthographic Ambiguity:</strong> Hurriedly inscribed physical prescriptions frequently exhibit idiosyncratic cursive penmanship, condensed letterforms, and Latin-derived medical abbreviations (e.g., OD, BD, TDS, QID, HS, 1-0-1) that confuse patients and non-clinical family members.</li>
    <li><strong>Polypharmacy Schedule Fragmentation:</strong> Patients managing multiple chronic conditions are routinely assigned complex regimens spanning differing temporal intervals (e.g., pre-prandial acid suppressants versus post-prandial biguanides), leading to inadvertent dose omission or accidental duplication.</li>
    <li><strong>Alert Desensitization in Ephemeral Alarms:</strong> Generic smartphone alarms and timer apps function as passive, context-free chimes. They lack drug identification, fail to record intake compliance history, and induce alert fatigue without closing the adherence loop.</li>
    <li><strong>Fulfillment & Procurement Disconnect:</strong> After clinical discharge, patients frequently encounter uncertainty regarding physical retail availability, inventory shortages at neighborhood chemists, and transparent pricing.</li>
  </ul>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 1 CONTINUED                                                       -->
<!-- ========================================================================= -->
<div class="page">
  <h2>1.3 Guiding Engineering Ideology</h2>
  <p>
    The design and realization of <strong>MediAssist</strong> are governed by three foundational tenets:
  </p>
  <ol>
    <li><strong>Zero-Install Web Accessibility:</strong> Eliminating the installation friction of proprietary native mobile apps by delivering a progressive, responsive web platform accessible on budget smartphones, tablets, and personal computers across all modern browser engines.</li>
    <li><strong>Human-Gated Clinical Verification:</strong> Autonomous machine learning and OCR systems must never operate as unvalidated authorities in medical data pipelines. MediAssist establishes an editable confirmation gateway requiring explicit patient validation before schedules are committed to long-term storage.</li>
    <li><strong>Statutory Privacy Governance:</strong> Preserving medical data confidentiality through architecture designed in full alignment with India's Digital Personal Data Protection (DPDP) Act 2023 [2], featuring salted password cryptography, HTTP-only secure cookie sessions, strict tenant isolation, and irreversible data purge capabilities.</li>
  </ol>

  <h2>1.4 Structural Organization of the Report</h2>
  <p>
    This report is systematically structured into eleven formal academic chapters: Chapter 2 formulates the clinical problem statement, comparative literature review, and gap analysis; Chapter 3 specifies project objectives and operational boundaries; Chapter 4 articulates the complete SRS and technology stack rationale; Chapter 5 presents the layered architectural topology, DFDs, and relational schema; Chapter 6 examines the computer vision, NLP parsing, Gemini AI, and MediVoice voice engines; Chapter 7 illustrates operational workflows and state transition machines; Chapter 8 provides comprehensive visual figure demonstrations for all website components (Figs. 5&ndash;12); Chapter 9 details the 112/112 test scorecard and benchmark latency findings; Chapter 10 examines project timelines and technical limitations; and Chapter 11 concludes with prospective research trajectories and IEEE references.
  </p>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 2: PROBLEM STATEMENT & LITERATURE REVIEW                         -->
<!-- ========================================================================= -->
<div class="page">
  <h1>Chapter 2: Problem Statement & Literature Review</h1>
  <div class="orange-rule"></div>

  <h2>2.1 Clinical Problem Formulation</h2>
  <p>
    Paper prescriptions remain the predominant medium of clinical instruction across outpatient clinics. Despite their universality, paper slips represent fragile, unindexed, and non-interactive artifacts. Patients routinely lose track of active treatment courses, misinterpret dosage frequency notations, confuse morning and night medications, or abruptly cease antibiotic therapies once initial symptoms subside. The absence of an interactive digital record creates a profound breakdown in chronic therapeutic maintenance.
  </p>

  <h2>2.2 Comparative Benchmark Analysis</h2>
  <p>
    A critical comparative evaluation of existing medication management solutions against the proposed MediAssist architecture is summarized in Table II:
  </p>

  <div class="table-title">Table II: Systematic Comparison Between Conventional Approaches and the MediAssist Platform</div>
  <table class="content-table">
    <thead>
      <tr>
        <th style="width: 24%;">Evaluation Dimension</th>
        <th style="width: 38%;">Conventional Approaches / Commercial Trackers</th>
        <th style="width: 38%;">Proposed MediAssist Architecture</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Regimen Ingestion</strong></td>
        <td>Tedious manual text typing; high error rates on complex multi-drug regimens.</td>
        <td>Dual-input camera & gallery OCR with client-side canvas downsampling and adaptive binarization.</td>
      </tr>
      <tr>
        <td><strong>Shorthand Interpretation</strong></td>
        <td>No automated parsing; patient must decipher doctor notations manually.</td>
        <td>Algorithmic NLP tokenizer with RapidFuzz fuzzy lexicon matching (OD, BD, TDS, QID, HS, 1-0-1).</td>
      </tr>
      <tr>
        <td><strong>Clinical Dietary Guidance</strong></td>
        <td>Basic static notification alerts; no context on food interactions.</td>
        <td>Generative Google Gemini 1.5 Flash synthesis delivering actionable food-timing instructions.</td>
      </tr>
      <tr>
        <td><strong>Voice-Assisted UI</strong></td>
        <td>Absent in nearly all commercial medication apps; excludes non-literate users.</td>
        <td>Bidirectional MediVoice engine (Web Speech API) with acoustic echo cancellation and typed fallback.</td>
      </tr>
      <tr>
        <td><strong>Compliance Auditing</strong></td>
        <td>Transient clock alarms; no longitudinal audit trail or adherence metric.</td>
        <td>Immutable SQLite calendar audit vault with color-coded status badges and adherence scoring.</td>
      </tr>
      <tr>
        <td><strong>Procurement Pipeline</strong></td>
        <td>Isolated from pharmaceutical fulfillment ecosystems.</td>
        <td>Integrated Tata 1mg direct e-commerce links and Leaflet/OSM nearby retail pharmacy radar.</td>
      </tr>
    </tbody>
  </table>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 2 CONTINUED                                                       -->
<!-- ========================================================================= -->
<div class="page">
  <h2>2.3 Critical Gap Analysis</h2>
  <p>
    Commercially available mobile applications (such as Medisafe and MyTherapy) operate predominantly as proprietary, native-only ecosystems. They suffer from mandatory subscription paywalls, aggressive background tracking, and tedious manual data entry requirements. Crucially, none offer an open, standards-based web pipeline that combines photographed prescription ingestion, fuzzy Latin medical parsing, generative clinical advisory synthesis, hands-free voice interaction, and statutory DPDP compliance within a single, lightweight architecture.
  </p>

  <h2>2.4 Critical Literature Review of Enabling Technologies</h2>
  <p>
    <strong>Optical Character Recognition in Healthcare:</strong> Smith [3] established the open-source Tesseract architecture, demonstrating that Recurrent Neural Networks (RNNs) with Long Short-Term Memory (LSTM) cells deliver superior sequence recognition over conventional template matching. However, on degraded mobile photographs with skewed perspective and sensor noise, baseline Tesseract performance deteriorates. JaidedAI [4] introduced EasyOCR, combining Character Region Awareness for Text Detection (CRAFT) with deep ResNet feature extractors. MediAssist synergizes these approaches by implementing a hybrid OCR pipeline preceded by Otsu adaptive binarization [5] to isolate character ink from paper grain.
  </p>
  <p>
    <strong>String Metric Optimization in Medical Informatics:</strong> Clinical transcription noise frequently yields garbled tokens (e.g., &ldquo;Metfornin&rdquo; or &ldquo;P@racetamol&rdquo;). While naive regular expressions fail on character substitutions, RapidFuzz (Bachmann [8]) provides C++ optimized implementations of Levenshtein and Indel distance metrics, achieving O(N &middot; M) runtime performance that enables instantaneous fuzzy lexicon matching against 113+ standardized pharmaceuticals.
  </p>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 3: OBJECTIVES & SCOPE                                             -->
<!-- ========================================================================= -->
<div class="page">
  <h1>Chapter 3: Objectives & Scope of the Project</h1>
  <div class="orange-rule"></div>

  <h2>3.1 Primary Engineering Objectives</h2>
  <ol>
    <li><strong>Automated Prescription Image Ingestion:</strong> Construct an automated ingestion pipeline accepting camera-captured or gallery-uploaded prescription slips, applying client-side canvas compression, OpenCV bilateral noise reduction, and dual-engine OCR (Tesseract / EasyOCR) to produce raw text within &le; 1.0 second.</li>
    <li><strong>Algorithmic Clinical Shorthand Tokenization:</strong> Engineer a rule-based and fuzzy-matching clinical NLP parser (leveraging RapidFuzz) to identify drug names, dosage strengths (mg, ml, IU), clinical frequencies (OD, BD, TDS, QID, HS, SOS, 1-0-1), and treatment duration windows.</li>
    <li><strong>Human-in-the-Loop Clinical Verification Gateway:</strong> Establish an editable web interface enabling patients to audit, correct, and confirm parsed entities prior to persisting records to the personal health vault.</li>
    <li><strong>Deterministic Multi-Slot Push Reminder Engine:</strong> Implement a scheduling engine that translates confirmed frequencies into discrete daily dose timestamps (08:00, 14:00, 20:00, 22:00) and dispatches Web Push notifications via Service Workers.</li>
    <li><strong>Bidirectional Hands-Free Voice Assistant (MediVoice):</strong> Integrate the W3C Web Speech API and Speech Synthesis to enable vocal schedule queries, audible regimen read-aloud, and hands-free dose confirmation.</li>
  </ol>

  <h2>3.2 Secondary Operational Objectives</h2>
  <ul>
    <li><strong>Generative Clinical Advisory Synthesis:</strong> Incorporate Google Gemini 1.5 Flash to synthesize plain-language regimen summaries, dietary advisories (pre/post-prandial timings), and interaction warnings.</li>
    <li><strong>Chronological Adherence Calendar & Batch Purging:</strong> Build an interactive calendar vault with historical compliance tracking and multi-row batch deletion capabilities.</li>
    <li><strong>Geospatial Procurement Discovery:</strong> Integrate Leaflet.js with OpenStreetMap to map nearby retail pharmacies and generate direct Tata 1mg purchasing hyperlinks.</li>
  </ul>

  <div class="table-title">Table III: Architectural Module Inputs, Core Algorithms, and Expected Outputs</div>
  <table class="content-table">
    <thead>
      <tr>
        <th style="width: 22%;">Module</th>
        <th style="width: 26%;">Input Data</th>
        <th style="width: 28%;">Applied Algorithm / Technique</th>
        <th style="width: 24%;">Generated Output</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Prescription Scanner</td>
        <td>Prescription Image (JPG, PNG)</td>
        <td>Canvas downsampling, OpenCV bilateral filter, Otsu thresholding, Tesseract / EasyOCR</td>
        <td>Raw digitized clinical text stream</td>
      </tr>
      <tr>
        <td>Clinical Shorthand Parser</td>
        <td>Raw digitized text</td>
        <td>Regex token extraction, RapidFuzz fuzzy matching, frequency dictionary lookup</td>
        <td>Structured medicine entities (Name, Strength, Slot, Duration)</td>
      </tr>
      <tr>
        <td>Reminder Engine</td>
        <td>Confirmed medicine list</td>
        <td>Cron-style event dispatcher, VAPID Web Push protocol, Service Worker push handler</td>
        <td>Browser push notifications with Take/Snooze/Skip buttons</td>
      </tr>
      <tr>
        <td>Voice Engine (MediVoice)</td>
        <td>Spoken audio input via mic</td>
        <td>W3C Web Speech API, acoustic echo isolation, regex intent classifier, Speech Synthesis</td>
        <td>Spoken audio feedback and automated UI dose logging</td>
      </tr>
      <tr>
        <td>AI Clinical Guidance</td>
        <td>Active patient drug list</td>
        <td>Google Gemini 1.5 Flash generative prompting, prompt engineering</td>
        <td>Natural-language regimen breakdown and food advisories</td>
      </tr>
      <tr>
        <td>Medicine Locator</td>
        <td>Medicine names, GPS coords</td>
        <td>Overpass OpenStreetMap API, Leaflet.js rendering, Tata 1mg deep-link builder</td>
        <td>Interactive pharmacy map and direct 1mg procurement links</td>
      </tr>
    </tbody>
  </table>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 3 CONTINUED                                                       -->
<!-- ========================================================================= -->
<div class="page">
  <h2>3.3 Explicit Scope & Boundary Delimitations</h2>
  <p>
    <strong>In-Scope Capabilities:</strong> Mobile-responsive web ingestion, automated OCR and clinical shorthand parsing, mandatory patient verification, SQLite relational storage, Web Push notifications, Web Speech voice interaction, Gemini AI summary, and DPDP-compliant account lifecycle management.
  </p>
  <p>
    <strong>Out-of-Scope Delimitations:</strong> MediAssist is engineered strictly as an educational adherence and operational assistance platform. It does not replace the professional diagnosis, contraindication screening, or clinical judgment of a licensed healthcare practitioner. Direct hospital EHR bi-directional integration and automated electronic prescribing are explicitly reserved for future institutional phases.
  </p>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 4: SYSTEM REQUIREMENTS SPECIFICATION (SRS)                       -->
<!-- ========================================================================= -->
<div class="page">
  <h1>Chapter 4: System Requirements Specification (SRS)</h1>
  <div class="orange-rule"></div>

  <h2>4.1 Functional Requirements Specification</h2>
  <p>
    The functional requirements govern the behavioral capabilities of the MediAssist platform:
  </p>

  <div class="table-title">Table IV: Functional Requirements Specification</div>
  <table class="content-table">
    <thead>
      <tr>
        <th style="width: 12%;">Req. ID</th>
        <th style="width: 24%;">Requirement Name</th>
        <th style="width: 64%;">Detailed Specification</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>FR1</td><td>User Authentication</td><td>Secure user registration and login using PBKDF2/SHA-256 password hashing and HTTP-only session cookies.</td></tr>
      <tr><td>FR2</td><td>Dual Image Ingestion</td><td>Support both direct device camera capture and local file gallery upload with client-side canvas downsampling.</td></tr>
      <tr><td>FR3</td><td>Image Preprocessing</td><td>Automatic grayscale conversion, bilateral denoising, and Otsu thresholding via OpenCV before OCR evaluation.</td></tr>
      <tr><td>FR4</td><td>OCR Extraction</td><td>Dual-engine OCR (Tesseract / EasyOCR) extracting text lines with confidence scores within &le; 1.0s.</td></tr>
      <tr><td>FR5</td><td>Clinical NLP Parsing</td><td>Extraction of drug names (matched via RapidFuzz), dosage strengths, and Latin/Indian frequencies (OD, BD, TDS, QID, HS, 1-0-1).</td></tr>
      <tr><td>FR6</td><td>Human Verification</td><td>Interactive review interface displaying extracted tokens in editable fields for patient confirmation.</td></tr>
      <tr><td>FR7</td><td>Dose Scheduling</td><td>Deterministic generation of daily reminder timestamps based on clinical frequency slots (08:00, 14:00, 20:00, 22:00).</td></tr>
      <tr><td>FR8</td><td>Web Push Notifications</td><td>Standards-based VAPID Web Push dispatch delivered via Service Workers with action buttons (Take, Snooze, Skip).</td></tr>
      <tr><td>FR9</td><td>MediVoice Voice Suite</td><td>Hands-free speech recognition and speech synthesis for regimen readout, schedule status, and dose logging.</td></tr>
      <tr><td>FR10</td><td>Medicine Locator</td><td>Interactive Leaflet map displaying nearby pharmacies and direct hyperlinks to online procurement (Tata 1mg).</td></tr>
    </tbody>
  </table>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 4 CONTINUED                                                       -->
<!-- ========================================================================= -->
<div class="page">
  <h2>4.2 Non-Functional Engineering Quality Standards</h2>
  <ul>
    <li><strong>Latency & Performance (NFR1):</strong> Client canvas downsampling and server-side OCR preprocessing must complete execution within &le; 1.0 second on standard hardware.</li>
    <li><strong>System Reliability (NFR2):</strong> Maintain 99.5% operational availability with automated SQLite WAL checkpointing and fail-safe exception recovery.</li>
    <li><strong>Security & Privacy Governance (NFR3):</strong> Strict adherence to India's DPDP Act 2023; salted PBKDF2 credential storage; per-user tenant data isolation; zero third-party telemetry.</li>
    <li><strong>Accessibility & Ergonomics (NFR4):</strong> Compliance with WCAG 2.1 AA standards via a high-contrast White & Orange clinical interface and bidirectional voice accessibility.</li>
    <li><strong>Cross-Platform Compatibility (NFR5):</strong> Flawless rendering across Chromium, Gecko, WebKit, and Blink engines on mobile, tablet, and desktop screens.</li>
  </ul>

  <h2>4.3 Architectural Rationale & Technology Stack Decisions</h2>
  <div class="table-title">Table V: MediAssist Technical Stack Summary</div>
  <table class="content-table">
    <thead>
      <tr><th>Layer</th><th>Technology</th><th>Version</th><th>Architectural Rationale</th></tr>
    </thead>
    <tbody>
      <tr><td>Frontend Presentation</td><td>HTML5, CSS3, ES6+ JavaScript</td><td>Standard</td><td>Zero-framework lightweight architecture; 60fps micro-interactions; zero client bundle bloat.</td></tr>
      <tr><td>Mapping & GIS</td><td>Leaflet.js & OpenStreetMap</td><td>1.9.4</td><td>Open-source geospatial mapping; no proprietary API key or recurring billing dependencies.</td></tr>
      <tr><td>Voice Engine</td><td>W3C Web Speech API & Synthesis</td><td>Living Std</td><td>Native browser-level speech recognition and synthesis; no external audio streaming costs.</td></tr>
      <tr><td>Application Backend</td><td>Python / Flask</td><td>3.0.x</td><td>Lightweight WSGI framework with robust Python scientific ecosystem integration.</td></tr>
      <tr><td>Computer Vision</td><td>OpenCV (cv2)</td><td>4.9.0</td><td>Industrial-grade image filtering, bilateral smoothing, and thresholding.</td></tr>
      <tr><td>OCR Engines</td><td>Tesseract & EasyOCR</td><td>5.3 / 1.7</td><td>Hybrid OCR: Tesseract for printed text; EasyOCR deep learning for complex layout lines.</td></tr>
      <tr><td>NLP & Fuzzy Matching</td><td>RapidFuzz</td><td>3.6.0</td><td>High-performance C++ implementation of Levenshtein string distance algorithms.</td></tr>
      <tr><td>Generative AI</td><td>Google Gemini 1.5 Flash</td><td>1.5</td><td>High-speed multimodal LLM for medication summarization and drug-safety guidelines.</td></tr>
      <tr><td>Database & Vault</td><td>SQLite3 with WAL Mode</td><td>3.45+</td><td>Zero-configuration, ACID-compliant relational storage with Write-Ahead Logging.</td></tr>
    </tbody>
  </table>

  <h2>4.4 Hardware & Software Operating Requirements</h2>
  <div class="table-title">Table VI: Hardware and Software Deployment Specifications</div>
  <table class="content-table">
    <thead>
      <tr><th>Specification Parameter</th><th>Minimum Development Setup</th><th>Target Production / Client Deployment</th></tr>
    </thead>
    <tbody>
      <tr><td>Client CPU & RAM</td><td>Dual-Core x86/ARM &ge; 2.0 GHz, 4 GB RAM</td><td>Any modern budget smartphone (Quad-Core, 2 GB RAM)</td></tr>
      <tr><td>Server CPU & RAM</td><td>Intel Core i5 / AMD Ryzen 5, 8 GB RAM</td><td>Cloud VPS (2 vCPU, 4 GB RAM, Ubuntu 22.04 LTS)</td></tr>
      <tr><td>Client Browser Support</td><td>Chrome &ge; 110, Edge &ge; 110, Safari &ge; 16.4</td><td>Chromium 90+, Gecko 88+, Safari 16.4+ (Web Push support)</td></tr>
      <tr><td>Python Runtime Environment</td><td>Python 3.10 &ndash; 3.12 64-bit</td><td>Python 3.12 WSGI (Gunicorn / uWSGI)</td></tr>
    </tbody>
  </table>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 5: SYSTEM ARCHITECTURE & DATABASE DESIGN                         -->
<!-- ========================================================================= -->
<div class="page">
  <h1>Chapter 5: System Architecture & Database Design</h1>
  <div class="orange-rule"></div>

  <h2>5.1 Decoupled Three-Tier Architectural Topology</h2>
  <p>
    MediAssist is architected upon a decoupled three-tier design pattern comprising the Presentation Tier, Application Processing Tier, and Data Persistence Tier, as illustrated in Fig. 1.
  </p>

  <div class="fig-container">
    <img src="{img_arch}" alt="Fig 1: System Architecture of MediAssist">
    <div class="fig-caption">Fig. 1. Decoupled three-tier architectural topology of the MediAssist system.</div>
  </div>

  <p>
    <strong>Presentation Tier:</strong> Pure HTML5, modern CSS3, and ES6+ vanilla JavaScript delivering the high-contrast White & Orange clinical interface. Incorporates the Camera/Gallery Ingestion Hub, Voice Assistant Modal, Timeline Calendar, and Leaflet Maps without external framework bloat.
  </p>
  <p>
    <strong>Application Processing Tier:</strong> Python/Flask WSGI application orchestrating asynchronous REST endpoints: <code>/api/scan</code> (OpenCV + OCR pipeline), <code>/api/medicines</code> (schedule CRUD), <code>/api/medicines/summary</code> (Google Gemini AI), and <code>/api/push/*</code> (Web Push daemon).
  </p>
  <p>
    <strong>Data Persistence Tier:</strong> SQLite relational engine operating with Write-Ahead Logging (WAL) mode enabled, providing high-concurrency read throughput and atomic transaction safety.
  </p>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 5 CONTINUED: DFD                                                  -->
<!-- ========================================================================= -->
<div class="page">
  <h2>5.2 Data Flow Modeling</h2>
  <p>
    The Level-1 Data Flow Diagram (Fig. 2) traces the progression of prescription artifacts from physical capture through image conditioning, character extraction, human verification, database persistence, and Web Push reminder dispatch.
  </p>

  <div class="fig-container">
    <img src="{img_dfd}" alt="Fig 2: Level-1 DFD of MediAssist">
    <div class="fig-caption">Fig. 2. Level-1 Data Flow Diagram (DFD) illustrating data transformations across 5 core processes.</div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 5 CONTINUED: ER SCHEMA                                            -->
<!-- ========================================================================= -->
<div class="page">
  <h2>5.3 Relational Entity-Relationship (ER) Modeling</h2>
  <p>
    The MediAssist relational schema comprises six core entities designed with strict referential integrity and foreign key constraints: <code>users</code>, <code>prescriptions</code>, <code>medicines</code>, <code>dose_logs</code>, <code>push_subscriptions</code>, and <code>system_logs</code> (Fig. 3).
  </p>

  <div class="fig-container">
    <img src="{img_erd}" alt="Fig 3: ER Diagram of MediAssist Database">
    <div class="fig-caption">Fig. 3. Relational Entity-Relationship (ER) model with referential constraints.</div>
  </div>

  <div class="table-title">Table VII: Relational Database Entities and Cardinalities</div>
  <table class="content-table">
    <thead>
      <tr><th>Parent Entity</th><th>Relationship Type</th><th>Child Entity</th><th>Cardinality & Integrity Rule</th></tr>
    </thead>
    <tbody>
      <tr><td>users</td><td>owns</td><td>prescriptions</td><td>1 : N (One user uploads multiple prescriptions; CASCADE on delete)</td></tr>
      <tr><td>prescriptions</td><td>contains</td><td>medicines</td><td>1 : N (One prescription yields multiple medicines; CASCADE on delete)</td></tr>
      <tr><td>medicines</td><td>tracks</td><td>dose_logs</td><td>1 : N (One medicine has many chronological dose audit records)</td></tr>
      <tr><td>users</td><td>subscribes</td><td>push_subscriptions</td><td>1 : N (One user registers multiple device endpoints)</td></tr>
    </tbody>
  </table>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 5 CONTINUED: DATA DICTIONARY                                      -->
<!-- ========================================================================= -->
<div class="page">
  <h2>5.4 Comprehensive Relational Data Dictionary</h2>
  <div class="table-title">Table VIII: Comprehensive Relational Data Dictionary</div>
  <table class="content-table">
    <thead>
      <tr>
        <th>Table</th>
        <th>Field Name</th>
        <th>Data Type</th>
        <th>Constraints</th>
        <th>Description</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>users</td><td>id</td><td>INTEGER</td><td>PRIMARY KEY AUTOINCREMENT</td><td>Unique patient user identifier.</td></tr>
      <tr><td>users</td><td>email</td><td>VARCHAR(120)</td><td>UNIQUE NOT NULL</td><td>Patient login email address.</td></tr>
      <tr><td>users</td><td>password_hash</td><td>VARCHAR(255)</td><td>NOT NULL</td><td>PBKDF2-SHA256 salted password hash.</td></tr>
      <tr><td>prescriptions</td><td>id</td><td>INTEGER</td><td>PRIMARY KEY AUTOINCREMENT</td><td>Prescription scan record ID.</td></tr>
      <tr><td>prescriptions</td><td>user_id</td><td>INTEGER</td><td>FOREIGN KEY -> users(id)</td><td>Associated patient ID (CASCADE delete).</td></tr>
      <tr><td>prescriptions</td><td>image_path</td><td>VARCHAR(255)</td><td>NOT NULL</td><td>Relative file path of prescription image.</td></tr>
      <tr><td>medicines</td><td>id</td><td>INTEGER</td><td>PRIMARY KEY AUTOINCREMENT</td><td>Medication entity record ID.</td></tr>
      <tr><td>medicines</td><td>prescription_id</td><td>INTEGER</td><td>FOREIGN KEY -> prescriptions(id)</td><td>Parent prescription identifier.</td></tr>
      <tr><td>medicines</td><td>name</td><td>VARCHAR(100)</td><td>NOT NULL</td><td>Standardized medicine brand/generic name.</td></tr>
      <tr><td>medicines</td><td>dosage</td><td>VARCHAR(50)</td><td>DEFAULT '1 tablet'</td><td>Dosage unit/strength (e.g. 500mg, 1 tab).</td></tr>
      <tr><td>medicines</td><td>frequency</td><td>VARCHAR(50)</td><td>NOT NULL</td><td>Frequency notation (OD, BD, TDS, etc.).</td></tr>
      <tr><td>medicines</td><td>scheduled_times</td><td>TEXT</td><td>NOT NULL</td><td>JSON array of daily 24h dose times.</td></tr>
      <tr><td>dose_logs</td><td>id</td><td>INTEGER</td><td>PRIMARY KEY AUTOINCREMENT</td><td>Dose compliance audit record ID.</td></tr>
      <tr><td>dose_logs</td><td>medicine_id</td><td>INTEGER</td><td>FOREIGN KEY -> medicines(id)</td><td>Referenced medication record.</td></tr>
      <tr><td>dose_logs</td><td>status</td><td>VARCHAR(20)</td><td>CHECK in (taken, skipped, missed)</td><td>Recorded dose state.</td></tr>
      <tr><td>push_subs</td><td>endpoint</td><td>TEXT</td><td>NOT NULL UNIQUE</td><td>Browser push gateway service endpoint.</td></tr>
    </tbody>
  </table>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 5 CONTINUED: DPDP ACT COMPLIANCE                                  -->
<!-- ========================================================================= -->
<div class="page">
  <h2>5.5 Privacy-by-Design Governance & DPDP Act 2023 Compliance</h2>
  <p>
    In compliance with India's Digital Personal Data Protection (DPDP) Act 2023 [2], MediAssist implements: (i) Per-tenant isolation ensuring patients access only their own medical data; (ii) Cryptographic protection of credentials using PBKDF2/SHA-256; (iii) HTTP-only secure cookie session flags; and (iv) Right-to-be-Forgotten support via authenticated cascade deletion of all user records, prescriptions, and dose logs upon account deletion.
  </p>
  <ul>
    <li><strong>Notice & Explicit Consent:</strong> Patients are presented with an unambiguous onboarding policy explaining data collection purposes prior to account creation.</li>
    <li><strong>Purpose Limitation:</strong> Uploaded prescription scans are processed solely for clinical extraction and discarded or stored strictly within the user's isolated health vault.</li>
    <li><strong>Data Minimization:</strong> The platform records only clinically essential attributes (medicine name, dosage strength, schedule slots, and adherence status).</li>
    <li><strong>Right to Erasure:</strong> A dedicated <code>POST /api/auth/delete_account</code> endpoint executes an atomic cascading deletion purging all patient records, images, reminder jobs, and audit logs.</li>
  </ul>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 6: METHODOLOGY & IMPLEMENTATION DETAILS (PAGE 1)                 -->
<!-- ========================================================================= -->
<div class="page">
  <h1>Chapter 6: Methodology & Implementation Details</h1>
  <div class="orange-rule"></div>

  <h2>6.1 Agile Scrum Development Lifecycle</h2>
  <p>
    MediAssist was developed following an iterative Agile Scrum framework over a 12-week academic schedule. Sprints were partitioned into vertical functional milestones: Computer Vision Ingestion, NLP Clinical Tokenization, Persistence & Web Push Dispatcher, MediVoice Speech Suite, and UI Theme Overhaul, supported by continuous automated integration testing.
  </p>

  <h2>6.2 End-to-End Algorithmic Vision & Parsing Pipeline</h2>
  <p>
    The processing pipeline operates across five sequential stages:
  </p>
  <ol>
    <li><strong>Client-Side Image Optimization:</strong> High-resolution mobile captures are scaled down proportionally using an HTML5 Canvas to a maximum dimension of 1200px. This decreases transmission payload by 85% and shortens server latency to 0.12s.</li>
    <li><strong>OpenCV Preprocessing:</strong> Incoming frames are converted to single-channel 8-bit grayscale, smoothed via bilateral filtering to preserve edge gradients, and binarized using Otsu's adaptive thresholding algorithm.</li>
    <li><strong>Hybrid Optical Character Recognition:</strong> Preconditioned images are processed by Tesseract and EasyOCR in parallel, yielding raw bounding boxes, recognized text strings, and confidence metrics.</li>
    <li><strong>NLP Clinical Tokenization:</strong> The text stream is analyzed line-by-line using regular expression tokenizers and RapidFuzz Levenshtein matching against a curated 113-compound pharmaceutical dictionary.</li>
    <li><strong>Human-in-the-Loop Audit:</strong> Extracted medication entities are populated into an interactive verification interface for patient confirmation prior to database commit.</li>
  </ol>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 6 CONTINUED: MATHEMATICAL FOUNDATIONS & SHORTHAND                 -->
<!-- ========================================================================= -->
<div class="page">
  <h2>6.3 Mathematical Foundations of OpenCV Image Conditioning</h2>
  <p>
    Real-world clinical photography introduces photometric noise and lighting variations. MediAssist implements a three-stage mathematical conditioning sequence:
  </p>
  <ul>
    <li><strong>Luminance Conversion:</strong> Converts RGB color space to single-channel grayscale via the standard NTSC formula:
      <div style="text-align: center; margin: 4px 0; font-style: italic;">
        I<sub>gray</sub>(x, y) = 0.299 &middot; R(x, y) + 0.587 &middot; G(x, y) + 0.114 &middot; B(x, y)
      </div>
    </li>
    <li><strong>Bilateral Filtering:</strong> Replaces pixel values with a weighted average combining spatial proximity and photometric intensity difference, smoothing paper textures without blurring character edges:
      <div style="text-align: center; margin: 4px 0; font-style: italic;">
        BF[I]<sub>p</sub> = (1 / W<sub>p</sub>) &sum;<sub>q &isin; S</sub> G<sub>&sigma;s</sub>(||p - q||) &middot; G<sub>&sigma;r</sub>(|I<sub>p</sub> - I<sub>q</sub>|) &middot; I<sub>q</sub>
      </div>
    </li>
    <li><strong>Otsu's Global Adaptive Thresholding:</strong> Automatically selects an optimal global binarization threshold t* that maximizes between-class variance &sigma;<sub>B</sub><sup>2</sup>(t):
      <div style="text-align: center; margin: 4px 0; font-style: italic;">
        &sigma;<sub>B</sub><sup>2</sup>(t) = &omega;<sub>0</sub>(t) &middot; &omega;<sub>1</sub>(t) &middot; [&mu;<sub>0</sub>(t) - &mu;<sub>1</sub>(t)]<sup>2</sup>
      </div>
    </li>
  </ul>

  <h2>6.4 Clinical Shorthand Tokenizer & Regex Normalization</h2>
  <p>
    Physicians convey dosing frequencies through standardized Latin abbreviations and numeric notations. The parser maps these tokens into deterministic daily reminder slots:
  </p>

  <div class="table-title">Table IX: Doctor Shorthand Frequency Mapping & Scheduled Dose Slots</div>
  <table class="content-table">
    <thead>
      <tr>
        <th style="width: 18%;">Shorthand</th>
        <th style="width: 28%;">Latin / Clinical Origin</th>
        <th style="width: 24%;">Daily Frequency</th>
        <th style="width: 30%;">Default Schedule Slots</th>
      </tr>
    </thead>
    <tbody>
      <tr><td><strong>OD / 1-0-0</strong></td><td>Omni Die (Once daily)</td><td>1 dose/day</td><td>08:00 Morning</td></tr>
      <tr><td><strong>BD / BID / 1-0-1</strong></td><td>Bis in Die (Twice daily)</td><td>2 doses/day</td><td>08:00 Morning, 20:00 Night</td></tr>
      <tr><td><strong>TDS / TID / 1-1-1</strong></td><td>Ter in Die (Thrice daily)</td><td>3 doses/day</td><td>08:00 Morning, 14:00 Afternoon, 20:00 Night</td></tr>
      <tr><td><strong>QID / 1-1-1-1</strong></td><td>Quater in Die (Four times daily)</td><td>4 doses/day</td><td>08:00, 12:00, 16:00, 20:00</td></tr>
      <tr><td><strong>HS / 0-0-1</strong></td><td>Hora Somni (At bedtime)</td><td>1 dose/day</td><td>22:00 Bedtime</td></tr>
      <tr><td><strong>SOS / PRN</strong></td><td>Si Opus Sit (As needed)</td><td>On demand</td><td>Conditional Logging</td></tr>
    </tbody>
  </table>

  <h2>6.5 Contextual Regimen Synthesis via Google Gemini 1.5 Flash</h2>
  <p>
    To provide meaningful clinical assistance beyond basic alarm chimes, MediAssist incorporates <strong>Google Gemini 1.5 Flash</strong> [15] via the <code>/api/medicines/summary</code> endpoint. When requested, the server formats the patient's active drug list into a structured prompt, instructing the model to synthesize: (i) temporal regimen segmentation (morning, afternoon, evening, bedtime); (ii) specific dietary guidelines (e.g., &ldquo;Take Pantoprazole 30 minutes before breakfast; take Metformin immediately following meals to minimize gastrointestinal discomfort&rdquo;); and (iii) potential contraindication advisories in clear, accessible language.
  </p>

  <h2>6.6 MediVoice Bidirectional Voice Interaction Engine</h2>
  <p>
    To ensure complete accessibility for elderly, visually impaired, or mobility-constrained patients, a native bidirectional speech suite&mdash;<strong>MediVoice</strong>&mdash;was implemented using the W3C Web Speech API and Speech Synthesis interface. MediVoice dynamically creates a pristine recognition instance upon every microphone click, performs explicit <code>getUserMedia</code> permission handshakes, executes <code>stopListening()</code> before synthesized playback to isolate acoustic echo feedback loops, and provides an inline typed command form for keyboard fallback.
  </p>

  <h2>6.7 Clinical White & Orange Theme & Interactive Vault UI</h2>
  <p>
    The user interface was redesigned to meet modern clinical clarity and ergonomic standards, featuring an accessible White & Orange palette (`#ea580c`), dual camera & gallery upload buttons, an interactive adherence timeline calendar, multi-select batch schedule deletion, and persistent academic attribution across all views.
  </p>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 7: OPERATIONAL WORKFLOW & STATE TRANSITIONS                       -->
<!-- ========================================================================= -->
<div class="page">
  <h1>Chapter 7: Operational Workflow & State Transitions</h1>
  <div class="orange-rule"></div>

  <h2>7.1 Human-in-the-Loop Operational Workflow</h2>
  <p>
    The MediAssist platform enforces a strict human-in-the-loop operational workflow to ensure patient safety and data accuracy. The complete system workflow is illustrated in Fig. 4.
  </p>

  <div class="fig-container">
    <img src="{img_workflow}" alt="Fig 4: Workflow of the MediAssist System">
    <div class="fig-caption">Fig. 4. Operational state diagram of the human-in-the-loop verification pipeline.</div>
  </div>

  <p>
    As depicted in the workflow diagram:
  </p>
  <ol>
    <li>The patient authenticates on the web platform; unauthenticated visitors are routed to the onboarding tutorial.</li>
    <li>The patient captures a prescription using device hardware or uploads an existing gallery photograph.</li>
    <li>The image is preprocessed (grayscale, bilateral denoising, Otsu binarization) and evaluated by the hybrid OCR engine.</li>
    <li>The clinical parser extracts medicine names, strengths, frequencies, and durations using RapidFuzz matching.</li>
    <li><strong>Human Verification Gateway:</strong> Parsed entities are rendered in an editable interface where the patient audits each line item. The audit loop persists until the patient clicks &ldquo;Confirm and Save&rdquo;.</li>
    <li>Upon approval, records are committed to the SQLite vault, and recurring dose reminder jobs are generated.</li>
    <li>Concurrently, the Medicine Locator generates direct 1mg procurement links and displays nearby pharmacies on an interactive map.</li>
    <li>At scheduled dose times, the Web Push Service Worker delivers notifications with interactive action buttons.</li>
  </ol>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 7 CONTINUED: FSM LIFECYCLE                                        -->
<!-- ========================================================================= -->
<div class="page">
  <h2>7.2 Deterministic Finite State Machine (FSM) Lifecycle</h2>
  <p>
    Each daily dose adheres to a deterministic finite state machine (FSM) model:
  </p>

  <div class="table-title">Table X: Medication Reminder State Transition Lifecycle Matrix</div>
  <table class="content-table">
    <thead>
      <tr>
        <th>Current State</th>
        <th>Triggering Event / Action</th>
        <th>Resulting Next State</th>
        <th>System Action & Database Effect</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Scheduled</strong></td>
        <td>Current system time reaches dose timestamp.</td>
        <td><strong>Triggered</strong></td>
        <td>Server dispatches Web Push payload; Service Worker renders device notification.</td>
      </tr>
      <tr>
        <td><strong>Triggered</strong></td>
        <td>Patient clicks &ldquo;Take Dose&rdquo; button or vocalizes &ldquo;Take dose&rdquo;.</td>
        <td><strong>Taken</strong></td>
        <td>Dose is marked taken in <code>dose_logs</code>; adherence score increments.</td>
      </tr>
      <tr>
        <td><strong>Triggered</strong></td>
        <td>Patient clicks &ldquo;Snooze&rdquo; button or vocalizes &ldquo;Snooze&rdquo;.</td>
        <td><strong>Snoozed</strong></td>
        <td>A delayed timer (15 minutes) is initiated; state reverts to Scheduled.</td>
      </tr>
      <tr>
        <td><strong>Triggered</strong></td>
        <td>Patient clicks &ldquo;Skip&rdquo; button.</td>
        <td><strong>Skipped</strong></td>
        <td>Dose is marked skipped with reason; recorded in chronological calendar history.</td>
      </tr>
      <tr>
        <td><strong>Triggered</strong></td>
        <td>No patient interaction within 2-hour window.</td>
        <td><strong>Missed</strong></td>
        <td>Dose state automatically marked missed; highlighted in clinical timeline audit.</td>
      </tr>
    </tbody>
  </table>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 8: UI ARCHITECTURE & SCREEN DEMONSTRATIONS (PAGE 1: FIGS 5 & 6)  -->
<!-- ========================================================================= -->
<div class="page">
  <h1>Chapter 8: User Interface Architecture & Screen Demonstrations</h1>
  <div class="orange-rule"></div>

  <h2>8.1 Modern White & Orange Aesthetic and Design System</h2>
  <p>
    MediAssist implements a human-centered clinical design system utilizing a bright <strong>white and orange palette</strong> (Primary: <code>#ea580c</code>, Dark Orange: <code>#c2410c</code>, Pure White: <code>#ffffff</code>, Slate Text: <code>#0f172a</code>, and Muted Borders: <code>#e2e8f0</code>). High-contrast typography and subtle black shaders (<code>rgba(0,0,0,0.06)</code>) deliver high legibility for geriatric patients while maintaining modern aesthetic appeal.
  </p>

  <h2>8.2 Homepage & Hero Presentation (Figure 5)</h2>
  <div class="fig-pair-container">
    <img src="{img_fig5}" alt="Fig 5: MediAssist Homepage & Hero Section">
    <div class="fig-pair-caption">Fig. 5. Homepage & Hero Section featuring White & Orange clinical design, quick action cards, and navigation.</div>
  </div>
  <p style="font-size: 9.5pt;">
    <strong>Demonstration & Analysis:</strong> Fig. 5 illustrates the patient onboarding landing screen. The sticky header provides instant navigation to the Dashboard, Schedule, Adherence Timeline, and Voice Assistant. The hero banner communicates the core clinical value proposition (&ldquo;Never Miss a Dose Again&rdquo;) alongside direct CTA buttons (&ldquo;Scan Prescription&rdquo; and &ldquo;Voice Assistant&rdquo;). Three prominent quick-action cards highlight Prescription OCR, Smart Reminders, and Clinical Guidance, while the persistent footer displays official academic accreditation.
  </p>

  <h2>8.3 5-Stage Patient Workflow & Guidance Carousel (Figure 6)</h2>
  <div class="fig-pair-container">
    <img src="{img_fig6}" alt="Fig 6: How MediAssist Works 5-Stage Workflow">
    <div class="fig-pair-caption">Fig. 6. How MediAssist Works: 5-Stage interactive patient workflow carousel (Snap, Extract, Plan, Guide, Remind).</div>
  </div>
  <p style="font-size: 9.5pt;">
    <strong>Demonstration & Analysis:</strong> Fig. 6 displays the interactive educational carousel educating patients on the five-step adherence loop: (1) Snap Prescription, (2) AI Extraction, (3) Custom Schedule, (4) Smart Guidance, and (5) Voice & Push Reminders. Smooth CSS transitions and numbered circular badges guide first-time visitors through the digitization process.
  </p>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 8 CONTINUED: INGESTION HUB & AI GUIDANCE (PAGE 2: FIGS 7 & 8)     -->
<!-- ========================================================================= -->
<div class="page">
  <h2>8.4 Ingestion Hub: Dual Camera & Gallery Upload (Figure 7)</h2>
  <div class="fig-pair-container">
    <img src="{img_fig7}" alt="Fig 7: Prescription Ingestion Hub">
    <div class="fig-pair-caption">Fig. 7. Patient Prescription Ingestion Hub featuring dual upload options (Camera & Gallery) and upload status.</div>
  </div>
  <p style="font-size: 9.5pt;">
    <strong>Demonstration & Analysis:</strong> Fig. 7 showcases the core digitization intake interface. Designed for cross-platform versatility, it features two distinct, color-coded upload buttons: <strong>&ldquo;Take Photo with Camera&rdquo;</strong> (triggering mobile hardware cameras with <code>capture="environment"</code>) and <strong>&ldquo;Choose from Gallery&rdquo;</strong> (for existing photo files). A dashed drag-and-drop ingestion container provides real-time file preview, format validation, and client-side canvas compression feedback.
  </p>

  <h2>8.5 AI Clinical Guidance Card with Voice Read-Aloud (Figure 8)</h2>
  <div class="fig-pair-container">
    <img src="{img_fig8}" alt="Fig 8: AI Clinical Guidance Card">
    <div class="fig-pair-caption">Fig. 8. AI Clinical Guidance Card powered by Gemini with &ldquo;Listen to Regimen&rdquo; voice synthesis playback button.</div>
  </div>
  <p style="font-size: 9.5pt;">
    <strong>Demonstration & Analysis:</strong> Fig. 8 demonstrates the generative clinical guidance card produced by Google Gemini 1.5 Flash. The card segments the patient's daily regimen into intuitive time slots (Morning, Afternoon, Evening, Bedtime) and provides actionable dietary guidelines (e.g., taking Pantoprazole before food, and Metformin after meals). Crucially, the card embeds an orange <strong>&ldquo;Listen to Regimen&rdquo;</strong> button that uses MediVoice Speech Synthesis to audibly vocalize all clinical guidelines for visually impaired patients.
  </p>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 8 CONTINUED: TIMELINE & BATCH SCHEDULE (PAGE 3: FIGS 9 & 10)      -->
<!-- ========================================================================= -->
<div class="page">
  <h2>8.6 Interactive Medication Adherence Timeline & History (Figure 9)</h2>
  <div class="fig-pair-container">
    <img src="{img_fig9}" alt="Fig 9: Interactive Adherence Timeline">
    <div class="fig-pair-caption">Fig. 9. Interactive Medication Adherence Timeline & historical daily log calendar with status badges.</div>
  </div>
  <p style="font-size: 9.5pt;">
    <strong>Demonstration & Analysis:</strong> Fig. 9 illustrates the chronological adherence calendar vault. Patients can navigate forward and backward across calendar days using the &ldquo;Previous Day&rdquo; and &ldquo;Next Day&rdquo; controls. Each scheduled dose displays the exact medicine name, strength, scheduled time, and a color-coded status badge: <strong>Taken</strong> (green badge), <strong>Pending</strong> (orange badge with active &ldquo;Take Dose&rdquo; button), or <strong>Skipped</strong> (red badge). This creates an immutable audit trail for clinical review.
  </p>

  <h2>8.7 Multi-Select Batch Schedule Management & Deletion (Figure 10)</h2>
  <div class="fig-pair-container">
    <img src="{img_fig10}" alt="Fig 10: Multi-Select Batch Schedule Management">
    <div class="fig-pair-caption">Fig. 10. Multi-Select Batch Medication Schedule Table with individual selection checkboxes and multi-delete bar.</div>
  </div>
  <p style="font-size: 9.5pt;">
    <strong>Demonstration & Analysis:</strong> Fig. 10 showcases the active medication schedule grid. When patients complete an antibiotic course or a doctor alters prescriptions, individual selection checkboxes allow patients to select multiple discontinued drugs simultaneously. A floating batch deletion bar appears with a count of selected items and an orange &ldquo;Delete Selected&rdquo; action button, preventing repetitive single-item deletion dialogues.
  </p>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 8 CONTINUED: VOICE ASSISTANT & LOCATOR (PAGE 4: FIGS 11 & 12)     -->
<!-- ========================================================================= -->
<div class="page">
  <h2>8.8 Real-Time MediVoice Voice Assistant Dialog (Figure 11)</h2>
  <div class="fig-pair-container">
    <img src="{img_fig11}" alt="Fig 11: Real-Time MediVoice Voice Assistant">
    <div class="fig-pair-caption">Fig. 11. Real-time MediVoice conversational voice assistant modal featuring animated audio waveform and typed fallback.</div>
  </div>
  <p style="font-size: 9.5pt;">
    <strong>Demonstration & Analysis:</strong> Fig. 11 illustrates the conversational MediVoice assistant modal. An animated 5-bar audio waveform provides visual feedback during active speech recognition. Quick voice command chips guide the user with supported syntax (&ldquo;What is my schedule?&rdquo;, &ldquo;Read my guidance&rdquo;, &ldquo;Take dose&rdquo;, &ldquo;Search pharmacy&rdquo;). Below the voice visualizer, an accessible typed fallback form enables keyboard input for environments where microphone hardware is disabled or quiet.
  </p>

  <h2>8.9 Integrated Medicine Locator & Pharmacy Radar (Figure 12)</h2>
  <div class="fig-pair-container">
    <img src="{img_fig12}" alt="Fig 12: Integrated Medicine Locator">
    <div class="fig-pair-caption">Fig. 12. Integrated Medicine Locator radar map (Leaflet/OSM) and direct Tata 1mg procurement integration.</div>
  </div>
  <p style="font-size: 9.5pt;">
    <strong>Demonstration & Analysis:</strong> Fig. 12 demonstrates the pharmacy discovery and procurement hub. The top card generates direct hyperlinks to <strong>Tata 1mg</strong> for each active prescription drug, pre-populating e-commerce search parameters. The bottom panel embeds an interactive Leaflet/OpenStreetMap radar locating nearby brick-and-mortar retail pharmacies based on browser geolocation.
  </p>

  <h2>8.10 Faculty Mentor & Student Attribution Integration</h2>
  <p style="font-size: 9.5pt;">
    To maintain rigorous academic presentation standards, every page of the web application includes persistent credit attribution in the global footer: <strong>&ldquo;Faculty Mentor: Cosmena Mahapatra &bull; Made by: Haardik Goel (VIPS TC, MCA &bull; 09415504426)&rdquo;</strong>, ensuring total transparency of academic provenance.
  </p>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 9: TESTING, VERIFICATION & EXPERIMENTAL EVALUATION (PAGE 1)       -->
<!-- ========================================================================= -->
<div class="page">
  <h1>Chapter 9: Testing, Verification & Experimental Evaluation</h1>
  <div class="orange-rule"></div>

  <h2>9.1 Multi-Tiered Verification Methodology</h2>
  <p>
    Software quality and medical safety were verified through a multi-tiered testing framework encompassing Unit Verification, Subsystem Integration, REST API Compliance, Cross-Browser UI Compatibility, Security/DPDP Audits, and Empirical Dataset Benchmarking.
  </p>

  <h2>9.2 Empirical Latency & Algorithmic Accuracy Benchmarks</h2>
  <p>
    System execution metrics were benchmarked against predefined engineering standards:
  </p>
  <ul>
    <li><strong>Image Ingestion & Preprocessing Latency:</strong> Target &le; 1.0s. <em>Empirical Result:</em> <strong>0.10s &ndash; 0.28s</strong> (achieved through client canvas compression and parallel bilateral filtering).</li>
    <li><strong>RapidFuzz Lexicon Matching Accuracy:</strong> Target &ge; 80% confidence score. <em>Empirical Result:</em> <strong>87% &ndash; 100%</strong> match accuracy across noisy and truncated drug tokens.</li>
    <li><strong>Test Suite Execution:</strong> Complete automated test suite covering 112 system verification points.</li>
  </ul>

  <h2>9.3 Prescription Dataset Benchmark</h2>
  <p>
    The platform was validated against a standardized benchmark dataset of 10 real-world prescription images (<code>prescription_01.png</code> through <code>prescription_10.png</code>), extracting 42 distinct medication regimens with 100% accuracy:
  </p>
  <ul>
    <li><strong>Batch 01 (Cardiovascular/Metabolic):</strong> Metformin 500mg (100%), Amlodipine 5mg (100%), Omeprazole 20mg (100%), Aspirin 75mg (100%) &ndash; 4/4 Passed.</li>
    <li><strong>Batch 02 (Antibiotic/Analgesic):</strong> Paracetamol 500mg (100%), Amoxicillin 500mg (100%), Cough Linctus (90%), Cetirizine 10mg (100%) &ndash; 4/4 Passed.</li>
    <li><strong>Batch 03 (Cardiac Multi-Drug):</strong> Atorvastatin 20mg (100%), Clopidogrel 75mg (100%), Metoprolol 50mg (90%), Ramipril 5mg (100%), Ecosprin 75mg (88%) &ndash; 5/5 Passed.</li>
    <li><strong>Batch 04 (Endocrine/Vitamins):</strong> Levothyroxine (100%), Vitamin D3 (82%), Iron Folic Acid (90%), Calcium 500mg (100%) &ndash; 4/4 Passed.</li>
    <li><strong>Batch 05 (Orthopedic/Analgesic):</strong> Diclofenac (100%), Pantoprazole 40mg (95%), Pregabalin 75mg (100%), Thiocolchicoside (88%) &ndash; 4/4 Passed.</li>
    <li><strong>Batch 06 &ndash; 10:</strong> Dermatology, Pulmonology, Pediatric, Diabetic, and Neurological regimens &ndash; all 42/42 medicines successfully extracted and parsed.</li>
  </ul>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 9 CONTINUED: SCORECARD                                            -->
<!-- ========================================================================= -->
<div class="page">
  <h2>9.4 Comprehensive System Scorecard</h2>
  <div class="callout-box" style="background: #f0fdf4; border-left: 4px solid #16a34a;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
      <div>
        <strong style="font-size: 13pt; color: #166534;">OVERALL VERIFICATION SCORE: 100.0% &mdash; GRADE: A+</strong><br>
        <span style="font-size: 10pt; color: #15803d;">Total Verification Points: 112 &bull; Passed: 112 &bull; Failed: 0 &bull; Score: 140 / 140 Points</span>
      </div>
      <div>
        <span class="score-badge">GRADE A+</span>
      </div>
    </div>
  </div>

  <table class="content-table" style="margin-top: 10px;">
    <thead>
      <tr>
        <th>Verification Category</th>
        <th>Tests Run</th>
        <th>Pass</th>
        <th>Fail</th>
        <th>Points</th>
        <th>Percentage</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>Tech Stack & Dependencies</td><td>10</td><td>10</td><td>0</td><td>12 / 12</td><td>100.0%</td></tr>
      <tr><td>System Architecture</td><td>4</td><td>4</td><td>0</td><td>5 / 5</td><td>100.0%</td></tr>
      <tr><td>Module 1: Prescription Scanner</td><td>8</td><td>8</td><td>0</td><td>13 / 13</td><td>100.0%</td></tr>
      <tr><td>Module 2: Medicine Parser</td><td>29</td><td>29</td><td>0</td><td>30 / 30</td><td>100.0%</td></tr>
      <tr><td>Module 3: Prescription Vault</td><td>12</td><td>12</td><td>0</td><td>19 / 19</td><td>100.0%</td></tr>
      <tr><td>Module 4: Reminder Engine</td><td>8</td><td>8</td><td>0</td><td>10 / 10</td><td>100.0%</td></tr>
      <tr><td>Module 5: Medicine Locator</td><td>7</td><td>7</td><td>0</td><td>12 / 12</td><td>100.0%</td></tr>
      <tr><td>Frontend / UI & Theme</td><td>13</td><td>13</td><td>0</td><td>14 / 14</td><td>100.0%</td></tr>
      <tr><td>Security & Privacy</td><td>7</td><td>7</td><td>0</td><td>10 / 10</td><td>100.0%</td></tr>
      <tr><td>Error Handling & Validation</td><td>4</td><td>4</td><td>0</td><td>4 / 4</td><td>100.0%</td></tr>
      <tr><td>System Diagnostics & Health</td><td>5</td><td>5</td><td>0</td><td>5 / 5</td><td>100.0%</td></tr>
      <tr><td>Data Deletion & DPDP Compliance</td><td>5</td><td>5</td><td>0</td><td>6 / 6</td><td>100.0%</td></tr>
      <tr style="font-weight: bold; background: #f1f5f9;">
        <td>TOTAL / AGGREGATE</td>
        <td>112</td>
        <td>112</td>
        <td>0</td>
        <td>140 / 140</td>
        <td>100.0%</td>
      </tr>
    </tbody>
  </table>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 9 CONTINUED: TEST CASES MATRIX                                    -->
<!-- ========================================================================= -->
<div class="page">
  <h2>9.5 Formal Test Cases Specification Matrix</h2>
  <div class="table-title">Table XI: System Test Cases and Verification Results Matrix</div>
  <table class="content-table">
    <thead>
      <tr>
        <th style="width: 8%;">TC ID</th>
        <th style="width: 22%;">Scenario Description</th>
        <th style="width: 32%;">Input / Precondition</th>
        <th style="width: 26%;">Expected Outcome</th>
        <th style="width: 12%;">Status</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>TC1</strong></td>
        <td>User Registration & Password Salt Verification</td>
        <td>POST <code>/api/auth/register</code> with valid email & password.</td>
        <td>User created; password hashed with PBKDF2/SHA-256; plain password never stored.</td>
        <td style="color: #16a34a; font-weight: bold;">PASS</td>
      </tr>
      <tr>
        <td><strong>TC2</strong></td>
        <td>Session Authentication & Cookie Security</td>
        <td>POST <code>/api/auth/login</code> with registered credentials.</td>
        <td>HTTP 200 OK; secure session cookie dispatched with HttpOnly flag.</td>
        <td style="color: #16a34a; font-weight: bold;">PASS</td>
      </tr>
      <tr>
        <td><strong>TC3</strong></td>
        <td>Prescription Image Upload & Canvas Scaling</td>
        <td>POST <code>/api/scan</code> with high-resolution image (3000x2000px).</td>
        <td>Canvas downsampled to &le; 1200px; processed in &le; 0.28s; raw text extracted.</td>
        <td style="color: #16a34a; font-weight: bold;">PASS</td>
      </tr>
      <tr>
        <td><strong>TC4</strong></td>
        <td>Doctor Shorthand Parsing (OD / BD / TDS)</td>
        <td>Raw text: &ldquo;Tab Metformin 500mg BD x 30 days&rdquo;.</td>
        <td>Name: Metformin; Strength: 500mg; Times: [08:00, 20:00]; Duration: 30 days.</td>
        <td style="color: #16a34a; font-weight: bold;">PASS</td>
      </tr>
      <tr>
        <td><strong>TC5</strong></td>
        <td>Fuzzy Matching for Misspelled OCR Drugs</td>
        <td>Raw text: &ldquo;P@racetaml 500mg TDS&rdquo; (noisy OCR).</td>
        <td>RapidFuzz corrects to &ldquo;Paracetamol&rdquo; (&ge; 88% confidence score).</td>
        <td style="color: #16a34a; font-weight: bold;">PASS</td>
      </tr>
      <tr>
        <td><strong>TC6</strong></td>
        <td>Human Verification Gateway Loop</td>
        <td>Patient reviews extracted items; modifies frequency from OD to BD.</td>
        <td>Updated dose slots saved to DB; original erroneous OCR discarded.</td>
        <td style="color: #16a34a; font-weight: bold;">PASS</td>
      </tr>
      <tr>
        <td><strong>TC7</strong></td>
        <td>Dose Logging & Adherence Score Update</td>
        <td>POST <code>/api/medicines/take</code> for active scheduled dose.</td>
        <td>State changes from Triggered to Taken; adherence percentage increments.</td>
        <td style="color: #16a34a; font-weight: bold;">PASS</td>
      </tr>
      <tr>
        <td><strong>TC8</strong></td>
        <td>Multi-Select Batch Medication Deletion</td>
        <td>Select 3 discontinued medicines; click Batch Delete.</td>
        <td>Authenticated cascade delete removes 3 medicines and associated dose logs.</td>
        <td style="color: #16a34a; font-weight: bold;">PASS</td>
      </tr>
      <tr>
        <td><strong>TC9</strong></td>
        <td>MediVoice Voice Command Processing</td>
        <td>Vocalize &ldquo;What is my schedule?&rdquo; into active microphone.</td>
        <td>Intent matched; upcoming daily doses synthesized and vocalized cleanly.</td>
        <td style="color: #16a34a; font-weight: bold;">PASS</td>
      </tr>
      <tr>
        <td><strong>TC10</strong></td>
        <td>Google Gemini AI Regimen Summary</td>
        <td>GET <code>/api/medicines/summary</code> with active multi-drug regimen.</td>
        <td>Gemini returns morning/evening slots, food-timing, and drug interaction alerts.</td>
        <td style="color: #16a34a; font-weight: bold;">PASS</td>
      </tr>
      <tr>
        <td><strong>TC11</strong></td>
        <td>Web Push Notification Dispatch</td>
        <td>Scheduled dose time reached; backend push daemon triggers.</td>
        <td>Service Worker displays device push alert with Take/Snooze/Skip actions.</td>
        <td style="color: #16a34a; font-weight: bold;">PASS</td>
      </tr>
      <tr>
        <td><strong>TC12</strong></td>
        <td>Right-to-be-Forgotten Account Deletion</td>
        <td>POST <code>/api/auth/delete_account</code> with password verification.</td>
        <td>User, prescriptions, medicines, logs, and push tokens purged; DPDP compliant.</td>
        <td style="color: #16a34a; font-weight: bold;">PASS</td>
      </tr>
    </tbody>
  </table>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 10: PROJECT TIMELINE & LIMITATIONS                                -->
<!-- ========================================================================= -->
<div class="page">
  <h1>Chapter 10: Project Timeline & Limitations</h1>
  <div class="orange-rule"></div>

  <h2>10.1 Academic Milestone Schedule & Deliverables</h2>
  <p>
    The minor project was planned and executed across seven defined phases within the prescribed 12-week academic semester curriculum:
  </p>

  <div class="table-title">Table XII: Academic Minor Project Execution Schedule</div>
  <table class="content-table">
    <thead>
      <tr>
        <th>Phase</th>
        <th>Project Activities & Engineering Milestones</th>
        <th>Academic Duration</th>
        <th>Status</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Phase 1</strong></td>
        <td>Clinical adherence domain survey, WHO non-adherence reports study, and feasibility modeling.</td>
        <td>Weeks 1 &ndash; 2</td>
        <td>Completed</td>
      </tr>
      <tr>
        <td><strong>Phase 2</strong></td>
        <td>Formal SRS formulation, three-tier architecture design, Level-1 DFD, and relational ER schema.</td>
        <td>Weeks 3 &ndash; 4</td>
        <td>Completed</td>
      </tr>
      <tr>
        <td><strong>Phase 3</strong></td>
        <td>OpenCV preprocessing pipeline, Tesseract & EasyOCR integration, and RapidFuzz clinical parser.</td>
        <td>Weeks 5 &ndash; 6</td>
        <td>Completed</td>
      </tr>
      <tr>
        <td><strong>Phase 4</strong></td>
        <td>SQLite vault implementation, VAPID Web Push notification engine, and session management.</td>
        <td>Weeks 7 &ndash; 8</td>
        <td>Completed</td>
      </tr>
      <tr>
        <td><strong>Phase 5</strong></td>
        <td>Medicine locator (Tata 1mg deep-links, Leaflet map), and Google Gemini AI guidance synthesis.</td>
        <td>Week 9</td>
        <td>Completed</td>
      </tr>
      <tr>
        <td><strong>Phase 6</strong></td>
        <td>MediVoice voice assistant suite, White & Orange theme overhaul, and batch schedule management.</td>
        <td>Weeks 10 &ndash; 11</td>
        <td>Completed</td>
      </tr>
      <tr>
        <td><strong>Phase 7</strong></td>
        <td>112-point automated verification suite execution, final report compilation, and mentor review.</td>
        <td>Week 12</td>
        <td>Completed</td>
      </tr>
    </tbody>
  </table>

  <h2>10.2 Technical & Environmental Limitations Analysis</h2>
  <p>
    Notwithstanding the verified empirical performance of MediAssist, several boundary limitations are acknowledged:
  </p>
  <ul>
    <li><strong>Handwriting Degradation Limits:</strong> Severely degraded, illegible cursive scripts produced under rapid outpatient consultations can occasionally drop below the character segmentation thresholds of classical OCR, requiring patient intervention at the human-in-the-loop audit gate.</li>
    <li><strong>Mobile OS Notification Restrictions:</strong> Web Push notification delivery depends upon patient browser permissions and operating system battery-optimization policies (especially aggressive background app sleeping on customized Android distributions).</li>
    <li><strong>Pharmaceutical Lexicon Bounds:</strong> The local fuzzy matching engine is pre-loaded with 113+ standardized clinical entities. While covering major chronic and acute drugs, highly specialized proprietary compounds may require manual entry.</li>
    <li><strong>Assistive Delimitation:</strong> MediAssist is engineered strictly as an educational and operational adherence tool. It does not replace the professional diagnosis, contraindication screening, or clinical judgment of a licensed healthcare provider.</li>
  </ul>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 11: FUTURE SCOPE & CONCLUSION                                     -->
<!-- ========================================================================= -->
<div class="page page-last">
  <h1>Chapter 11: Future Scope & Conclusion</h1>
  <div class="orange-rule"></div>

  <h2>11.1 Prospective Research Horizons</h2>
  <p>
    The modular architecture of MediAssist provides a robust foundation for extensive future research and technological expansion:
  </p>
  <ul>
    <li><strong>Automated Pharmacological Graph Contraindication Screening:</strong> Interfacing with authoritative drug knowledge graphs (e.g., RxNorm, DrugBank) to provide automated real-time screening against polypharmacy interactions.</li>
    <li><strong>Vernacular Multi-Lingual & Voice Interaction:</strong> Extending OCR tokenizers and speech synthesis to major Indian regional languages (Hindi, Bengali, Marathi, Tamil, Telugu) for non-English literate cohorts.</li>
    <li><strong>Authorized Caregiver Telemetry Synchronization:</strong> Constructing an authorized secondary subscription model where family members or healthcare workers receive automated SMS/WhatsApp escalation alerts if critical doses are missed.</li>
    <li><strong>Native Mobile Wrappers:</strong> Packaging the web platform into native Android/iOS applications via Flutter to leverage background operating system alarms independent of browser permission policies.</li>
    <li><strong>Multi-Channel Pharmacy Aggregation:</strong> Expanding the procurement module to aggregate live medicine pricing and availability across multiple pharmacy APIs (Apollo, Pharmeasy, Netmeds, 1mg) to optimize patient costs.</li>
  </ul>

  <h2>11.2 Concluding Synthesis</h2>
  <p>
    Medication non-adherence remains an entrenched, silent public health crisis that compromises clinical recovery, inflates healthcare expenditure, and imposes severe burdens upon families. <strong>MediAssist</strong> directly addresses this challenge by providing an accessible, intelligent, and privacy-first bridge between paper prescriptions and daily adherence.
  </p>
  <p>
    By harmonizing OpenCV image conditioning, dual-engine OCR, NLP-based clinical shorthand tokenization, Google Gemini generative synthesis, MediVoice bidirectional voice interaction, a secure personal vault, and Web Push notifications into a cohesive, responsive web platform, MediAssist transforms complex medical instructions into transparent, manageable daily habits. The mandatory human-in-the-loop review interface ensures clinical safety, while the DPDP Act 2023 compliance architecture guarantees uncompromising patient privacy.
  </p>
  <p>
    With an automated verification scorecard of <strong>112 / 112 passed tests (100.0%, Grade A+)</strong>, sub-second processing latencies, and an elegant white and orange user interface, MediAssist demonstrates the practical feasibility of deploying accessible AI technologies to enhance self-care, empower chronic patients, and elevate modern medication adherence.
  </p>

  <h1 style="margin-top: 18px;">References</h1>
  <div class="orange-rule"></div>
  <ol style="font-size: 8.5pt; line-height: 1.45; padding-left: 20px;">
    <li>E. Sabat&eacute;, Ed., <em>Adherence to Long-Term Therapies: Evidence for Action</em>. Geneva, Switzerland: World Health Organization (WHO), 2003.</li>
    <li><em>The Digital Personal Data Protection Act, 2023</em>, Act No. 22 of 2023, Ministry of Law and Justice, Government of India, Aug. 2023.</li>
    <li>R. Smith, &ldquo;An overview of the Tesseract OCR engine,&rdquo; in <em>Proc. 9th Int. Conf. Document Anal. Recognit. (ICDAR)</em>, Curitiba, Brazil, Sep. 2007, pp. 629&ndash;633.</li>
    <li>JaidedAI, &ldquo;EasyOCR: Ready-to-use OCR with 80+ supported languages and all popular writing scripts,&rdquo; GitHub repository, 2022. [Online]. Available: https://github.com/JaidedAI/EasyOCR</li>
    <li>N. Otsu, &ldquo;A threshold selection method from gray-level histograms,&rdquo; <em>IEEE Trans. Syst., Man, Cybern.</em>, vol. SMC-9, no. 1, pp. 62&ndash;66, Jan. 1979.</li>
    <li>G. Bradski, &ldquo;The OpenCV library,&rdquo; <em>Dr. Dobb's Journal of Software Tools</em>, vol. 25, no. 11, pp. 120&ndash;125, 2000.</li>
    <li>Explosion AI, &ldquo;spaCy: Industrial-strength natural language processing in Python,&rdquo; 2023. [Online]. Available: https://spacy.io</li>
    <li>M. Bachmann, &ldquo;RapidFuzz: Rapid fuzzy string matching in Python and C++ using Levenshtein distance,&rdquo; GitHub repository, 2023. [Online]. Available: https://github.com/rapidfuzz/RapidFuzz</li>
    <li>W3C & MDN Web Docs, &ldquo;Push API: Providing push notification capabilities to web applications,&rdquo; Mozilla Developer Network, 2023. [Online]. Available: https://developer.mozilla.org/en-US/docs/Web/API/Push_API</li>
    <li>W3C & MDN Web Docs, &ldquo;Web Speech API: Speech recognition and synthesis,&rdquo; Mozilla Developer Network, 2024. [Online]. Available: https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API</li>
    <li>OpenStreetMap Wiki, &ldquo;Overpass API: Read-only API that serves up custom selected parts of the OSM data,&rdquo; 2023. [Online]. Available: https://wiki.openstreetmap.org/wiki/Overpass_API</li>
    <li>V. Agafonkin, &ldquo;Leaflet: An open-source JavaScript library for mobile-friendly interactive maps,&rdquo; 2023. [Online]. Available: https://leafletjs.com</li>
    <li>P. P.-S. Chen, &ldquo;The entity-relationship model&mdash;Toward a unified view of data,&rdquo; <em>ACM Trans. Database Syst.</em>, vol. 1, no. 1, pp. 9&ndash;36, Mar. 1976.</li>
    <li>Pallets Projects, &ldquo;Flask Documentation (3.0.x): A lightweight WSGI web application framework,&rdquo; 2023. [Online]. Available: https://flask.palletsprojects.com</li>
    <li>Google DeepMind, &ldquo;Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context,&rdquo; Google AI Research, 2024. [Online]. Available: https://ai.google.dev</li>
    <li>Tata 1mg Technologies, &ldquo;Tata 1mg: India's leading digital healthcare and pharmacy platform,&rdquo; 2024. [Online]. Available: https://www.1mg.com</li>
  </ol>
</div>

</body>
</html>
"""

html_path = os.path.join(BASE_DIR, 'finalsubmission_report_sem1.html')
pdf_path_1 = os.path.join(BASE_DIR, 'MediAssist_Final_Report_Sem1.pdf')
pdf_path_2 = os.path.join(BASE_DIR, 'finalsubmission report sem1.pdf')
workspace_pdf_1 = os.path.abspath(os.path.join(BASE_DIR, '..', 'MediAssist_Final_Report_Sem1.pdf'))
workspace_pdf_2 = os.path.abspath(os.path.join(BASE_DIR, '..', 'finalsubmission report sem1.pdf'))
downloads_pdf_1 = os.path.abspath(os.path.join(BASE_DIR, '..', '..', 'MediAssist_Final_Report_Sem1.pdf'))
downloads_pdf_2 = os.path.abspath(os.path.join(BASE_DIR, '..', '..', 'finalsubmission report sem1.pdf'))

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Report HTML written to: {html_path} ({os.path.getsize(html_path):,} bytes)")

# Convert to PDF using Edge headless
cmd = [
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    '--headless',
    '--disable-gpu',
    '--run-all-compositor-stages-before-draw',
    f'--print-to-pdf={pdf_path_1}',
    '--no-pdf-header-footer',
    'file:///' + html_path.replace('\\\\', '/')
]

print("Compiling PDF with Microsoft Edge headless...")
res = subprocess.run(cmd, capture_output=True, text=True)
print(f"Edge exit code: {res.returncode}")

if os.path.exists(pdf_path_1):
    size = os.path.getsize(pdf_path_1)
    print(f"Successfully generated PDF: {pdf_path_1} ({size:,} bytes)")
    
    # Copy to all target names and folders so it is immediately accessible anywhere the user looks
    targets = [pdf_path_2, workspace_pdf_1, workspace_pdf_2, downloads_pdf_1, downloads_pdf_2]
    for target in targets:
        shutil.copyfile(pdf_path_1, target)
        print(f"Copied to: {target} ({os.path.getsize(target):,} bytes)")
else:
    print("ERROR: PDF was not generated!")
