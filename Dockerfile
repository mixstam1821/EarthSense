# ==============================================
# 🌍 EarthSense - Interactive Climate Dashboard
# Author: Dr. Michael Stamatis
# ==============================================

# 1️⃣ Use an official lightweight Python base image
FROM python:3.11-slim

# 2️⃣ Set working directory
WORKDIR /app

# 3️⃣ Install system dependencies (for numpy, pandas, xarray, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libhdf5-dev \
    libnetcdf-dev \
    && rm -rf /var/lib/apt/lists/*

# 4️⃣ Copy requirements first (for Docker caching efficiency)
COPY requirements.txt .

# 5️⃣ Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6️⃣ Copy the rest of the app
COPY . .

# 7️⃣ Ensure start.sh is executable
RUN chmod +x start.sh

# 8️⃣ Expose the app port (adjust if needed)
EXPOSE 9797

# 9️⃣ Default command to run the app
CMD ["bash", "start.sh"]
