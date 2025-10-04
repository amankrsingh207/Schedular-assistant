# Appointment Scheduler Backend

A Flask-based backend service that extracts and normalizes **appointment information** (department, date, time, timezone) from **text or images** using OCR and entity recognition.

---

## Features
- OCR text extraction using **Tesseract**
- Entity extraction from text (department, date, time)
- Normalization to structured JSON
- Supports **multiple appointments in one image**
- Clean modular structure (`entity_service`, `normalize_service`, `ocr_service`, `utils`)
  

---

##  Project Architecture
appointment-scheduler-backend/
│
├── app.py # Main Flask application
├── ocr_service.py # Extract text from images using pytesseract
├── entity_service.py # Extract department, date, and time entities
├── normalize_service.py # Normalize extracted entities to standard format
├── utils.py # Build final JSON response
├── requirements.txt # Python dependencies
└── README.md # Project documentation


---

## ⚙️ Setup Instructions

### 1️ Clone the repository
```bash
git clone https://github.com/amankrsingh207/Schedular-assistant.git
cd Schedular-assistant

### 2.Create a virtual environment
 python -m venv venv

3️. Install dependencies
 pip install -r requirements.txt

 4.Run the Flask app
  python app.py

**API usage examples.**
case 1: for text type input (request on   https://jacklyn-cyetic-overconfidently.ngrok-free.dev/schedule_text)
input: {
  "text": [
    "Book a dentist appointment on 26th September 2025 at 3 PM",
    "Schedule a cardiologist visit on 28th September 2025 at 10 AM"
  ]
}

output:{
    "appointments": [
        {
            "appointment": {
                "date": "2025-09-01",
                "department": "dentist",
                "time": "15:00",
                "tz": "Asia/Kolkata"
            },
            "status": "ok"
        },
        {
            "appointment": {
                "date": "2025-09-28",
                "department": "cardiologist",
                "time": "10:00",
                "tz": "Asia/Kolkata"
            },
            "status": "ok"
        }
    ],
    "status": "ok"
}
case 2:image type input (request on   https://jacklyn-cyetic-overconfidently.ngrok-free.dev/schedule_image)
input: sample.png
output:{
    "appointments": [
        {
            "appointment": {
                "date": "2025-10-10",
                "department": "dentist",
                "time": "17:00",
                "tz": "Asia/Kolkata"
            },
            "status": "ok"
        },
        {
            "appointment": {
                "date": "2025-10-11",
                "department": "doctor",
                "time": "10:00",
                "tz": "Asia/Kolkata"
            },
            "status": "ok"
        },
        {
            "appointment": {
                "date": "2025-10-12",
                "department": "cardiologist",
                "time": "09:00",
                "tz": "Asia/Kolkata"
            },
            "status": "ok"
        },
        {
            "message": "Ambiguous department",
            "status": "needs_clarification"
        }
    ],
    "status": "ok"
}
