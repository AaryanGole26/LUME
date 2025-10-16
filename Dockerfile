FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for image processing and compilation
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libjpeg-dev \
    libpng-dev \
    libfreetype6-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy all application files
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt \
    && pip3 check  # Verify dependencies

# Expose port (optional, Render uses $PORT)
EXPOSE 8501

# Health check (optional, ensure Streamlit version supports it)
HEALTHCHECK --interval=30s --timeout=3s \
    CMD curl --fail http://localhost:${PORT:-8501}/_stcore/health || exit 1

# Run the Streamlit app with dynamic port
ENTRYPOINT ["sh", "-c", "streamlit run app.py --server.port ${PORT:-8501} --server.address 0.0.0.0"]
