import unittest
import requests
import time
import os

API_URL = os.environ.get("API_URL", "https://igor53627-shitposter-api.hf.space")

class TestShitposterAPI(unittest.TestCase):
    def test_e2e_encryption_flow(self):
        print(f"\nTesting against: {API_URL}")
        
        # 0. Wait for service (simple retry loop)
        retries = 5
        while retries > 0:
            try:
                requests.get(f"{API_URL}/docs", timeout=5)
                break
            except:
                print("Waiting for API to wake up...")
                time.sleep(5)
                retries -= 1
        
        # 1. Generate Alice
        print("[1] Generating Alice...")
        resp = requests.get(f"{API_URL}/keygen")
        if resp.status_code == 503:
            self.skipTest("API Service is unavailable (still building?)")
            
        self.assertEqual(resp.status_code, 200)
        alice = resp.json()
        self.assertTrue("private_key_b64" in alice)
        self.assertTrue("public_signal" in alice)

        # 2. Generate Bob
        print("[2] Generating Bob...")
        resp = requests.get(f"{API_URL}/keygen")
        self.assertEqual(resp.status_code, 200)
        bob = resp.json()

        # 3. Alice Encrypts for Bob
        message = "The eagle flies at midnight."
        print(f"[3] Encrypting: '{message}'")
        
        payload = {
            "message": message,
            "sender_private_key_b64": alice["private_key_b64"],
            "recipient_public_signal": bob["public_signal"],
            "stealth": True
        }
        resp = requests.post(f"{API_URL}/encrypt", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue("shitpost" in data)
        ciphertext = data["shitpost"]
        print(f"    Shitpost: {ciphertext[:50]}...")

        # 4. Bob Decrypts
        print("[4] Decrypting...")
        payload = {
            "ciphertext_shitpost": ciphertext,
            "recipient_private_key_b64": bob["private_key_b64"],
            "sender_public_signal": alice["public_signal"]
        }
        resp = requests.post(f"{API_URL}/decrypt", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["message"], message)
        
        print(f"    Decrypted: {data['message']}")
        print("[SUCCESS] API E2E Test Passed.")

if __name__ == '__main__':
    unittest.main()
