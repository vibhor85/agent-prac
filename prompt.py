from pathlib import Path

PROMPT_PATH = Path("prompts/system_prompt.txt")


def read_system_prompt(path: Path = PROMPT_PATH) -> str:
    """Read the system prompt text from a file."""
    prompt = path.read_text(encoding="utf-8")
    print(f"[log] Loaded system prompt from {path}")
    return prompt
