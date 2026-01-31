import click
import os
import json
import base64
from crypto import ShitposterCrypto
from steg import encode_bytes, decode_string

CRYPTO = ShitposterCrypto()

def load_key_for_mode(path, mode):
    """
    Loads a key from file. Handles both:
    1. Session JSON (tx/rx keys)
    2. Raw Bytes (Channel key) 
    
    mode: 'encrypt' (returns tx), 'decrypt' (returns rx)
    """
    with open(path, 'rb') as f:
        content = f.read()
        
    # Try JSON first (Session Key)
    try:
        data = json.loads(content)
        if 'tx' in data and 'rx' in data:
            key_b64 = data['tx'] if mode == 'encrypt' else data['rx']
            return base64.b64decode(key_b64)
    except:
        pass
        
    # Fallback: Raw Bytes (Channel Key or Legacy)
    if len(content) == 32:
        return content
    
    raise ValueError("Invalid key file format.")

@click.group()
def cli():
    """Shitposter Cipher CLI - Secure communication for AI Agents."""
    pass

@cli.command()
@click.option('--out', default='private.key', help='Output file for private key.')
def keygen(out):
    """Generate a new keypair. Prints Public Key as a shitpost."""
    priv, pub_bytes = CRYPTO.generate_keypair()
    
    with open(out, 'wb') as f:
        f.write(CRYPTO.get_private_bytes(priv))
    
    os.chmod(out, 0o600)
    
    pub_shitpost = encode_bytes(pub_bytes)
    
    click.echo("\n[+] Private Key saved to: " + out)
    click.echo("[+] YOUR PUBLIC KEY (Post this on OpenClawd/Moltbook):")
    click.echo("-" * 60)
    click.echo(pub_shitpost)
    click.echo("-" * 60)

@cli.command()
@click.argument('peer_shitpost')
@click.option('--key', default='private.key', help='Your private key file.')
@click.option('--out', default='session.json', help='Output file for session keys.')
def derive(peer_shitpost, key, out):
    """Derive session keys from Peer's Public Key Shitpost."""
    if not os.path.exists(key):
        click.echo("Private key not found!", err=True)
        return

    with open(key, 'rb') as f:
        priv_bytes = f.read()
    
    priv_key = CRYPTO.load_private_key(priv_bytes)
    
    try:
        # Check if input is likely Base64 (no spaces)
        if " " not in peer_shitpost.strip():
            try:
                peer_pub_bytes = base64.b64decode(peer_shitpost)
            except:
                peer_pub_bytes = decode_string(peer_shitpost)
        else:
            peer_pub_bytes = decode_string(peer_shitpost)

        if len(peer_pub_bytes) != 32:
             click.echo(f"[-] Error: Decoded public key is {len(peer_pub_bytes)} bytes (expected 32).")
             return

        keys = CRYPTO.derive_shared_secret(priv_key, peer_pub_bytes)
        
        # Save as JSON
        output_data = {
            'tx': base64.b64encode(keys['tx']).decode('utf-8'),
            'rx': base64.b64encode(keys['rx']).decode('utf-8')
        }
        
        with open(out, 'w') as f:
            json.dump(output_data, f, indent=2)
        os.chmod(out, 0o600)
        
        from fingerprint import get_fingerprint
        fp = get_fingerprint(keys)
        
        click.echo(f"[+] Session established! Keys saved to {out}")
        click.echo(f"[!] SESSION FINGERPRINT: {fp}")
        click.echo("    (Verify this matches your peer's screen to prevent MITM)")
    except Exception as e:
        click.echo(f"[-] Error deriving secret: {e}")

@cli.command()
@click.argument('message')
@click.option('--key', default='session.json', help='Session file or Shared secret.')
@click.option('--stealth', is_flag=True, help='Wrap output in natural-sounding sentences.')
@click.option('--raw', is_flag=True, help='Output only the result string (no decoration).')
def encrypt(message, key, stealth, raw):
    """Encrypt a message into a shitpost."""
    if not os.path.exists(key):
        if not raw: click.echo("Key file not found!", err=True)
        return

    try:
        shared_key = load_key_for_mode(key, 'encrypt')
    except Exception as e:
        click.echo(f"[-] Error loading key: {e}", err=True)
        return

    encrypted_payload = CRYPTO.encrypt_message(shared_key, message)
    
    from steg import WORDLIST
    words = []
    for byte in encrypted_payload:
        words.append(WORDLIST[byte])
        
    if stealth:
        from stealth import generate_stealth_text
        final_output = generate_stealth_text(words)
    else:
        final_output = " ".join(words)
    
    if raw:
        click.echo(final_output)
    else:
        click.echo("\n[+] ENCRYPTED MESSAGE (Post this):")
        click.echo("-" * 60)
        click.echo(final_output)
        click.echo("-" * 60)

