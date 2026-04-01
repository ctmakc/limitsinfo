import json
import os
from typing import Dict, Any

STATE_FILE = "state.json"

class StateManager:
    def __init__(self, filepath: str = STATE_FILE):
        self.filepath = filepath
        self._state = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    def _save_state(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self._state, f, indent=4)

    def get_limit(self, service: str) -> Dict[str, Any]:
        return self._state.get(service, {})

    def update_limit(self, service: str, current: int, max_limit: int, next_reset: str = None):
        """
        Updates the usage statistics for a given service.
        Returns the previous state to compare triggers.
        """
        old_state = self._state.get(service, {})
        self._state[service] = {
            "current": current,
            "max": max_limit,
            "next_reset": next_reset,
            "last_alerted_level": old_state.get("last_alerted_level", 100) # 100, 50, 25, 0 (percentage)
        }
        self._save_state()
        return old_state
        
    def set_alert_level(self, service: str, level: int):
        if service not in self._state:
            self._state[service] = {}
        self._state[service]["last_alerted_level"] = level
        self._save_state()
        
state = StateManager()
