from fastapi import FastAPI, BackgroundTasks
from emailer import send_newsletter_to_all
from google.cloud import firestore

app = FastAPI(title="Daily Newsletter")

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/run-newsletter")
async def run_newsletter(background_tasks: BackgroundTasks):
    """
    Trigger the daily newsletter run.
    Cloud Scheduler will call this endpoint (POST).
    We launch the heavy work in background to quickly return HTTP 200.
    """
    # Kick off background task
    background_tasks.add_task(send_newsletter_to_all)
    return {"status":"started"}
