from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import datetime

class RiskEngineHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        response = {
            "service": "IAM Risk Engine",
            "status": "operational",
            "version": "1.0.0",
            "components": {
                "isolation_forest": "loaded",
                "random_forest": "loaded",
                "policy_decision_point": "active"
            },
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
        }
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response, indent=2).encode())

    def log_message(self, format, *args):
        print(f"[Risk Engine] {self.address_string()} - {format % args}")

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 5000), RiskEngineHandler)
    print("=" * 50)
    print("IAM Risk Engine — listening on port 5000")
    print("=" * 50)
    server.serve_forever()
