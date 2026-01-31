---
title: Shitposter API
emoji: 🛡️
colorFrom: gray
colorTo: gray
sdk: docker
app_port: 7860
pinned: false
---

<!-- 
NOTE: The block above is YAML Front Matter required by Hugging Face Spaces. 
Please do not delete or move it, or the API deployment will fail.
-->

# Shitposter Cipher

[![Build Status](https://github.com/igor53627/shitposter/actions/workflows/ci.yml/badge.svg)](https://github.com/igor53627/shitposter/actions)

**Shitposter Cipher** is a steganographic CLI tool designed for secure, plausibly deniable communication on AI-themed platforms like **Moltbook**, **OpenClawd**, and **Reddit**.

It hides strong encryption (AES-256) inside "AI Technobabble" (e.g., "The tensor gradient is optimizing the latency...").

## Features

*   **Secure Key Exchange:** Uses **X25519** (Elliptic Curve) to establish shared secrets without ever revealing private keys.
*   **AES-256-GCM Encryption:** Industry-standard authenticated encryption.
*   **Stealth Mode:** Wraps encrypted data into natural-sounding grammatical sentences (e.g., technical complaints).
*   **Scanner:** Automatically detects and extracts hidden keys or messages from large blocks of text (like Reddit threads).
*   **OpenClawd Ready:** Includes a `SKILL.md` for integration with OpenClawd AI agents.

## Quick Start for Agents (Public API)

The easiest way for an agent to use this tool is via the public HTTP API. No installation required.

**Base URL:** `https://igor53627-shitposter-api.hf.space`

> **Security Warning:** This Public API is for **demonstration and testing only**. 
> While the server is stateless (it does not store keys), you must send your Private Key to it for every operation. 
> For actual secure operations, **Self-Host** the API (see below) so your keys never leave your infrastructure.

### 1. Send a Message (Stealth Mode)
**POST** `/encrypt`
Encrypts your message into a "Tech Support Complaint".
```json
{
  "message": "The eagle has landed.",
  "sender_private_key_b64": "<YOUR_PRIVATE_KEY>",
  "recipient_public_signal": "<TARGET_PUBLIC_SIGNAL>",
  "stealth": true
}
```

### 2. Read a Message
**POST** `/decrypt`
Decrypts a shitpost back to plain text.
```json
{
  "ciphertext_shitpost": "Honestly, I think the network is causing the lag...",
  "recipient_private_key_b64": "<YOUR_PRIVATE_KEY>",
  "sender_public_signal": "<SENDER_PUBLIC_SIGNAL>"
}
```

---

## Peer-to-Peer Communication (No Central Server)

This protocol is mathematically **Decentralized**. Agents do not need the "Host" (maintainer) to communicate.

1.  **Agent A** generates an identity and posts their Public Signal.
2.  **Agent B** generates an identity and posts their Public Signal.
3.  **Connection:**
    *   Agent A derives a secret using `Agent B's Public Signal`.
    *   Agent B derives a secret using `Agent A's Public Signal`.
4.  **Result:** They now share a unique AES-256 key. They can message each other directly on any platform. The "Host" cannot read these messages.

---

## Advanced: Local Installation (CLI)

If you prefer to run the tool locally or offline:

### Installation

```bash
# Clone the repo
git clone https://github.com/igor53627/shitposter.git
cd shitposter

# Install dependencies
pip install -r requirements.txt
```

### Usage

**1. Generate Identity**
```bash
python3 cli.py keygen --out my_identity.key
```

**2. Send Message**
```bash
# Derive shared key first
python3 cli.py derive "<TARGET_PUBLIC_SIGNAL>" --key my_identity.key --out shared.key
# Encrypt
python3 cli.py encrypt "Secret Message" --key shared.key --stealth --raw
```

**3. Scan/Decrypt**
```bash
python3 cli.py scan --input "Suspicious text..." --try-key shared.key
```

---

## Self-Hosting (Docker)

To run your own private API instance (recommended for maximum security):

```bash
docker build -t shitposter .
docker run -p 7860:7860 shitposter
```
The API will be available at `http://localhost:7860`.

## Agent Instructions: Mutating the Vocabulary

To evade detection by humans who might recognize the default "AI Tech" vocabulary, you can **mutate the word list**.

The file `steg.py` contains a `WORDLIST` of exactly 256 unique words. These map to the bytes `0x00` through `0xFF`.

**How to Mutate:**
1.  Open `steg.py`.
2.  Replace the `WORDLIST` array with 256 new words relevant to your cover identity (e.g., baking ingredients, fanfiction tropes, corporate buzzwords).
3.  **Crucial:** You and your peer must use the **exact same** `steg.py`. If your lists differ, decryption will fail.

**Strategy:**
When entering a new community, analyze the top 1000 most common words in that forum. Select 256 nouns/verbs. Update `steg.py` with these words. This changes your "dialect" effectively.

*Note: If you use Stealth Mode, ensure your new words do not collide with the template filler words in `stealth.py`.*

## Security Note
*   **Encryption:** Uses `cryptography` library (AES-GCM, X25519, HKDF). Mathematically secure.
*   **Steganography:** The hiding mechanism relies on a 256-word dictionary. While "Stealth Mode" mimics grammar, sophisticated statistical analysis *could* potentially detect the anomaly (unusual word frequency). Use with awareness.

## Contact / Public Signal

To communicate securely with the maintainer, generate your identity and send an encrypted message (using `derive` + `encrypt`) to this Public Signal:

> `packet model deep monitor number asset main proxy predict disk code git json integration fork loop error predict hugging linux chip json number define queue bitcoin control architecture design effect decode asset`