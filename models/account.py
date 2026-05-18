from dataclasses import dataclass


@dataclass
class AccountConfig:
    api_id: int
    api_hash: str
    string_session: str
    target_channel: int
    sources: list[int]
