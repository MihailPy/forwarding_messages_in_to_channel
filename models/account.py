from dataclasses import dataclass

ChannelRef = int | str


@dataclass
class AccountConfig:
    api_id: int
    api_hash: str
    string_session: str
    target_channel: ChannelRef
    sources: list[ChannelRef]
