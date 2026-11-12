"""
Generate sample doctor prescription images for OCR testing.
Run: python datasets/create_samples.py
Creates PNG images in datasets/prescriptions/
"""
import numpy as np
import cv2
import os

OUT_DIR = os.path.join(os.path.dirname(__file__), "prescriptions")
os.makedirs(OUT_DIR, exist_ok=True)

# ---------- prescription data ----------
PRESCRIPTIONS = [
    {
        "file": "prescription_01.png",
        "doctor": "Dr. Rajesh Kumar, MBBS, MD",
        "clinic": "City Care Hospital, Delhi",
        "patient": "Ravi Sharma, Age: 45, M",
        "date": "10/11/2026",
        "lines": [
            "Tab. Metformin 500mg     1-0-1    30 days",
            "Tab. Amlodipine 5mg      OD       30 days",
            "Cap. Omeprazole 20mg     1-0-0    14 days",
            "Tab. Aspirin 75mg        OD       30 days",
        ],
    },
    {
        "file": "prescription_02.png",
        "doctor": "Dr. Priya Mehta, MBBS",
        "clinic": "Apollo Clinic, Mumbai",
        "patient": "Sunita Devi, Age: 32, F",
        "date": "08/11/2026",
        "lines": [
            "Tab. Paracetamol 500mg    TDS     5 days",
            "Cap. Amoxicillin 500mg    BD      7 days",
            "Syp. Cough Linctus 5ml    TDS     5 days",
            "Tab. Cetirizine 10mg      HS      5 days",
        ],
    },
    {
        "file": "prescription_03.png",
        "doctor": "Dr. Anand Verma, MD, DM (Cardio)",
        "clinic": "Heart Care Centre, Lucknow",
        "patient": "Mohan Lal, Age: 60, M",
        "date": "05/11/2026",
        "lines": [
            "Tab. Atorvastatin 20mg     HS      30 days",
            "Tab. Clopidogrel 75mg      OD      30 days",
            "Tab. Metoprolol 50mg       BD      30 days",
            "Tab. Ramipril 5mg          OD      30 days",
            "Tab. Ecosprin 75mg         OD      30 days",
        ],
    },
    {
        "file": "prescription_04.png",
        "doctor": "Dr. Suman Gupta, MBBS, MD",
        "clinic": "Fortis Hospital, Bangalore",
        "patient": "Neha Agarwal, Age: 28, F",
        "date": "09/11/2026",
        "lines": [
            "Tab. Levothyroxine 50mcg   OD      30 days",
            "Cap. Vitamin D3 60000IU    1/week  8 weeks",
            "Tab. Iron Folic Acid       BD      30 days",
            "Tab. Calcium 500mg         BD      30 days",
        ],
    },
    {
        "file": "prescription_05.png",
        "doctor": "Dr. Vikram Singh, MBBS, MS (Ortho)",
        "clinic": "Bone & Joint Clinic, Jaipur",
        "patient": "Ajay Patel, Age: 50, M",
        "date": "07/11/2026",
        "lines": [
            "Tab. Diclofenac 50mg      BD      7 days",
            "Tab. Pantoprazole 40mg     1-0-0   7 days",
            "Cap. Pregabalin 75mg       HS      14 days",
            "Tab. Thiocolchicoside 4mg  BD      7 days",
        ],
    },
    {
        "file": "prescription_06.png",
        "doctor": "Dr. Meena Sharma, MD (Derma)",
        "clinic": "Skin & Hair Clinic, Chandigarh",
        "patient": "Pooja Rawat, Age: 24, F",
        "date": "06/11/2026",
        "lines": [
            "Tab. Doxycycline 100mg     BD      14 days",
            "Tab. Isotretinoin 20mg     OD      30 days",
            "Cap. Biotin 10mg           OD      30 days",
            "Tab. Levocetirizine 5mg    HS      14 days",
        ],
    },
    {
        "file": "prescription_07.png",
        "doctor": "Dr. A.K. Pandey, MBBS, MD (Pulmo)",
        "clinic": "Chest & Lung Hospital, Patna",
        "patient": "Rakesh Kumar, Age: 55, M",
        "date": "04/11/2026",
        "lines": [
            "Tab. Montelukast 10mg      HS       30 days",
            "Cap. Doxofylline 400mg     BD       14 days",
            "Tab. Prednisolone 10mg     1-0-0    5 days",
            "Inj. Deriphyllin 2ml       BD       3 days",
        ],
    },
    {
        "file": "prescription_08.png",
        "doctor": "Dr. Nisha Kapoor, MD (Paed)",
        "clinic": "Rainbow Children Hospital, Hyderabad",
        "patient": "Arjun, Age: 8, M",
        "date": "03/11/2026",
        "lines": [
            "Syp. Amoxicillin 125mg/5ml   TDS    5 days",
            "Tab. Paracetamol 250mg        TDS    3 days",
            "Syp. Cetirizine 5mg/5ml       OD     5 days",
            "Syp. Multivitamin 5ml         OD     30 days",
        ],
    },
    {
        "file": "prescription_09.png",
        "doctor": "Dr. R.P. Mishra, MBBS, MD (Gen Med)",
        "clinic": "AIIMS OPD, New Delhi",
        "patient": "Kamla Devi, Age: 68, F",
        "date": "02/11/2026",
        "lines": [
            "Tab. Glimepiride 2mg        OD       30 days",
            "Tab. Metformin 1000mg        BD       30 days",
            "Tab. Telmisartan 40mg        OD       30 days",
            "Tab. Rosuvastatin 10mg       HS       30 days",
            "Inj. Insulin Glargine 10U    OD       30 days",
        ],
    },
    {
        "file": "prescription_10.png",
        "doctor": "Dr. Suresh Reddy, MBBS, MD (Psych)",
        "clinic": "Mind Wellness Centre, Chennai",
        "patient": "Arun M., Age: 35, M",
        "date": "01/11/2026",
        "lines": [
            "Tab. Escitalopram 10mg      OD      30 days",
            "Tab. Clonazepam 0.5mg       HS      14 days",
            "Tab. Propranolol 20mg       BD      30 days",
            "Cap. Methylcobalamin 1500mcg OD     30 days",
        ],
    },
]

