from dataclasses import dataclass, asdict, fields
from datetime import datetime, timezone
from enum import Enum

from passlib.context import CryptContext


pwd_context: CryptContext = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserRole(Enum):
    ADMIN: str = 'admin'
    USER: str = 'user'


@dataclass
class User:
    first_name: str
    second_name: str
    email: str
    phone: str
    hashed_password: str
    role: UserRole = UserRole.USER.value
    created_at: datetime = datetime.now(tz=timezone.utc)
    id: str | None = None

    @classmethod
    def from_dict(cls, user_dict: dict):
        return cls(**user_dict)

    def to_dict(self):
        return asdict(self)

    def update(self, params: dict) -> 'User':
        field_names: set = {field.name for field in fields(self)}
        for attr, value in params.items():
            if attr in field_names:
                if attr in self._get_forbidden_params():
                    continue
                self.__setattr__(attr, value)
        return self

    def _get_forbidden_params(self):
        return ('id', 'created_at',)

    def __bool__(self):
        return True
    
    def check_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.hashed_password)

    @classmethod
    def get_password_hash(cls, password: str) -> str:
        return pwd_context.hash(password)