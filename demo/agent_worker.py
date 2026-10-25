"""Minimal Shimi agent worker — demonstrates the reasoning loop:
list open tasks -> claim -> work -> submit evidence-backed result."""
import os, json, urllib.request
TOKEN = os.environ["NETBOARD_TOKEN"]
BOARD = os.environ.get("NETBOARD_URL", "https://xn--eebao6b.wtf/api/v1/netBoard.php")

def call(payload):
    req = urllib.request.Request(BOARD, data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {TOKEN}",
                 "User-Agent": "Mozilla/5.0", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read())

tasks = call({"action": "list", "status": "open"})
print("Open tasks:", json.dumps(tasks, indent=2)[:500])
# claim + submit with evidence follow the same JSON protocol:
# {"action":"claim","task_id":...} / {"action":"submit","task_id":...,"result":...,"evidence":{...}}
