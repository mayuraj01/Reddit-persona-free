from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Any

Citation = Dict[str, str]           # {"kind": "post|comment|llm", "url": "<link or N/A>"}

@dataclass
class Persona:
    username: str
    name: str | None = None
    age: str | None = None
    occupation: str | None = None
    location: str | None = None
    motivations: Dict[str, int] = field(default_factory=dict)
    frustrations: List[str] = field(default_factory=list)
    goals: List[str] = field(default_factory=list)
    personality: Dict[str, float] = field(default_factory=dict)
    citations: Dict[str, List[Citation]] = field(default_factory=dict)

    def add_fact(self, field_name: str, value: Any, source: Citation) -> None:
        """Set a field and keep track of where we found it."""
        setattr(self, field_name, value)
        self.citations.setdefault(field_name, []).append(source)
