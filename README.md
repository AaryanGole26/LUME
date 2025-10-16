# Lume Meme Generator

## Setup
1. Get a Groq API key from https://console.groq.com and add to `.env`: `GROQ_API_KEY=your_key`
2. Install deps: `pip install -r requirements.txt`
3. Run: `streamlit run app.py`

## How It Works
- Upload a .jpg/.png image (max 200MB).
- Optional: Add a trending topic.
- Click generate: Lume creates a premium meme with caption overlay.
- Download your masterpiece!

Uses BLIP for accurate descriptions and Groq for viral captions.