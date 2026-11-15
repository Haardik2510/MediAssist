"""
Script to generate the comprehensive, official Minor Project Final Report (Semester 1)
Title: MediAssist: Smart Prescription Scanner and Medicine Reminder System
Author: Haardik Goel (09417704426), MCA 1 (B)
Mentor: Dr. Cosmina, VSIT, VIPS-TC, GGSIPU Delhi
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

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>MediAssist - Minor Project Final Report (Semester 1)</title>
<style>
  @page {{
    size: A4 portrait;
    margin: 22mm 20mm 22mm 20mm;
    @bottom-right {{
      content: counter(page);
    }}
  }}
  
  body {{
    font-family: 'Times New Roman', Times, serif, 'Segoe UI', Tahoma, Geneva, Verdana;
    font-size: 11.5pt;
    line-height: 1.55;
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
    padding: 30px 24px;
    height: 94%;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }}

  .inst-header {{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 14pt;
    font-weight: bold;
    color: #0f172a;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    margin: 0;
    line-height: 1.3;
  }}

  .inst-sub {{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 11.5pt;
    font-weight: 600;
    color: #334155;
    margin-top: 4px;
    text-transform: uppercase;
  }}

  .logos-container {{
    display: flex;
    justify-content: space-around;
    align-items: center;
    margin: 18px 0;
  }}

  .logo-box img {{
    max-height: 85px;
    width: auto;
    object-fit: contain;
  }}

  .project-title-box {{
    margin: 22px 0 16px 0;
    border-top: 2px solid #ea580c;
    border-bottom: 2px solid #ea580c;
    padding: 18px 0;
    background: #fffaf5;
  }}

  .project-title {{
    font-family: 'Arial', sans-serif;
    font-size: 19pt;
    font-weight: 800;
    color: #c2410c;
    line-height: 1.25;
    margin: 0 0 6px 0;
  }}

  .project-subtitle {{
    font-size: 13pt;
    font-style: italic;
    color: #475569;
    margin: 0;
  }}

  .degree-text {{
    font-size: 11pt;
    margin: 14px 0;
    color: #1e293b;
    line-height: 1.4;
  }}

  .meta-table {{
    width: 100%;
    margin-top: 15px;
    font-size: 11pt;
    text-align: left;
  }}

  .meta-table td {{
    vertical-align: top;
    padding: 6px 10px;
    border: none;
  }}

  .meta-title {{
    font-weight: bold;
    color: #0f172a;
    text-transform: uppercase;
    font-size: 10pt;
    letter-spacing: 0.5px;
  }}

  .meta-val {{
    font-size: 11pt;
    color: #1e293b;
  }}

  .session-text {{
    margin-top: 20px;
    font-weight: bold;
    font-size: 11pt;
    color: #0f172a;
  }}

  /* Headings */
  h1 {{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 14.5pt;
    font-weight: bold;
    color: #0f172a;
    border-bottom: 1.5pt solid #ea580c;
    padding-bottom: 4px;
    margin-top: 24px;
    margin-bottom: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    page-break-after: avoid;
  }}

  h2 {{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 12.5pt;
    font-weight: bold;
    color: #1e293b;
    margin-top: 18px;
    margin-bottom: 8px;
    page-break-after: avoid;
  }}

  h3 {{
    font-family: Arial, Helvetica, sans-serif;
    font-size: 11pt;
    font-weight: bold;
    color: #334155;
    margin-top: 12px;
    margin-bottom: 6px;
    page-break-after: avoid;
  }}

  p {{
    margin-top: 0;
    margin-bottom: 10px;
    text-indent: 0;
  }}

  ul, ol {{
    margin-top: 0;
    margin-bottom: 12px;
    padding-left: 24px;
  }}

  li {{
    margin-bottom: 4px;
  }}

  /* Formal Tables */
  table.content-table {{
    width: 100%;
    border-collapse: collapse;
    margin: 14px 0 16px 0;
    font-size: 9.5pt;
    page-break-inside: avoid;
  }}

  table.content-table th {{
    background-color: #f1f5f9;
    color: #0f172a;
    font-weight: bold;
    border: 1px solid #94a3b8;
    padding: 6px 8px;
    text-align: left;
  }}

  table.content-table td {{
    border: 1px solid #cbd5e1;
    padding: 6px 8px;
    vertical-align: top;
  }}

  table.content-table tr:nth-child(even) {{
    background-color: #f8fafc;
  }}

  .table-title {{
    font-family: Arial, sans-serif;
    font-size: 9.5pt;
    font-weight: bold;
    margin-bottom: 4px;
    text-align: center;
    color: #334155;
    text-transform: uppercase;
  }}

  /* Figures */
  .fig-container {{
    text-align: center;
    margin: 16px 0;
    page-break-inside: avoid;
  }}

  .fig-container img {{
    max-width: 94%;
    max-height: 290px;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    padding: 4px;
    background: #ffffff;
  }}

  .fig-caption {{
    font-family: Arial, sans-serif;
    font-size: 9.5pt;
    font-weight: bold;
    color: #334155;
    margin-top: 6px;
  }}

  /* Certificate / Declaration signatures */
  .sign-container {{
    margin-top: 40px;
    display: flex;
    justify-content: space-between;
    page-break-inside: avoid;
  }}

  .sign-box {{
    width: 44%;
    text-align: left;
  }}

  .sign-line {{
    border-top: 1px solid #0f172a;
    margin-top: 45px;
    padding-top: 4px;
  }}

  .callout-box {{
    background: #fff7ed;
    border-left: 4px solid #ea580c;
    padding: 10px 14px;
    margin: 14px 0;
    font-size: 10pt;
    border-radius: 0 4px 4px 0;
  }}

  .score-badge {{
    display: inline-block;
    background: #16a34a;
    color: #ffffff;
    font-weight: bold;
    padding: 3px 10px;
    border-radius: 4px;
    font-size: 10pt;
  }}

  .toc-item {{
    display: flex;
    justify-content: space-between;
    margin-bottom: 6px;
    border-bottom: 1px dotted #cbd5e1;
    padding-bottom: 2px;
  }}
  .toc-title {{ font-weight: bold; }}
  .toc-sub {{ padding-left: 20px; font-weight: normal; }}

  .code-snippet {{
    font-family: 'Courier New', Courier, monospace;
    font-size: 8.5pt;
    background: #f1f5f9;
    border: 1px solid #cbd5e1;
    padding: 8px 12px;
    border-radius: 4px;
    line-height: 1.4;
    overflow-x: auto;
    margin: 8px 0;
  }}
</style>
</head>
<body>

<!-- ========================================================================= -->
<!-- TITLE PAGE                                                                -->
<!-- ========================================================================= -->
<div class="page title-page">
  <div>
    <div class="inst-header">Vivekananda Institute of Professional Studies - TC</div>
    <div class="inst-sub">Vivekananda School of Information Technology</div>
    <div style="font-size: 10pt; color: #475569; margin-top: 3px;">Affiliated to Guru Gobind Singh Indraprastha University (GGSIPU), Delhi</div>
  </div>

  <div class="logos-container">
    <div class="logo-box">
      <img src="{img_vips}" alt="VIPS Logo">
    </div>
    <div class="logo-box">
      <img src="{img_ggsipu}" alt="GGSIPU Logo">
    </div>
  </div>

  <div>
    <div style="font-size: 11pt; font-weight: bold; color: #0f172a; text-transform: uppercase; letter-spacing: 1px;">
      Master of Computer Applications (MCA)
    </div>
    <div style="font-size: 10pt; color: #64748b; font-style: italic; margin-top: 2px;">
      Minor Project Final Report &bull; Semester 1
    </div>
  </div>

  <div class="project-title-box">
    <div class="project-title">MediAssist: Smart Prescription Scanner & Medicine Reminder System</div>
    <div class="project-subtitle">An AI-Assisted Clinical Digitization, Regimen Scheduling, and Pharmacy Assistance Web Platform</div>
  </div>

  <div class="degree-text">
    A report submitted in partial fulfillment of the requirements for the award of the degree of<br>
    <strong>MASTER OF COMPUTER APPLICATIONS</strong>
  </div>

  <table class="meta-table">
    <tr>
      <td style="width: 50%;">
        <div class="meta-title">Submitted To:</div>
        <div class="meta-val" style="margin-top: 4px;">
          <strong>Dr. Cosmina</strong><br>
          Project Mentor & Assistant Professor<br>
          VSIT, VIPS-TC, Delhi
        </div>
      </td>
      <td style="width: 50%; text-align: right;">
        <div class="meta-title" style="text-align: right;">Submitted By:</div>
        <div class="meta-val" style="margin-top: 4px;">
          <strong>Haardik Goel</strong><br>
          Enrollment No.: <strong>09417704426</strong><br>
          MCA 1 (B)<br>
          VIPS-TC, Delhi
        </div>
      </td>
    </tr>
  </table>

  <div class="session-text">
    Academic Session: 2026 – 2027<br>
    Delhi, India
  </div>
</div>

<!-- ========================================================================= -->
<!-- CERTIFICATE OF APPROVAL                                                   -->
<!-- ========================================================================= -->
<div class="page">
  <div style="text-align: center; margin-bottom: 25px;">
    <div style="font-size: 13pt; font-weight: bold; text-transform: uppercase;">Vivekananda School of Information Technology</div>
    <div style="font-size: 11pt; color: #475569;">Vivekananda Institute of Professional Studies - TC, Delhi</div>
  </div>

  <h1>Certificate of Approval</h1>

  <p>
    This is to certify that the minor project report entitled <strong>&ldquo;MediAssist: Smart Prescription Scanner and Medicine Reminder System&rdquo;</strong> submitted by <strong>Haardik Goel</strong> (Enrollment No. <strong>09417704426</strong>), student of Master of Computer Applications, <strong>MCA 1 (B)</strong>, at Vivekananda School of Information Technology (VSIT), Vivekananda Institute of Professional Studies-TC, affiliated to Guru Gobind Singh Indraprastha University (GGSIPU), Delhi, is an authentic record of the candidate's own work carried out under my direct supervision and academic mentorship during Semester 1.
  </p>

  <p>
    The project embodies a complete, functioning, cloud-integrated web application featuring automated Optical Character Recognition (OCR), Natural Language Processing (NLP) rule-based clinical frequency parsing, a secure personal vault, Web Push notification scheduling, and geolocation-assisted medicine procurement with 100% test coverage and validation.
  </p>

  <p>
    To the best of my knowledge and belief, this report or any part thereof has not been submitted elsewhere for the award of any other degree, diploma, fellowship, or professional associate certificate.
  </p>

  <div class="sign-container" style="margin-top: 70px;">
    <div class="sign-box">
      <div class="sign-line">
        <strong>Dr. Cosmina</strong><br>
        Project Mentor & Assistant Professor<br>
        VSIT, VIPS-TC, Delhi
      </div>
    </div>
    <div class="sign-box" style="text-align: right;">
      <div class="sign-line" style="text-align: right;">
        <strong>Head of Department / Dean</strong><br>
        Vivekananda School of Information Technology<br>
        VIPS-TC, Delhi
      </div>
    </div>
  </div>

  <div style="margin-top: 35px; font-size: 10.5pt; color: #475569;">
    <strong>Date:</strong> 16th November 2026<br>
    <strong>Place:</strong> New Delhi
  </div>
</div>

<!-- ========================================================================= -->
<!-- DECLARATION & ACKNOWLEDGEMENT                                             -->
<!-- ========================================================================= -->
<div class="page">
  <h1>Declaration of Originality</h1>

  <p>
    I, <strong>Haardik Goel</strong>, a student of <strong>Master of Computer Applications, MCA 1 (B)</strong>, Enrollment Number <strong>09417704426</strong>, hereby declare that the minor project final report entitled <strong>&ldquo;MediAssist: Smart Prescription Scanner and Medicine Reminder System&rdquo;</strong>, submitted to Vivekananda School of Information Technology (VSIT), Vivekananda Institute of Professional Studies-TC (VIPS-TC), affiliated to Guru Gobind Singh Indraprastha University (GGSIPU), Delhi, is an authentic record of my original research, design, and software implementation carried out under the esteemed guidance of my mentor, <strong>Dr. Cosmina</strong>.
  </p>

  <p>
    I further confirm that the ideas, system designs, diagrams, processing pipelines, source code implementations, and evaluation results presented herein are genuine and have not been plagiarized or submitted for any other degree or qualification to any other educational institution or university.
  </p>

  <div class="sign-container" style="margin-top: 35px;">
    <div class="sign-box">
      <strong>Place:</strong> Delhi<br>
      <strong>Date:</strong> 16th November 2026
    </div>
    <div class="sign-box" style="text-align: right;">
      <div class="sign-line" style="text-align: right;">
        <strong>Haardik Goel</strong><br>
        Enrollment No.: 09417704426<br>
        MCA 1 (B), VSIT, VIPS-TC
      </div>
    </div>
  </div>

  <h1 style="margin-top: 35px;">Acknowledgement</h1>

  <p>
    I express my profound gratitude and sincere respect to my project mentor, <strong>Dr. Cosmina</strong>, for her exceptional guidance, invaluable technical insights, and consistent encouragement throughout the conceptualization, development, and testing phases of the <strong>MediAssist</strong> project. Her rigorous feedback on system architecture, clinical parsing rules, and error mitigation strategies has been instrumental in the successful completion of this system.
  </p>

  <p>
    I also extend my heartfelt thanks to the leadership and faculty of the <strong>Vivekananda School of Information Technology (VSIT)</strong>, VIPS-TC, for fostering an enriching academic ecosystem equipped with the requisite technical resources, laboratories, and developmental tools to undertake this endeavor.
  </p>

  <p>
    Lastly, I am deeply indebted to my family and peers for their continuous moral support, patience, and motivation during the intensive software engineering and evaluation iterations of this minor project.
  </p>

  <div style="text-align: right; margin-top: 20px;">
    <strong>Haardik Goel</strong><br>
    MCA 1 (B), Roll No. 09417704426
  </div>
</div>

<!-- ========================================================================= -->
<!-- ABSTRACT & INDEX TERMS                                                    -->
<!-- ========================================================================= -->
<div class="page">
  <h1>Abstract</h1>

  <p>
    Medication non-adherence remains one of the most critical challenges confronting global public healthcare systems. According to the World Health Organization (WHO), nearly 50% of patients with chronic illnesses fail to adhere strictly to their prescribed medical regimens, resulting in preventable disease progressions, increased hospital readmission rates, and substantial economic burdens. A predominant driver of this non-adherence is the inherent illegibility, complexity, and ambiguity of handwritten or densely structured medical prescriptions, which patients struggle to comprehend, remember, and schedule accurately.
  </p>

  <p>
    To resolve these interrelated challenges, this project presents <strong>MediAssist</strong>, an integrated, intelligent, web-based healthcare assistant designed to convert raw prescription photographs into verified, structured, and clinically synchronized medication regimens. The platform employs a multi-tiered pipeline:
  </p>

  <ul>
    <li><strong>Adaptive Preprocessing & Dual-Engine OCR:</strong> Leverages OpenCV image enhancements (bilateral filtering, Gaussian blur, and Otsu binarization) coupled with Tesseract OCR (with fallback to Google Gemini Vision for dense handwritten scripts), achieving sub-second extraction latencies (&lt;0.28 seconds).</li>
    <li><strong>NLP & Fuzzy Regimen Parsing:</strong> Employs a deterministic NLP engine with RapidFuzz token matching to identify 113+ standardized clinical formulations, extract dosage strengths, and interpret physician notations (e.g., OD, BD, TDS, HS, 1-0-1, 1-0-0) into precise daily dose timestamps (08:00, 13:00, 20:00, 22:00).</li>
    <li><strong>Human-in-the-Loop Verification & Secure Vault:</strong> Ensures medical safety by requiring an explicit review step before data commitment. Approved schedules are permanently isolated in a relational vault conforming to India's Digital Personal Data Protection (DPDP) Act 2023.</li>
    <li><strong>Interactive Timeline, AI Synthesis & Reminders:</strong> Integrates Google Gemini 1.5 Flash for contextual meal-timing synthesis, provides browser Web Push reminders with Taken/Skip/Snooze state tracking, and incorporates an interactive calendar for dose logging.</li>
    <li><strong>Medicine Locator:</strong> Provides direct hyperlinks to online procurement (Tata 1mg) and a Leaflet/Google Maps interface for nearby pharmacy discovery.</li>
  </ul>

  <p>
    The entire system was subjected to an exhaustive 112-point automated test suite encompassing unit, integration, security, and dataset evaluation across 10 real-world prescription batches (yielding 42 extracted medicines), achieving a <strong>100% pass rate (Grade A+)</strong>. The project successfully demonstrates an accessible, privacy-preserving, and clinically viable solution for modern patient self-care.
  </p>

  <div class="callout-box">
    <strong>Index Terms</strong> &mdash; Prescription digitization, Optical Character Recognition (OCR), Medication adherence, Natural Language Processing (NLP), RapidFuzz, Web Push API, Google Gemini AI, DPDP Act 2023, Leaflet Maps, Responsive UI.
  </div>
</div>

<!-- ========================================================================= -->
<!-- TABLE OF CONTENTS                                                         -->
<!-- ========================================================================= -->
<div class="page">
  <h1>Table of Contents</h1>

  <div class="toc-item"><span class="toc-title">Certificate of Approval</span><span>i</span></div>
  <div class="toc-item"><span class="toc-title">Declaration of Originality</span><span>ii</span></div>
  <div class="toc-item"><span class="toc-title">Acknowledgement</span><span>ii</span></div>
  <div class="toc-item"><span class="toc-title">Abstract & Index Terms</span><span>iii</span></div>
  <div class="toc-item"><span class="toc-title">List of Figures & Tables</span><span>iv</span></div>

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

  <div class="toc-item"><span class="toc-title">Chapter 3: Objectives & Scope of the Project</span><span>6</span></div>
  <div class="toc-item"><span class="toc-sub">3.1 Primary Objectives</span><span>6</span></div>
  <div class="toc-item"><span class="toc-sub">3.2 Secondary Objectives</span><span>6</span></div>
  <div class="toc-item"><span class="toc-sub">3.3 Scope: In-Scope, Out-of-Scope, and Constraints</span><span>7</span></div>

  <div class="toc-item"><span class="toc-title">Chapter 4: System Requirements Specification (SRS)</span><span>8</span></div>
  <div class="toc-item"><span class="toc-sub">4.1 Functional Requirements (FR1 &ndash; FR10)</span><span>8</span></div>
  <div class="toc-item"><span class="toc-sub">4.2 Non-Functional Requirements (NFR1 &ndash; NFR8)</span><span>9</span></div>
  <div class="toc-item"><span class="toc-sub">4.3 Technology Stack & Architectural Decisions</span><span>9</span></div>
  <div class="toc-item"><span class="toc-sub">4.4 Hardware & Software Operating Requirements</span><span>10</span></div>

  <div class="toc-item"><span class="toc-title">Chapter 5: System Architecture & Database Design</span><span>11</span></div>
  <div class="toc-item"><span class="toc-sub">5.1 Layered System Architecture (Presentation, App, Data)</span><span>11</span></div>
  <div class="toc-item"><span class="toc-sub">5.2 Data Flow Modeling (Level 0 and Level 1 DFD)</span><span>12</span></div>
  <div class="toc-item"><span class="toc-sub">5.3 Entity-Relationship (ER) Schema Modeling</span><span>13</span></div>
  <div class="toc-item"><span class="toc-sub">5.4 Comprehensive Data Dictionary</span><span>14</span></div>
  <div class="toc-item"><span class="toc-sub">5.5 Security, Privacy & DPDP Act 2023 Compliance</span><span>15</span></div>

  <div class="toc-item"><span class="toc-title">Chapter 6: Methodology & Implementation Details</span><span>16</span></div>
  <div class="toc-item"><span class="toc-sub">6.1 Development Methodology (Agile Scrum)</span><span>16</span></div>
  <div class="toc-item"><span class="toc-sub">6.2 End-to-End Processing Pipeline</span><span>16</span></div>
  <div class="toc-item"><span class="toc-sub">6.3 Image Preprocessing Algorithms</span><span>17</span></div>
  <div class="toc-item"><span class="toc-sub">6.4 NLP Clinical Parsing & Doctor Shorthand Engine</span><span>18</span></div>
  <div class="toc-item"><span class="toc-sub">6.5 AI Clinical Guidance Integration (Google Gemini)</span><span>19</span></div>
  <div class="toc-item"><span class="toc-sub">6.6 Web Push Engine, Calendar Vault & UI Redesign</span><span>20</span></div>

  <div class="toc-item"><span class="toc-title">Chapter 7: Operational Workflow & State Transitions</span><span>21</span></div>
  <div class="toc-item"><span class="toc-sub">7.1 Overall System Operational Workflow</span><span>21</span></div>
  <div class="toc-item"><span class="toc-sub">7.2 Medication Reminder Lifecycle & State Transitions</span><span>22</span></div>

  <div class="toc-item"><span class="toc-title">Chapter 8: Testing, Verification & Experimental Evaluation</span><span>23</span></div>
  <div class="toc-item"><span class="toc-sub">8.1 Multi-Tier Testing Strategy</span><span>23</span></div>
  <div class="toc-item"><span class="toc-sub">8.2 Quantitative Evaluation Metrics & Latency Benchmarks</span><span>23</span></div>
  <div class="toc-item"><span class="toc-sub">8.3 Prescription Dataset Validation (10 Batches, 42 Meds)</span><span>24</span></div>
  <div class="toc-item"><span class="toc-sub">8.4 Comprehensive System Scorecard (112/112 &ndash; Grade A+)</span><span>25</span></div>
  <div class="toc-item"><span class="toc-sub">8.5 Test Case Execution Matrix (TC1 &ndash; TC12)</span><span>26</span></div>

  <div class="toc-item"><span class="toc-title">Chapter 9: Project Timeline & Limitations</span><span>27</span></div>
  <div class="toc-item"><span class="toc-sub">9.1 Academic Project Timeline & Deliverables</span><span>27</span></div>
  <div class="toc-item"><span class="toc-sub">9.2 Current System Limitations</span><span>27</span></div>

  <div class="toc-item"><span class="toc-title">Chapter 10: Future Scope & Conclusion</span><span>28</span></div>
  <div class="toc-item"><span class="toc-sub">10.1 Future Scope & Research Horizons</span><span>28</span></div>
  <div class="toc-item"><span class="toc-sub">10.2 Conclusion</span><span>28</span></div>

  <div class="toc-item"><span class="toc-title">References</span><span>29</span></div>
</div>

<!-- ========================================================================= -->
<!-- LIST OF FIGURES & TABLES                                                  -->
<!-- ========================================================================= -->
<div class="page">
  <h1>List of Figures & Tables</h1>

  <h2>List of Figures</h2>
  <div class="toc-item"><span>Fig. 1. Layered system architecture of MediAssist (Presentation, App, Data Layers)</span><span>11</span></div>
  <div class="toc-item"><span>Fig. 2. Level-1 Data Flow Diagram (DFD) showing 5 primary processes and 4 datastores</span><span>12</span></div>
  <div class="toc-item"><span>Fig. 3. Entity-Relationship (ER) diagram of the MediAssist database schema</span><span>13</span></div>
  <div class="toc-item"><span>Fig. 4. Complete operational workflow of the MediAssist human-in-the-loop pipeline</span><span>21</span></div>

  <h2 style="margin-top: 25px;">List of Tables</h2>
  <div class="toc-item"><span>Table I. Project metadata and submission details</span><span>Title Page</span></div>
  <div class="toc-item"><span>Table II. Comparison between conventional alarms and the MediAssist platform</span><span>3</span></div>
  <div class="toc-item"><span>Table III. Architectural module inputs, core algorithms, and expected outputs</span><span>5</span></div>
  <div class="toc-item"><span>Table IV. Functional requirements specification (FR1 &ndash; FR10)</span><span>8</span></div>
  <div class="toc-item"><span>Table V. MediAssist technical stack summary</span><span>9</span></div>
  <div class="toc-item"><span>Table VI. Hardware and software deployment specifications</span><span>10</span></div>
  <div class="toc-item"><span>Table VII. Relational database entities and cardinalities</span><span>13</span></div>
  <div class="toc-item"><span>Table VIII. Comprehensive relational data dictionary</span><span>14</span></div>
  <div class="toc-item"><span>Table IX. Doctor shorthand frequency mapping and scheduled dose slots</span><span>18</span></div>
  <div class="toc-item"><span>Table X. Medication reminder state transition lifecycle matrix</span><span>22</span></div>
  <div class="toc-item"><span>Table XI. System test cases and evaluation results matrix (TC1 &ndash; TC12)</span><span>26</span></div>
  <div class="toc-item"><span>Table XII. Academic minor project execution schedule and milestone timeline</span><span>27</span></div>
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
    This minor project final report is organized into eleven structured chapters. Chapter 2 details the problem statement, literature survey, and gap analysis. Chapter 3 defines the project's primary/secondary objectives and boundary scope. Chapter 4 provides the complete System Requirements Specification (SRS) and technology stack. Chapter 5 articulates the layered architecture, DFDs, ER schema, and data dictionary. Chapter 6 examines the algorithmic methodology and implementation pipelines. Chapter 7 details the operational workflow and state transitions. Chapter 8 provides an exhaustive review of test results (112/112 score, Grade A+) and experimental benchmarks. Chapter 9 outlines project timelines and limitations. Chapter 10 presents future research directions and concluding remarks, followed by formal IEEE references.
  </p>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 2: PROBLEM STATEMENT & LITERATURE REVIEW                         -->
<!-- ========================================================================= -->
<div class="page">
  <h1>Chapter 2: Problem Statement & Literature Review</h1>

  <h2>2.1 Problem Description</h2>
  <p>
    The workflow of paper-based prescription handling is fundamentally error-prone. Patients receive physical prescription sheets containing abbreviated drug nomenclature, dosage units (mg, ml, IU), frequency shorthand, and duration windows. In the absence of an immediate, intelligible digital translation, patients frequently:
  </p>
  <ul>
    <li>Confuse morning and evening doses;</li>
    <li>Omit midday doses due to workday distractions;</li>
    <li>Prematurely terminate antibiotic or maintenance therapies;</li>
    <li>Misplace physical prescription slips, losing track of their ongoing clinical history.</li>
  </ul>

  <h2>2.2 Limitations of Existing Approaches</h2>
  <p>
    Conventional solutions currently available in the marketplace suffer from distinct systemic drawbacks:
  </p>

  <div class="table-title">Table II: Comparison Between Conventional Alarms and Proposed MediAssist System</div>
  <table class="content-table">
    <thead>
      <tr>
        <th>Capability / Feature</th>
        <th>Manual / Generic Smartphone Alarms</th>
        <th>Commercial Native Pill Apps</th>
        <th>Proposed MediAssist Platform</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Prescription Ingestion</strong></td>
        <td>None; requires manual entry of alarm times.</td>
        <td>Manual text entry or locked behind premium subscriptions.</td>
        <td>Instant camera capture / file upload with sub-second OCR.</td>
      </tr>
      <tr>
        <td><strong>Frequency Interpretation</strong></td>
        <td>None; user must manually compute recurrence.</td>
        <td>Limited static time pickers; cannot parse OD, BD, 1-0-1.</td>
        <td>Automated rule-based conversion into exact daily dose slots.</td>
      </tr>
      <tr>
        <td><strong>Fuzzy Medicine Matching</strong></td>
        <td>None.</td>
        <td>Often restricted to Western/US drug compendia.</td>
        <td>RapidFuzz matching against 113+ common Indian clinical formulations.</td>
      </tr>
      <tr>
        <td><strong>AI Clinical Guidance</strong></td>
        <td>None.</td>
        <td>Generic text snippets without context.</td>
        <td>Google Gemini live synthesis for meal-time regimen coordination.</td>
      </tr>
      <tr>
        <td><strong>Cross-Platform Access</strong></td>
        <td>Tied to individual physical device hardware.</td>
        <td>Heavy mobile OS installs; no cross-browser sync.</td>
        <td>Zero-install responsive web app (mobile, tablet, desktop).</td>
      </tr>
      <tr>
        <td><strong>Pharmacy Integration</strong></td>
        <td>None.</td>
        <td>Commercial affiliate advertisements.</td>
        <td>One-click Tata 1mg direct links and Google Maps locator.</td>
      </tr>
    </tbody>
  </table>

  <h2>2.3 Gap Analysis</h2>
  <p>
    The gap analysis indicates that while high-end hospital information systems (HIS) provide electronic health records, no lightweight, accessible, and privacy-respecting consumer tool bridges the everyday gap between a patient photographing a prescription slip and receiving automated, context-aware reminders coupled with fulfillment assistance. MediAssist explicitly addresses this void.
  </p>

  <h2>2.4 Literature Survey of Core Technologies</h2>
  <h3>2.4.1 Optical Character Recognition (OCR)</h3>
  <p>
    Tesseract OCR, initially engineered by Hewlett-Packard and subsequently maintained by Google, represents the state-of-the-art open-source text extraction engine utilizing multi-layer LSTM neural networks [3]. In MediAssist, Tesseract v4.1.1 is integrated via <code>pytesseract</code>. To accommodate challenging handwritten prescriptions, the pipeline is augmented with Google Gemini Vision API fallback.
  </p>

  <h3>2.4.2 Image Preprocessing & Binarization</h3>
  <p>
    Raw mobile camera uploads inevitably contain non-uniform lighting, shadows, paper wrinkles, and optical noise. Otsu's thresholding algorithm [5] automatically calculates an optimal binarization threshold by minimizing intra-class variance. Combined with OpenCV [6] bilateral noise filtering and Gaussian smoothing, the OCR character recognition rate improves significantly.
  </p>

  <h3>2.4.3 Natural Language Processing & Fuzzy String Matching</h3>
  <p>
    OCR outputs often contain minor character corruptions (e.g., &ldquo;Paracetarnol&rdquo; instead of &ldquo;Paracetamol&rdquo;). The Levenshtein distance metric, efficiently implemented in C++ via the RapidFuzz library [8], computes token-sort similarity ratios, enabling robust fuzzy correction with confidence scoring above 80%.
  </p>

  <h3>2.4.4 Push Notifications & Browser Scheduling</h3>
  <p>
    The W3C Push API and Service Workers [9] allow web applications to receive server-dispatched push events and trigger system-level desktop/mobile banner alerts even when the main website tab is inactive. MediAssist utilizes this standard for deterministic, battery-efficient reminder delivery.
  </p>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 3: OBJECTIVES & SCOPE                                             -->
<!-- ========================================================================= -->
<div class="page">
  <h1>Chapter 3: Objectives & Scope of the Project</h1>

  <h2>3.1 Primary Objectives</h2>
  <p>
    The core objective of the MediAssist minor project is to design, implement, and validate an intelligent web platform that automates the translation of paper prescriptions into actionable therapeutic routines. The primary engineering objectives comprise:
  </p>
  <ul>
    <li><strong>Automated Digitization:</strong> Ingest prescription images via camera capture or file upload and extract textual data within 5 seconds using an OpenCV preprocessing and OCR pipeline.</li>
    <li><strong>Clinical Entity Extraction:</strong> Parse raw extracted text to detect medication names, dosage strengths, administration frequencies, and durations using regex and fuzzy matching against a verified clinical lexicon.</li>
    <li><strong>Shorthand Translation:</strong> Convert standard clinical shorthand (OD, BD, TDS, QID, HS, 1-0-1, 1-0-0) into discrete daily dose timestamps (08:00 Morning, 13:00 Afternoon, 20:00 Evening, 22:00 Bedtime).</li>
    <li><strong>Human Verification Gateway:</strong> Implement an editable review interface allowing users to audit, adjust, or supplement extracted medication entities prior to permanent database commitment.</li>
    <li><strong>Multi-Action Reminders:</strong> Implement a client-side and server-synchronized notification engine allowing users to mark doses as Taken, Skipped, or Snoozed.</li>
    <li><strong>Medicine Procurement Support:</strong> Seamlessly integrate direct links to trusted online pharmacies (Tata 1mg) and provide an interactive Google Maps/Leaflet interface for local pharmacy discovery.</li>
  </ul>

  <h2>3.2 Secondary Objectives</h2>
  <ul>
    <li>Provide an AI-powered clinical guidance engine leveraging Google Gemini to synthesize multi-drug timing instructions into a coherent, meal-synchronized daily schedule.</li>
    <li>Deliver an interactive calendar interface maintaining an immutable chronological audit trail of taken and skipped medication history.</li>
    <li>Implement a batch deletion facility allowing users to manage their active medication vault with multi-select convenience.</li>
    <li>Ensure full compliance with modern web accessibility guidelines, mobile-first responsive viewports, and Indian data protection standards (DPDP Act 2023).</li>
  </ul>

  <h2>3.3 Scope of the Project</h2>
  <h3>3.3.1 In Scope</h3>
  <ul>
    <li>Web-based user registration, authentication, and session persistence across page refreshes.</li>
    <li>Mobile camera dual-upload (native camera trigger and gallery file picker).</li>
    <li>Image preprocessing (grayscale conversion, Gaussian denoising, Otsu adaptive thresholding).</li>
    <li>OCR extraction via Tesseract with handwriting fallback.</li>
    <li>Fuzzy medication matching against 113+ Indian pharmaceutical formulations.</li>
    <li>Doctor shorthand normalization (OD, BD, TDS, HS, 1-0-1).</li>
    <li>AI meal-timing synthesis via Google Gemini 1.5 Flash.</li>
    <li>Web Push notifications with Taken/Skip/Snooze state tracking.</li>
    <li>Online pharmacy integration (Tata 1mg) and nearby store locator via Google Maps.</li>
  </ul>

  <h3>3.3.2 Out of Scope</h3>
  <ul>
    <li>Automated digital signing or issuing of new legal prescriptions by physicians.</li>
    <li>Direct electronic billing, insurance claims, or commercial payment gateway processing.</li>
    <li>Physical integration with automated smart pill-dispenser hardware.</li>
  </ul>

  <h3>3.3.3 Assumptions and Technical Constraints</h3>
  <ul>
    <li>The patient or caregiver possesses a smartphone, tablet, or PC with a modern web browser supporting JavaScript, Canvas, and Service Workers.</li>
    <li>Prescriptions must be photographed with reasonable clarity and illumination.</li>
    <li>The system operates as an assistive personal tool and does not replace professional clinical judgment.</li>
  </ul>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 4: SYSTEM REQUIREMENTS SPECIFICATION (SRS)                       -->
<!-- ========================================================================= -->
<div class="page">
  <h1>Chapter 4: System Requirements Specification (SRS)</h1>

  <h2>4.1 Functional Requirements</h2>
  <div class="table-title">Table IV: Functional Requirements Specification</div>
  <table class="content-table">
    <thead>
      <tr>
        <th style="width: 12%;">Req. ID</th>
        <th style="width: 25%;">Requirement Category</th>
        <th>Detailed Functional Specification</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>FR1</strong></td>
        <td>User Authentication</td>
        <td>The system shall allow users to register with full name, email, and password, verify accounts, and log in securely.</td>
      </tr>
      <tr>
        <td><strong>FR2</strong></td>
        <td>Prescription Ingestion</td>
        <td>The system shall accept prescription images via direct file upload or smartphone camera capture (max 8MB).</td>
      </tr>
      <tr>
        <td><strong>FR3</strong></td>
        <td>Image Preprocessing</td>
        <td>The system shall apply bilateral filtering, Gaussian blur, and Otsu binarization to enhance text clarity.</td>
      </tr>
      <tr>
        <td><strong>FR4</strong></td>
        <td>OCR Text Extraction</td>
        <td>The system shall extract textual lines from preprocessed images using Tesseract OCR within 5.0 seconds.</td>
      </tr>
      <tr>
        <td><strong>FR5</strong></td>
        <td>Clinical Entity Parsing</td>
        <td>The system shall parse extracted text to identify drug names, strengths, frequencies, and durations.</td>
      </tr>
      <tr>
        <td><strong>FR6</strong></td>
        <td>Human Verification</td>
        <td>The system shall display a mandatory review screen allowing the patient to modify extracted data before saving.</td>
      </tr>
      <tr>
        <td><strong>FR7</strong></td>
        <td>Personal Vault Storage</td>
        <td>The system shall persist confirmed prescriptions, medicines, and dosage times in a relational database.</td>
      </tr>
      <tr>
        <td><strong>FR8</strong></td>
        <td>AI Timing Synthesis</td>
        <td>The system shall invoke Google Gemini to generate comprehensive meal-time consumption guidelines.</td>
      </tr>
      <tr>
        <td><strong>FR9</strong></td>
        <td>Push Notifications</td>
        <td>The system shall schedule browser notifications for each daily dose with Taken, Snooze, and Skip actions.</td>
      </tr>
      <tr>
        <td><strong>FR10</strong></td>
        <td>Medicine Locator</td>
        <td>The system shall provide direct 1mg purchase links and render a Google Maps / Leaflet store finder.</td>
      </tr>
    </tbody>
  </table>

  <h2>4.2 Non-Functional Requirements</h2>
  <ul>
    <li><strong>Performance (NFR1):</strong> OCR processing and text parsing shall complete within 5.0 seconds under standard loads (empirically benchmarked at 0.10s &ndash; 0.28s).</li>
    <li><strong>Security & Privacy (NFR2):</strong> Passwords must be hashed using salted PBKDF2/Werkzeug algorithms. Sessions must utilize HTTP-Only, SameSite=Lax cookies.</li>
    <li><strong>Availability (NFR3):</strong> The cloud web service shall maintain 99.5% uptime during operational testing.</li>
    <li><strong>Usability (NFR4):</strong> The user interface shall feature a responsive, high-contrast white and orange theme with subtle black shaders, WCAG-compliant font sizes, and touch-friendly controls.</li>
    <li><strong>Data Tenancy (NFR5):</strong> All API queries must filter by authenticated <code>user_id</code> to prevent cross-account data leaks.</li>
    <li><strong>Data Deletion (NFR6):</strong> In compliance with the DPDP Act 2023, the system must provide a one-click account deletion facility that cascades across all associated prescriptions, medicines, and logs.</li>
  </ul>

  <h2>4.3 Technology Stack</h2>
  <div class="table-title">Table V: MediAssist Technology Stack Summary</div>
  <table class="content-table">
    <thead>
      <tr>
        <th>Tier / Domain</th>
        <th>Technologies / Libraries</th>
        <th>Rationale & Key Capabilities</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>Frontend</strong></td>
        <td>HTML5, CSS3, ES6 JavaScript, Anime.js, Leaflet.js</td>
        <td>Lightweight, zero-framework dependency, rapid DOM rendering, 60fps micro-animations, and interactive map displays.</td>
      </tr>
      <tr>
        <td><strong>Backend API</strong></td>
        <td>Python 3.12, Flask 3.0, Flask-Limiter</td>
        <td>Lightweight microframework, robust WSGI routing, built-in REST serialization, and rate-limiting brute force protection.</td>
      </tr>
      <tr>
        <td><strong>Computer Vision</strong></td>
        <td>OpenCV (cv2), NumPy</td>
        <td>High-performance matrix operations, image resizing, Gaussian filtering, and Otsu binarization.</td>
      </tr>
      <tr>
        <td><strong>OCR Engine</strong></td>
        <td>pytesseract, Tesseract OCR v4.1.1, Gemini Vision</td>
        <td>Neural LSTM OCR extraction paired with multimodal generative vision fallback for unconstrained handwriting.</td>
      </tr>
      <tr>
        <td><strong>NLP & Matching</strong></td>
        <td>RapidFuzz, Regular Expressions</td>
        <td>C++ accelerated Levenshtein token sort matching against 113+ standardized clinical drug entities.</td>
      </tr>
      <tr>
        <td><strong>Generative AI</strong></td>
        <td>Google Gemini 1.5 Flash API</td>
        <td>Live synthesis of complex drug interactions and food-timing regimens.</td>
      </tr>
      <tr>
        <td><strong>Database Tier</strong></td>
        <td>SQLite 3 / PostgreSQL (Supabase Compatible)</td>
        <td>ACID-compliant relational persistence, foreign key cascading, and cloud database portability.</td>
      </tr>
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
    MediAssist is structured around a modular, three-tiered architectural paradigm comprising the Presentation Tier, the Application Logic Tier, and the Data/External Services Tier. This modular decoupling ensures that computer vision pipelines, NLP parsers, and database operations can be independently maintained and scaled.
  </p>

  <div class="fig-container">
    <img src="{img_arch}" alt="Fig 1: Layered System Architecture">
    <div class="fig-caption">Fig. 1. Layered system architecture of the MediAssist platform.</div>
  </div>

  <p>
    As depicted in Fig. 1:
  </p>
  <ul>
    <li><strong>Presentation Tier:</strong> Operates entirely inside the client browser. It manages camera access, asynchronous fetch requests, interactive schedule rendering, the Web Push Service Worker listener, and Leaflet mapping.</li>
    <li><strong>Application Logic Tier:</strong> Implemented as a Python Flask REST API. It encapsulates the core intelligence modules: User Auth, Preprocessing & OCR, Clinical Regex Parsing, Gemini AI Synthesis, Reminder Dispatcher, and Pharmacy Locator.</li>
    <li><strong>Data & External Services Tier:</strong> Provides persistent storage via SQLite/PostgreSQL, integrates Google Gemini 1.5 Flash, the W3C Web Push notification network, and OpenStreetMap/Google Maps tiles.</li>
  </ul>

  <h2>5.2 Data Flow Modeling</h2>
  <p>
    The operational flow of data across system boundaries is modeled through Data Flow Diagrams. Fig. 2 illustrates the Level-1 DFD of the MediAssist system.
  </p>

  <div class="fig-container">
    <img src="{img_dfd}" alt="Fig 2: Level-1 Data Flow Diagram">
    <div class="fig-caption">Fig. 2. Level-1 Data Flow Diagram (DFD) showing core processes and datastores.</div>
  </div>

  <p>
    The Level-1 DFD reveals five primary processes interacting with four major datastores:
  </p>
  <ul>
    <li><strong>Process 1.0 (Authentication):</strong> Validates user credentials, sets secure HTTP-only cookies, and reads/writes to Datastore D1 (Users).</li>
    <li><strong>Process 2.0 (Scan & Extract):</strong> Ingests prescription images, executes preprocessing, calls OCR, and extracts raw text.</li>
    <li><strong>Process 3.0 (Parse & Verify):</strong> Correlates raw text with Datastore D3 (Medicine Reference), identifies dosages, presents human review, and writes to Datastore D2 (Prescriptions).</li>
    <li><strong>Process 4.0 (Schedule & Remind):</strong> Computes daily dose timestamps, registers Web Push jobs in Datastore D4 (Reminders & Dose Log), and logs user responses.</li>
    <li><strong>Process 5.0 (Locate Medicines):</strong> Takes verified medicine names and user coordinates to query Google Maps and generate Tata 1mg hyperlinks.</li>
  </ul>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 5 CONTINUED: ER SCHEMA & DATA DICTIONARY                         -->
<!-- ========================================================================= -->
<div class="page">
  <h2>5.3 Entity-Relationship (ER) Schema Modeling</h2>
  <p>
    The database is engineered using the Entity-Relationship modeling paradigm [13] to ensure referential integrity, eliminate data redundancy, and support relational queries. Fig. 3 depicts the normalized ER schema.
  </p>

  <div class="fig-container">
    <img src="{img_erd}" alt="Fig 3: Entity-Relationship Diagram">
    <div class="fig-caption">Fig. 3. Entity-Relationship diagram of the MediAssist relational database.</div>
  </div>

  <div class="table-title">Table VII: Database Entity Cardinality Summary</div>
  <table class="content-table">
    <thead>
      <tr>
        <th>Relationship</th>
        <th>Connected Entities</th>
        <th>Cardinality</th>
        <th>Clinical & Functional Semantics</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>uploads</strong></td>
        <td>USER &ndash; PRESCRIPTION</td>
        <td>1 : N</td>
        <td>A single registered user can upload and manage multiple prescriptions.</td>
      </tr>
      <tr>
        <td><strong>contains</strong></td>
        <td>PRESCRIPTION &ndash; ITEM</td>
        <td>1 : N</td>
        <td>A single prescription contains multiple parsed medication items.</td>
      </tr>
      <tr>
        <td><strong>references</strong></td>
        <td>ITEM &ndash; MEDICINE_REF</td>
        <td>N : 1</td>
        <td>Many prescription items reference a standard entry in the drug master catalog.</td>
      </tr>
      <tr>
        <td><strong>schedules</strong></td>
        <td>ITEM &ndash; REMINDER</td>
        <td>1 : N</td>
        <td>Each medication item has one or more daily scheduled reminder times.</td>
      </tr>
      <tr>
        <td><strong>records</strong></td>
        <td>REMINDER &ndash; DOSE_LOG</td>
        <td>1 : N</td>
        <td>Each scheduled reminder generates multiple historical dose consumption records.</td>
      </tr>
      <tr>
        <td><strong>registers</strong></td>
        <td>USER &ndash; PUSH_SUB</td>
        <td>1 : N</td>
        <td>A user can register multiple browser devices for push alert delivery.</td>
      </tr>
    </tbody>
  </table>

  <h2>5.4 Comprehensive Data Dictionary</h2>
  <div class="table-title">Table VIII: MediAssist Relational Data Dictionary</div>
  <table class="content-table">
    <thead>
      <tr>
        <th>Table Name</th>
        <th>Field Name</th>
        <th>Data Type & Constraints</th>
        <th>Description & Purpose</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>users</strong></td>
        <td>id<br>email<br>password_hash<br>full_name<br>is_verified<br>created_at</td>
        <td>INTEGER PRIMARY KEY<br>TEXT UNIQUE NOT NULL<br>TEXT NOT NULL<br>TEXT NOT NULL<br>INTEGER DEFAULT 0<br>TEXT NOT NULL</td>
        <td>Stores registered patient account credentials, verification flags, and account creation timestamps.</td>
      </tr>
      <tr>
        <td><strong>prescriptions</strong></td>
        <td>id<br>user_id<br>doctor_name<br>issue_date<br>ocr_raw_text<br>created_at</td>
        <td>INTEGER PRIMARY KEY<br>INTEGER (FK users.id)<br>TEXT<br>TEXT<br>TEXT<br>TEXT NOT NULL</td>
        <td>Records prescription metadata, physician name, date issued, and raw OCR transcription.</td>
      </tr>
      <tr>
        <td><strong>medicines</strong></td>
        <td>id<br>user_id<br>prescription_id<br>name<br>strength<br>frequency<br>duration<br>instructions</td>
        <td>INTEGER PRIMARY KEY<br>INTEGER (FK users.id)<br>INTEGER (FK prescriptions.id)<br>TEXT NOT NULL<br>TEXT<br>TEXT<br>TEXT<br>TEXT</td>
        <td>Stores verified medication entities, strengths (e.g., 500mg), frequencies (e.g., 1-0-1), and durations.</td>
      </tr>
      <tr>
        <td><strong>reminders</strong></td>
        <td>id<br>user_id<br>medicine_id<br>time_of_day<br>is_active</td>
        <td>INTEGER PRIMARY KEY<br>INTEGER (FK users.id)<br>INTEGER (FK medicines.id)<br>TEXT NOT NULL<br>INTEGER DEFAULT 1</td>
        <td>Maintains specific daily reminder times (e.g., '08:00', '20:00') linked to each medication.</td>
      </tr>
      <tr>
        <td><strong>dose_logs</strong></td>
        <td>id<br>reminder_id<br>user_id<br>scheduled_time<br>status<br>logged_at</td>
        <td>INTEGER PRIMARY KEY<br>INTEGER (FK reminders.id)<br>INTEGER (FK users.id)<br>TEXT NOT NULL<br>TEXT ('taken'|'skipped')<br>TEXT NOT NULL</td>
        <td>Audits actual dose consumption status, timestamp of intake, and compliance history.</td>
      </tr>
      <tr>
        <td><strong>push_subscriptions</strong></td>
        <td>id<br>user_id<br>endpoint<br>p256dh_key<br>auth_token</td>
        <td>INTEGER PRIMARY KEY<br>INTEGER (FK users.id)<br>TEXT UNIQUE NOT NULL<br>TEXT NOT NULL<br>TEXT NOT NULL</td>
        <td>Stores Web Push cryptographic keys for browser-level notification dispatch.</td>
      </tr>
    </tbody>
  </table>

  <h2>5.5 Security, Privacy & DPDP Act 2023 Compliance</h2>
  <p>
    Recognizing that prescription records constitute sensitive personal health data, MediAssist enforces strict technical safeguards aligned with the Digital Personal Data Protection (DPDP) Act 2023 [2]:
  </p>
  <ul>
    <li><strong>Cryptographic Salting & Hashing:</strong> Plaintext passwords are never stored. The system employs Werkzeug's PBKDF2 with SHA-256 and unique per-user salts.</li>
    <li><strong>Session Defense:</strong> Session cookies are signed with a cryptographically deterministic server secret and flagged with <code>HttpOnly</code> and <code>SameSite=Lax</code> to prevent Cross-Site Scripting (XSS) and Request Forgery (CSRF).</li>
    <li><strong>Per-User Data Tenancy:</strong> All database CRUD operations strictly bind queries to <code>WHERE user_id = ?</code>, guaranteeing complete tenant isolation.</li>
    <li><strong>Right to Erasure:</strong> A dedicated <code>POST /api/account/delete</code> endpoint executes an atomic cascading delete across all records, purging the user's data completely upon request.</li>
  </ul>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 6: METHODOLOGY & IMPLEMENTATION DETAILS                          -->
<!-- ========================================================================= -->
<div class="page">
  <h1>Chapter 6: Methodology & Implementation Details</h1>

  <h2>6.1 Development Methodology</h2>
  <p>
    MediAssist was engineered following the Agile Scrum methodology over a 12-week iterative lifecycle. Sprints were structured around specific vertical modules: Core Vision Pipeline, Regimen Parsing & Doctor Shorthand Engine, Personal Vault & Web Push Dispatcher, and AI/Procurement Integration, culminating in extensive automated test verification.
  </p>

  <h2>6.2 End-to-End Processing Pipeline</h2>
  <p>
    The software pipeline consists of five sequential stages:
  </p>
  <ol>
    <li><strong>Client-Side Image Optimization:</strong> When an image is captured via mobile camera or uploaded, a client-side HTML5 Canvas compresses high-resolution photographs to a maximum dimension of 1200px while retaining sharp text edges. This dramatically optimizes upload bandwidth and reduces server processing latency from 4.8s to 0.12s.</li>
    <li><strong>OpenCV Preprocessing Engine:</strong> The server converts the raw image into an 8-bit grayscale matrix, applies bilateral filtering to suppress background paper noise while preserving stroke boundaries, and computes Otsu's adaptive thresholding for optimal binarization.</li>
    <li><strong>Dual-Engine OCR Extraction:</strong> The binarized matrix is evaluated by Tesseract OCR v4.1.1 configured with Page Segmentation Mode (PSM 6 &ndash; assume a single uniform block of text). For complex handwritten prescriptions, an automated fallback invokes Gemini Vision.</li>
    <li><strong>Clinical Entity Extraction & Normalization:</strong> The raw text stream is tokenized and processed through regular expression extractors and RapidFuzz fuzzy string matching against the clinical medication lexicon.</li>
    <li><strong>Human Verification & Vault Commitment:</strong> The extracted entities are rendered in an editable grid for patient confirmation before being stored in the database.</li>
  </ol>

  <h2>6.3 Image Preprocessing Algorithms</h2>
  <p>
    Image enhancement is governed by the following OpenCV algorithmic pipeline:
  </p>
  <div class="code-snippet">
# OpenCV Image Preprocessing Pipeline
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
denoised = cv2.bilateralFilter(gray, d=9, sigmaColor=75, sigmaSpace=75)
blurred = cv2.GaussianBlur(denoised, (3, 3), 0)
# Otsu's optimal global thresholding
_, otsu_bin = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
# Adaptive Gaussian thresholding for uneven illumination
adaptive_bin = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                     cv2.THRESH_BINARY, blockSize=31, C=11)
  </div>

  <h2>6.4 NLP Clinical Parsing & Doctor Shorthand Engine</h2>
  <p>
    Physicians routinely utilize standardized Latin abbreviations and numeric matrices to convey dosing regimens. MediAssist implements a deterministic parser that normalizes OCR character confusions (e.g., '0D' &rarr; 'OD', '8D' &rarr; 'BD', '1-0-I' &rarr; '1-0-1') and maps them into exact daily dose schedules:
  </p>

  <div class="table-title">Table IX: Doctor Shorthand Frequency Mapping & Scheduled Dose Slots</div>
  <table class="content-table">
    <thead>
      <tr>
        <th>Physician Shorthand</th>
        <th>Clinical Meaning</th>
        <th>Daily Dosing Slots</th>
        <th>Default Scheduled Times</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td><strong>OD / 1-0-0 / 0-0-1</strong></td>
        <td>Once daily (Omni Die)</td>
        <td>Morning (Breakfast) or Bedtime</td>
        <td>08:00 Morning / 22:00 Night</td>
      </tr>
      <tr>
        <td><strong>BD / BID / 1-0-1</strong></td>
        <td>Twice daily (Bis in Die)</td>
        <td>Morning and Night</td>
        <td>08:00 Morning & 20:00 Evening</td>
      </tr>
      <tr>
        <td><strong>TDS / TID / 1-1-1</strong></td>
        <td>Three times daily (Ter Die Sumendum)</td>
        <td>Morning, Afternoon, and Night</td>
        <td>08:00, 13:00, and 20:00</td>
      </tr>
      <tr>
        <td><strong>QID / 1-1-1-1</strong></td>
        <td>Four times daily (Quater in Die)</td>
        <td>Four evenly spaced doses</td>
        <td>08:00, 12:00, 16:00, and 20:00</td>
      </tr>
      <tr>
        <td><strong>HS</strong></td>
        <td>At bedtime (Hora Somni)</td>
        <td>Night only</td>
        <td>22:00 Bedtime</td>
      </tr>
      <tr>
        <td><strong>SOS / PRN</strong></td>
        <td>As needed (Si Opus Sit)</td>
        <td>On demand</td>
        <td>Conditional Logging</td>
      </tr>
    </tbody>
  </table>

  <h2>6.5 AI Clinical Guidance Integration (Google Gemini)</h2>
  <p>
    To provide holistic clinical assistance beyond simple alarm chimes, MediAssist incorporates the <strong>Google Gemini 1.5 Flash</strong> generative model via the <code>/api/medicines/summary</code> endpoint. When invoked, the endpoint supplies the patient's active medication list to Gemini, prompting the model to analyze potential drug interactions, categorize medicines into morning/afternoon/evening/night slots, and synthesize explicit food-timing instructions (e.g., &ldquo;Take Pantoprazole 30 minutes before breakfast; take Metformin immediately following food to minimize GI discomfort&rdquo;).
  </p>

  <h2>6.6 Web Push Engine, Calendar Vault & UI Redesign</h2>
  <p>
    The user interface was redesigned to meet modern aesthetic and usability criteria:
  </p>
  <ul>
    <li><strong>Theme Architecture:</strong> Transformed from a dark theme to a bright, clinical <strong>white and orange theme</strong> accented with deep black shaders, subtle card elevations (<code>box-shadow: 0 4px 16px -2px rgba(0,0,0,0.06)</code>), and smooth 60fps micro-interactions.</li>
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
        <td>Patient clicks &ldquo;Take Dose&rdquo; button.</td>
        <td><strong>Taken</strong></td>
        <td>Dose is marked taken in <code>dose_logs</code>; adherence score increments.</td>
      </tr>
      <tr>
        <td><strong>Triggered</strong></td>
        <td>Patient clicks &ldquo;Snooze&rdquo; button.</td>
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
<!-- CHAPTER 8: TESTING, VERIFICATION & EXPERIMENTAL EVALUATION                 -->
<!-- ========================================================================= -->
<div class="page">
  <h1>Chapter 8: Testing, Verification & Experimental Evaluation</h1>

  <h2>8.1 Multi-Tier Testing Strategy</h2>
  <p>
    Software quality and medical safety were verified through a comprehensive, multi-tiered testing methodology covering Unit Testing, Integration Testing, System API Testing, UI Responsiveness Testing, Security Verification, and Dataset Benchmark Testing.
  </p>

  <h2>8.2 Quantitative Evaluation Metrics & Latency Benchmarks</h2>
  <p>
    System performance was evaluated against the following quantitative benchmarks:
  </p>
  <ul>
    <li><strong>OCR Processing Latency:</strong> Requirement &le; 5.0 seconds. <em>Empirical Benchmark:</em> <strong>0.10s &ndash; 0.28s</strong> (achieved through client-side canvas scaling and optimized bilateral filtering).</li>
    <li><strong>Fuzzy Match Accuracy:</strong> Requirement &ge; 80% confidence score. <em>Empirical Benchmark:</em> <strong>87% &ndash; 100%</strong> match confidence across test drug names.</li>
    <li><strong>Test Suite Execution:</strong> Complete automated test suite covering 112 system verification points.</li>
  </ul>

  <h2>8.3 Prescription Dataset Validation</h2>
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

  <h2>8.4 Comprehensive System Scorecard</h2>
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
      <tr><td>Tech Stack & Dependencies (Synopsis VII-C)</td><td>10</td><td>10</td><td>0</td><td>12 / 12</td><td>100.0%</td></tr>
      <tr><td>System Architecture (Synopsis VIII-A)</td><td>4</td><td>4</td><td>0</td><td>5 / 5</td><td>100.0%</td></tr>
      <tr><td>Module 1: Prescription Scanner (Synopsis VI-B-1)</td><td>8</td><td>8</td><td>0</td><td>13 / 13</td><td>100.0%</td></tr>
      <tr><td>Module 2: Medicine Parser (Synopsis VI-B-2)</td><td>29</td><td>29</td><td>0</td><td>30 / 30</td><td>100.0%</td></tr>
      <tr><td>Module 3: Prescription Vault (Synopsis VI-B-3)</td><td>12</td><td>12</td><td>0</td><td>19 / 19</td><td>100.0%</td></tr>
      <tr><td>Module 4: Reminder Engine (Synopsis VI-B-4)</td><td>8</td><td>8</td><td>0</td><td>10 / 10</td><td>100.0%</td></tr>
      <tr><td>Module 5: Medicine Locator (Synopsis VI-B-5)</td><td>7</td><td>7</td><td>0</td><td>12 / 12</td><td>100.0%</td></tr>
      <tr><td>Frontend / UI & Theme (Synopsis VII-B)</td><td>13</td><td>13</td><td>0</td><td>14 / 14</td><td>100.0%</td></tr>
      <tr><td>Security & Privacy (Synopsis VIII-E)</td><td>7</td><td>7</td><td>0</td><td>10 / 10</td><td>100.0%</td></tr>
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
<!-- CHAPTER 8 CONTINUED: TEST CASES MATRIX                                    -->
<!-- ========================================================================= -->
<div class="page">
  <h2>8.5 Test Cases Specification Matrix</h2>
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
        <td>Printed Prescription Parsing</td>
        <td>High-res printed prescription containing 4 medicines.</td>
        <td>All 4 drug names, strengths, and frequencies parsed accurately.</td>
        <td><strong style="color: #16a34a;">PASS</strong></td>
      </tr>
      <tr>
        <td><strong>TC2</strong></td>
        <td>Blurred / Skewed Image</td>
        <td>Low-light, slightly skewed smartphone photograph.</td>
        <td>Bilateral filter clarifies text; review interface allows correction.</td>
        <td><strong style="color: #16a34a;">PASS</strong></td>
      </tr>
      <tr>
        <td><strong>TC3</strong></td>
        <td>Handwritten Prescription</td>
        <td>Cursive handwriting with doctor shorthand notations.</td>
        <td>OCR extracts shorthand; Gemini Vision fallback assists unreadable tokens.</td>
        <td><strong style="color: #16a34a;">PASS</strong></td>
      </tr>
      <tr>
        <td><strong>TC4</strong></td>
        <td>Fuzzy Typo Correction</td>
        <td>Corrupted token: &ldquo;Metforrmin 500mg&rdquo;.</td>
        <td>RapidFuzz matches to &ldquo;Metformin&rdquo; with 95% confidence score.</td>
        <td><strong style="color: #16a34a;">PASS</strong></td>
      </tr>
      <tr>
        <td><strong>TC5</strong></td>
        <td>Shorthand Expansion</td>
        <td>Prescription contains &lsquo;1-0-1&rsquo; and &lsquo;TDS&rsquo;.</td>
        <td>Converted into Morning/Evening and Morning/Afternoon/Night slots.</td>
        <td><strong style="color: #16a34a;">PASS</strong></td>
      </tr>
      <tr>
        <td><strong>TC6</strong></td>
        <td>Human Review Gateway</td>
        <td>User adjusts strength from 250mg to 500mg.</td>
        <td>Modified values accurately persisted to database vault.</td>
        <td><strong style="color: #16a34a;">PASS</strong></td>
      </tr>
      <tr>
        <td><strong>TC7</strong></td>
        <td>Web Push Dispatch</td>
        <td>System clock reaches scheduled dose time (08:00).</td>
        <td>Browser push notification appears with Take/Skip buttons.</td>
        <td><strong style="color: #16a34a;">PASS</strong></td>
      </tr>
      <tr>
        <td><strong>TC8</strong></td>
        <td>Reminder Snooze Action</td>
        <td>User selects &ldquo;Snooze&rdquo; on active notification.</td>
        <td>Reminder suppressed and re-triggered after 15-minute interval.</td>
        <td><strong style="color: #16a34a;">PASS</strong></td>
      </tr>
      <tr>
        <td><strong>TC9</strong></td>
        <td>Tenancy Data Isolation</td>
        <td>User A requests prescription ID belonging to User B.</td>
        <td>HTTP 401/403 Forbidden returned; data access strictly denied.</td>
        <td><strong style="color: #16a34a;">PASS</strong></td>
      </tr>
      <tr>
        <td><strong>TC10</strong></td>
        <td>Invalid File Type Upload</td>
        <td>User uploads an executable or non-image format (.exe, .pdf).</td>
        <td>Request rejected with HTTP 400 and explicit user error toast.</td>
        <td><strong style="color: #16a34a;">PASS</strong></td>
      </tr>
      <tr>
        <td><strong>TC11</strong></td>
        <td>AI Meal-Timing Synthesis</td>
        <td>User requests clinical summary with 4 active drugs.</td>
        <td>Google Gemini synthesizes meal-time guidelines and warnings.</td>
        <td><strong style="color: #16a34a;">PASS</strong></td>
      </tr>
      <tr>
        <td><strong>TC12</strong></td>
        <td>Account Cascading Deletion</td>
        <td>User triggers account deletion via settings.</td>
        <td>User record, medicines, reminders, and dose logs permanently purged.</td>
        <td><strong style="color: #16a34a;">PASS</strong></td>
      </tr>
    </tbody>
  </table>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 9: PROJECT TIMELINE & LIMITATIONS                                 -->
<!-- ========================================================================= -->
<div class="page">
  <h1>Chapter 9: Project Timeline & Limitations</h1>

  <h2>9.1 Academic Project Timeline</h2>
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
        <td>Full system integration, 112 automated tests execution, and UI white/orange theme redesign.</td>
        <td>Weeks 10 &ndash; 11</td>
        <td>Completed</td>
      </tr>
      <tr>
        <td><strong>Phase 7</strong></td>
        <td>Final minor project documentation, experimental report compilation, and mentor review.</td>
        <td>Week 12</td>
        <td>Completed</td>
      </tr>
    </tbody>
  </table>

  <h2>9.2 Current System Limitations</h2>
  <p>
    Notwithstanding the successful validation of the platform, several technical and environmental limitations are acknowledged:
  </p>
  <ul>
    <li><strong>Handwriting Variability:</strong> Highly degraded, illegible cursive scripts produced by hurried clinicians can occasionally exceed the deciphering threshold of classical OCR engines, necessitating reliance on multimodal cloud vision or patient manual correction during human-in-the-loop review.</li>
    <li><strong>Browser Notification Dependencies:</strong> Web Push notification reliability depends upon browser permissions granted by the patient and operating system battery-saver policies (particularly on aggressive mobile OS backgrounds).</li>
    <li><strong>Lexicon Coverage:</strong> The local fuzzy matching engine is pre-loaded with 113+ standardized clinical entities. While covering major chronic and acute drugs, highly specialized proprietary compounds may require manual entry.</li>
    <li><strong>Assistive Nature:</strong> MediAssist is engineered strictly as an educational and operational adherence tool. It does not replace the professional diagnosis, contraindication screening, or clinical judgment of a licensed healthcare provider.</li>
  </ul>
</div>

<!-- ========================================================================= -->
<!-- CHAPTER 10: FUTURE SCOPE & CONCLUSION                                     -->
<!-- ========================================================================= -->
<div class="page page-last">
  <h1>Chapter 10: Future Scope & Conclusion</h1>

  <h2>10.1 Future Scope & Research Horizons</h2>
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

  <h2>10.2 Conclusion</h2>
  <p>
    Medication non-adherence represents a multifaceted public health crisis that diminishes therapeutic outcomes and strains healthcare systems. <strong>MediAssist</strong> directly addresses this challenge by providing a smart, intuitive, and accessible bridge from paper prescriptions to structured daily adherence.
  </p>
  <p>
    By synergistically harmonizing OpenCV image preprocessing, dual-engine OCR, NLP-based clinical shorthand parsing, Google Gemini generative synthesis, a secure personal vault, and Web Push notifications into a cohesive, responsive web platform, MediAssist transforms complex medical instructions into transparent, manageable daily habits. The mandatory human-in-the-loop review interface ensures clinical safety, while the DPDP Act 2023 compliance architecture guarantees uncompromising patient privacy.
  </p>
  <p>
    With an automated verification scorecard of <strong>112 / 112 passed tests (100.0%, Grade A+)</strong>, sub-second processing latencies, and an elegant white and orange user interface, MediAssist demonstrates the practical feasibility of deploying accessible AI technologies to enhance self-care, empower chronic patients, and elevate modern medication adherence.
  </p>

  <h1 style="margin-top: 25px;">References</h1>
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
    <li>W3C & MDN Web Docs, &ldquo;Geolocation API: Interfacing client geographical location,&rdquo; Mozilla Developer Network, 2023. [Online]. Available: https://developer.mozilla.org/en-US/docs/Web/API/Geolocation_API</li>
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
downloads_pdf_path = os.path.abspath(os.path.join(BASE_DIR, '..', 'finalsubmission report sem1.pdf'))

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Report HTML written to: {html_path} ({os.path.getsize(html_path)} bytes)")

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
    # Also copy to downloads directory
    shutil.copyfile(pdf_path, downloads_pdf_path)
    print(f"Copied to downloads location: {downloads_pdf_path} ({os.path.getsize(downloads_pdf_path):,} bytes)")
else:
    print("ERROR: PDF was not generated!")
