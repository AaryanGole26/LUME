import streamlit as st
from utils import get_image_description, generate_meme_caption
from PIL import Image, ImageDraw, ImageFont, ImageOps, ExifTags
import os
import requests
from io import BytesIO

st.set_page_config(page_title="Lume", layout="centered", initial_sidebar_state="collapsed")
st.markdown("""
    <style>
    .stApp {
        background-color: #ffffff;
        color: #000000;
    }
    .stButton>button {
        background-color: #2ecc71;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
    }
    .stTextInput>div>input {
        background-color: #f0f0f0;
        color: #000000;
        border: 2px solid #2ecc71;
        border-radius: 5px;
    }
    .stFileUploader {
        border: 2px dashed #2ecc71;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🌟 LumeAI — Meme Generator")

# Premium Layout: Upload or URL above Trend
image_source = st.radio("Select Source", ["Upload Image", "Image URL"])
if image_source == "Upload Image":
    image_input = st.file_uploader("📸 Upload Your Image", type=["jpg", "png"], help="Max 200MB, .jpg/.png only")
    if image_input and image_input.size > 200 * 1024 * 1024:
        st.error("File exceeds 200MB limit!")
        image_input = None
else:
    image_input = st.text_input("📍 Enter Image URL", help="Paste a valid image URL (e.g., https://example.com/image.jpg)")

trend = st.text_input("📊 Trend (Optional)", value="", help="Add a hot topic for extra flair")

if image_input:
    if image_source == "Upload Image":
        st.image(image_input, width='content')
    else:
        try:
            response = requests.get(image_input)
            img = Image.open(BytesIO(response.content))
            st.image(img, width='content')
        except Exception as e:
            st.error(f"Invalid URL or image: {str(e)}")
            image_input = None
    
if st.button("🎨 Create your LUME") and image_input:
    with st.spinner("Crafting your premium meme..."):
        temp_path = "temp.jpg"
        if image_source == "Upload Image":
            with open(temp_path, "wb") as f:
                f.write(image_input.getvalue())
        else:
            response = requests.get(image_input)
            with open(temp_path, "wb") as f:
                f.write(response.content)
        
        # Load image and handle orientation
        img = Image.open(temp_path).convert("RGB")
        try:
            # Extract EXIF data for orientation
            exif = img._getexif()
            if exif:
                orientation = exif.get(ExifTags.TAGS.get(274))  # 274 is Orientation tag
                if orientation == 3:  # 180° rotation
                    img = img.rotate(180, expand=True)
                elif orientation == 6:  # 270° rotation (right)
                    img = img.rotate(270, expand=True)
                elif orientation == 8:  # 90° rotation (left)
                    img = img.rotate(90, expand=True)
        except (AttributeError, KeyError, IndexError):
            # Fallback if no EXIF data (e.g., edited images)
            pass
        
        img.save(temp_path)  # Save corrected orientation
        
        desc = get_image_description(temp_path)
        if "error" in desc.lower():
            st.error(desc)
        else:
            st.info(f"**Scene:** {desc}")
            
            caption = generate_meme_caption(f"{desc}. Incorporate the trend '{trend}' and ensure the caption matches the image's mood with a humorous twist.", trend)
            st.markdown(f'<div class="custom-success">**🌟 Caption:**<br><h3>{caption}</h3></div>', unsafe_allow_html=True)
            
            draw = ImageDraw.Draw(img)
            try:
                # Initial font size based on smaller dimension of image
                initial_size = min(img.width, img.height) // 20  # ~5% of smaller dimension
                font = ImageFont.truetype("arial.ttf", max(10, initial_size))  # Minimum 10
            except:
                font = ImageFont.load_default()
            
            # Dynamic text sizing and positioning with background
            bbox = draw.textbbox((0, 0), caption, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            max_width = img.width * 0.8  # Limit to 80% of image width
            max_height = img.height * 0.2  # Limit to 20% of image height
            
            while (text_width > max_width or text_height > max_height) and font.size > 10:
                font = ImageFont.truetype("arial.ttf", font.size - 5) if font != ImageFont.load_default() else ImageFont.load_default()
                bbox = draw.textbbox((0, 0), caption, font=font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
            
            # Adjust caption position based on corrected orientation (bottom center)
            x = (img.width - text_width) // 2
            y = img.height - text_height - 20
            
            # Add semi-transparent background for better readability
            padding = 10
            bg_box = (x - padding, y - padding, x + text_width + padding, y + text_height + padding)
            draw.rectangle(bg_box, fill=(0, 0, 0, 128))  # Black with 50% opacity
            
            draw.text((x, y), caption, fill="white", font=font, stroke_width=1, stroke_fill="black")  # Reduced stroke for clarity
            
            st.image(img, caption="YOUR LUME MEME!", width='content')
            img.save("lume_output.png")
            
            os.remove(temp_path)
    
    st.download_button("💾 Save your Lume", data=open("lume_output.png", "rb"), file_name="lume_meme.png")