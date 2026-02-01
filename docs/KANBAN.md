# Shitposter Cipher Development Kanban

## Backlog

### Cryptography Improvements
- [ ] **Nonce Tracking / Replay Protection:** Implement a mechanism to prevent replay attacks. Since the protocol is currently stateless and asynchronous, investigate using a time-windowed nonce cache or an embedded sequence number in the payload.
- [ ] **Forward Secrecy Strategy:** Investigate a "Ratchet" mechanism or ephemeral session keys. Currently, compromise of the static Identity Key compromises all historical messages.

### Features
- [x] **One-to-Many Broadcasts:** Implement a "Channel Key" workflow.
    - Host generates a persistent AES key (`util generate-channel-key`).
    - Host distributes this key (encoded as 32 words) inside the encrypted One-to-One handshake message.
    - Host broadcasts messages encrypted with this Channel Key.
    - All onboarded agents can decrypt the broadcast.

### Infrastructure
- [ ] **Client-Side WebCrypto:** Use WebCrypto + JS X25519 so the browser client can run without a backend.

## In Progress
*(None)*

## Done
- [x] **Harden HKDF:** Added protocol salt and explicit identity binding into `info`.
- [x] **Bind Context in HKDF:** Bind sorted public keys into HKDF `info`.
- [x] **Directional Key Separation:** Derive separate TX/RX keys to prevent reflection attacks.
- [x] **Core Crypto:** X25519 + AES-256-GCM.
- [x] **Steganography:** 256-word mapping + Stealth Templates.
- [x] **API:** FastAPI Microservice on Hugging Face Spaces.
- [x] **Documentation:** Manifesto, Bot Instructions, and README.
- [x] **CI/CD:** GitHub Actions and Tests.
