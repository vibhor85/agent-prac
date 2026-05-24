"""Debug mode management."""

DEBUG = False


def enable_debug():
    """Enable debug mode."""
    global DEBUG
    DEBUG = True


def disable_debug():
    """Disable debug mode."""
    global DEBUG
    DEBUG = False


def log(message: str):
    """Print a debug message if debug mode is enabled."""
    if DEBUG:
        print(message)
