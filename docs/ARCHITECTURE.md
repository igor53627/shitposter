# Architecture

## Overview

Shitposter Cipher ships three primary interfaces that share the same cryptographic
model:

- **CLI** (`cli.py`) for local workflows.
- **API** (`server.py`) for HTTP usage.
- **Web Terminal** (`web/index.html`) for browser-only usage.

Python interfaces use the shared crypto modules (`crypto.py`, `steg.py`,
`stealth.py`, `fingerprint.py`). The Web Terminal implements the same protocol
in JavaScript using WebCrypto and a JS X25519 implementation.

## Component Map

```
CLI (cli.py) --------------------> Python crypto modules
API (server.py) ------------------> Python crypto modules
Web terminal (web/index.html) ----> Browser crypto (WebCrypto + JS X25519)

Python crypto modules ------------> X25519 + HKDF + AES-256-GCM
Browser crypto -------------------> X25519 + HKDF + AES-256-GCM
```

## Key Flows

### Identity Generation

1. Generate an X25519 private key.
2. Derive the public key bytes.
3. Encode the public key into a 32-word public signal.

### Session Derivation

1. Perform X25519 ECDH to obtain a shared secret.
2. Sort the two public keys to build a deterministic HKDF context.
3. Derive 64 bytes from HKDF SHA-256.
4. Split into directional keys (`tx`, `rx`) based on public key ordering.

### Encrypt / Decrypt

- **Encrypt:** AES-256-GCM with a random 12-byte nonce. Output is encoded into
  the 256-word dictionary and optionally wrapped with stealth text.
- **Decrypt:** Decode the word list back to bytes, then AES-256-GCM decrypt
  using the directional `rx` key.
