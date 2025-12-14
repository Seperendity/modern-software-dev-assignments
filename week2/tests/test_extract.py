import json
import os
import types

import pytest

from ..app.services.extract import extract_action_items, extract_action_items_llm


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


class _DummyResponse:
    def __init__(self, content: str):
        self.message = types.SimpleNamespace(content=content)


def test_extract_action_items_llm_bullet_input(monkeypatch):
    text = "- finalize metrics dashboard\n- send launch email"

    def fake_chat(**kwargs):
        return _DummyResponse(
            json.dumps({"action_items": ["Finalize metrics dashboard", "Send launch email"]})
        )

    monkeypatch.setattr("week2.app.services.extract.chat", lambda **kwargs: fake_chat(**kwargs))

    items = extract_action_items_llm(text, model="mock-model")
    assert items == ["Finalize metrics dashboard", "Send launch email"]


def test_extract_action_items_llm_keyword_lines(monkeypatch):
    text = "TODO: refresh staging database\nAction: review QA sign-off"
    payload = {"action_items": ["Refresh staging database", "Review QA sign-off"]}

    def fake_chat(**kwargs):
        user_message = kwargs["messages"][-1]["content"]
        assert "refresh staging database" in user_message.lower()
        return _DummyResponse(json.dumps(payload))

    monkeypatch.setattr("week2.app.services.extract.chat", lambda **kwargs: fake_chat(**kwargs))

    items = extract_action_items_llm(text, model="mock-model")
    assert items == ["Refresh staging database", "Review QA sign-off"]


def test_extract_action_items_llm_empty_input(monkeypatch):
    def fake_chat(**kwargs):  # pragma: no cover - should never run
        raise AssertionError("LLM should not run for empty text")

    monkeypatch.setattr("week2.app.services.extract.chat", lambda **kwargs: fake_chat(**kwargs))

    assert extract_action_items_llm("", model="mock-model") == []


def test_extract_action_items_llm_fallback_on_invalid_response(monkeypatch):
    text = "- build CLI\n- demo app"

    def fake_chat(**kwargs):
        return _DummyResponse("not-json")

    monkeypatch.setattr("week2.app.services.extract.chat", lambda **kwargs: fake_chat(**kwargs))

    # Should fall back to heuristic extractor when parsing fails
    items = extract_action_items_llm(text, model="mock-model")
    assert "build CLI" in [item.lower() for item in items]
