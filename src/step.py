from collections.abc import Callable
from dataclasses import dataclass


@dataclass(frozen=True)
class Step:
    name: str
    description: str
    method: Callable = None
    display_name: str = None
    skippable: bool = False
    repeatable: bool = False
    critical: bool = False

    @property
    def preferred_name(self):
        if self.display_name:
            return self.display_name
        else:
            return self.name
