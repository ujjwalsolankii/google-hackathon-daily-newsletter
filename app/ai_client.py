# app/ai_client.py
import logging
from typing import List, Dict

# Try to import Vertex AI SDK
try:
    from google.cloud import aiplatform
    HAS_AIP = True
except Exception:
    HAS_AIP = False

# Model name to use if the SDK supports the high-level helper
MODEL = "text-bison@001"

def _simple_fallback_html(news_items: List[Dict]) -> str:
    """
    Build a simple HTML newsletter using the RSS summaries.
    This is a deterministic fallback when Vertex AI helper isn't available.
    """
    parts = []
    parts.append("<div style='font-family: Arial, sans-serif; max-width:600px; margin:auto;'>")
    parts.append("<p><strong>Today's headlines</strong></p>")
    for it in news_items:
        title = it.get("title", "No title")
        summary = it.get("summary") or ""
        link = it.get("link", "#")
        parts.append(f"<p><strong>{title}</strong><br/>{summary} <br/><a href='{link}'>Read more</a></p>")
    parts.append("<hr/><p style='font-size:12px;color:#666'>To unsubscribe, remove your email from the subscribers collection.</p>")
    parts.append("</div>")
    return "\n".join(parts)

def generate_newsletter_text(news_items: List[Dict]) -> str:
    """
    Try to use Vertex AI high-level helper to generate newsletter HTML.
    If the helper/class isn't available in this environment, return fallback HTML.
    Returns: HTML string
    """
    if HAS_AIP:
        try:
            # Initialize with defaults (Cloud Run uses ADC - service account)
            # Optionally specify project and location if you want:
            # aiplatform.init(project="YOUR_PROJECT_ID", location="us-central1")
            # Try to use TextGenerationModel helper if available
            TextGen = getattr(aiplatform, "TextGenerationModel", None)
            if TextGen:
                logging.info("Using aiplatform.TextGenerationModel for generation.")
                aiplatform.init()  # safe to call; uses ADC on Cloud Run
                model = TextGen.from_pretrained(MODEL)
                prompt = "Write a short HTML newsletter with 4-6 short paragraphs summarizing these headlines. " \
                         "Do not invent facts; include the source link in each paragraph.\n\nHeadlines:\n"
                for it in news_items:
                    prompt += f"- {it.get('title','')}: {it.get('link','')}\n"
                response = model.predict(prompt, max_output_tokens=512, temperature=0.2)
                return str(response)
            else:
                logging.warning("aiplatform.TextGenerationModel not found on this google-cloud-aiplatform version.")
        except Exception as e:
            logging.exception("Vertex AI call failed; falling back to simple summarizer.")
    else:
        logging.warning("google.cloud.aiplatform not available; using fallback summarizer.")

    # Fallback path
    return _simple_fallback_html(news_items)
