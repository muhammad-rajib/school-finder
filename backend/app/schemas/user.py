from uuid import UUID

from pydantic import BaseModel, ConfigDict


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class CreatePrincipalRequest(BaseModel):
    name: str
    email: str
    password: str
    school_id: UUID


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: str
    role: str
    school_id: UUID | None = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
