from app.models.entities import UserRole
from app.schemas.common import ORMModel


class UserRead(ORMModel):
    id: int
    email: str
    full_name: str
    role: UserRole
    is_active: bool


class UserCreate(ORMModel):
    email: str
    full_name: str
    password: str
    role: UserRole = UserRole.viewer
