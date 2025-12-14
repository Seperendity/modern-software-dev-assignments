# Week 2 Write-up
Tip: To preview this markdown file
- On Mac, press `Command (⌘) + Shift + V`
- On Windows/Linux, press `Ctrl + Shift + V`

## INSTRUCTIONS

Fill out all of the `TODO`s in this file.

## SUBMISSION DETAILS

Name: **TODO** \
SUNet ID: **TODO** \
Citations: **TODO**

This assignment took me about **TODO** hours to do. 


## YOUR RESPONSES
For each exercise, please include what prompts you used to generate the answer, in addition to the location of the generated response. Make sure to clearly add comments in your code documenting which parts are generated.

### Exercise 1: Scaffold a New Feature
Prompt: 
```
TODO
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
TODO
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
TODO
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
