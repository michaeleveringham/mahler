from dataclasses import dataclass


# TODO: expand this.
@dataclass
class Fingerprint:
    """Fingerprint class to hold browser signature."""
    headers: dict | None
    user_agent: str | None
