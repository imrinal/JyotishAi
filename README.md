# 🔮 Astrology Chatbot — Your AI-Powered Vedic Guide

**A custom-built AI chatbot that blends traditional Vedic astrology with modern AI (LLaMa) — fully powered by your own JSON rules and logic.**

> ✨ Built by Mrinal Paul | Powered by JyotishAI™

---

## 🌟 Project Overview

This is a custom-built astrology chatbot that:

- Calculates planetary charts (D1 to D60), dashas, doshas, panchang, and more
- Matches your hand-written rules from JSON files
- Uses an AI model (LLaMa) to convert raw rules into **human-like, emotional predictions**
- Generates structured reports and supports **PDF downloads**
- Entirely **frontend + Flask based**, no database or login system (for now)

---

## 🚀 Live Features

✅ Panchang details (Tithi, Yoga, Karana, Nakshatra)  
✅ Charts: D1, D9, D10, D7, D24, D60, Lal Kitab  
✅ Mahadasha → Antardasha → Pratyantar Dasha  
✅ Dosha analysis (Mangal, Kalsarpa, etc.)  
✅ Vastu-based suggestions  
✅ Career, love, marriage prediction  
✅ Emotionally wise AI-generated responses  
✅ Chat UI + downloadable PDF report

---

## 📁 Project Structure

astrology_chatbot/
├── frontend/
│ ├── index.html # UI: Birth form + chat section
│ ├── css/style.css # Glassmorphism, colors, layout
│ └── js/main.js # Chat logic, API calls, PDF creation
│
├── backend/
│ ├── app.py # Flask routes for /predict and /chat
│ ├── requirements.txt # Python packages needed
│
│ ├── astrology_engine/
│ │ ├── calculator.py # PySwisseph chart, dasha, dosha calc
│ │ └── rule_matcher.py # Matches chart with JSON rules
│
│ ├── rules/ # Your custom-written logic
│ │ ├── house_rules.json
│ │ ├── dasha_rules.json
│ │ ├── ...more
│
│ └── ai_integrator.py # Loads LLaMa model, beautifies reply
│
└── README.md # Project overview and instructions

yaml
Copy
Edit

---

## ⚙️ Tech Stack

| Layer      | Tools Used                      |
| ---------- | ------------------------------- |
| Frontend   | HTML5, CSS3, JavaScript, jsPDF  |
| Backend    | Python, Flask, PySwisseph       |
| AI/NLP     | HuggingFace Transformers, LLaMa |
| Data Layer | JSON-based custom rule engine   |

---

## 🧪 How It Works

1. **User Inputs**:

   - Birth date, time, and location via `index.html`

2. **Flask Receives Request** (`/predict`):

   - Uses `calculator.py` to generate charts + dashas
   - Matches with your custom logic in `rules/*.json`

3. **AI Response** (`/chat`):

   - `ai_integrator.py` sends raw predictions to LLaMa
   - Returns beautiful, emotionally wise interpretation

4. **Frontend Displays**:
   - Chat-style conversation
   - Optional PDF download via `jsPDF`

---

## 🛠️ Getting Started

### 🔧 Step 1: Clone the Repo

```bash
git clone https://github.com/your-username/astrology_chatbot.git
cd astrology_chatbot/backend
🐍 Step 2: Set Up Python Environment
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
📦 Step 3: Install Requirements
bash
Copy
Edit
pip install -r requirements.txt
▶️ Step 4: Run the Flask Server
bash
Copy
Edit
python app.py
🌐 Step 5: Open the Frontend
Open frontend/index.html in your browser. (Connects to localhost:5000)

🧠 JSON Rule System
Your logic lives in /rules/ folder in simple, editable files like:

json
Copy
Edit
{
  "sun_in_7th": {
    "effect": "Ego issues in marriage",
    "intensity": "Medium",
    "remedy": "Chant Aditya Hridaya Stotra on Sundays"
  }
}
You can expand to hundreds of rules across:

house_rules.json

dasha_rules.json

love_marriage_rules.json

vastu_rules.json
...and more.

🤖 LLaMa AI Layer
Located in ai_integrator.py

Uses a system prompt like:

"You are a wise astrologer. Explain raw predictions in emotional, spiritual tone. Avoid jargon."

Converts rules like:

text
Copy
Edit
Sun in 7th → Ego issues
Jupiter Mahadasha → Growth & stability
into:

"During this phase, relationship tensions may arise due to ego clashes. But Jupiter will give you strength and guidance to heal and expand emotionally."

📄 Output Sample
Chat Format (Frontend):
yaml
Copy
Edit
🧘‍♂️ AstroMate says:
“In 2026, Jupiter’s grace blesses your career. A shift in March 2027 may test your trust in relationships, but brings clarity...”
PDF Format:
vbnet
Copy
Edit
=============================
🌟 JyotishAI™ Report
Name: User | DOB: 03/12/2004 | Time: 08:30 AM | Place: Kolkata
=============================

🪐 Dasha: Jupiter → Saturn
❤️ Relationship: Challenges in ego due to Sun in 7th
📈 Career: Strong success due to Mars in 10th

✅ Remedies:
- Wear white on Thursdays
- Donate wheat on Sundays
...

-- End of Report --
Made by Mrinal | Powered by JyotishAI™
📌 To Do / Future Features
 Dynamic chart drawing (base64 image)

 Export report via email

 User history storage (optional DB)

 Add chatbot memory (multi-turn)

 Integrate Google Maps API for location coords

🙏 Credits & License
Created by Mrinal Paul with 💙
Inspired by Vedic astrology + modern AI

Feel free to use, fork, and improve — give credit where due.

✉️ Contact
📧 Email: [your-email@example.com]
🌐 Portfolio: [your-site-link-here]
📸 Instagram / LinkedIn: [Your handles]

🌠 “May the stars guide you, and the code empower you.”
— Team JyotishAI™

```
