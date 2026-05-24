import random
import time
import asyncio

class SimulationService:
    def __init__(self, callback):
        self.callback = callback
        self.is_running = False

    async def start(self):
        self.is_running = True
        ips = ["192.168.1.10", "192.168.1.15", "10.0.0.5", "172.16.0.20"]

        while self.is_running:
            is_attack = random.random() < 0.2
            src = random.choice(ips)
            dst = "192.168.1.1"

            if is_attack:
                severity = random.choice(["MEDIUM", "HIGH", "CRITICAL"])
                attack_type = random.choice(["DoS Attack", "Brute Force", "Port Scan"])
                probability = random.uniform(0.7, 0.99)
            else:
                severity = "LOW"
                attack_type = "Normal"
                probability = random.uniform(0.01, 0.3)

            event = {
                "timestamp": time.strftime("%H:%M:%S"),
                "src": src,
                "dst": dst,
                "proto": "TCP",
                "severity": severity,
                "prediction": "ATTACK" if is_attack else "NORMAL",
                "probability": probability,
                "attack_type": attack_type,
                "details": {
                    "duration": random.uniform(0, 10),
                    "src_bytes": random.randint(100, 5000),
                    "count": random.randint(1, 200),
                    "serror_rate": random.uniform(0, 1) if is_attack else 0
                }
            }

            # Support both async and sync callbacks
            if asyncio.iscoroutinefunction(self.callback):
                await self.callback(event)
            else:
                self.callback(event)

            await asyncio.sleep(2)

    def stop(self):
        self.is_running = False
