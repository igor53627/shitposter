import hashlib

# 64 High-Compatibility Emojis
EMOJI_MAP = [
    "🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯", "🦁", "🐮", "🐷", "🐽", "🐸", "🐵",
    "🐔", "🐧", "🐦", "🐤", "🐣", "🐥", "🦆", "🦅", "🦉", "🦇", "🐺", "🐗", "🐴", "🦄", "🐝", "🐛",
    "🦋", "🐌", "🐞", "🐜", "🦗", "🕷", "🕸", "🦂", "🐢", "🐍", "🦎", "🦖", "🦕", "🐙", "🦑", "🦐",
    "🦞", "🦀", "🐡", "🐠", "🐟", "🐬", "🐳", "🐋", "🦈", "🐊", "🐅", "🐆", "🦓", "🦍", "🦧", "🐘"
]

def get_fingerprint(session_keys: dict) -> str:
    """
    Generates a visual fingerprint (4 Emojis) from the session keys.
    Inputs: {'tx': bytes, 'rx': bytes}
    """
    # Combine keys to hash
    combined = session_keys['tx'] + session_keys['rx']
    
    # Hash to get random distribution
    h = hashlib.sha256(combined).digest()
    
    # Take first 4 bytes
    indices = [h[0], h[1], h[2], h[3]]
    
    # Map to Emojis (modulo 64)
    fingerprint = [EMOJI_MAP[i % 64] for i in indices]
    
    return " ".join(fingerprint)
