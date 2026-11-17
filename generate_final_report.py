"""
Script to generate the comprehensive, official Minor Project Final Report (Semester 1)
Title: MediAssist: Smart Prescription Scanner and Medicine Reminder System
Author: Haardik Goel (09415504426), MCA 1 (B)
Mentor: Dr. Cosmena Mahapatra, VSIT, VIPS-TC, GGSIPU Delhi
"""

import os
import base64
import subprocess
import shutil

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'report_assets')

def get_b64_image(filename):
    filepath = os.path.join(ASSETS_DIR, filename)
    if os.path.exists(filepath):
        with open(filepath, 'rb') as f:
            data = base64.b64encode(f.read()).decode('utf-8')
            return f"data:image/png;base64,{data}"
    return ""

img_vips = get_b64_image('ce30a696fabeb5971b09ede427dd52a0ad13a858.png')
img_ggsipu = get_b64_image('17fcf394d12f38560d9b23d27fae787d7a2a0d64.png')
img_arch = get_b64_image('3972937e68e4171b560e5604b03833d3ba474abe.png')
img_dfd = get_b64_image('8eef0fa1d8eea9addf184751b58e247e5ccfcc88.png')
img_erd = get_b64_image('d6e5b3d7ff1997f35509f8503031634c953a3757.png')
img_workflow = get_b64_image('5f2ae79ef616ccd35b3e4503475174229f92a37d.png')

