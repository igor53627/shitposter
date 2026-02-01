# Deployment

## Local API (FastAPI)

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the API locally:

```bash
uvicorn server:app --host 0.0.0.0 --port 7860
```

Alternatively:

```bash
python3 server.py
```

## Docker

Build and run the container:

```bash
docker build -t shitposter .
docker run -p 7860:7860 shitposter
```

## Web Terminal (Static)

The web terminal is a static page in `web/index.html`. It runs entirely in the
browser with WebCrypto and does not require a backend service.

### GitHub Pages

The Pages workflow copies `web/index.html` plus the Python modules into a flat
`public/` directory so the browser can load the same wordlist and helpers.
Deployments are triggered by pushes to `main`.