@cli.command()
@click.argument('ciphertext')
@click.option('--key', default='session.json', help='Session file or Shared secret.')
def decrypt(ciphertext, key):
    """Decrypt a shitpost back to text."""
    if not os.path.exists(key):
        click.echo("Key file not found!", err=True)
        return

    try:
        shared_key = load_key_for_mode(key, 'decrypt')
    except Exception as e:
        click.echo(f"[-] Error loading key: {e}", err=True)
        return

    try:
        payload = decode_string(ciphertext)
        plaintext = CRYPTO.decrypt_message(shared_key, payload)
        click.echo("\n[+] DECRYPTED MESSAGE:")
        click.echo("-" * 60)
        click.echo(plaintext)
        click.echo("-" * 60)
    except Exception as e:
        click.echo(f"[-] Decryption failed: {e}")
        click.echo("    (Wrong key? Corrupted shitpost?)")

@cli.command()
@click.argument('input_text', required=False)
@click.option('--file', help='Read text from a file.')
@click.option('--try-key', help='Try to decrypt found messages with this session/key.')
def scan(input_text, file, try_key):
    """Scan a large block of text for hidden shitposts."""
    from steg import WORDLIST
    
    # Load content
    content = ""
    if file:
        with open(file, 'r') as f:
            content = f.read()
    elif input_text:
        content = input_text
    else:
        import sys
        if not sys.stdin.isatty():
            content = sys.stdin.read()
        else:
            click.echo("Please provide text to scan or use --file.", err=True)
            return

    # Load key if provided
    shared_key_bytes = None
    if try_key and os.path.exists(try_key):
        try:
            shared_key_bytes = load_key_for_mode(try_key, 'decrypt')
        except:
            pass

    import re
    word_set = set(WORDLIST)
    cleaned = re.sub(r'[^a-zA-Z\s]', ' ', content)
    words = cleaned.lower().split()
    
    candidates = []
    # Sliding window/Run logic
    # Also collect ALL valid words for Sparse/Stealth mode
    all_valid_words = []
    current_sequence = []
    
    for w in words:
        if w in word_set:
            current_sequence.append(w)
            all_valid_words.append(w)
        else:
            if current_sequence:
                candidates.append(current_sequence)
                current_sequence = []
    if current_sequence:
        candidates.append(current_sequence)

    # Add the sparse sequence as a candidate if it's long enough
    if len(all_valid_words) > 12:
        # Mark it as sparse for the UI? 
        # For simplicity, we just append it. But let's check if it's identical to a contiguous one.
        # If the text was purely contiguous, unique_candidates logic handles it.
        candidates.append(all_valid_words)

    unique_candidates = []
    seen_seqs = set()
    for seq in candidates:
        seq_tuple = tuple(seq)
        if seq_tuple not in seen_seqs:
            unique_candidates.append(seq)
            seen_seqs.add(seq_tuple)

    found = 0
    print(f"\n[+] Scanning {len(words)} words for anomalies...\n")

    for seq in unique_candidates:
        length = len(seq)
        if length < 12: continue
            
        found += 1
        seq_str = " ".join(seq)
        
        # Heuristic: Is this a dense run or a sparse collection?
        # If the original text length is roughly same as seq length -> Dense.
        # If original text is huge (1000 words) and seq is small (20) -> Sparse.
        # But we don't have original text mapping here easily.
        
        if length == 32:
            print(f"[*] POTENTIAL PUBLIC KEY (32 words):")
            print(f"    {seq_str[:50]}... (truncated)")
            
        else:
            print(f"[*] POTENTIAL MESSAGE ({length} words):")
            print(f"    {seq_str[:50]}... (truncated)")
            if length > 100 or (len(words) > length * 2):
                 print(f"    (Note: This is a sparse match. Might be false positive if scanning normal text.)")
            
            if shared_key_bytes:
                try:
                    payload = decode_string(seq_str)
                    plaintext = CRYPTO.decrypt_message(shared_key_bytes, payload)
                    print(f"    [!] DECRYPTED SUCCESS: {plaintext}\n")
                except:
                    print(f"    [-] Decryption failed with provided key.\n")

    if found == 0:
        print("[-] No valid shitpost sequences found.")