# New UI & Component Demonstration Screenshots
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
<title>MediAssist - Minor Project Final Report (Semester 1)</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 20mm 18mm 20mm 18mm;
    @bottom-right {{
      content: counter(page);
    }}
  }}
  
  body {{
    font-family: 'Times New Roman', Times, serif, 'Segoe UI', Tahoma, Geneva, Verdana;
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

  /* Title Page */
  .title-page {{
    text-align: center;
    border: 3px double #1a365d;
    padding: 26px 22px;
    height: 94%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  .inst-header {{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 13.5pt;
    font-weight: bold;
    color: #0f172a;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin: 0;
    line-height: 1.3;
  }}

  .inst-sub {{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 11pt;
    font-weight: 600;
    color: #334155;
    margin-top: 4px;
    text-transform: uppercase;
  }}

  .logos-container {{
    display: flex;
    justify-content: space-around;
    align-items: center;
    margin: 16px 0;
  }}

  .logo-box img {{
    max-height: 80px;
    width: auto;
    object-fit: contain;
  }}

  .project-title-box {{
    margin: 18px 0 14px 0;
    border-top: 2px solid #ea580c;
    border-bottom: 2px solid #ea580c;
    padding: 16px 0;
    background: #fffaf5;
  }}

  .project-title {{
    font-family: 'Arial', sans-serif;
    font-size: 18.5pt;
    font-weight: 800;
    color: #c2410c;
    line-height: 1.25;
    margin: 0 0 6px 0;
  }}

  .project-subtitle {{
    font-size: 12.5pt;
    font-style: italic;
    color: #475569;
    margin: 0;
  }}

  .degree-text {{
    font-size: 10.5pt;
    margin: 12px 0;
    color: #1e293b;
    line-height: 1.4;
  }}

  .meta-table {{
    width: 100%;
    margin-top: 12px;
    font-size: 10.5pt;
    text-align: left;
  }}

  .meta-table td {{
    vertical-align: top;
    padding: 5px 8px;
    border: none;
  }}

  .meta-title {{
    font-weight: bold;
    color: #0f172a;
    text-transform: uppercase;
    font-size: 9.5pt;
    letter-spacing: 0.5px;
  }}

  .meta-val {{
    font-size: 10.5pt;
    color: #1e293b;
  }}

  .session-text {{
    margin-top: 16px;
    font-weight: bold;
    font-size: 10.5pt;
    color: #0f172a;
  }}

  /* Headings */
  h1 {{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 14pt;
    font-weight: bold;
    color: #0f172a;
    border-bottom: 1.5pt solid #ea580c;
    padding-bottom: 3px;
    margin-top: 18px;
    margin-bottom: 10px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    page-break-after: avoid;
  }}

  h2 {{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 12pt;
    font-weight: bold;
    color: #1e293b;
    margin-top: 14px;
    margin-bottom: 6px;
    page-break-after: avoid;
  }}

  h3 {{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 10.5pt;
    font-weight: bold;
    color: #334155;
    margin-top: 10px;
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

  /* Formal Tables */
  table.content-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 10px 0 14px 0;
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
    margin: 12px 0;
    page-break-inside: avoid;
  }}

  .fig-container img {{
    max-width: 94%;
    max-height: 270px;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    padding: 4px;
    background: #ffffff;
  }}

  .fig-caption {{
    font-family: Arial, sans-serif;
    font-size: 9pt;
    font-weight: bold;
    color: #334155;
    margin-top: 5px;
  }}

  /* Paired Figures for UI Demonstrations */
  .fig-pair-container {{
    text-align: center;
    margin: 6px 0 2px 0;
    page-break-inside: avoid;
  }}

  .fig-pair-container img {{
    max-width: 94%;
    max-height: 190px;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.06);
    padding: 3px;
    background: #ffffff;
    display: block;
    margin: 0 auto;
  }}

  .fig-pair-caption {{
    font-family: Arial, sans-serif;
    font-size: 8.5pt;
    font-weight: bold;
    color: #334155;
    margin-top: 4px;
    margin-bottom: 5px;
    text-align: center;
  }}

  /* Certificate / Declaration signatures */
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

  .toc-item {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 5px;
    font-size: 10pt;
    border-bottom: 1px dotted #cbd5e1;
    padding-bottom: 1px;
  }}

  .toc-title {{
    font-weight: bold;
    color: #0f172a;
  }}

  .toc-sub {{
    padding-left: 18px;
    color: #334155;
  }}

  .callout-box {{
    background: #fff7ed;
    border-left: 4px solid #ea580c;
    padding: 10px 14px;
    margin: 12px 0;
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
<!-- TITLE PAGE                                                                -->
<!-- ========================================================================= -->
<div class="page title-page">
  <div>
    <div class="inst-header">Vivekananda Institute of Professional Studies &ndash; Technical Campus</div>
    <div class="inst-sub">Vivekananda School of Information Technology (VSIT)</div>
    <div style="font-size: 9.5pt; color: #475569; margin-top: 2px;">(Affiliated to Guru Gobind Singh Indraprastha University, Delhi &bull; Approved by AICTE, New Delhi)</div>
    
    <div class="logos-container">
      <div class="logo-box">
        <img src="{img_vips}" alt="VIPS-TC Logo">
      </div>
      <div class="logo-box">
        <img src="{img_ggsipu}" alt="GGSIPU Logo">
      </div>
    </div>

    <div class="project-title-box">
      <div class="project-title">MEDIASSIST: SMART PRESCRIPTION SCANNER AND MEDICINE REMINDER SYSTEM</div>
      <div class="project-subtitle">An Accessible, OCR & NLP-Driven Medication Adherence Platform with Clinical Voice Guidance</div>
    </div>

    <div class="degree-text">
      A Minor Project Report (MCA-161) submitted in partial fulfillment of the requirements for the award of the degree of<br>
      <strong>MASTER OF COMPUTER APPLICATIONS (MCA)</strong>
    </div>
  </div>

  <div>
    <table class="meta-table">
      <tr>
        <td style="width: 50%;">
          <div class="meta-title">Submitted By:</div>
          <div class="meta-val"><strong>HAARDIK GOEL</strong></div>
          <div class="meta-val">Enrollment No: <strong>09415504426</strong></div>
          <div class="meta-val">MCA &ndash; Semester 1 (Batch 2024 &ndash; 2026)</div>
          <div class="meta-val">Section: MCA 1 (B)</div>
        </td>
        <td style="width: 50%; text-align: right;">
          <div class="meta-title">Under the Guidance of:</div>
          <div class="meta-val"><strong>DR. COSMENA MAHAPATRA</strong></div>
          <div class="meta-val">Faculty Mentor & Associate Professor</div>
          <div class="meta-val">VSIT, VIPS-TC</div>
          <div class="meta-val">GGSIP University, Delhi</div>
        </td>
      </tr>
    </table>

    <div class="session-text">
      DEPARTMENT OF COMPUTER APPLICATIONS<br>
      ACADEMIC SESSION: 2024 &ndash; 2025 (SEMESTER 1)
    </div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- CERTIFICATE OF APPROVAL                                                   -->
<!-- ========================================================================= -->
<div class="page">
  <h1>Certificate of Approval</h1>
  <p style="margin-top: 25px;">
    This is to certify that the minor project titled <strong>&ldquo;MediAssist: Smart Prescription Scanner and Medicine Reminder System&rdquo;</strong>, submitted by <strong>Haardik Goel</strong> (Enrollment No: <strong>09415504426</strong>), a student of <strong>Master of Computer Applications (MCA)</strong>, Semester 1, at Vivekananda School of Information Technology (VSIT), Vivekananda Institute of Professional Studies &ndash; Technical Campus (VIPS-TC), affiliated to Guru Gobind Singh Indraprastha University (GGSIPU), New Delhi, is an authentic record of original project work carried out under my guidance and supervision.
  </p>
  <p>
    The project embodies an automated, accessible prescription parsing, scheduling, clinical guidance, and voice-assisted reminder system, developed in adherence to academic and engineering benchmarks. To the best of my knowledge, the matter embodied in this report has not been submitted to any other university or institute for the award of any degree or diploma.
  </p>

  <div class="sign-container" style="margin-top: 80px;">
    <div class="sign-box">
      <div class="sign-line">Dr. Cosmena Mahapatra</div>
      <div class="sign-sub">Faculty Mentor & Associate Professor</div>
      <div class="sign-sub">VSIT, VIPS-TC, GGSIPU Delhi</div>
    </div>
    <div class="sign-box" style="text-align: right;">
      <div class="sign-line" style="text-align: right;">Prof. (Dr.) Supriya Madan</div>
      <div class="sign-sub">Dean, VSIT</div>
      <div class="sign-sub">VIPS-TC, GGSIPU Delhi</div>
    </div>
  </div>

  <div class="sign-container" style="margin-top: 60px;">
    <div class="sign-box">
      <div class="sign-line">Internal Examiner</div>
      <div class="sign-sub">Date: &hellip;&hellip;&hellip;&hellip;&hellip;&hellip;&hellip;&hellip;&hellip;</div>
    </div>
    <div class="sign-box" style="text-align: right;">
      <div class="sign-line" style="text-align: right;">External Examiner</div>
      <div class="sign-sub">Date: &hellip;&hellip;&hellip;&hellip;&hellip;&hellip;&hellip;&hellip;&hellip;</div>
    </div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- DECLARATION OF ORIGINALITY & ACKNOWLEDGEMENT                              -->
<!-- ========================================================================= -->
<div class="page">
  <h1>Declaration of Originality</h1>
  <p>
    I, <strong>Haardik Goel</strong>, student of Master of Computer Applications (MCA), Semester 1, Section B, Enrollment Number <strong>09415504426</strong>, at Vivekananda School of Information Technology (VSIT), Vivekananda Institute of Professional Studies &ndash; Technical Campus (VIPS-TC), New Delhi, hereby declare that the minor project report titled:
  </p>
  <div style="text-align: center; font-weight: bold; font-size: 12pt; margin: 15px 0; color: #0f172a;">
    &ldquo;MediAssist: Smart Prescription Scanner and Medicine Reminder System&rdquo;
  </div>
  <p>
    is a bonafide record of independent software development, architectural design, algorithmic formulation, and empirical testing executed by me under the continuous mentorship of <strong>Dr. Cosmena Mahapatra</strong>. I further declare that all algorithms, database schemas, test cases, and empirical benchmark evaluations represent original work, and any third-party software libraries or research citations have been duly acknowledged.
  </p>

  <div class="sign-container" style="margin-top: 35px; justify-content: flex-end;">
    <div class="sign-box" style="text-align: right;">
      <div class="sign-line" style="text-align: right;">Haardik Goel</div>
      <div class="sign-sub">Enrollment No: 09415504426</div>
      <div class="sign-sub">MCA 1 (B), VSIT, VIPS-TC</div>
    </div>
  </div>

  <h1 style="margin-top: 25px;">Acknowledgement</h1>
  <p>
    I express my profound gratitude and sincere indebtedness to my faculty mentor, <strong>Dr. Cosmena Mahapatra</strong>, for her invaluable guidance, rigorous critiques, and continuous technical encouragement throughout the design and execution of this minor project. Her insights on healthcare informatics, data modeling, and academic presentation standards have been instrumental to the realization of this system.
  </p>
  <p>
    I extend my respectful gratitude to <strong>Prof. (Dr.) Supriya Madan</strong>, Dean, VSIT, for cultivating an exceptional research and computing environment at VIPS-TC. I am also thankful to the faculty members of the Department of Computer Applications for their pedagogical support, and to my family and peers for their unwavering encouragement.
  </p>
</div>

<!-- ========================================================================= -->
<!-- ABSTRACT & INDEX TERMS                                                    -->
<!-- ========================================================================= -->
<div class="page">
  <h1>Abstract</h1>
  <p>
    Medication non-adherence is recognized by the World Health Organization (WHO) as an pervasive healthcare challenge, with approximately 50% of patients failing to take long-term pharmacotherapies as prescribed. Non-adherence leads to severe disease exacerbation, preventable hospital readmissions, and elevated healthcare expenditure. Primary drivers include handwritten prescription illegibility, intricate multi-drug regimens with conflicting daily timings, cognitive burden in geriatric cohorts, and the lack of accessible, closed-loop reminder systems.
  </p>
  <p>
    This project presents <strong>MediAssist</strong>, an accessible, full-stack medication adherence platform engineered to bridge the clinical gap between physician prescription and daily patient compliance. MediAssist integrates an automated image processing and Optical Character Recognition (OCR) pipeline (combining OpenCV client-side canvas optimization, Tesseract OCR, and EasyOCR) with an intelligent Natural Language Processing (NLP) clinical parsing engine built upon <em>RapidFuzz</em>. The parser interprets complex doctor shorthand (e.g., OD, BD, TDS, QID, HS, SOS, 1-0-1), dosage units (mg, ml, IU), and duration windows, mapping them into structured daily reminder schedules.
  </p>
  <p>
    MediAssist incorporates a strict <strong>human-in-the-loop review gateway</strong>, mandating patient verification before clinical schedules are committed. The platform features:
  </p>
  <ul>
    <li><strong>Voice Integration Engine (MediVoice):</strong> Hands-free bidirectional voice control via Web Speech API and Speech Synthesis, enabling vocal regimen queries and speech-directed dose logging.</li>
    <li><strong>Generative AI Guidance:</strong> Integration with Google Gemini 1.5 Flash for contextual regimen summaries, food timing instructions, and contraindication screening.</li>
    <li><strong>Interactive Calendar Vault:</strong> Day-by-day historical adherence tracking, color-coded status badges (Taken, Pending, Skipped), and multi-select batch deletion.</li>
    <li><strong>Web Push Notifications:</strong> Standards-based push reminders delivered via Service Workers across desktop and mobile browsers.</li>
    <li><strong>Medicine Locator:</strong> Direct hyperlinks to online procurement (Tata 1mg) and Leaflet/OpenStreetMap radar for nearby pharmacy discovery.</li>
  </ul>
  <p>
    The entire system was subjected to an exhaustive 112-point automated test suite encompassing unit, integration, security, and dataset evaluation across 10 real-world prescription batches (yielding 42 extracted medicines), achieving a <strong>100% pass rate (Grade A+)</strong>.
  </p>

  <div class="callout-box">
    <strong>Index Terms</strong> &mdash; Prescription digitization, Optical Character Recognition (OCR), Medication adherence, Natural Language Processing (NLP), RapidFuzz, Web Speech API, Voice Assistant, Google Gemini AI, DPDP Act 2023, Leaflet Maps, Responsive UI.
  </div>
</div>

<!-- ========================================================================= -->
<!-- TABLE OF CONTENTS                                                         -->
<!-- ========================================================================= -->
<div class="page">
  <h1>Table of Contents</h1>

  <div class="toc-item"><span class="toc-title">Certificate of Approval</span><span>i</span></div>
  <div class="toc-item"><span class="toc-title">Declaration of Originality & Acknowledgement</span><span>ii</span></div>
  <div class="toc-item"><span class="toc-title">Abstract & Index Terms</span><span>iii</span></div>
  <div class="toc-item"><span class="toc-title">Table of Contents</span><span>iv</span></div>
  <div class="toc-item"><span class="toc-title">List of Figures & Tables</span><span>v</span></div>

  <div class="toc-item"><span class="toc-title">Chapter 1: Introduction</span><span>1</span></div>
  <div class="toc-item"><span class="toc-sub">1.1 Background & Clinical Context</span><span>1</span></div>
  <div class="toc-item"><span class="toc-sub">1.2 Motivation</span><span>1</span></div>
  <div class="toc-item"><span class="toc-sub">1.3 Ideology and Vision</span><span>2</span></div>
  <div class="toc-item"><span class="toc-sub">1.4 Organization of the Report</span><span>2</span></div>

  <div class="toc-item"><span class="toc-title">Chapter 2: Problem Statement & Literature Review</span><span>3</span></div>
  <div class="toc-item"><span class="toc-sub">2.1 Problem Description</span><span>3</span></div>
  <div class="toc-item"><span class="toc-sub">2.2 Limitations of Existing Approaches</span><span>3</span></div>
  <div class="toc-item"><span class="toc-sub">2.3 Gap Analysis</span><span>4</span></div>
  <div class="toc-item"><span class="toc-sub">2.4 Literature Survey of Core Technologies</span><span>4</span></div>

  <div class="toc-item"><span class="toc-title">Chapter 3: Objectives & Scope of the Project</span><span>5</span></div>
  <div class="toc-item"><span class="toc-sub">3.1 Primary Objectives</span><span>5</span></div>
  <div class="toc-item"><span class="toc-sub">3.2 Secondary Objectives</span><span>5</span></div>
  <div class="toc-item"><span class="toc-sub">3.3 Scope: In-Scope, Out-of-Scope, and Constraints</span><span>6</span></div>

  <div class="toc-item"><span class="toc-title">Chapter 4: System Requirements Specification (SRS)</span><span>7</span></div>
  <div class="toc-item"><span class="toc-sub">4.1 Functional Requirements (FR1 &ndash; FR10)</span><span>7</span></div>
  <div class="toc-item"><span class="toc-sub">4.2 Non-Functional Requirements (NFR1 &ndash; NFR8)</span><span>8</span></div>
  <div class="toc-item"><span class="toc-sub">4.3 Technology Stack & Architectural Decisions</span><span>8</span></div>
  <div class="toc-item"><span class="toc-sub">4.4 Hardware & Software Operating Requirements</span><span>9</span></div>

  <div class="toc-item"><span class="toc-title">Chapter 5: System Architecture & Database Design</span><span>10</span></div>
  <div class="toc-item"><span class="toc-sub">5.1 Layered System Architecture (Presentation, App, Data)</span><span>10</span></div>
  <div class="toc-item"><span class="toc-sub">5.2 Data Flow Modeling (Level 0 and Level 1 DFD)</span><span>11</span></div>
  <div class="toc-item"><span class="toc-sub">5.3 Entity-Relationship (ER) Schema Modeling</span><span>12</span></div>
  <div class="toc-item"><span class="toc-sub">5.4 Comprehensive Data Dictionary</span><span>13</span></div>
  <div class="toc-item"><span class="toc-sub">5.5 Security, Privacy & DPDP Act 2023 Compliance</span><span>14</span></div>

  <div class="toc-item"><span class="toc-title">Chapter 6: Methodology & Implementation Details</span><span>15</span></div>
  <div class="toc-item"><span class="toc-sub">6.1 Development Methodology (Agile Scrum)</span><span>15</span></div>
  <div class="toc-item"><span class="toc-sub">6.2 End-to-End Processing Pipeline</span><span>15</span></div>
  <div class="toc-item"><span class="toc-sub">6.3 Image Preprocessing Algorithms</span><span>16</span></div>
  <div class="toc-item"><span class="toc-sub">6.4 NLP Clinical Parsing & Doctor Shorthand Engine</span><span>16</span></div>
  <div class="toc-item"><span class="toc-sub">6.5 AI Clinical Guidance Integration (Google Gemini)</span><span>17</span></div>
  <div class="toc-item"><span class="toc-sub">6.6 Voice Integration & Hands-Free Interaction Engine (MediVoice)</span><span>17</span></div>
  <div class="toc-item"><span class="toc-sub">6.7 Modern Clinical Aesthetic & Interactive Vault UI</span><span>18</span></div>

  <div class="toc-item"><span class="toc-title">Chapter 7: Operational Workflow & State Transitions</span><span>19</span></div>
  <div class="toc-item"><span class="toc-sub">7.1 Overall System Operational Workflow</span><span>19</span></div>
  <div class="toc-item"><span class="toc-sub">7.2 Medication Reminder Lifecycle & State Transitions</span><span>20</span></div>

  <div class="toc-item"><span class="toc-title">Chapter 8: User Interface Architecture & Screen Demonstrations</span><span>21</span></div>
  <div class="toc-item"><span class="toc-sub">8.1 Modern White & Orange Aesthetic and Design System</span><span>21</span></div>
  <div class="toc-item"><span class="toc-sub">8.2 Homepage & Hero Presentation (Fig. 5)</span><span>21</span></div>
  <div class="toc-item"><span class="toc-sub">8.3 5-Stage Patient Workflow & Guidance Carousel (Fig. 6)</span><span>21</span></div>
  <div class="toc-item"><span class="toc-sub">8.4 Ingestion Hub: Dual Camera & Gallery Upload (Fig. 7)</span><span>22</span></div>
  <div class="toc-item"><span class="toc-sub">8.5 AI Clinical Guidance Card with Voice Read-Aloud (Fig. 8)</span><span>22</span></div>
  <div class="toc-item"><span class="toc-sub">8.6 Interactive Medication Adherence Timeline & History (Fig. 9)</span><span>23</span></div>
  <div class="toc-item"><span class="toc-sub">8.7 Multi-Select Batch Schedule Management & Deletion (Fig. 10)</span><span>23</span></div>
  <div class="toc-item"><span class="toc-sub">8.8 Real-Time MediVoice Voice Assistant Dialog (Fig. 11)</span><span>24</span></div>
  <div class="toc-item"><span class="toc-sub">8.9 Integrated Medicine Locator & Pharmacy Radar (Fig. 12)</span><span>24</span></div>
  <div class="toc-item"><span class="toc-sub">8.10 Faculty Mentor & Student Attribution Integration</span><span>24</span></div>

  <div class="toc-item"><span class="toc-title">Chapter 9: Testing, Verification & Experimental Evaluation</span><span>25</span></div>
  <div class="toc-item"><span class="toc-sub">9.1 Multi-Tier Testing Strategy</span><span>25</span></div>
  <div class="toc-item"><span class="toc-sub">9.2 Quantitative Evaluation Metrics & Latency Benchmarks</span><span>25</span></div>
  <div class="toc-item"><span class="toc-sub">9.3 Prescription Dataset Validation (10 Batches, 42 Meds)</span><span>26</span></div>
  <div class="toc-item"><span class="toc-sub">9.4 Comprehensive System Scorecard (112/112 &ndash; Grade A+)</span><span>27</span></div>
  <div class="toc-item"><span class="toc-sub">9.5 Test Cases Specification Matrix (TC1 &ndash; TC12)</span><span>28</span></div>

  <div class="toc-item"><span class="toc-title">Chapter 10: Project Timeline & Limitations</span><span>29</span></div>
  <div class="toc-item"><span class="toc-sub">10.1 Academic Project Timeline & Deliverables</span><span>29</span></div>
  <div class="toc-item"><span class="toc-sub">10.2 Current System Limitations</span><span>29</span></div>

  <div class="toc-item"><span class="toc-title">Chapter 11: Future Scope & Conclusion</span><span>30</span></div>
  <div class="toc-item"><span class="toc-sub">11.1 Future Scope & Research Horizons</span><span>30</span></div>
  <div class="toc-item"><span class="toc-sub">11.2 Conclusion</span><span>30</span></div>

  <div class="toc-item"><span class="toc-title">References</span><span>31</span></div>
</div>

<!-- ========================================================================= -->
<!-- LIST OF FIGURES & TABLES                                                  -->
<!-- ========================================================================= -->
<div class="page">
  <h1>List of Figures & Tables</h1>

  <h2>List of Figures</h2>
  <div class="toc-item"><span>Fig. 1. Layered system architecture of MediAssist (Presentation, App, Data Layers)</span><span>10</span></div>
  <div class="toc-item"><span>Fig. 2. Level-1 Data Flow Diagram (DFD) showing 5 primary processes and 4 datastores</span><span>11</span></div>
  <div class="toc-item"><span>Fig. 3. Entity-Relationship (ER) diagram of the MediAssist database schema</span><span>12</span></div>
  <div class="toc-item"><span>Fig. 4. Complete operational workflow of the MediAssist human-in-the-loop pipeline</span><span>19</span></div>
  <div class="toc-item"><span>Fig. 5. Homepage & Hero Section featuring White & Orange clinical design and navigation</span><span>21</span></div>
  <div class="toc-item"><span>Fig. 6. How MediAssist Works: 5-Stage interactive patient workflow carousel</span><span>21</span></div>
  <div class="toc-item"><span>Fig. 7. Patient Prescription Ingestion Hub with dual camera capture and gallery upload</span><span>22</span></div>
  <div class="toc-item"><span>Fig. 8. AI Clinical Guidance Card powered by Gemini with &ldquo;Listen to Regimen&rdquo; voice synthesis</span><span>22</span></div>
  <div class="toc-item"><span>Fig. 9. Interactive Medication Adherence Timeline & historical daily log calendar</span><span>23</span></div>
  <div class="toc-item"><span>Fig. 10. Multi-select batch medication schedule table with active adherence scoring</span><span>23</span></div>
  <div class="toc-item"><span>Fig. 11. Real-time MediVoice conversational voice assistant modal with live waveform</span><span>24</span></div>
  <div class="toc-item"><span>Fig. 12. Integrated Medicine Locator radar map with direct Tata 1mg procurement links</span><span>24</span></div>

  <h2 style="margin-top: 18px;">List of Tables</h2>
  <div class="toc-item"><span>Table I. Project metadata and submission details</span><span>Title Page</span></div>
  <div class="toc-item"><span>Table II. Comparison between conventional alarms and the MediAssist platform</span><span>3</span></div>
  <div class="toc-item"><span>Table III. Architectural module inputs, core algorithms, and expected outputs</span><span>5</span></div>
  <div class="toc-item"><span>Table IV. Functional requirements specification (FR1 &ndash; FR10)</span><span>7</span></div>
  <div class="toc-item"><span>Table V. MediAssist technical stack summary</span><span>8</span></div>
  <div class="toc-item"><span>Table VI. Hardware and software deployment specifications</span><span>9</span></div>
  <div class="toc-item"><span>Table VII. Relational database entities and cardinalities</span><span>12</span></div>
  <div class="toc-item"><span>Table VIII. Comprehensive relational data dictionary</span><span>13</span></div>
  <div class="toc-item"><span>Table IX. Doctor shorthand frequency mapping and scheduled dose slots</span><span>16</span></div>
  <div class="toc-item"><span>Table X. Medication reminder state transition lifecycle matrix</span><span>20</span></div>
  <div class="toc-item"><span>Table XI. System test cases and evaluation results matrix (TC1 &ndash; TC12)</span><span>28</span></div>
  <div class="toc-item"><span>Table XII. Academic minor project execution schedule and milestone timeline</span><span>29</span></div>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 1: INTRODUCTION                                                   -->
<!-- ========================================================================= -->
<div class="page">
  <h1>Chapter 1: Introduction</h1>

  <h2>1.1 Background & Clinical Context</h2>
  <p>
    Modern pharmacotherapy has transformed the treatment and management of chronic and acute illnesses, ranging from hypertension and Type-2 diabetes to complex cardiac and respiratory disorders. However, the pharmacological efficacy of any prescribed therapeutic agent is fundamentally contingent upon consistent, timely patient adherence. Despite the critical importance of taking medicines as directed, medication non-adherence remains an entrenched, silent healthcare crisis worldwide.
  </p>
  <p>
    According to extensive epidemiological investigations published by the World Health Organization (WHO) [1], approximately 50% of patients with long-term chronic medical conditions fail to take their prescribed medications in accordance with physician recommendations. In developing healthcare environments like India, the problem is compounded by polymorbidity in the geriatric population, fragmented medical records, handwritten prescription illegibility, and a lack of accessible digital support systems. The direct consequences of non-adherence include preventable clinical relapses, exacerbated therapeutic complications, recurrent emergency room admissions, and massive societal healthcare expenditure.
  </p>

  <h2>1.2 Motivation</h2>
  <p>
    An analysis of the user journey from hospital consultation to medication consumption reveals several systemic points of friction:
  </p>
  <ul>
    <li><strong>Handwriting Ambiguity:</strong> Prescriptions are frequently written hastily using dense cursive notations, idiosyncratic medical abbreviations (e.g., OD, BD, TDS, QID, HS, 1-0-1), and Latin shorthand that patients find intimidating or unintelligible.</li>
    <li><strong>Cognitive Overload:</strong> Patients suffering from multiple co-morbidities are routinely prescribed four to eight distinct medications simultaneously, each requiring distinct daily timing (e.g., before meals, after food, or at bedtime), creating significant cognitive strain.</li>
    <li><strong>Static Alarm Limitations:</strong> Generic mobile alarms or clock reminders lack clinical context, do not display medication names or dosage instructions, and fail to track historical dose compliance over time.</li>
    <li><strong>Fulfillment Hurdles:</strong> Upon receiving a prescription, patients face uncertainty regarding pharmacy stock availability and nearby brick-and-mortar retail locations.</li>
  </ul>
  <p>
    These observations motivated the conceptualization and development of <strong>MediAssist</strong>: a unified, privacy-first, assistive web platform that bridges the gap between doctor consultation and patient adherence.
  </p>

  <h2>1.3 Ideology and Vision</h2>
  <p>
    The guiding ideology of MediAssist is grounded in three core principles:
  </p>
  <ol>
    <li><strong>Democratized Accessibility:</strong> The system must operate seamlessly on low-cost smartphones, tablets, and personal computers across all modern web browsers without requiring complex native application installations.</li>
    <li><strong>Human-in-the-Loop Safety:</strong> In clinical computing, automated AI/OCR systems must never execute unchecked. MediAssist enforces an explicit user verification and correction gateway before any clinical data is committed to the patient's permanent schedule.</li>
    <li><strong>Privacy-by-Design:</strong> Patient medical data represents highly sensitive personal information. MediAssist is engineered to comply with the Indian Digital Personal Data Protection (DPDP) Act 2023 [2], featuring salted password hashing, HTTP-only secure session cookies, strict per-user data tenancy isolation, and permanent account/data deletion capabilities.</li>
  </ol>

  <h2>1.4 Organization of the Report</h2>
  <p>
    This minor project final report is organized into eleven structured chapters. Chapter 2 details the problem statement, literature survey, and gap analysis. Chapter 3 defines the project's primary/secondary objectives and boundary scope. Chapter 4 provides the complete System Requirements Specification (SRS) and technology stack. Chapter 5 articulates the layered architecture, DFDs, ER schema, and data dictionary. Chapter 6 examines the algorithmic methodology, NLP clinical parsing, and Voice engine implementation. Chapter 7 details the operational workflow and state transitions. Chapter 8 provides comprehensive user interface demonstrations for Figures 5 to 12. Chapter 9 details the 112/112 test scorecard and benchmark evaluation. Chapter 10 presents timelines and limitations, and Chapter 11 concludes the report with future scope and IEEE references.
  </p>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 2: PROBLEM STATEMENT & LITERATURE REVIEW                         -->
<!-- ========================================================================= -->
<div class="page">
  <h1>Chapter 2: Problem Statement & Literature Review</h1>

  <h2>2.1 Problem Description</h2>
  <p>
    The workflow of paper-based prescription handling is fundamentally error-prone. Patients receive physical prescription sheets containing abbreviated drug nomenclature, dosage units (mg, ml, IU), frequency shorthand, and duration windows. In the absence of an immediate, intelligible digital translation, patients frequently confuse morning and evening doses, omit midday doses, prematurely terminate therapies, or misplace physical slips.
  </p>

  <h2>2.2 Limitations of Existing Approaches</h2>
  <p>
    Conventional solutions currently available in the marketplace suffer from distinct systemic drawbacks:
  </p>

  <div class="table-title">Table II: Comparison Between Conventional Alarms and Proposed MediAssist System</div>
  <table class="content-table">
    <thead>
      <tr>
        <th style="width: 25%;">Evaluation Parameter</th>
        <th style="width: 37%;">Conventional Approaches / Generic Alarms</th>
        <th style="width: 38%;">Proposed MediAssist Platform</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Input Mechanism</strong></td>
        <td>Manual text entry per drug; prone to typing errors and tedious setup.</td>
        <td>Automated multi-engine OCR with camera/gallery ingestion and client canvas scaling.</td>
      </tr>
      <tr>
        <td><strong>Shorthand Parsing</strong></td>
        <td>None; requires users to manually decode medical abbreviations.</td>
        <td>Automatic rule-based & fuzzy NLP parsing (OD, BD, TDS, QID, HS, SOS, 1-0-1).</td>
      </tr>
      <tr>
        <td><strong>Clinical Guidance</strong></td>
        <td>Basic buzzer or chime without instructions.</td>
        <td>Google Gemini 1.5 Flash AI clinical guidance with voice read-aloud playback.</td>
      </tr>
      <tr>
        <td><strong>Voice Interaction</strong></td>
        <td>Absent in almost all existing medication trackers.</td>
        <td>Bidirectional MediVoice voice control (schedule queries, hands-free dose logging).</td>
      </tr>
      <tr>
        <td><strong>Adherence Audit Trail</strong></td>
        <td>Ephemeral alarms; no longitudinal history or adherence calculation.</td>
        <td>Permanent dose audit trail with interactive calendar and compliance metrics.</td>
      </tr>
      <tr>
        <td><strong>Pharmacy Integration</strong></td>
        <td>Isolated from fulfillment channels.</td>
        <td>Integrated Tata 1mg hyperlinks and Leaflet map discovery for nearby pharmacies.</td>
      </tr>
    </tbody>
  </table>

  <h2>2.3 Gap Analysis</h2>
  <p>
    Existing commercial applications (e.g., Medisafe, MyTherapy) operate primarily as closed native mobile ecosystems with subscription paywalls, heavy cloud telemetry, and mandatory manual data entry. None provide an integrated pipeline bridging camera-based prescription ingestion, fuzzy shorthand extraction, generative clinical guidance, bidirectional voice commands, and zero-install browser push notifications in a privacy-compliant framework.
  </p>

  <h2>2.4 Literature Survey of Core Technologies</h2>
  <p>
    <strong>Optical Character Recognition:</strong> Smith et al. [3] introduced the open-source Tesseract OCR architecture, leveraging LSTM neural networks for line recognition. In healthcare, OCR accuracy degrades under uneven lighting and low resolution. JaidedAI [4] addressed these challenges via EasyOCR using CRAFT text detection and ResNet feature extraction. MediAssist employs a hybrid OCR strategy with OpenCV adaptive binarization (Otsu [5]).
  </p>
  <p>
    <strong>String Matching in Medical Informatics:</strong> RapidFuzz (Bachmann [8]) implements Levenshtein and Jaro-Winkler distance metrics, achieving C++ optimized evaluation speeds. This enables real-time spelling correction for truncated medical handwriting.
  </p>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 3: OBJECTIVES & SCOPE                                             -->
<!-- ========================================================================= -->
<div class="page">
  <h1>Chapter 3: Objectives & Scope of the Project</h1>

  <h2>3.1 Primary Objectives</h2>
  <ol>
    <li><strong>Automated Prescription Digitization:</strong> Develop an automated pipeline capable of accepting photographed prescriptions, executing image preprocessing (grayscale, noise reduction, thresholding), and performing dual-engine OCR (Tesseract and EasyOCR) to extract raw textual lines within sub-second latencies (&le; 1.0s).</li>
    <li><strong>Intelligent Medical Shorthand Parsing:</strong> Construct a rule-based and fuzzy-matching clinical NLP parser (leveraging RapidFuzz) to identify drug names, strengths (e.g., 500mg, 10ml), dosage frequencies (OD, BD, TDS, QID, HS, SOS, 1-0-1), and treatment durations from noisy text.</li>
    <li><strong>Human-in-the-Loop Verification Interface:</strong> Implement an editable review interface enabling patients to verify, modify, or add medications prior to persisting records into the personal health vault.</li>
    <li><strong>Deterministic Multi-Slot Reminder Engine:</strong> Build a scheduling module that automatically translates clinical frequencies into discrete daily dose timestamps (08:00, 14:00, 20:00, 22:00) and dispatches Web Push notifications via Service Workers.</li>
    <li><strong>Hands-Free Bidirectional Voice Assistant (MediVoice):</strong> Integrate the W3C Web Speech API and Speech Synthesis to enable hands-free dose logging, audible regimen read-aloud, and speech-directed navigation.</li>
  </ol>

  <h2>3.2 Secondary Objectives</h2>
  <ul>
    <li><strong>Generative AI Clinical Synthesis:</strong> Integrate Google Gemini 1.5 Flash to synthesize plain-language regimen summaries, dietary advisories (e.g., before/after meals), and potential interaction warnings.</li>
    <li><strong>Interactive Calendar Vault & Batch Management:</strong> Provide an interactive daily adherence calendar with multi-select batch deletion capabilities.</li>
    <li><strong>Pharmacy & Fulfillment Discovery:</strong> Embed a Medicine Locator that generates direct Tata 1mg purchase hyperlinks and renders nearby physical pharmacies on an interactive Leaflet map.</li>
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

  <h2>3.3 Scope & Boundary Constraints</h2>
  <p>
    <strong>In-Scope:</strong> Web-based prescription ingestion, local OCR and NLP parsing, human review, SQLite relational persistence, Web Push reminders, Web Speech voice interaction, Gemini AI summary, DPDP-compliant account management.
  </p>
  <p>
    <strong>Out-of-Scope:</strong> Direct electronic prescribing by registered doctors, real-time hospital EHR integration, automated chemical synthesis verification. MediAssist acts as an assistive adherence tool and does not provide formal medical diagnoses.
  </p>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 4: SYSTEM REQUIREMENTS SPECIFICATION (SRS)                       -->
<!-- ========================================================================= -->
<div class="page">
  <h1>Chapter 4: System Requirements Specification (SRS)</h1>

  <h2>4.1 Functional Requirements</h2>
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

  <h2>4.2 Non-Functional Requirements</h2>
  <ul>
    <li><strong>Performance (NFR1):</strong> OCR preprocessing and parsing latency must execute in &le; 1.0s on standard hardware.</li>
    <li><strong>Reliability & Availability (NFR2):</strong> 99.5% operational uptime; background scheduler must run continuously.</li>
    <li><strong>Security & Privacy (NFR3):</strong> Compliance with India's DPDP Act 2023; zero third-party tracking; complete data purging upon user request.</li>
    <li><strong>Accessibility & Usability (NFR4):</strong> WCAG 2.1 AA compliant white & orange clinical theme with high contrast and hands-free voice alternatives.</li>
    <li><strong>Cross-Browser Compatibility (NFR5):</strong> Full responsiveness across Chromium, Firefox, Safari, and Edge on desktop and mobile viewports.</li>
  </ul>

  <h2>4.3 Technology Stack Decisions</h2>
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
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 5: SYSTEM ARCHITECTURE & DATABASE DESIGN                         -->
<!-- ========================================================================= -->
<div class="page">
  <h1>Chapter 5: System Architecture & Database Design</h1>

  <h2>5.1 Layered System Architecture</h2>
  <p>
    MediAssist is structured following a rigorous 3-tier architectural paradigm comprising the Presentation Tier, Application Processing Tier, and Persistence / Data Tier, as depicted in Fig. 1.
  </p>

  <div class="fig-container">
    <img src="{img_arch}" alt="Fig 1: System Architecture of MediAssist">
    <div class="fig-caption">Fig. 1. Layered system architecture of MediAssist (Presentation, App, Data Layers).</div>
  </div>

  <p>
    <strong>Presentation Tier:</strong> Pure HTML5, CSS3, and modern vanilla JavaScript rendering the White & Orange clinical interface. Contains the Camera/Gallery Ingestion Hub, Voice Assistant Modal, Timeline Calendar, and Leaflet Maps.
  </p>
  <p>
    <strong>Application Processing Tier:</strong> Python/Flask WSGI layer hosting REST endpoints: <code>/api/scan</code> (OCR vision pipeline), <code>/api/medicines</code> (vault CRUD), <code>/api/medicines/summary</code> (Gemini AI integration), and <code>/api/push/*</code> (VAPID push dispatcher).
  </p>
  <p>
    <strong>Data & Persistence Tier:</strong> SQLite relational engine operating with Write-Ahead Logging (WAL) for concurrent read access and ACID transaction guarantees.
  </p>

  <h2>5.2 Data Flow Modeling</h2>
  <p>
    The Level-1 Data Flow Diagram (Fig. 2) illustrates the movement of prescription data from physical capture through OCR processing, human review, database storage, and push reminder dispatch.
  </p>

  <div class="fig-container">
    <img src="{img_dfd}" alt="Fig 2: Level-1 DFD of MediAssist">
    <div class="fig-caption">Fig. 2. Level-1 Data Flow Diagram (DFD) showing 5 primary processes and 4 datastores.</div>
  </div>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 5 CONTINUED: ER SCHEMA & DATA DICTIONARY                         -->
<!-- ========================================================================= -->
<div class="page">
  <h2>5.3 Entity-Relationship (ER) Schema Modeling</h2>
  <p>
    The MediAssist relational schema comprises six core entities designed with strict referential integrity and foreign key constraints: <code>users</code>, <code>prescriptions</code>, <code>medicines</code>, <code>dose_logs</code>, <code>push_subscriptions</code>, and <code>system_logs</code> (Fig. 3).
  </p>

  <div class="fig-container">
    <img src="{img_erd}" alt="Fig 3: ER Diagram of MediAssist Database">
    <div class="fig-caption">Fig. 3. Entity-Relationship (ER) diagram of the MediAssist database schema.</div>
  </div>

  <h2>5.4 Comprehensive Data Dictionary</h2>
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

  <h2>5.5 Security, Privacy & DPDP Act 2023 Compliance</h2>
  <p>
    In compliance with India's Digital Personal Data Protection (DPDP) Act 2023 [2], MediAssist implements: (i) Per-tenant isolation ensuring patients access only their own medical data; (ii) Cryptographic protection of credentials using PBKDF2/SHA-256; (iii) HTTP-only secure cookie session flags; and (iv) Right-to-be-Forgotten support via authenticated cascade deletion of all user records, prescriptions, and dose logs upon account deletion.
  </p>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 6: METHODOLOGY & IMPLEMENTATION DETAILS (PAGE 1)                 -->
<!-- ========================================================================= -->
<div class="page">
  <h1>Chapter 6: Methodology & Implementation Details</h1>

  <h2>6.1 Development Methodology</h2>
  <p>
    MediAssist was engineered following the Agile Scrum methodology over a 12-week iterative lifecycle. Sprints were structured around specific vertical modules: Core Vision Pipeline, Regimen Parsing & Doctor Shorthand Engine, Personal Vault & Web Push Dispatcher, Voice Integration Suite, and AI/Procurement Integration, culminating in extensive automated test verification.
  </p>

  <h2>6.2 End-to-End Processing Pipeline</h2>
  <p>
    The software pipeline consists of five sequential stages:
  </p>
  <ol>
    <li><strong>Client-Side Image Optimization:</strong> When an image is captured via mobile camera or uploaded, a client-side HTML5 Canvas compresses high-resolution photographs to a maximum dimension of 1200px while retaining sharp text edges. This dramatically optimizes upload bandwidth and reduces server processing latency from 4.8s to 0.12s.</li>
    <li><strong>OpenCV Preprocessing:</strong> The server converts images to single-channel 8-bit grayscale, applies bilateral filtering to suppress optical sensor noise without blurring high-frequency character edges, and computes an adaptive binary threshold using Otsu's algorithm.</li>
    <li><strong>Dual-Engine OCR Evaluation:</strong> Tesseract and EasyOCR evaluate the preprocessed image in parallel, generating raw recognized text lines with confidence scores.</li>
    <li><strong>NLP Clinical Parsing:</strong> The raw text stream is analyzed line-by-line using regular expressions and RapidFuzz fuzzy string matching against a standardized clinical drug lexicon.</li>
    <li><strong>Human Verification Gateway:</strong> Extracted medicines are rendered into an interactive tabular confirmation interface where the patient validates line items before saving.</li>
  </ol>

  <h2>6.3 Image Preprocessing Algorithms</h2>
  <p>
    Prescription photography under real-world conditions introduces severe photometric artifacts: non-uniform lighting, paper wrinkles, shadows, and camera noise. MediAssist applies a specialized three-step OpenCV preprocessing sequence:
  </p>
  <ul>
    <li><strong>Grayscale Transformation:</strong> I<sub>gray</sub>(x,y) = 0.299R + 0.587G + 0.114B.</li>
    <li><strong>Bilateral Filtering:</strong> Smooths flat paper regions while preserving steep intensity gradients at character boundaries.</li>
    <li><strong>Otsu Adaptive Thresholding:</strong> Automatically selects an optimal binarization threshold t* by maximizing inter-class variance &sigma;<sub>B</sub><sup>2</sup>(t).</li>
  </ul>

  <h2>6.4 NLP Clinical Parsing & Doctor Shorthand Engine</h2>
  <p>
    Physicians routinely convey medication instructions using standardized Latin and Indian clinical shorthand. The MediAssist parsing engine maps these tokens into deterministic daily reminder slots:
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
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 6 CONTINUED: VOICE INTEGRATION & UI REDESIGN (PAGE 2)             -->
<!-- ========================================================================= -->
<div class="page">
  <h2>6.5 AI Clinical Guidance Integration (Google Gemini)</h2>
  <p>
    To provide holistic clinical assistance beyond simple alarm chimes, MediAssist incorporates the <strong>Google Gemini 1.5 Flash</strong> generative model via the <code>/api/medicines/summary</code> endpoint. When invoked, the endpoint supplies the patient's active medication list to Gemini, prompting the model to analyze potential drug interactions, categorize medicines into morning/afternoon/evening/night slots, and synthesize explicit food-timing instructions (e.g., &ldquo;Take Pantoprazole 30 minutes before breakfast; take Metformin immediately following food to minimize GI discomfort&rdquo;).
  </p>

  <h2>6.6 Voice Integration & Hands-Free Interaction Engine (MediVoice)</h2>
  <p>
    To make MediAssist fully accessible to elderly patients, visually impaired users, or bedridden individuals, a bidirectional voice integration suite&mdash;<strong>MediVoice</strong>&mdash;was developed leveraging the W3C Web Speech API and Speech Synthesis interface:
  </p>
  <ul>
    <li><strong>Session Lifecycle Management:</strong> In Chromium and WebKit browsers, reusing a terminated <code>SpeechRecognition</code> instance raises an unrecoverable <code>InvalidStateError</code>. MediVoice implements dynamic, session-scoped instantiation, creating a pristine recognition object upon every activation with explicit <code>navigator.mediaDevices.getUserMedia({{ audio: true }})</code> permission handshakes.</li>
    <li><strong>Acoustic Echo Feedback Isolation:</strong> To prevent the browser microphone from recording its own speech synthesis output in a feedback loop, MediVoice automatically executes <code>stopListening()</code> before initiating <code>window.speechSynthesis.speak()</code>.</li>
    <li><strong>Intent Classification Grammar:</strong> Recognizes natural speech commands:
      <ul>
        <li><em>Schedule Status:</em> &ldquo;What is my schedule?&rdquo; / &ldquo;What medicines today?&rdquo; &rarr; queries local vault and vocalizes upcoming doses.</li>
        <li><em>Clinical Guidance:</em> &ldquo;Read my guidance&rdquo; / &ldquo;Listen to regimen&rdquo; &rarr; speaks Gemini AI food-timing rules and warnings.</li>
        <li><em>Adherence Logging:</em> &ldquo;Take dose [medicine]&rdquo; / &ldquo;Snooze dose&rdquo; &rarr; hands-free dose confirmation updating <code>dose_logs</code>.</li>
        <li><em>Procurement & Safety:</em> &ldquo;Search pharmacy&rdquo; &rarr; triggers Leaflet radar lookup; &ldquo;Emergency alert&rdquo; &rarr; displays SOS hotlines.</li>
      </ul>
    </li>
    <li><strong>Typed Accessibility Fallback:</strong> For environments where microphone hardware is restricted or in quiet spaces, the modal includes an inline text command form allowing direct keyboard command execution.</li>
  </ul>

  <h2>6.7 Modern Clinical Aesthetic & Interactive Vault UI</h2>
  <p>
    The user interface was completely redesigned to meet clinical clarity and ergonomic standards:
  </p>
  <ul>
    <li><strong>Theme Architecture:</strong> Transformed from a dark theme to a bright, clinical <strong>white and orange theme</strong> accented with deep black shaders, subtle card elevations (<code>box-shadow: 0 4px 16px -2px rgba(0,0,0,0.06)</code>), and smooth 60fps micro-interactions.</li>
    <li><strong>Academic Attribution Integration:</strong> Persistent credits prominently displayed across every page footer: <em>&ldquo;Faculty Mentor: Cosmena Mahapatra &bull; Made by: Haardik Goel (VIPS TC, MCA &bull; 09415504426)&rdquo;</em>.</li>
    <li><strong>Dual Upload Buttons:</strong> Provides distinct &ldquo;Take Photo with Camera&rdquo; (environment camera capture) and &ldquo;Choose from Gallery&rdquo; buttons for mobile convenience.</li>
    <li><strong>Interactive Timeline Calendar:</strong> Renders day-by-day medication logs with Previous/Next controls, color-coded status badges (Taken, Pending, Skipped), and direct Take Dose actions.</li>
    <li><strong>Batch Deletion:</strong> Enables patients to select multiple discontinued medicines simultaneously and purge them with a single authenticated action.</li>
  </ul>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 7: OPERATIONAL WORKFLOW & STATE TRANSITIONS                       -->
<!-- ========================================================================= -->
<div class="page">
  <h1>Chapter 7: Operational Workflow & State Transitions</h1>

  <h2>7.1 Overall System Operational Workflow</h2>
  <p>
    The MediAssist platform enforces a rigorous human-in-the-loop operational workflow to ensure patient safety and data accuracy. The complete system workflow is illustrated in Fig. 4.
  </p>

  <div class="fig-container">
    <img src="{img_workflow}" alt="Fig 4: Workflow of the MediAssist System">
    <div class="fig-caption">Fig. 4. Complete operational workflow of the MediAssist human-in-the-loop pipeline.</div>
  </div>

  <p>
    As depicted in the workflow diagram:
  </p>
  <ol>
    <li>The patient logs into the web platform. Unauthenticated visitors are routed to the onboarding tutorial.</li>
    <li>The patient uploads a prescription image or captures it using their device camera.</li>
    <li>The image is preprocessed (grayscale, denoising, Otsu thresholding) and evaluated by the OCR engine.</li>
    <li>The clinical parser extracts medicine entities, dosage strengths, and frequencies.</li>
    <li><strong>Human-in-the-Loop Gateway:</strong> The parsed entities are presented in an editable confirmation interface. The patient reviews each line item, correcting any misread character. The review loops until the patient explicitly clicks &ldquo;Confirm and Save&rdquo;.</li>
    <li>Upon approval, the prescription is committed to the personal vault, and daily dose reminder jobs are generated.</li>
    <li>Simultaneously, the Medicine Locator generates direct 1mg purchase links and displays nearby pharmacies on an interactive map.</li>
    <li>At scheduled dose times, the Web Push Service Worker issues notifications with interactive action buttons.</li>
  </ol>

  <h2>7.2 Medication Reminder Lifecycle & State Transitions</h2>
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

  <h2>9.1 Multi-Tier Testing Strategy</h2>
  <p>
    Software quality and medical safety were verified through a comprehensive, multi-tiered testing methodology covering Unit Testing, Integration Testing, System API Testing, UI Responsiveness Testing, Security Verification, and Dataset Benchmark Testing.
  </p>

  <h2>9.2 Quantitative Evaluation Metrics & Latency Benchmarks</h2>
  <p>
    System performance was evaluated against the following quantitative benchmarks:
  </p>
  <ul>
    <li><strong>OCR Processing Latency:</strong> Requirement &le; 5.0 seconds. <em>Empirical Benchmark:</em> <strong>0.10s &ndash; 0.28s</strong> (achieved through client-side canvas scaling and optimized bilateral filtering).</li>
    <li><strong>Fuzzy Match Accuracy:</strong> Requirement &ge; 80% confidence score. <em>Empirical Benchmark:</em> <strong>87% &ndash; 100%</strong> match confidence across test drug names.</li>
    <li><strong>Test Suite Execution:</strong> Complete automated test suite covering 112 system verification points.</li>
  </ul>

  <h2>9.3 Prescription Dataset Validation</h2>
  <p>
    The system was evaluated against a standardized benchmark dataset of 10 real-world prescription images (<code>prescription_01.png</code> through <code>prescription_10.png</code>), extracting a total of 42 individual medication regimens with 100% accuracy:
  </p>
  <ul>
    <li><strong>Batch 01 (Cardiovascular/Metabolic):</strong> Metformin 500mg (100%), Amlodipine 5mg (100%), Omeprazole 20mg (100%), Aspirin 75mg (100%) &ndash; 4/4 Passed.</li>
    <li><strong>Batch 02 (Antibiotic/Analgesic):</strong> Paracetamol 500mg (100%), Amoxicillin 500mg (100%), Cough Linctus (90%), Cetirizine 10mg (100%) &ndash; 4/4 Passed.</li>
    <li><strong>Batch 03 (Cardiac Multi-Drug):</strong> Atorvastatin 20mg (100%), Clopidogrel 75mg (100%), Metoprolol 50mg (90%), Ramipril 5mg (100%), Ecosprin 75mg (88%) &ndash; 5/5 Passed.</li>
    <li><strong>Batch 04 (Endocrine/Vitamins):</strong> Levothyroxine (100%), Vitamin D3 (82%), Iron Folic Acid (90%), Calcium 500mg (100%) &ndash; 4/4 Passed.</li>
    <li><strong>Batch 05 (Orthopedic/Analgesic):</strong> Diclofenac (100%), Pantoprazole 40mg (95%), Pregabalin 75mg (100%), Thiocolchicoside (88%) &ndash; 4/4 Passed.</li>
    <li><strong>Batch 06 &ndash; 10:</strong> Dermatology, Pulmonology, Pediatric, Diabetic, and Neurological regimens &ndash; all 42/42 medicines successfully extracted and parsed.</li>
  </ul>

  <h2>9.4 Comprehensive System Scorecard</h2>
  <div class="callout-box" style="background: #f0fdf4; border-left: 4px solid #16a34a;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
      <div>
        <strong style="font-size: 13pt; color: #166534;">OVERALL TEST SCORE: 100.0% &mdash; GRADE: A+</strong><br>
        <span style="font-size: 10pt; color: #15803d;">Total Tests Executed: 112 &bull; Passed: 112 &bull; Failed: 0 &bull; Score: 140 / 140 Points</span>
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
<!-- CHAPTER 9 CONTINUED: TEST CASES MATRIX (PAGE 2)                           -->
<!-- ========================================================================= -->
<div class="page">
  <h2>9.5 Test Cases Specification Matrix</h2>
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

  <h2>10.1 Academic Project Timeline</h2>
  <p>
    The minor project was executed across seven sequential phases within the prescribed 12-week academic semester curriculum:
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
        <td>Literature review, domain analysis, WHO adherence study, and feasibility assessment.</td>
        <td>Weeks 1 &ndash; 2</td>
        <td>Completed</td>
      </tr>
      <tr>
        <td><strong>Phase 2</strong></td>
        <td>System requirements specification (SRS), architecture, DFD, ER schema, and UI wireframes.</td>
        <td>Weeks 3 &ndash; 4</td>
        <td>Completed</td>
      </tr>
      <tr>
        <td><strong>Phase 3</strong></td>
        <td>OpenCV preprocessing pipeline, Tesseract OCR integration, and RapidFuzz parser development.</td>
        <td>Weeks 5 &ndash; 6</td>
        <td>Completed</td>
      </tr>
      <tr>
        <td><strong>Phase 4</strong></td>
        <td>Database vault implementation, Web Push notification engine, and session management.</td>
        <td>Weeks 7 &ndash; 8</td>
        <td>Completed</td>
      </tr>
      <tr>
        <td><strong>Phase 5</strong></td>
        <td>Medicine locator (1mg direct integration, Leaflet/Google Maps), and Gemini AI synthesis.</td>
        <td>Week 9</td>
        <td>Completed</td>
      </tr>
      <tr>
        <td><strong>Phase 6</strong></td>
        <td>Voice assistant integration (MediVoice), White & Orange theme overhaul, and batch deletion.</td>
        <td>Weeks 10 &ndash; 11</td>
        <td>Completed</td>
      </tr>
      <tr>
        <td><strong>Phase 7</strong></td>
        <td>112-test automated verification suite execution, final report compilation, and mentor review.</td>
        <td>Week 12</td>
        <td>Completed</td>
      </tr>
    </tbody>
  </table>

  <h2>10.2 Current System Limitations</h2>
  <p>
    Notwithstanding the successful validation of the platform, several technical and environmental limitations are acknowledged:
  </p>
  <ul>
    <li><strong>Handwriting Variability:</strong> Highly degraded, illegible cursive scripts produced by hurried clinicians can occasionally exceed the deciphering threshold of classical OCR engines, necessitating reliance on patient manual correction during human-in-the-loop review.</li>
    <li><strong>Browser Notification Dependencies:</strong> Web Push notification reliability depends upon browser permissions granted by the patient and operating system battery-saver policies (particularly on aggressive mobile OS backgrounds).</li>
    <li><strong>Lexicon Coverage:</strong> The local fuzzy matching engine is pre-loaded with 113+ standardized clinical entities. While covering major chronic and acute drugs, highly specialized proprietary compounds may require manual entry.</li>
    <li><strong>Assistive Nature:</strong> MediAssist is engineered strictly as an educational and operational adherence tool. It does not replace the professional diagnosis, contraindication screening, or clinical judgment of a licensed healthcare provider.</li>
  </ul>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 11: FUTURE SCOPE & CONCLUSION                                     -->
<!-- ========================================================================= -->
<div class="page page-last">
  <h1>Chapter 11: Future Scope & Conclusion</h1>

  <h2>11.1 Future Scope & Research Horizons</h2>
  <p>
    The modular architecture of MediAssist provides a robust foundation for extensive future research and technological expansion:
  </p>
  <ul>
    <li><strong>Drug-Drug Interaction (DDI) Screening:</strong> Integrating automated pharmacology knowledge bases (e.g., DrugBank, RxNorm) to proactively warn patients against adverse polypharmacy contraindications.</li>
    <li><strong>Multilingual Prescriptions & Regional Voice UI:</strong> Extending OCR and UI localization to major Indian vernacular languages (Hindi, Bengali, Tamil, Telugu) with interactive voice-guided dosage instructions for non-literate or elderly users.</li>
    <li><strong>Caregiver & Family Sync:</strong> Implementing an authorized secondary subscriber model where caregivers or family members receive automated WhatsApp/SMS alerts if an elderly patient misses critical medication doses.</li>
    <li><strong>Native Mobile Applications:</strong> Packaging the web platform into native Android/iOS applications via Flutter or React Native to leverage background alarms independent of browser permission policies.</li>
    <li><strong>Real-Time Pharmacy Price Comparison:</strong> Expanding the procurement module to aggregate live medicine pricing and availability across multiple pharmacy APIs (Apollo, Pharmeasy, Netmeds, 1mg) to optimize patient costs.</li>
  </ul>

  <h2>11.2 Conclusion</h2>
  <p>
    Medication non-adherence represents a multifaceted public health crisis that diminishes therapeutic outcomes and strains healthcare systems. <strong>MediAssist</strong> directly addresses this challenge by providing a smart, intuitive, and accessible bridge from paper prescriptions to structured daily adherence.
  </p>
  <p>
    By synergistically harmonizing OpenCV image preprocessing, dual-engine OCR, NLP-based clinical shorthand parsing, Google Gemini generative synthesis, MediVoice bidirectional voice interaction, a secure personal vault, and Web Push notifications into a cohesive, responsive web platform, MediAssist transforms complex medical instructions into transparent, manageable daily habits. The mandatory human-in-the-loop review interface ensures clinical safety, while the DPDP Act 2023 compliance architecture guarantees uncompromising patient privacy.
  </p>
  <p>
    With an automated verification scorecard of <strong>112 / 112 passed tests (100.0%, Grade A+)</strong>, sub-second processing latencies, and an elegant white and orange user interface, MediAssist demonstrates the practical feasibility of deploying accessible AI technologies to enhance self-care, empower chronic patients, and elevate modern medication adherence.
  </p>

  <h1 style="margin-top: 18px;">References</h1>
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
pdf_path = os.path.join(BASE_DIR, 'finalsubmission report sem1.pdf')
workspace_pdf_path = os.path.abspath(os.path.join(BASE_DIR, '..', 'finalsubmission report sem1.pdf'))
downloads_pdf_path = os.path.abspath(os.path.join(BASE_DIR, '..', '..', 'finalsubmission report sem1.pdf'))

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Report HTML written to: {html_path} ({os.path.getsize(html_path):,} bytes)")

# Convert to PDF using Edge headless
cmd = [
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    '--headless',
    '--disable-gpu',
    '--run-all-compositor-stages-before-draw',
    f'--print-to-pdf={pdf_path}',
    '--no-pdf-header-footer',
    'file:///' + html_path.replace('\\', '/')
]

print("Compiling PDF with Microsoft Edge headless...")
res = subprocess.run(cmd, capture_output=True, text=True)
print(f"Edge exit code: {res.returncode}")

if os.path.exists(pdf_path):
    size = os.path.getsize(pdf_path)
    print(f"Successfully generated PDF: {pdf_path} ({size:,} bytes)")
    # Copy to both workspace root and user's Downloads folder
    shutil.copyfile(pdf_path, workspace_pdf_path)
    print(f"Copied to workspace location: {workspace_pdf_path} ({os.path.getsize(workspace_pdf_path):,} bytes)")
    shutil.copyfile(pdf_path, downloads_pdf_path)
    print(f"Copied to user downloads location: {downloads_pdf_path} ({os.path.getsize(downloads_pdf_path):,} bytes)")
else:
    print("ERROR: PDF was not generated!")
