import time
from collections import defaultdict
from scapy.all import IP, TCP
import numpy as np

class PacketProcessor:
    def __init__(self):
        self.connections = defaultdict(lambda: {
            "start_time": time.time(),
            "src_bytes": 0,
            "packets": 0,
            "syn_errors": 0
        })
        self.recent_connections = []

    def process_packet(self, packet):
        if IP not in packet:
            return None

        src = packet[IP].src
        dst = packet[IP].dst
        proto = packet[IP].proto

        key = (src, dst, proto)
        conn = self.connections[key]

        size = len(packet)
        conn["packets"] += 1
        conn["src_bytes"] += size

        if TCP in packet and packet[TCP].flags == "S":
            conn["syn_errors"] += 1

        now = time.time()
        self.recent_connections.append((now, key))
        self.recent_connections[:] = [(t, k) for t, k in self.recent_connections if now - t < 2]

        duration = now - conn["start_time"]
        count = len(self.recent_connections)
        serror_rate = conn["syn_errors"] / max(1, conn["packets"])

        # Construct feature vector for Random Forest (9 features matching original training)
        features = np.array([[
            duration,
            conn["src_bytes"],
            0, 0, 0, 0, # Placeholder features (unused in basic RF but required for input shape)
            count,
            count,
            serror_rate
        ]])

        return {
            "src": src,
            "dst": dst,
            "proto": proto,
            "size": size,
            "duration": duration,
            "count": count,
            "serror_rate": serror_rate,
            "features": features
        }

processor = PacketProcessor()
