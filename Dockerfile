FROM mcr.microsoft.com/playwright/python:v1.44.0-jammy

# Install ffmpeg for GIF/Video generation
RUN pip install playwright
RUN playwright install

# Create workspace
WORKDIR /workspace

# Copy Playwright script
COPY preview_generator.py .

# Install Python dependencies if needed
# RUN pip install -r requirements.txt

# Entry point
CMD ["python", "preview_generator.py"]
