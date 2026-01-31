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
        """
        Derives directional session keys.
        Returns a dictionary: {'tx': bytes, 'rx': bytes}
        
        Logic:
        1. ECDH -> Shared Secret
        2. HKDF context = Sorted(AlicePub, BobPub)
        3. Derive 64 bytes -> Split into Key A and Key B
        4. If MyPub < PeerPub: I use Key A to transmit, Key B to receive.
           Else: I use Key B to transmit, Key A to receive.
        """
        # 1. Get my public bytes
        my_public_bytes = private_key.public_key().public_bytes(
            encoding=Encoding.Raw,
            format=PublicFormat.Raw
        )
        
        peer_public_key = x25519.X25519PublicKey.from_public_bytes(peer_public_bytes)
        shared_secret = private_key.exchange(peer_public_key)

        # 2. Sort keys for deterministic context
        if my_public_bytes < peer_public_bytes:
            context_info = my_public_bytes + peer_public_bytes
            i_am_alice = True
        else:
            context_info = peer_public_bytes + my_public_bytes
            i_am_alice = False

        # 3. HKDF Expand (64 bytes)
        derived_material = HKDF(
            algorithm=hashes.SHA256(),
            length=64, # 32 bytes for A->B, 32 bytes for B->A
            salt=None, # Fixed protocol salt could be added here in future
            info=b'shitposter-v2-directional' + context_info,
        ).derive(shared_secret)
        
        key_a = derived_material[:32]
        key_b = derived_material[32:]
        
        # 4. Assign Direction
        if i_am_alice:
            return {'tx': key_a, 'rx': key_b}
        else:
            return {'tx': key_b, 'rx': key_a}

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
