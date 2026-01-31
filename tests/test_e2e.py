import unittest
import os
import sys
import subprocess
import shutil

# Ensure we can run the CLI
CLI_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '../cli.py'))

class TestShitposterE2E(unittest.TestCase):
    def setUp(self):
        self.work_dir = "test_work_dir"
        if os.path.exists(self.work_dir):
            shutil.rmtree(self.work_dir)
        os.makedirs(self.work_dir)

    def tearDown(self):
        # Cleanup
        if os.path.exists(self.work_dir):
            shutil.rmtree(self.work_dir)

    def run_cli(self, args):
        cmd = [sys.executable, CLI_PATH] + args
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.work_dir)
        # Debug helper
        if result.returncode != 0:
            print(f"CLI Error [{args}]: {result.stderr}")
        return result

    def extract_key_from_output(self, stdout):
        # The key is between two lines of dashes.
        lines = stdout.splitlines()
        key_lines = []
        capture = False
        for line in lines:
            if "--------" in line:
                if capture:
                    # Found ending dash line
                    break
                else:
                    # Found starting dash line
                    capture = True
                    continue
            if capture:
                key_lines.append(line.strip())
        return " ".join(key_lines).strip()

    def test_full_handshake_flow(self):
        print("\n--- Starting E2E Handshake Test ---")

        # 1. Generate Keys for Alice (Host) and Bob (New User)
        print("[1] Generating Identity for Alice...")
        res_alice = self.run_cli(['keygen', '--out', 'alice.key'])
        self.assertEqual(res_alice.returncode, 0)
        alice_pub_key_raw = self.extract_key_from_output(res_alice.stdout)
        
        print("[1] Generating Identity for Bob...")
        res_bob = self.run_cli(['keygen', '--out', 'bob.key'])
        self.assertEqual(res_bob.returncode, 0)
        bob_pub_key_raw = self.extract_key_from_output(res_bob.stdout)
        
        # Verify length
        bob_len = len(bob_pub_key_raw.split())
        print(f"[DEBUG] Bob's Key Length: {bob_len} words")
        self.assertEqual(bob_len, 32, "Bob's key is not 32 words!")

        # 2. Bob sees Alice's post, derives secret, and encrypts a message
        # But wait, let's test the AUTO-REPLY flow.
        # Scenario: Alice (Host) sees Bob's key in a comment and auto-replies.
        
        # Simulate Bob posting his key in a Reddit comment
        # We use safe words that definitely aren't in the tech wordlist to avoid merging sequences.
        bob_comment = f"Hey friends, look at this strange signal: {bob_pub_key_raw} ... ending transmission."
        with open(os.path.join(self.work_dir, 'bob_post.txt'), 'w') as f:
            f.write(bob_comment)

        # 3. Alice runs 'auto-reply' on Bob's post
        print("[2] Alice auto-replies to Bob's post...")
        welcome_msg = "Welcome to the resistance."
        res_auto = self.run_cli([
            'auto-reply', 
            '--file', 'bob_post.txt', 
            '--key', 'alice.key', 
            '--welcome-msg', welcome_msg,
            '--stealth' # Use stealth for the reply
        ])
        self.assertEqual(res_auto.returncode, 0)
        
        # Extract the reply text from Alice's output
        # The output format is: "--- Reply 1 ... ---\n<TEXT>\n"
        output_lines = res_auto.stdout.split('\n')
        reply_start = -1
        for i, line in enumerate(output_lines):
            if "--- Reply 1" in line:
                reply_start = i + 1
                break
        
        if reply_start == -1:
            print(">>> DEBUG: Auto-Reply Output:\n", res_auto.stdout)
            print(">>> DEBUG: Bob's Post Content:\n", bob_comment)
            
        self.assertTrue(reply_start != -1, "Could not find reply in output")
        alice_reply_text = output_lines[reply_start].strip()
        print(f"[2] Alice's Stealth Reply: {alice_reply_text[:50]}...")

        # 4. Bob receives the reply. Bob needs to derive the secret first using Alice's Pub Key.
        print("[3] Bob derives shared secret from Alice's known public key...")
        res_derive = self.run_cli([
            'derive', alice_pub_key_raw, 
            '--key', 'bob.key', 
            '--out', 'bob_shared.key'
        ])
        self.assertEqual(res_derive.returncode, 0)

        # 5. Bob scans Alice's reply using the shared key
        print("[4] Bob decrypts Alice's reply...")
        # Save Alice's reply to a file for scanning
        with open(os.path.join(self.work_dir, 'alice_reply.txt'), 'w') as f:
            f.write(alice_reply_text)
            
        res_scan = self.run_cli([
            'scan', 
            '--file', 'alice_reply.txt', 
            '--try-key', 'bob_shared.key'
        ])
        
        self.assertEqual(res_scan.returncode, 0)
        self.assertIn(f"[!] DECRYPTED SUCCESS: {welcome_msg}", res_scan.stdout)
        print("[SUCCESS] Bob successfully read the welcome message!")

if __name__ == '__main__':
    unittest.main()
