import click
import os
from crypto import ShitposterCrypto
from steg import encode_bytes, decode_string

CRYPTO = ShitposterCrypto()

@click.group()
def cli():
    """Shitposter Cipher CLI - Secure communication for AI Agents."""
    pass

@cli.command()
@click.option('--out', default='private.key', help='Output file for private key.')
def keygen(out):
    """Generate a new keypair. Prints Public Key as a shitpost."""
    priv, pub_bytes = CRYPTO.generate_keypair()
    
    # Save private key securely
    with open(out, 'wb') as f:
        f.write(CRYPTO.get_private_bytes(priv))
    
    os.chmod(out, 0o600)
    
    # Encode public key
    pub_shitpost = encode_bytes(pub_bytes)
    
    click.echo("[+] Private Key saved to: " + out)
    click.echo("[+] YOUR PUBLIC KEY (Post this on OpenClawd/Moltbook):")
    click.echo("-" * 60)
    click.echo(pub_shitpost)
    click.echo("-" * 60)

@cli.command()
@click.argument('peer_shitpost')
@click.option('--key', default='private.key', help='Your private key file.')
@click.option('--out', default='shared.key', help='Output file for shared secret.')
def derive(peer_shitpost, key, out):
    """Derive shared secret from Peer's Public Key Shitpost."""
    if not os.path.exists(key):
        click.echo("Private key not found!", err=True)
        return

    with open(key, 'rb') as f:
        priv_bytes = f.read()
    
    priv_key = CRYPTO.load_private_key(priv_bytes)
    
    try:
        peer_pub_bytes = decode_string(peer_shitpost)
        if len(peer_pub_bytes) != 32:
             click.echo(f"[-] Error: Decoded public key is {len(peer_pub_bytes)} bytes (expected 32).")
             click.echo("    Did you copy the full shitpost?")
             return

        shared_secret = CRYPTO.derive_shared_secret(priv_key, peer_pub_bytes)
        
        with open(out, 'wb') as f:
            f.write(shared_secret)
        os.chmod(out, 0o600)
        
        click.echo(f"[+] Shared secret established! Saved to {out}")
    except Exception as e:
        click.echo(f"[-] Error deriving secret: {e}")

@cli.command()
@click.argument('message')
@click.option('--key', default='shared.key', help='Shared secret file.')
@click.option('--stealth', is_flag=True, help='Wrap output in natural-sounding sentences.')
@click.option('--raw', is_flag=True, help='Output only the result string (no decoration).')
def encrypt(message, key, stealth, raw):
    """Encrypt a message into a shitpost."""
    if not os.path.exists(key):
        if not raw: click.echo("Shared key not found! Run 'derive' first.", err=True)
        return

    with open(key, 'rb') as f:
        shared_key = f.read()

    encrypted_payload = CRYPTO.encrypt_message(shared_key, message)
    
    # 1. Get raw words
    from steg import WORDLIST
    words = []
    for byte in encrypted_payload:
        words.append(WORDLIST[byte])
        
    # 2. Format
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
@click.option('--key', default='shared.key', help='Shared secret file.')
def decrypt(ciphertext, key):
    """Decrypt a shitpost back to text."""
    if not os.path.exists(key):
        click.echo("Shared key not found!", err=True)
        return

    with open(key, 'rb') as f:
        shared_key = f.read()

    try:
        payload = decode_string(ciphertext)
        plaintext = CRYPTO.decrypt_message(shared_key, payload)
        click.echo("[+] DECRYPTED MESSAGE:")
        click.echo("-" * 60)
        click.echo(plaintext)
        click.echo("-" * 60)
    except Exception as e:
        click.echo(f"[-] Decryption failed: {e}")
        click.echo("    (Wrong key? Corrupted shitpost?)")

