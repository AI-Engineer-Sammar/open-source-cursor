import re

# Restricted terminal command patterns that require user confirmation
DANGEROUS_PATTERNS = [
    r"rm\s+-rf\s+/",            # Root deletion
    r"rm\s+-rf\s+\*",            # Mass file deletion
    r"mkfs",                     # Disk format
    r"dd\s+if=",                 # Raw disk write
    r">:?\s*/dev/sd",            # Overwriting disk blocks
    r"shutdown",                 # System shutdown
    r"reboot",                   # System reboot
    r"chmod\s+-R\s+777\s+/",     # Broad permission change
]

def validate_command(command: str) -> tuple[bool, str]:
    """
    Validates a shell command for dangerous operations.
    Returns (is_safe: bool, reason: str).
    """
    if not command or not command.strip():
        return True, "Empty command."

    cmd_clean = command.strip().lower()

    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, cmd_clean):
            return False, f"Potentially dangerous command pattern detected: '{pattern}'"

    return True, "Command is safe."
