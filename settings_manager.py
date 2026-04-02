import os
import json
from cryptography.fernet import Fernet
from config import settings

DATA_DIR = "data"
MASTER_KEY_FILE = os.path.join(DATA_DIR, "master.key")
CREDENTIALS_FILE = os.path.join(DATA_DIR, "credentials.json")

class SecureSettingsManager:
    def __init__(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        self._key = self._load_or_create_key()
        self._cipher = Fernet(self._key)
        self._credentials = self._load_credentials()

    def _load_or_create_key(self) -> bytes:
        if os.path.exists(MASTER_KEY_FILE):
            with open(MASTER_KEY_FILE, "rb") as f:
                return f.read()
        else:
            key = Fernet.generate_key()
            with open(MASTER_KEY_FILE, "wb") as f:
                f.write(key)
            return key

    def _load_credentials(self) -> dict:
        if os.path.exists(CREDENTIALS_FILE):
            try:
                with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
                    encrypted_data = json.load(f)
                    decrypted = {}
                    for k, v in encrypted_data.items():
                        try:
                            decrypted[k] = self._cipher.decrypt(v.encode()).decode("utf-8")
                        except Exception:
                            print(f"Failed to decrypt key: {k}")
                    return decrypted
            except Exception as e:
                print(f"Error loading credentials: {e}")
                return {}
        return {}

    def _save_credentials(self):
        encrypted_data = {}
        for k, v in self._credentials.items():
            if v:
                encrypted_data[k] = self._cipher.encrypt(v.encode("utf-8")).decode("utf-8")
        with open(CREDENTIALS_FILE, "w", encoding="utf-8") as f:
            json.dump(encrypted_data, f, indent=4)

    def get(self, key_name: str) -> str:
        """Get key from encrypted storage, fallback to .env/config."""
        val = self._credentials.get(key_name)
        if val:
            return val
        # fallback to config.py settings
        return getattr(settings, key_name, "")

    def set(self, key_name: str, value: str):
        """Set key in encrypted storage."""
        if value:
            self._credentials[key_name] = value
        elif key_name in self._credentials:
            del self._credentials[key_name]
        self._save_credentials()

    def get_public_status(self) -> dict:
        """Returns True if a key is configured, False otherwise. Does not leak keys."""
        public_keys = ["OPENAI_API_KEY", "CLAUDE_SESSION_KEY", "GEMINI_API_KEY", "PERPLEXITY_API_KEY"]
        status = {}
        for k in public_keys:
            val = self.get(k)
            status[k] = bool(val and len(val) > 0)
        return status

secure_settings = SecureSettingsManager()
