# Week 2 Write-up

Tip: To preview this markdown file

- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **TODO**
SUNet ID: **TODO**
Citations: **TODO**

This assignment took me about **TODO** hours to do.

## YOUR RESPONSES

For each exercise, please include what prompts you used to generate the answer, in addition to the location of the generated response. Make sure to clearly add comments in your code documenting which parts are generated.

### Exercise 1: Scaffold a New Feature

Prompt:

```
1. Analyze the heuristics in extract action items

2. Your task is to implement an LLM-powered alternative, extract_action_items_llm(), that utilizes Ollama to perform action item extraction via a large language model.

Some tips:

To produce structured outputs (i.e. JSON array of strings), refer to this documentation: https://ollama.com/blog/structured-outputs
To browse available Ollama models, refer to this documentation: https://ollama.com/library. Note that larger models will be more resource-intensive, so start small. llama3.1:8b have pulled.

3. After generating the code, write the full Generated Code Snippets at the corresponding location under "Exercise 1: Scaffold a New Feature" in the writeup.md file.
```

Generated Code Snippets:

```
File: week2/app/services/extract.py
- Lines 12-31: Added Ollama model configuration (`DEFAULT_OLLAMA_MODEL`) and JSON schema `LLM_RESPONSE_FORMAT` for structured outputs.
- Lines 33-41: Added `LLM_SYSTEM_PROMPT` describing extraction behavior.
- Lines 84-95: Added `_dedupe_preserve_order` helper to reuse ordering logic across heuristics and LLM flows.
- Lines 98-117: Added `_parse_llm_items()` to parse and normalize structured responses (includes defensive JSON parsing).
- Lines 120-162: Implemented `extract_action_items_llm()` performing Ollama chat call with retries, structured response parsing, and heuristic fallback.
```

### Exercise 2: Add Unit Tests

Prompt:

```
The AI automatically generated comprehensive unit tests after implementing the LLM function (using Codex). However, if this did not happen, I would have said something like "now generate comprehensive unit tests. consider a wide range of normal and edge cases.
```

Generated Code Snippets:

```
File: week2/tests/test_extract.py
- Lines 1-7: Added imports for `json`, `types`, `pytest`, and `extract_action_items_llm`.
- Lines 18-22: Added `_DummyResponse` helper for mocking Ollama responses.
- Lines 25-40: Added `test_extract_action_items_llm_bullet_input` to validate simple bullet extraction via mocked LLM.
- Lines 43-58: Added `test_extract_action_items_llm_keyword_lines` covering keyword-prefixed notes.
- Lines 61-69: Added `test_extract_action_items_llm_empty_input` ensuring no LLM call for blank text.
- Lines 72-82: Added `test_extract_action_items_llm_fallback_on_invalid_response` to assert heuristic fallback when LLM output is invalid JSON.
```

### Exercise 3: Refactor Existing Code for Clarity

Prompt:

```
Refactor the code for clarity, safety, and testability without changing behavior. Goals:
- Normalize naming and typing; remove dead code and duplication.

- Improve comments/docstrings only where intent is non-obvious.
- Keep interfaces stable; avoid scope creep or new features.
- Add/adjust lightweight tests to lock in behavior.
- Ensure consistent formatting, imports,  Minimize added code.
```

Generated/Modified Code Snippets:

```
TODO: List all modified code files with the relevant line numbers. (We anticipate there may be multiple scattered changes here – just produce as comprehensive of a list as you can.)
```

### Exercise 4: Use Agentic Mode to Automate a Small Task

Prompt:

```
TODO
```

Generated Code Snippets:

```
TODO: List all modified code files with the relevant line numbers.
```

### Exercise 5: Generate a README from the Codebase

Prompt:

```
TODO
```

Generated Code Snippets:

```
TODO: List all modified code files with the relevant line numbers.
```

## SUBMISSION INSTRUCTIONS

1. Hit a `Command (⌘) + F` (or `Ctrl + F`) to find any remaining `TODO`s in this file. If no results are found, congratulations – you've completed all required fields.
2. Make sure you have all changes pushed to your remote repository for grading.
3. Submit via Gradescope.
