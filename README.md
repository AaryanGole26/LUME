# LUMI

Welcome to **LUME**, an AI-powered meme generator that transforms your images into hilarious memes with dynamic captions! Using the BLIP model for image description and the Groq API for witty captions, this Streamlit app lets you upload images, add trending topics, and create shareable memes. Deployed on Render at [https://lume-ai-l9ji.onrender.com](https://lume-ai-l9ji.onrender.com), it can also be installed locally for offline use.

---

## Features
- **Image Upload:** Upload JPG or PNG images (max 200MB).
- **URL Support:** Generate memes from online image URLs.
- **Dynamic Captions:** AI-generated captions tailored to image content and trends.
- **Orientation Handling:** Automatically adjusts captions for rotated images (90°, 180°, 270°).
- **Downloadable Output:** Save your memes as PNG files.
- **Trend Integration:** Add hot topics (e.g., "Twitter Drama") for extra flair.

  ---

## Installation

### Prerequisites
- Python 3.12+
- Pip (Python package manager)
- A Groq API key (sign up at [groq.com](https://console.groq.com))

### Steps:

1. **Clone the Repository:**
   ```
   git clone https://github.com/yourusername/lumeai-meme-generator.git
   cd lumeai-meme-generator
   ```
2. **Install Dependencies:**
   ```
   pip install -r requirements.txt
   ```
3. **Set Up Environment Variables:**
   Create a .env file:
   ```
   GROQ_API_KEY=your_groq_api_key
   ```
4. **Run Locally:**
   Start the Streamlit app:
   ```
    streamlit run app.py
   ```
5. **Access it at http://localhost:8501**

---

## Usage

**Select Source:** 

Choose "Upload Image" to upload a file or "Image URL" to enter a link.

**Add Trend (Optional):**

Input a trend (e.g., "Twitter Drama") for a themed caption.

**Generate Lume:**

Click "Create Lume Meme" to process the image and display the result.

**Download:**

Save the meme using the "Save your Lume" button.

---

## Contributing
We welcome contributions! To get started:

Fork the repository.
Create a branch: git checkout -b feature/your-feature.
Commit changes: git commit -m "Add your feature".
Push to GitHub: git push origin feature/your-feature.
Open a Pull Request.


