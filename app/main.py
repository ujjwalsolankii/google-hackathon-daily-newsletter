from fastapi import FastAPI, BackgroundTasks
from emailer import send_newsletter_to_all

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/run-newsletter")
async def run_newsletter(background_tasks: BackgroundTasks):
    background_tasks.add_task(send_newsletter_to_all)
    return {"status": "newsletter started"}
