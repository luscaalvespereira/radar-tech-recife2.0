from http.server import BaseHTTPRequestHandler
import json

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        
        response_data = {
            "name": "RADAR TECH RECIFE",
            "status": "online",
            "territory": "Recife / Pernambuco",
            "monitored_nodes": [
                "Porto Digital",
                "CESAR & CESAR School",
                "Edifício O NERD",
                "Sympla Tecnologia Recife",
                "SECTI-PE / FACEPE"
            ],
            "total_captured_baseline": 24,
            "architecture": "Local-First Python Daemon + Vercel Web Dashboard"
        }
        
        self.wfile.write(json.dumps(response_data, ensure_ascii=False, indent=2).encode("utf-8"))

