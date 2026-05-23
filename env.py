import os

from dotenv import load_dotenv


def load_environment() -> None:
    """Load environment variables from a .env file."""
    load_dotenv()
    print("[log] Environment loaded from .env")
