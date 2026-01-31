FROM python:3.9-slim

WORKDIR /app

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Create a non-root user with UID 1000
RUN useradd -m -u 1000 user

COPY requirements.txt .
# Pin cryptography to avoid build issues (prefer binary wheels)
# Install separately to ensure binary wheel preference
RUN pip install --no-cache-dir cryptography==42.0.5
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Switch to the non-root user
USER user

# Expose port 7860
EXPOSE 7860

# Run the server
CMD ["python", "server.py"]
