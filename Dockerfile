
FROM python:3.10-slim


WORKDIR /app

# 3. System dependencies (sometimes needed for building Python packages like chroma)
RUN apt-get update && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy ONLY the requirements file first. 
# This is a Docker trick to cache the installation step and make future builds much faster!
COPY requirements.txt .

# 5. Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of your application code into the container
COPY . .

# 7. Expose the port that Uvicorn/FastAPI will run on
EXPOSE 8000

# 8. The command to start the server when the container launches
# Notice we use 0.0.0.0 so it is accessible from outside the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]