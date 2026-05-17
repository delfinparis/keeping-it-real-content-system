"""
Example: Using D.J.'s voice profile as a system prompt with the Anthropic API.

This injects EDITORIAL-VOICE-STANDARDS.md as the system prompt so any
content Claude generates through the API sounds like D.J.

Requirements: pip install anthropic
Set ANTHROPIC_API_KEY in your environment.
"""

import anthropic
from pathlib import Path


def load_voice_profile() -> str:
    """Load the condensed voice profile from the repo."""
    profile_path = Path(__file__).parent.parent / "EDITORIAL-VOICE-STANDARDS.md"
    return profile_path.read_text()


def generate_in_voice(user_prompt: str, model: str = "claude-sonnet-4-20250514") -> str:
    """Generate content in D.J.'s voice using the API."""
    client = anthropic.Anthropic()

    voice_profile = load_voice_profile()

    system_prompt = (
        "You are a ghostwriter for D.J. Paris. "
        "Apply the following voice profile to everything you write. "
        "Do not mention or reference the voice profile itself -- just write naturally in this voice.\n\n"
        f"{voice_profile}"
    )

    message = client.messages.create(
        model=model,
        max_tokens=4096,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_prompt}
        ],
    )

    return message.content[0].text


if __name__ == "__main__":
    # Example usage
    result = generate_in_voice(
        "Write a short blog post about why I hate parallel parking."
    )
    print(result)
