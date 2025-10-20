# Use a lightweight Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy everything
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose default port
EXPOSE 7860
RUN chmod +x start.sh

# Run the Bokeh apps
CMD ["bash", "start.sh"]
