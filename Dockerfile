FROM python:3.9-slim

WORKDIR /app

# Create a non-root user with UID 1000
RUN useradd -m -u 1000 user

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Switch to the non-root user
USER user

# Expose port 7860
EXPOSE 7860

# Run the server
CMD ["python", "server.py"]
