from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, description="Minimum 6 characters")
    full_name: str = Field(default="", description="User's display name")


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int
    email: str
    full_name: str
    tier: str


class UserProfileResponse(BaseModel):
    id: int
    email: str
    full_name: str
    tier: str
    created_at: str

    class Config:
        from_attributes = True
