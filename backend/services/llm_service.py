"""
LangChain-powered LLM service for FusionGPT.

Uses langchain-groq (ChatGroq) as the chat model backend.
Provides two entry points:
  - run_chain()      → preferred: takes a ChatPromptTemplate + input vars
  - generate_text()  → legacy-compatible: takes a raw messages list
  - build_messages() → helper kept for any direct callers
"""

import os
from typing import Optional

from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# ---------------------------------------------------------------------------
# Default model
# ---------------------------------------------------------------------------
DEFAULT_MODEL = "llama-3.3-70b-versatile"

# ---------------------------------------------------------------------------
# LLM factory — returns a configured ChatGroq instance
# ---------------------------------------------------------------------------

def get_llm(
    model: str = DEFAULT_MODEL,
    temperature: float = 0.7,
    max_tokens: int = 2048,
) -> Optional[ChatGroq]:
    """
    Create and return a ChatGroq LangChain LLM instance.

    Returns None if GROQ_API_KEY is not set.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    return ChatGroq(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        api_key=api_key,
    )


# ---------------------------------------------------------------------------
# Primary chain runner — preferred approach (LangChain LCEL pipe)
# ---------------------------------------------------------------------------

def run_chain(
    prompt_template: ChatPromptTemplate,
    input_vars: dict,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.7,
    max_tokens: int = 2048,
) -> tuple[str, int]:
    """
    Build and invoke a LangChain chain: prompt | llm.

    Args:
        prompt_template: A ChatPromptTemplate built by prompt_service.
        input_vars:      Dict of variables to fill into the template.
        model:           Groq model ID.
        temperature:     Sampling temperature (0.0 – 1.0).
        max_tokens:      Maximum tokens in the response.

    Returns:
        Tuple of (response_text: str, total_tokens: int)
    """
    fallback = (
        "AI service is unavailable right now. "
        "Please configure GROQ_API_KEY to enable full responses.",
        0,
    )

    llm = get_llm(model=model, temperature=temperature, max_tokens=max_tokens)
    if llm is None:
        return fallback

    try:
        chain = prompt_template | llm
        response = chain.invoke(input_vars)
        content = response.content or ""
        # LangChain AIMessage carries usage_metadata when available
        tokens = 0
        if hasattr(response, "usage_metadata") and response.usage_metadata:
            tokens = response.usage_metadata.get("total_tokens", 0)
        return content, tokens
    except Exception as exc:
        return f"AI service is temporarily unavailable: {exc}", 0


# ---------------------------------------------------------------------------
# Legacy-compatible: generate_text()
# ---------------------------------------------------------------------------

def generate_text(
    messages: list[dict | BaseMessage],
    model: str = DEFAULT_MODEL,
    temperature: float = 0.7,
    max_tokens: int = 2048,
) -> tuple[str, int]:
    """
    Send a messages list to ChatGroq via LangChain and return (response_text, total_tokens).

    Accepts either OpenAI-style dicts or LangChain BaseMessage objects.

    Args:
        messages:    List of message dicts e.g.
                     [{"role": "system", "content": "..."}, {"role": "user", "content": "..."}]
                     or LangChain BaseMessage instances.
        model:       Groq model ID (default: llama-3.3-70b-versatile)
        temperature: Sampling temperature (0.0 – 1.0)
        max_tokens:  Maximum tokens in the response

    Returns:
        Tuple of (response_text: str, total_tokens: int)
    """
    fallback = (
        "AI service is unavailable right now. "
        "Please configure GROQ_API_KEY to enable full responses.",
        0,
    )

    llm = get_llm(model=model, temperature=temperature, max_tokens=max_tokens)
    if llm is None:
        return fallback

    # Convert dicts → LangChain message objects if needed
    lc_messages: list[BaseMessage] = []
    for msg in messages:
        if isinstance(msg, BaseMessage):
            lc_messages.append(msg)
        elif isinstance(msg, dict):
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "system":
                lc_messages.append(SystemMessage(content=content))
            elif role == "assistant":
                lc_messages.append(AIMessage(content=content))
            else:
                lc_messages.append(HumanMessage(content=content))

    try:
        response = llm.invoke(lc_messages)
        content = response.content or ""
        tokens = 0
        if hasattr(response, "usage_metadata") and response.usage_metadata:
            tokens = response.usage_metadata.get("total_tokens", 0)
        return content, tokens
    except Exception as exc:
        return f"AI service is temporarily unavailable: {exc}", 0


# ---------------------------------------------------------------------------
# Helper: build messages list (kept for backward compatibility)
# ---------------------------------------------------------------------------

def build_messages(
    system_prompt: str,
    user_message: str,
    history: Optional[list[dict]] = None,
) -> list[dict]:
    """
    Construct the full messages list for a generate_text() call.

    Args:
        system_prompt: The system instruction.
        user_message:  The latest user message.
        history:       Optional prior turns [{"role": "user"|"assistant", "content": "..."}]

    Returns:
        List of message dicts compatible with generate_text().
    """
    messages: list[dict] = [{"role": "system", "content": system_prompt}]
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_message})
    return messages
