import unittest
import os
import shutil
import time
import threading
import http.server
import socketserver
import base64
from playwright.sync_api import sync_playwright

PORT = 8081
DIST_DIR = "dist_test"

def start_server():
    os.chdir(DIST_DIR)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        httpd.serve_forever()

class TestWebTerminal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # 1. Prepare dist folder (Mimic GitHub Pages flat structure)
        if os.path.exists(DIST_DIR):
            shutil.rmtree(DIST_DIR)
        os.makedirs(DIST_DIR)
        
        # Copy web files
        shutil.copy("web/index.html", DIST_DIR)
        
        # Copy python modules
        for f in ["crypto.py", "steg.py", "stealth.py", "fingerprint.py"]:
            shutil.copy(f, DIST_DIR)
            
        # 2. Start Server in background
        cls.server_thread = threading.Thread(target=start_server, daemon=True)
        cls.server_thread.start()
        
        # Give it a moment
        time.sleep(2)

    @classmethod
    def tearDownClass(cls):
        # Cleanup dist
        if os.path.exists(DIST_DIR):
            try:
                shutil.rmtree(DIST_DIR)
            except:
                pass

    def test_terminal_loads(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            
            # Hook console logs early
            page.on("console", lambda msg: print(f"BROWSER LOG: {msg.text}"))
            
            print(f"Loading http://localhost:{PORT}/index.html ...")
            page.goto(f"http://localhost:{PORT}/index.html")
            
            # Wait for WebCrypto to initialize
            # The status text should change to "WebCrypto Secure Terminal Online"
            print("Waiting for WebCrypto initialization...")
            try:
                page.wait_for_selector("text=WebCrypto Secure Terminal Online", timeout=60000) # 60s timeout for slow init
                print("[PASS] Terminal Initialized.")
            except Exception as e:
                # Capture error if any
                status = page.inner_text("#status")
                print(f"[FAIL] Stuck on status: {status}")
                
                # Check WebCrypto availability
                try:
                    is_loaded = page.evaluate("() => Boolean(window.crypto && window.crypto.subtle)")
                    print(f"DEBUG: webcrypto available = {is_loaded}")
                except:
                    print("DEBUG: Could not evaluate JS")

                # Check console logs
                print("Console Logs:")
                page.on("console", lambda msg: print(f"  {msg.text}"))
                raise e

            # Check if buttons are enabled
            btn = page.is_enabled("#btnKeygen")
            self.assertTrue(btn, "Keygen button should be enabled")
            print("[PASS] Buttons enabled.")
            
            browser.close()

    def test_encrypt_decrypt_with_base64_key(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            page.goto(f"http://localhost:{PORT}/index.html")
            page.wait_for_selector("text=WebCrypto Secure Terminal Online", timeout=60000)

            key_b64 = base64.b64encode(bytes(range(32))).decode("utf-8")
            message = "hello from base64"

            page.fill("#keyInput", key_b64)
            page.fill("#mainInput", message)
            page.click("#btnEncrypt")
            page.wait_for_function(
                "() => document.querySelector('#output').innerText !== 'Processing...'"
            )

            encrypted = page.inner_text("#output")
            self.assertFalse(
                encrypted.startswith("Error:"),
                f"Unexpected error during encrypt: {encrypted}",
            )

            page.fill("#mainInput", encrypted)
            page.click("#btnDecrypt")
            page.wait_for_function(
                "() => document.querySelector('#output').innerText !== 'Processing...'"
            )

            decrypted = page.inner_text("#output")
            self.assertEqual(message, decrypted)

            browser.close()

if __name__ == '__main__':
    unittest.main()
