from scapy.all import sniff
import threading
import time
from app.core.processor import processor
from app.services.prediction import prediction_service
from app.services.severity import severity_service

class SnifferService:
    def __init__(self, event_callback):
        self.callback = event_callback
        self.stop_event = threading.Event()
        self.thread = None

    def _packet_handler(self, packet):
        processed = processor.process_packet(packet)
        if processed:
            prediction, probability = prediction_service.predict(processed["features"])
            severity = severity_service.calculate(probability, processed)
            attack_type = severity_service.get_attack_type(prediction, processed)
            
            event = {
                "timestamp": time.strftime("%H:%M:%S"),
                "src": processed["src"],
                "dst": processed["dst"],
                "proto": str(processed["proto"]),
                "severity": severity,
                "prediction": "ATTACK" if prediction == 1 else "NORMAL",
                "probability": probability,
                "attack_type": attack_type,
                "details": {k: v for k, v in processed.items() if k != "features"}
            }
            self.callback(event)

    def start(self):
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()

    def _run(self):
        sniff(filter="ip", prn=self._packet_handler, stop_filter=lambda x: self.stop_event.is_set(), store=False)

    def stop(self):
        self.stop_event.set()
