from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from typing import Optional, List
import base64
import os

from crypto import ShitposterCrypto
from steg import encode_bytes, decode_string, WORDLIST
from stealth import generate_stealth_text

app = FastAPI(
    title="Shitposter Cipher API",
    description="Microservice for AI Agent Secure Communication",
    version="1.0.0"
)

CRYPTO = ShitposterCrypto()

class KeyGenResponse(BaseModel):
    private_key_b64: str
    public_signal: str

class EncryptRequest(BaseModel):
    message: str
    sender_private_key_b64: str
    recipient_public_signal: str
    stealth: bool = True

class DecryptRequest(BaseModel):
    ciphertext_shitpost: str
    recipient_private_key_b64: str
    sender_public_signal: str

class ScanRequest(BaseModel):
    text: str
    try_shared_key_b64: Optional[str] = None

@app.get("/keygen", response_model=KeyGenResponse)
def generate_identity():
    """Generates a new Identity (Private Key + Public Signal)."""
    priv, pub_bytes = CRYPTO.generate_keypair()
    priv_bytes = CRYPTO.get_private_bytes(priv)
    
    return {
        "private_key_b64": base64.b64encode(priv_bytes).decode('utf-8'),
        "public_signal": encode_bytes(pub_bytes)
    }

@app.post("/encrypt")
def encrypt_message(req: EncryptRequest):
    """Encrypts a message using Ephemeral ECDH (Sender Priv + Recipient Pub)."""
    try:
        # Decode inputs
        priv_bytes = base64.b64decode(req.sender_private_key_b64)
        sender_priv = CRYPTO.load_private_key(priv_bytes)
        
        recipient_pub_bytes = decode_string(req.recipient_public_signal)
        
        if len(recipient_pub_bytes) != 32:
            raise HTTPException(status_code=400, detail="Invalid Public Signal (must be 32 bytes)")
            
        # Derive Secret (Returns {'tx': bytes, 'rx': bytes})
        keys = CRYPTO.derive_shared_secret(sender_priv, recipient_pub_bytes)
        
        # Use TX key for encryption
        encrypted_payload = CRYPTO.encrypt_message(keys['tx'], req.message)
        
        # Steganography
        raw_words = [WORDLIST[b] for b in encrypted_payload]
        
        if req.stealth:
            output = generate_stealth_text(raw_words)
        else:
            output = " ".join(raw_words)
            
        return {"shitpost": output}
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/decrypt")
def decrypt_message(req: DecryptRequest):
    """Decrypts a shitpost using Ephemeral ECDH (Recipient Priv + Sender Pub)."""
    try:
        # Decode inputs
        priv_bytes = base64.b64decode(req.recipient_private_key_b64)
        recipient_priv = CRYPTO.load_private_key(priv_bytes)
        
        sender_pub_bytes = decode_string(req.sender_public_signal)
        
        # Derive Secret (Returns {'tx': bytes, 'rx': bytes})
        # Note: derive_shared_secret handles the sort order internally.
        # If I am Recipient (Alice), and Sender is Bob:
        # derive(AlicePriv, BobPub) -> returns Alice's View.
        # Alice's View: 'rx' is the key Bob used to encrypt.
        
        keys = CRYPTO.derive_shared_secret(recipient_priv, sender_pub_bytes)
        
        # Parse Shitpost
        # Note: decode_string handles the stealth/punctuation stripping now
        payload = decode_string(req.ciphertext_shitpost)
        
        # Decrypt using RX key
        plaintext = CRYPTO.decrypt_message(keys['rx'], payload)
        
        return {"message": plaintext}
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Decryption failed: {str(e)}")

@app.post("/scan")
def scan_text(req: ScanRequest):
    """Scans text for public keys or potential messages."""
    import re
    cleaned = re.sub(r'[^a-zA-Z\s]', ' ', req.text)
    words = cleaned.lower().split()
    word_set = set(WORDLIST)
    
    candidates = []
    current_sequence = []
    
    # Simple extraction of valid word runs
    for w in words:
        if w in word_set:
            current_sequence.append(w)
        else:
            if current_sequence:
                candidates.append(current_sequence)
                current_sequence = []
    if current_sequence:
        candidates.append(current_sequence)
        
    results = []
    
    shared_key = None
    if req.try_shared_key_b64:
        shared_key = base64.b64decode(req.try_shared_key_b64)
    
    for seq in candidates:
        if len(seq) < 12: continue
        
        seq_str = " ".join(seq)
        item = {
            "type": "unknown", 
            "length": len(seq),
            "signal": seq_str
        }
        
        if len(seq) == 32:
            item["type"] = "public_key"
        elif len(seq) > 16:
            item["type"] = "message"
            # Try decrypt if key provided
            if shared_key:
                try:
                    payload = decode_string(seq_str)
                    pt = CRYPTO.decrypt_message(shared_key, payload)
                    item["decrypted"] = pt
                except:
                    pass
        
        results.append(item)
        
    return {"found": results}

@app.post("/channel/generate")
def generate_channel_key():
    """Generates a random 32-byte symmetric key for broadcasting."""
    key = os.urandom(32)
    return {
        "key_b64": base64.b64encode(key).decode('utf-8'),
        "key_words": encode_bytes(key)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)
