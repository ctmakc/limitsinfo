from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseClient(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def get_usage(self) -> Dict[str, Any]:
        """
        Returns a dictionary with current usage:
        {
            "current": int,  # The current amount used
            "max": int,      # The maximum allowed limit
            "next_reset": str # Description or timestamp of when it resets
        }
        """
        pass
