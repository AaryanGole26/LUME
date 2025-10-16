import os
from dotenv import load_dotenv
from groq import Groq
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import requests
from io import BytesIO
import streamlit as st  # Add this

load_dotenv()

# Cache BLIP model globally (loads once, shared across sessions)
@st.cache_resource
def load_blip_model():
    processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base", use_fast=True)
    model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
    return processor, model

def get_image_description(image_url_or_path):
    try:
        processor, model = load_blip_model()  # Cached!
        
        if image_url_or_path.startswith("http"):
            response = requests.get(image_url_or_path)
            image = Image.open(BytesIO(response.content))
        else:
            image = Image.open(image_url_or_path)
        
        inputs = processor(image, return_tensors="pt")
        out = model.generate(**inputs)
        return processor.decode(out[0], skip_special_tokens=True)
    except Exception as e:
        return f"Image error: {str(e)}"

def generate_meme_caption(description, trend=""):
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return "❌ Add GROQ_API_KEY=your_key to .env file!"
    
    client = Groq(api_key=api_key)
    prompt = f"Turn this image description into an edgy, viral meme caption: '{description}'. Incorporate: '{trend}'. Short and punchy."
    
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
            max_tokens=50
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Groq error: {str(e)}"