from typing import Any, Dict
from dataclasses import dataclass, field

@dataclass
class DIContainer:
    # Use default_factory to create a new dictionary for each instance
    _services: Dict[str, Any] = field(default_factory=dict)

    def register(self, name: str, obj: Any):
        """Register a service with a given name."""
        self._services[name] = obj

    def get(self, name: str) -> Any:
        """Retrieve a service by name."""
        return self._services.get(name)
