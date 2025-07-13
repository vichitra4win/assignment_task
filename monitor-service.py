import os
import json
from datetime import datetime
import socket

services = ["apache2", "rabbitmq-server", "postgresql"]
host_name = socket.gethostname()

for service in services:
    status_cmd = f"systemctl is-active {service}"
    result = os.popen(status_cmd).read().strip()
    service_status = "UP" if result == "active" else "DOWN"

    payload = {
        "service_name": service,
        "service_status": service_status,
        "host_name": host_name,
        "@timestamp": datetime.utcnow().isoformat() 
    }

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = f"{service}-status-{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(payload, f, indent=2)

    print(f"[✓] Status saved: {filename}")