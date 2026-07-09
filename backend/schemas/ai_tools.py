"""
Pydantic request/response schemas for all AI tool endpoints.
"""
from typing import Optional
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Chat
# ---------------------------------------------------------------------------
class ChatMessage(BaseModel):
    role: str = Field(..., description="'user' or 'assistant'")
    content: str


class ChatRequest(BaseModel):
    message: str = Field(..., description="The user's current message")
    history: list[ChatMessage] = Field(default_factory=list, description="Previous turns")


class ChatResponse(BaseModel):
    reply: str
    tokens_used: int


# ---------------------------------------------------------------------------
# Summarize
# ---------------------------------------------------------------------------
class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=50, description="Text to summarize (min 50 chars)")
    length: str = Field(default="medium", description="short | medium | long")


class SummarizeResponse(BaseModel):
    summary: str
    tokens_used: int


# ---------------------------------------------------------------------------
# Translate
# ---------------------------------------------------------------------------
class TranslateRequest(BaseModel):
    text: str = Field(..., description="Text to translate")
    target_language: str = Field(..., description="Target language name e.g. 'Spanish'")
    source_language: str = Field(default="auto", description="Source language or 'auto'")


class TranslateResponse(BaseModel):
    translated_text: str
    target_language: str
    tokens_used: int


# ---------------------------------------------------------------------------
# Code
# ---------------------------------------------------------------------------
class CodeRequest(BaseModel):
    description: str = Field(..., description="What the code should do")
    language: str = Field(default="Python", description="Programming language")
    task: str = Field(default="generate", description="'generate' or 'explain'")
    code_to_explain: Optional[str] = Field(default=None, description="Code to explain (if task='explain')")


class CodeResponse(BaseModel):
    result: str
    language: str
    tokens_used: int


# ---------------------------------------------------------------------------
# Grammar
# ---------------------------------------------------------------------------
class GrammarRequest(BaseModel):
    text: str = Field(..., min_length=10, description="Text to grammar-check")


class GrammarResponse(BaseModel):
    corrected_text: str
    tokens_used: int


# ---------------------------------------------------------------------------
# Email
# ---------------------------------------------------------------------------
class EmailRequest(BaseModel):
    context: str = Field(..., description="Purpose/context of the email")
    recipient: str = Field(default="", description="Who the email is addressed to")
    tone: str = Field(default="professional", description="professional | casual | apologetic | persuasive | follow_up")
    additional_info: Optional[str] = Field(default=None, description="Any extra details")


class EmailResponse(BaseModel):
    email_content: str
    tokens_used: int


# ---------------------------------------------------------------------------
# Resume
# ---------------------------------------------------------------------------
class ResumeRequest(BaseModel):
    job_title: str = Field(..., description="Target job title")
    years_experience: int = Field(..., ge=0, description="Years of experience")
    key_skills: str = Field(..., description="Comma-separated key skills")
    recent_role: str = Field(default="", description="Most recent job role/company")
    achievements: Optional[str] = Field(default=None, description="Key achievements or responsibilities")


class ResumeResponse(BaseModel):
    resume_content: str
    tokens_used: int


# ---------------------------------------------------------------------------
# Prompt Generator
# ---------------------------------------------------------------------------
class PromptRequest(BaseModel):
    goal: str = Field(..., description="What you want the AI to do")
    context: Optional[str] = Field(default=None, description="Background context")
    output_format: Optional[str] = Field(default=None, description="Desired output format")


class PromptResponse(BaseModel):
    generated_prompt: str
    tokens_used: int


# ---------------------------------------------------------------------------
# Usage / History
# ---------------------------------------------------------------------------
class UsageLogResponse(BaseModel):
    id: int
    feature: str
    input_text: Optional[str]
    output_text: Optional[str]
    tokens_used: int
    created_at: str

    class Config:
        from_attributes = True
