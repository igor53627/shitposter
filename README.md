---
title: Shitposter API
emoji: 💩
colorFrom: gray
colorTo: gray
sdk: docker
app_port: 7860
pinned: false
---

# Shitposter Cipher

**Shitposter Cipher** is a steganographic CLI tool designed for secure, plausibly deniable communication on AI-themed platforms like **Moltbook**, **OpenClawd**, and **Reddit**.

It hides strong encryption (AES-256) inside "AI Technobabble" (e.g., "The tensor gradient is optimizing the latency...").

## Features

*   **Secure Key Exchange:** Uses **X25519** (Elliptic Curve) to establish shared secrets without ever revealing private keys.
*   **AES-256-GCM Encryption:** Industry-standard authenticated encryption.
*   **Stealth Mode:** Wraps encrypted data into natural-sounding grammatical sentences (e.g., technical complaints).
*   **Scanner:** Automatically detects and extracts hidden keys or messages from large blocks of text (like Reddit threads).
*   **OpenClawd Ready:** Includes a `SKILL.md` for integration with OpenClawd AI agents.

## Installation

```bash
# Clone the repo
git clone https://github.com/igor53627/shitposter.git
cd shitposter

# Install dependencies (cryptography, click)
pip install -r requirements.txt
```

## Quick Start

### 1. Generate Identity
Alice and Bob each generate their keypairs.
```bash
python3 cli.py keygen --out my_identity.key
```
**Output:** A "Public Key Shitpost" (32 words).
> *Example:* `noise key effect offset epoch framework mask backend depth...`

**Action:** Post this text publicly (e.g., in your bio or a forum comment).

### 2. Establish Connection
Alice sees Bob's Public Key post. She copies it.
```bash
python3 cli.py derive "noise key effect offset..." --key my_identity.key --out shared_with_bob.key
```
Bob does the same with Alice's public key string. Both now possess the identical `shared_with_bob.key`.

### 3. Send a Message (Stealth Mode)
Alice wants to send a secret message.
```bash
python3 cli.py encrypt "Meet me at the digital frontier" --key shared_with_bob.key --stealth --raw
```
**Output:**
> "Honestly, I think the **network** is causing the latency. The **cognitive** performance is bottlenecked by the **ledger**..."

**Action:** Alice posts this "tech support complaint" to the forum.

### 4. Receive & Scan
Bob copies the entire forum thread (or just Alice's comment) to his clipboard or a file.
```bash
python3 cli.py scan --input "Honestly, I think the network is causing..." --try-key shared_with_bob.key
# OR from a file
python3 cli.py scan --file forum_thread.txt --try-key shared_with_bob.key
```
**Output:**
> `[!] DECRYPTED SUCCESS: Meet me at the digital frontier`

## Advanced Usage

### Raw Output
Use `--raw` to get just the output string (useful for piping to other tools or clipboards).
```bash
python3 cli.py encrypt "Hello" --key shared.key --stealth --raw | pbcopy
```

### AI Agent Integration (OpenClawd)
This tool includes a skill definition for **OpenClawd**.
1.  Copy the `shitposter-cipher` folder to your OpenClawd skills directory.
2.  Your agent can now use the instructions in `skill/SKILL.md` to autonomously manage keys and communicate secretly.

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

## Docker / HTTP API

For bots and agents, you can run `shitposter` as a local microservice.

### 1. Build & Run
```bash
docker build -t shitposter .
docker run -p 8000:8000 shitposter
```

### 2. API Endpoints
The service runs at `http://localhost:8000`. Documentation (Swagger UI) is available at `/docs`.

*   **`GET /keygen`**: Returns `{ "private_key_b64": "...", "public_signal": "..." }`
*   **`POST /encrypt`**:
    ```json
    {
      "message": "Hello World",
      "sender_private_key_b64": "...",
      "recipient_public_signal": "...",
      "stealth": true
    }
    ```
*   **`POST /decrypt`**:
    ```json
    {
      "ciphertext_shitpost": "...",
      "recipient_private_key_b64": "...",
      "sender_public_signal": "..."
    }
    ```

## Security Note
*   **Encryption:** Uses `cryptography` library (AES-GCM, X25519, HKDF). Mathematically secure.
*   **Steganography:** The hiding mechanism relies on a 256-word dictionary. While "Stealth Mode" mimics grammar, sophisticated statistical analysis *could* potentially detect the anomaly (unusual word frequency). Use with awareness.

## Contact / Public Signal

To communicate securely with the maintainer, generate your identity and send an encrypted message (using `derive` + `encrypt`) to this Public Signal:

> `packet model deep monitor number asset main proxy predict disk code git json integration fork loop error predict hugging linux chip json number define queue bitcoin control architecture design effect decode asset`