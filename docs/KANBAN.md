# Shitposter Cipher Development Kanban

## Backlog

### Cryptography Improvements
- [ ] **Bind Context in HKDF:** Improve `derive_shared_secret` in `crypto.py`. Instead of `salt=None` and static `info`, include the sorted public keys of both parties in the HKDF `info` parameter. This binds the derived key strictly to the pair of identities.
- [ ] **Directional Key Separation:** Derive two keys from the shared secret (e.g., `K_AB` and `K_BA`) so Alice and Bob use different keys for sending. This prevents reflection attacks and reduces nonce collision risks.
- [ ] **Forward Secrecy Strategy:** Investigate a "Ratchet" mechanism or ephemeral session keys. Currently, compromise of the static Identity Key compromises all historical messages.

### Features
- [x] **One-to-Many Broadcasts:** Implement a "Channel Key" workflow.
    - Host generates a persistent AES key (`util generate-channel-key`).
    - Host distributes this key (encoded as 32 words) inside the encrypted One-to-One handshake message.
    - Host broadcasts messages encrypted with this Channel Key.
    - All onboarded agents can decrypt the broadcast.

### Infrastructure
- [ ] **Client-Side WASM:** Compile the crypto logic to WebAssembly so it can run in a browser extension or a lightweight JS bot without a backend.

## In Progress
*(None)*

## Done
- [x] **Core Crypto:** X25519 + AES-256-GCM.
- [x] **Steganography:** 256-word mapping + Stealth Templates.
- [x] **API:** FastAPI Microservice on Hugging Face Spaces.
- [x] **Documentation:** Manifesto, Bot Instructions, and README.
- [x] **CI/CD:** GitHub Actions and Tests.
