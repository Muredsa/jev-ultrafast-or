"""OpenRouter compatibility for the upstream Jev Ultrafast policy.

The upstream project calls TypeSafe's native /v1/systemone endpoint directly.
OpenRouter exposes the same state + questions contract through its Decisions API.
This adapter keeps the browser policy untouched and redirects only the transport.
"""

import os

OPENROUTER_DECISIONS_URL = "https://openrouter.ai/api/alpha/decisions"
OPENROUTER_CHAT_URL = "https://openrouter.ai/api/v1"
OPENROUTER_JEV_MODEL = "~typesafe/jev-latest"


def configure():
    """Configure the upstream model module to use OpenRouter."""
    key = os.environ.get("OPENROUTER_API_KEY")
    if key:
        os.environ.setdefault("TYPESAFE_API_KEY", key)
        os.environ.setdefault("TEXT_MODEL_API_KEY", key)

    os.environ.setdefault("TYPESAFE_MODEL", os.environ.get("JEV_MODEL", OPENROUTER_JEV_MODEL))
    os.environ.setdefault("TEXT_MODEL_BASE_URL", OPENROUTER_CHAT_URL)
    os.environ.setdefault("TEXT_MODEL", "inception/mercury-2.5")
    os.environ.setdefault("TEXT_MODEL_REASONING", "none")

    from . import model

    if getattr(model.post_json, "_openrouter_adapter", False):
        return

    original_post_json = model.post_json

    def openrouter_post_json(url, api_key, body):
        if url == "https://api.typesafe.ai/v1/systemone":
            url = os.environ.get("JEV_DECISIONS_URL", OPENROUTER_DECISIONS_URL)
        return original_post_json(url, api_key, body)

    openrouter_post_json._openrouter_adapter = True
    model.post_json = openrouter_post_json
