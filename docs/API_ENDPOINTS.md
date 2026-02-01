# API Endpoints

Base server implementation: `server.py` (FastAPI).

## GET /keygen

Generates a new identity.

Response:

```json
{
  "private_key_b64": "<base64>",
  "public_signal": "<32-word signal>"
}
```

## POST /encrypt

Encrypts a message using sender private key and recipient public signal.

Request:

```json
{
  "message": "The eagle has landed.",
  "sender_private_key_b64": "<base64>",
  "recipient_public_signal": "<32-word signal>",
  "stealth": true
}
```

Response:

```json
{
  "shitpost": "<encoded text>"
}
```

## POST /decrypt

Decrypts a message using recipient private key and sender public signal.

Request:

```json
{
  "ciphertext_shitpost": "<encoded text>",
  "recipient_private_key_b64": "<base64>",
  "sender_public_signal": "<32-word signal>"
}
```

Response:

```json
{
  "message": "<plaintext>"
}
```

## POST /scan

Scans free-form text for public keys or messages.

Request:

```json
{
  "text": "<free-form text>",
  "try_shared_key_b64": "<optional base64 shared key>"
}
```

Response:

```json
{
  "found": [
    {
      "type": "public_key",
      "length": 32,
      "signal": "<32-word signal>"
    }
  ]
}
```

## POST /channel/generate

Generates a random symmetric key for broadcast channels.

Response:

```json
{
  "key_b64": "<base64>",
  "key_words": "<32-word signal>"
}
```
