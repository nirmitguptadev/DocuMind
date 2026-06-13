# ==========================================
# STAGE 1: The Builder (Heavy and Temporary)
# ==========================================
FROM python:3.10-slim AS builder

WORKDIR /app

# Install system dependencies required for compiling Python packages
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create a Python virtual environment inside the builder
RUN python -m venv /opt/venv
# Activate the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install them INTO the virtual environment
COPY requirements.txt .

# Notice there is only one 'RUN' here, and we added the CPU flag!
RUN pip install --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu

# ==========================================
# STAGE 2: The Final Runner (Light and Fast)
# ==========================================
FROM python:3.10-slim

WORKDIR /app

# COPY the completed virtual environment from the "builder" stage!
COPY --from=builder /opt/venv /opt/venv

# Activate the virtual environment in this new container
ENV PATH="/opt/venv/bin:$PATH"

# Copy your actual application code
COPY . .

# Make the run script executable
RUN chmod +x run.sh

# Expose the API and Streamlit ports (Hugging Face Spaces uses 7860)
EXPOSE 8000
EXPOSE 7860

# Start both services using the run script
CMD ["bash", "run.sh"]