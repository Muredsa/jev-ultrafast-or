"""Jev chooses an observed action. Code owns execution."""

from .openrouter import configure as _configure_openrouter

_configure_openrouter()

from .agent import Agent
from .browser import Browser

__all__ = ["Agent", "Browser"]