def draw_prescription(data):
    """Create a realistic-looking prescription image."""
    W, H = 800, 1000
    img = np.ones((H, W, 3), dtype=np.uint8) * 245  # off-white paper

    # Add slight noise for realism
    noise = np.random.normal(0, 3, (H, W, 3)).astype(np.int16)
    img = np.clip(img.astype(np.int16) + noise, 0, 255).astype(np.uint8)

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_small = cv2.FONT_HERSHEY_PLAIN
    black = (15, 15, 15)
    blue = (180, 50, 20)
    gray = (120, 120, 120)

    y = 50
    # Header
    cv2.putText(img, data["doctor"], (40, y), font, 0.7, blue, 2)
    y += 30
    cv2.putText(img, data["clinic"], (40, y), font_small, 1.2, gray, 1)
    y += 35
    cv2.line(img, (40, y), (W - 40, y), gray, 1)
    y += 30

    # Patient info
    cv2.putText(img, f"Patient: {data['patient']}", (40, y), font, 0.55, black, 1)
    cv2.putText(img, f"Date: {data['date']}", (520, y), font, 0.55, black, 1)
    y += 35
    cv2.line(img, (40, y), (W - 40, y), gray, 1)
    y += 35

    # Rx symbol
    cv2.putText(img, "Rx", (40, y), font, 1.0, blue, 2)
    y += 45

    # Medicine lines
    for line in data["lines"]:
        cv2.putText(img, line, (60, y), font, 0.5, black, 1)
        y += 35

    y += 30
    cv2.line(img, (40, y), (W - 40, y), gray, 1)
    y += 35

    # Signature area
    cv2.putText(img, "Signature", (550, y), font_small, 1.1, gray, 1)
    cv2.line(img, (540, y + 5), (740, y + 5), gray, 1)

    return img


if __name__ == "__main__":
    for data in PRESCRIPTIONS:
        img = draw_prescription(data)
        path = os.path.join(OUT_DIR, data["file"])
        cv2.imwrite(path, img)
        print(f"Created: {path}")

    print(f"\nGenerated {len(PRESCRIPTIONS)} prescription images in {OUT_DIR}")