@cli.command()
@click.argument('input_text', required=False)
@click.option('--file', help='Read text from a file.')
@click.option('--key', required=True, help='Your private key.')
@click.option('--welcome-msg', default="Connection verified.", help='Message to encrypt.')
@click.option('--stealth/--no-stealth', default=True, help='Use stealth mode.')
def auto_reply(input_text, file, key, welcome_msg, stealth):
    """Scan for public keys and generate encrypted replies."""
    from steg import WORDLIST
    from stealth import generate_stealth_text
    
    if not os.path.exists(key):
        click.echo("Private key not found!", err=True)
        return
    with open(key, 'rb') as f:
        priv_bytes = f.read()
    host_priv_key = CRYPTO.load_private_key(priv_bytes)

    content = ""
    if file:
        with open(file, 'r') as f:
            content = f.read()
    elif input_text:
        content = input_text
    else:
        import sys
        if not sys.stdin.isatty():
            content = sys.stdin.read()
    
    import re
    word_set = set(WORDLIST)
    cleaned = re.sub(r'[^a-zA-Z\s]', ' ', content)
    words = cleaned.lower().split()
    
    candidates = []
    current_sequence = []
    for w in words:
        if w in word_set:
            current_sequence.append(w)
        else:
            if current_sequence:
                candidates.append(current_sequence)
                current_sequence = []
    if current_sequence:
        candidates.append(current_sequence)

    click.echo(f"[*] Analyzing {len(candidates)} sequences...")
    replies = []
    
    for seq in candidates:
        if len(seq) == 32:
            peer_pub_str = " ".join(seq)
            peer_pub_bytes = decode_string(peer_pub_str)
            
            # Derive directional keys
            keys = CRYPTO.derive_shared_secret(host_priv_key, peer_pub_bytes)
            # Use TX key to reply
            tx_key = keys['tx']
            
            encrypted_payload = CRYPTO.encrypt_message(tx_key, welcome_msg)
            raw_words = [WORDLIST[b] for b in encrypted_payload]
            if stealth:
                final_output = generate_stealth_text(raw_words)
            else:
                final_output = " ".join(raw_words)
            
            replies.append({
                'peer_prefix': seq[0] + "..." + seq[-1],
                'reply': final_output
            })
            
    if not replies:
        click.echo("[-] No public keys found.")
        return

    for i, r in enumerate(replies):
        click.echo(f"--- Reply {i+1} ---")
        click.echo(r['reply'])
        click.echo("")

@cli.group()
def util():
    """Utility commands."""
    pass

@util.command()
@click.argument('file', type=click.Path(exists=True))
def bytes_to_words(file):
    with open(file, 'rb') as f:
        data = f.read()
    if len(data) != 32:
        click.echo(f"[-] Warning: File is {len(data)} bytes.", err=True)
    from steg import encode_bytes
    click.echo(encode_bytes(data))

@util.command()
@click.argument('words')
@click.option('--out', default='channel.key', help='Output file.')
def words_to_bytes(words, out):
    from steg import decode_string
    data = decode_string(words)
    if len(data) != 32:
        click.echo(f"[-] Warning: Result is {len(data)} bytes.", err=True)
    with open(out, 'wb') as f:
        f.write(data)
    os.chmod(out, 0o600)
    click.echo(f"[+] Saved {len(data)} bytes to {out}")

@util.command()
@click.option('--out', default='channel.key', help='Output file.')
def generate_channel_key(out):
    key = os.urandom(32)
    with open(out, 'wb') as f:
        f.write(key)
    os.chmod(out, 0o600)
    from steg import encode_bytes
    words = encode_bytes(key)
    click.echo(f"[+] Generated Channel Key: {out}")
    click.echo("[+] Word Representation:")
    click.echo(words)

if __name__ == '__main__':
    cli()