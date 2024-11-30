from dataclasses import dataclass, asdict
from datetime import datetime, timezone

@dataclass
class AnimalView:
    user_id: str
    animal_id: str
    viewed_at: datetime = datetime.now(tz=timezone.utc)
    id: str | None = None

    def __bool__(self):
        return True

    @classmethod
    def from_dict(cls, animal_view_dict: dict) -> 'AnimalView':
        animal_view: 'AnimalView' = cls(**animal_view_dict)
        return animal_view
    
    def to_dict(self):
        return asdict(self)
    
