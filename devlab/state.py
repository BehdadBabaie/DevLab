from dataclasses import dataclass


@dataclass(slots=True)
class RuntimeState:
    verbose: bool = False


state = RuntimeState()
