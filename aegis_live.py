import time
import threading
import joblib
import numpy as np
from scapy.all import sniff, IP, TCP
from collections import defaultdict
import tkinter as tk
from tkinter import ttk

# ---------------- LOAD TRAINED AI MODEL ----------------
model = joblib.load("aegis_rf_model.pkl")

# ---------------- GLOBAL STATE ----------------
state = {
    "ai_decision": "INITIALIZING",
    "firewall_action": "MONITORING",
    "confidence": 0.0,
    "src": "-",
    "dst": "-",
    "bytes": 0,
    "duration": 0.0,
    "last_update": "-"
}

ATTACK_THRESHOLD = 0.6
blocked_ips = set()

# ---------------- CONNECTION TRACKING ----------------
connections = defaultdict(lambda: {
    "start_time": time.time(),
    "src_bytes": 0,
    "packets": 0,
    "syn_errors": 0
})

recent_connections = []

# ---------------- PACKET CALLBACK ----------------
def packet_callback(packet):
    if IP not in packet:
        return

    src = packet[IP].src
    dst = packet[IP].dst
    proto = packet[IP].proto

    key = (src, dst, proto)
    conn = connections[key]

    size = len(packet)
    conn["packets"] += 1
    conn["src_bytes"] += size

    if TCP in packet and packet[TCP].flags == "S":
        conn["syn_errors"] += 1

    now = time.time()
    recent_connections.append((now, key))
    recent_connections[:] = [(t, k) for t, k in recent_connections if now - t < 2]

    # -------- NSL-KDD STYLE FEATURES --------
    duration = now - conn["start_time"]
    count = len(recent_connections)
    serror_rate = conn["syn_errors"] / max(1, conn["packets"])

    X = np.array([[duration,
                   conn["src_bytes"],
                   0, 0, 0, 0,
                   count,
                   count,
                   serror_rate]])

    # -------- AI PREDICTION --------
    prediction = model.predict(X)[0]
    confidence = model.predict_proba(X)[0][1]

    # -------- FIREWALL DECISION --------
    if prediction == 1 and confidence >= ATTACK_THRESHOLD:
        state["ai_decision"] = "🚨 AI PREDICTION: ATTACK"
        if src not in blocked_ips:
            blocked_ips.add(src)
            state["firewall_action"] = "🛑 FIREWALL ACTION: BLOCKED"
        else:
            state["firewall_action"] = "🛑 FIREWALL ACTION: BLOCKED"
    else:
        state["ai_decision"] = "✅ AI PREDICTION: NORMAL"
        state["firewall_action"] = "🟢 FIREWALL ACTION: MONITORING"

    # -------- UPDATE STATE --------
    state["confidence"] = confidence
    state["src"] = src
    state["dst"] = dst
    state["bytes"] = conn["src_bytes"]
    state["duration"] = duration
    state["last_update"] = time.strftime("%H:%M:%S")

# ---------------- SNIFFER THREAD ----------------
def start_sniffing():
    sniff(filter="ip", prn=packet_callback, store=False)

# ---------------- TKINTER DASHBOARD ----------------
def launch_dashboard():
    root = tk.Tk()
    root.title("Wi-Fi Threat Detection System (AI-Powered)")
    root.geometry("560x420")
    root.configure(bg="#0f111a")

    style = ttk.Style()
    style.theme_use("default")

    def label(text, y, size=12, bold=False):
        font = ("Consolas", size, "bold" if bold else "normal")
        l = tk.Label(root, text=text, fg="#00ffcc", bg="#0f111a", font=font)
        l.place(x=20, y=y)
        return l

    label("Wi-Fi Threat Detection System (AI-Powered)", 20, 15, True)
    decision = label("AI Decision:", 80, 13, True)
    firewall = label("Firewall Status:", 115, 13, True)
    src = label("Source IP:", 160)
    dst = label("Destination IP:", 190)
    byt = label("Source Bytes:", 220)
    dur = label("Connection Duration:", 250)
    upd = label("Last Update:", 280)

    label("AI Confidence Level", 315)
    bar = ttk.Progressbar(root, length=500, maximum=100)
    bar.place(x=20, y=345)

    def refresh():
        decision.config(text=state["ai_decision"])
        firewall.config(text=state["firewall_action"])
        src.config(text=f"Source IP: {state['src']}")
        dst.config(text=f"Destination IP: {state['dst']}")
        byt.config(text=f"Source Bytes: {state['bytes']}")
        dur.config(text=f"Connection Duration: {state['duration']:.2f}s")
        upd.config(text=f"Last Update: {state['last_update']}")
        bar["value"] = state["confidence"] * 100
        root.after(500, refresh)

    refresh()
    root.mainloop()

# ---------------- MAIN ----------------
if __name__ == "__main__":
    threading.Thread(target=start_sniffing, daemon=True).start()
    launch_dashboard()






