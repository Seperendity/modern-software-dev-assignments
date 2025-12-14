from __future__ import annotations

import os
import re
from typing import List
import json
from typing import Any
from ollama import chat
from dotenv import load_dotenv

load_dotenv()

DEFAULT_OLLAMA_MODEL = (
    os.getenv("OLLAMA_ACTION_MODEL")
    or os.getenv("OLLAMA_MODEL")
    or "llama3.1:8b"
)

LLM_RESPONSE_FORMAT: dict[str, Any] = {
    "type": "json_schema",
    "json_schema": {
        "name": "action_items",
        "schema": {
            "type": "object",
            "properties": {
                "action_items": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Ordered action items extracted verbatim or lightly paraphrased from the notes.",
                }
            },
            "required": ["action_items"],
            "additionalProperties": False,
        },
    },
}

LLM_SYSTEM_PROMPT = """\
You extract concrete action items from meeting transcripts, tickets, or unstructured notes.
Return succinct bullet-friendly fragments and preserve the order they appear.
Only include actionable work. If none exist, return an empty list.
Output must follow the provided JSON schema exactly.
"""

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)


def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def extract_action_items(text: str) -> List[str]:
    lines = text.splitlines()
    extracted: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            # Trim common checkbox markers
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            extracted.append(cleaned)
    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)
    return _dedupe_preserve_order(extracted)


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    # Crude heuristic: treat these as imperative starters
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters


def _dedupe_preserve_order(items: List[str]) -> List[str]:
    seen: set[str] = set()
    unique: List[str] = []
    for item in items:
        normalized = item.strip()
        if not normalized:
            continue
        lowered = normalized.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(normalized)
    return unique


def _parse_llm_items(payload: Any) -> List[str] | None:
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except json.JSONDecodeError:
            return None
    if not isinstance(payload, dict):
        return None
    raw_items = payload.get("action_items", [])
    if not isinstance(raw_items, list):
        return None
    cleaned: List[str] = []
    for candidate in raw_items:
        if not isinstance(candidate, str):
            continue
        cleaned_line = candidate.strip()
        if not cleaned_line:
            continue
        cleaned.append(cleaned_line)
    return _dedupe_preserve_order(cleaned)


def extract_action_items_llm(text: str, *, model: str | None = None, max_retries: int = 2) -> List[str]:
    """Use an Ollama-hosted LLM to extract actionable items with structured output."""
    note_text = text.strip()
    if not note_text:
        return []
    chosen_model = model or DEFAULT_OLLAMA_MODEL
    if not chosen_model:
        raise ValueError("An Ollama model name must be provided for LLM extraction.")

    messages = [
        {"role": "system", "content": LLM_SYSTEM_PROMPT},
        {
            "role": "user",
            "content": (
                "Identify the actionable tasks contained in the notes below. "
                "Only return concrete next steps.\n\n"
                f"Notes:\n{note_text}"
            ),
        },
    ]

    last_error: Exception | None = None
    for _ in range(max_retries):
        try:
            response = chat(
                model=chosen_model,
                messages=messages,
                format=LLM_RESPONSE_FORMAT,
                options={"temperature": 0.1},
            )
        except Exception as exc:  # pragma: no cover - network/engine failure path
            last_error = exc
            continue
        parsed = _parse_llm_items(response.message.content)
        if parsed is not None:
            return parsed
    # Fall back to heuristics if the LLM call keeps failing, keeping the API usable.
    return extract_action_items(text)
