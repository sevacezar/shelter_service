from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from enum import Enum


class RequestStatus(Enum):
    PENDING: str = 'pending'
    APPROVED: str = 'approved'
    REJECTED: str = 'rejected'
    CANCELLED: str = 'cancelled'


@dataclass
class AdoptionRequest:
    user_id: str
    animal_id: str
    status: str = RequestStatus.PENDING.value
    user_comment: str | None = None
    created_at: datetime = datetime.now(tz=timezone.utc)
    updated_at: datetime | None = None
    id: str = None


    def __post_init__(self):
        if self.updated_at is None:
            self.updated_at = self.created_at
    
    def __bool__(self):
        return True
    
    @classmethod
    def from_dict(cls, adoption_request_dict: dict) -> 'AdoptionRequest':
        adoption_request: 'AdoptionRequest' = cls(**adoption_request_dict)
        return adoption_request
    
    def to_dict(self) -> dict:
        return asdict(self)



