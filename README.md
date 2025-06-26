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
