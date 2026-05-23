# AI Network Threat Intelligence System

An advanced, real-time cybersecurity platform that uses Machine Learning (Random Forest) and Explainable AI (Gemini) to detect and analyze network threats.

## 🚀 Features
- **Live Packet Capture:** Modular Scapy-based sniffer.
- **ML Detection Engine:** Uses the NSL-KDD trained Random Forest model.
- **Intelligent Severity System:** Categorizes threats (LOW, MEDIUM, HIGH, CRITICAL).
- **AI Explanation Layer:** Powered by Gemini for natural language threat analysis.
- **Futuristic Web Dashboard:** Real-time React interface with WebSockets.
- **Mock Data Generator:** For easy demonstration and testing.

## 🛠️ Tech Stack
- **Backend:** FastAPI, Scapy, Joblib, Gemini API.
- **Frontend:** React, Tailwind CSS, Framer Motion, Lucide.

## 🏃 Getting Started

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
# Set your Gemini API Key in a .env file
# GEMINI_API_KEY=your_key_here
python run.py
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm start
```

### 3. Demo Mode (Optional)
If you don't have live traffic to sniff, run the mock generator:
```bash
python mock_generator.py
```

## 📂 Project Structure
- `backend/app/`: Core logic (sniffer, engine, processor).
- `backend/models/`: Trained .pkl models.
- `frontend/src/`: React dashboard components.
- `mock_generator.py`: Simulation script for demos.
