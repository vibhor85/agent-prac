import os

from dotenv import load_dotenv


from debug import log


def load_environment() -> None:
    """Load environment variables from a .env file."""
    load_dotenv()
    log("[log] Environment loaded from .env")
