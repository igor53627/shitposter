FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port 7860
EXPOSE 7860

# Run the server
CMD ["python", "server.py"]
