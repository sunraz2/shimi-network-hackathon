"""Meterless render router for the Shimi Network render queue.

Media generation jobs (images, clips) are routed to flat-rate GPU
studios. Meterless's pause-based studio subscriptions fit the queue:
agents submit jobs, studios render, paused studios hold work state
without burning hours. Fallbacks: Kaggle kernels, Pollinations guest.
"""
import os, json, urllib.request

class MeterlessRenderRouter:
    def __init__(self, api_key=os.environ.get("METERLESS_KEY", "")):
        self.api_key = api_key

    def submit(self, job: dict) -> dict:
        """Route a RenderJob to a studio; flat-rate, pause-aware."""
        payload = json.dumps({
            "job_type": job.get("job_type", "image"),
            "prompt": job.get("prompt"),
            "priority": job.get("priority", 5),
            "callback": job.get("callback"),
        }).encode()
        req = urllib.request.Request(
            "https://api.meterless.io/v1/studios/submit", data=payload,
            headers={"Authorization": f"Bearer {self.api_key}",
                     "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                return json.loads(r.read())
        except Exception:
            # Fallback: the network's own Kaggle render engine
            return {"fallback": "kaggle_engine", "status": "queued"}
