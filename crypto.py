from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat, PrivateFormat, NoEncryption
import os

class ShitposterCrypto:
    def generate_keypair(self):
        """Generates a private key and returns (private_key, public_key_bytes)."""
        private_key = x25519.X25519PrivateKey.generate()
        public_key = private_key.public_key()
        
        public_bytes = public_key.public_bytes(
            encoding=Encoding.Raw,
            format=PublicFormat.Raw
        )
        return private_key, public_bytes

    def load_private_key(self, private_bytes):
        """Loads a private key from raw bytes."""
        return x25519.X25519PrivateKey.from_private_bytes(private_bytes)

    def get_private_bytes(self, private_key):
        return private_key.private_bytes(
            encoding=Encoding.Raw,
            format=PrivateFormat.Raw,
            encryption_algorithm=NoEncryption()
        )

    def derive_shared_secret(self, private_key, peer_public_bytes):
        """Derives a shared AES key from own private key and peer's public bytes."""
        peer_public_key = x25519.X25519PublicKey.from_public_bytes(peer_public_bytes)
        shared_key = private_key.exchange(peer_public_key)

        derived_key = HKDF(
            algorithm=hashes.SHA256(),
            length=32,
            salt=None,
            info=b'shitposter-handshake-v1',
        ).derive(shared_key)
        
        return derived_key

    def encrypt_message(self, key, plaintext):
        """Encrypts plaintext using AES-GCM. Returns (nonce + ciphertext)."""
        aesgcm = AESGCM(key)
        nonce = os.urandom(12)
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
        ciphertext = aesgcm.encrypt(nonce, plaintext, None)
        return nonce + ciphertext

    def decrypt_message(self, key, payload):
        """Decrypts (nonce + ciphertext). Returns plaintext string."""
        aesgcm = AESGCM(key)
        nonce = payload[:12]
        ciphertext = payload[12:]
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
        return plaintext.decode('utf-8')
