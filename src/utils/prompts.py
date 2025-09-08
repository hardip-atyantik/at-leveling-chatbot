"""Simplified prompt management"""

from pathlib import Path
from functools import lru_cache


@lru_cache(maxsize=4)
def load_prompt(filename: str, prompts_dir: str = "prompts") -> str:
    """Load prompt from text file with caching"""
    filepath = Path(prompts_dir) / filename
    if not filepath.exists():
        raise FileNotFoundError(f"Prompt file not found: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read().strip()


def get_prompts() -> tuple[str, str]:
    """Get system and user prompts"""
    return (
        load_prompt("system_cto.txt"),
        load_prompt("user_query.txt")
    )