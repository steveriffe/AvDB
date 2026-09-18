import subprocess
import json
from collections import Counter
from datetime import datetime

print("Fetching Cloud Run request logs for service 'avdb'...")
cmd = [
    "gcloud", "logging", "read",
    'resource.type="cloud_run_revision" AND resource.labels.service_name="avdb" AND logName:"logs/run.googleapis.com%2Frequests"',
    "--limit=2000",
    "--format=json"
]

res = subprocess.run(cmd, capture_output=True, text=True)
if res.returncode != 0:
    print("Error:", res.stderr)
    exit(1)

logs = json.loads(res.stdout)
print(f"Total request log entries analyzed: {len(logs)}")

ips = Counter()
user_agents = Counter()
urls = Counter()
status_codes = Counter()
dates = Counter()

for entry in logs:
    http = entry.get("httpRequest", {})
    ip = http.get("remoteIp", "unknown")
    ua = http.get("userAgent", "unknown")
    url = http.get("requestUrl", "")
    status = http.get("status", 0)
    ts = entry.get("timestamp", "")
    date_str = ts[:10] if ts else "unknown"

    ips[ip] += 1
    user_agents[ua] += 1
    urls[url.split("?")[0]] += 1
    status_codes[status] += 1
    dates[date_str] += 1

print("\n--- Activity by Date ---")
for d, count in sorted(dates.items()):
    print(f"{d}: {count} requests")

print("\n--- Remote IP Addresses ---")
for ip, count in ips.most_common(20):
    print(f"{ip}: {count} requests")

print("\n--- Top User Agents ---")
for ua, count in user_agents.most_common(10):
    print(f"[{count}] {ua[:100]}")

print("\n--- Top Endpoints ---")
for u, count in urls.most_common(15):
    print(f"[{count}] {u}")
