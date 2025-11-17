from google.cloud import aiplatform

aiplatform.init()

MODEL = "text-bison@001"

def generate_newsletter_text(news_items):
    prompt = "Write a short HTML newsletter summarizing these headlines:\n\n"
    for item in news_items:
        prompt += f"- {item['title']} ({item['link']})\n"

    model = aiplatform.TextGenerationModel.from_pretrained(MODEL)
    response = model.predict(prompt, max_output_tokens=500)
    return str(response)