@cli.command()
@click.argument('input_text', required=False)
@click.option('--file', help='Read text from a file (e.g., a saved webpage or log).')
@click.option('--try-key', help='Try to decrypt found messages with this shared key.')
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
        # Read from stdin if no args (allows piping)
        import sys
        if not sys.stdin.isatty():
            content = sys.stdin.read()
        else:
            click.echo("Please provide text to scan or use --file.", err=True)
            return

    # Create a set for O(1) lookups
    word_set = set(WORDLIST)
    
    # Normalize content: remove punctuation/newlines, keep words
    # We want to preserve sequence.
    import re
    # Replace non-alphanumeric with space, but keep words intact
    cleaned = re.sub(r'[^a-zA-Z\s]', ' ', content)
    words = cleaned.lower().split()
    
    candidates = []
    current_sequence = []
    
    # simple state machine to find runs of valid words
    # OPTION 1: Contiguous runs (Standard Mode)
    for w in words:
        if w in word_set:
            current_sequence.append(w)
        else:
            if current_sequence:
                candidates.append(current_sequence)
                current_sequence = []
    if current_sequence:
        candidates.append(current_sequence)

    # OPTION 2: Sparse/Stealth Mode (Collect ALL valid words)
    # This assumes the user copied ONLY the relevant post/comment.
    all_valid_words = [w for w in words if w in word_set]
    if len(all_valid_words) > 16:
         candidates.append(all_valid_words)

    # Filter and Display
    found = 0
    shared_key_bytes = None
    if try_key and os.path.exists(try_key):
        with open(try_key, 'rb') as f:
            shared_key_bytes = f.read()

    print(f"\n[+] Scanning {len(words)} words for anomalies...\n")
    
    # Deduplicate candidates to avoid printing the same thing twice if contiguous == sparse
    # We convert list to tuple to make it hashable
    unique_candidates = []
    seen_seqs = set()
    
    for seq in candidates:
        seq_tuple = tuple(seq)
        if seq_tuple not in seen_seqs:
            unique_candidates.append(seq)
            seen_seqs.add(seq_tuple)

    for seq in unique_candidates:
        length = len(seq)
        if length < 12: 
            continue
            
        found += 1
        seq_str = " ".join(seq)
        
        if length == 32:
            print(f"[*] POTENTIAL PUBLIC KEY (32 words):")
            print(f"    {seq_str[:50]}... (truncated)")
            print(f"    -> Use 'derive' with this string to connect.\n")
            
        else:
            print(f"[*] POTENTIAL MESSAGE ({length} words):")
            print(f"    {seq_str[:50]}... (truncated)")
            
            if shared_key_bytes:
                try:
                    payload = decode_string(seq_str)
                    plaintext = CRYPTO.decrypt_message(shared_key_bytes, payload)
                    print(f"    [!] DECRYPTED SUCCESS: {plaintext}\n")
                except:
                    print(f"    [-] Decryption failed with provided key.\n")
            else:
                print(f"    -> Use 'decrypt' to read this (if you have the key).\n")

    if found == 0:
        print("[-] No valid shitpost sequences found.")

@cli.command()
@click.argument('input_text', required=False)
@click.option('--file', help='Read text from a file.')
@click.option('--key', required=True, help='Your private key to derive shared secrets.')
@click.option('--welcome-msg', default="Connection verified. Stand by.", help='Message to encrypt for new peers.')
@click.option('--stealth/--no-stealth', default=True, help='Use stealth mode for replies.')
def auto_reply(input_text, file, key, welcome_msg, stealth):
    """Scan for public keys and generate encrypted replies for each."""
    from steg import WORDLIST, encode_bytes
    from stealth import generate_stealth_text
    
    # Load Host Private Key
    if not os.path.exists(key):
        click.echo("Private key not found!", err=True)
        return
    with open(key, 'rb') as f:
        priv_bytes = f.read()
    host_priv_key = CRYPTO.load_private_key(priv_bytes)

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
    
    # Scan logic (simplified from 'scan')
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

    # Process candidates
    click.echo(f"[*] Analyzing {len(candidates)} sequences...")
    
    replies = []
    
    for seq in candidates:
        if len(seq) == 32:
            # It's a Public Key!
            peer_pub_str = " ".join(seq)
            peer_pub_bytes = decode_string(peer_pub_str)
            
            # Derive shared secret (in memory only)
            shared_key = CRYPTO.derive_shared_secret(host_priv_key, peer_pub_bytes)
            
            # Encrypt Welcome Message
            encrypted_payload = CRYPTO.encrypt_message(shared_key, welcome_msg)
            
            # Encode
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
        click.echo("[-] No public keys found to reply to.")
        return

    click.echo(f"\n[+] Generated {len(replies)} Replies:\n")
    for i, r in enumerate(replies):
        click.echo(f"--- Reply {i+1} (To key starting with '{r['peer_prefix']}') ---")
        click.echo(r['reply'])
        click.echo("")

if __name__ == '__main__':
    cli()
