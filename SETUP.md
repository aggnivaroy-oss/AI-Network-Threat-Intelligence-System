# AI Network Threat Intelligence System — Setup Guide

Before running this project, make sure you have everything installed below.

---

## System Requirements

| Requirement | Version | Download |
|---|---|---|
| Python | 3.10 or higher | https://www.python.org/downloads/ |
| Node.js | 18 or higher | https://nodejs.org/ |
| npm | comes with Node.js | — |
| Git | any recent version | https://git-scm.com/ |

---

## Step 1 — Clone the Repository

```bash
git clone https://github.com/aggnivaroy-oss/AI-Network-Threat-Intelligence-System.git
cd AI-Network-Threat-Intelligence-System
```

---

## Step 2 — Backend Setup (Python / FastAPI)

Navigate to the backend folder:

```bash
cd backend
```

Install all Python dependencies:

```bash
pip install -r requirements.txt
```

Also install uvicorn with WebSocket support:

```bash
pip install "uvicorn[standard]" websockets
```

### Environment Variables

Create a `.env` file inside the `backend/` folder:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

Get your Gemini API key from: https://aistudio.google.com/app/apikey

---

## Step 3 — Frontend Setup (React / Tailwind)

Open a new terminal and navigate to the frontend folder:

```bash
cd frontend
```

Install all Node dependencies:

```bash
npm install
```

Also install Tailwind CSS:

```bash
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

Install UI libraries:

```bash
npm install lucide-react recharts
```

---

## Step 4 — Running the Project

You need **two terminals open at the same time**.

### Terminal 1 — Start Backend

```bash
cd backend
python run.py
```

Backend will run at: `http://localhost:8000`
WebSocket at: `ws://localhost:8000/ws`

### Terminal 2 — Start Frontend

```bash
cd frontend
npm start
```

Frontend will open at: `http://localhost:3000` or `http://localhost:3001`

---

## Python Dependencies (from requirements.txt)

| Package | Purpose |
|---|---|
| fastapi | Web framework for the API |
| uvicorn[standard] | ASGI server to run FastAPI |
| websockets | WebSocket support |
| scapy | Live network packet sniffing |
| scikit-learn | AI/ML threat prediction model |
| pandas | Data processing |
| numpy | Numerical operations |
| python-dotenv | Load environment variables |
| google-generativeai | Gemini AI explanations |

---

## Node Dependencies

| Package | Purpose |
|---|---|
| react | Frontend UI framework |
| recharts | Charts and graphs |
| lucide-react | Icons |
| tailwindcss | CSS styling |
| postcss | CSS processing |
| autoprefixer | CSS compatibility |

---

## Troubleshooting

**Dashboard shows "Disconnected"**
- Make sure the backend is running on port 8000
- Run `pip install "uvicorn[standard]" websockets` and restart

**Tailwind styles not showing**
- Make sure `src/index.css` has the three `@tailwind` directives
- Make sure `src/index.js` imports `./index.css`

**Backend crashes on startup**
- Check your `.env` file has a valid `GEMINI_API_KEY`
- Run `pip install -r requirements.txt` again

**npm errors**
- Make sure Node.js 18+ is installed: `node --version`
- Delete `node_modules/` and run `npm install` again

---

## Project Structure

```
AI-Network-Threat-Intelligence-System/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes.py        # REST API endpoints
│   │   │   └── websockets.py    # WebSocket connection manager
│   │   ├── core/
│   │   │   ├── config.py        # App configuration
│   │   │   └── processor.py     # Packet processor
│   │   ├── services/
│   │   │   ├── sniffer.py       # Live packet sniffing (Scapy)
│   │   │   ├── simulation.py    # Simulated traffic for demo
│   │   │   ├── prediction.py    # AI threat prediction
│   │   │   ├── severity.py      # Severity classification
│   │   │   └── explanation.py   # Gemini AI explanations
│   │   └── main.py              # FastAPI app entry point
│   ├── models/                  # Trained ML model files
│   ├── requirements.txt
│   └── run.py                   # Start the backend server
├── frontend/
│   ├── public/
│   │   └── index.html
│   ├── src/
│   │   ├── App.js
│   │   ├── Dashboard.js
│   │   ├── index.js
│   │   └── index.css
│   ├── tailwind.config.js
│   └── package.json
└── SETUP.md                     # This file
```

---

*Built with FastAPI, React, Tailwind CSS, and Scapy.*
