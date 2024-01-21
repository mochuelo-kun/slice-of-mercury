import re

def str_to_safe_id(text: str) -> str:
    no_spaces = text.replace(" ", "_")
    alphanumderscore_only = re.sub(r'[^A-Za-z0-9_]+', "", no_spaces)
    no_multi_underscore = re.sub(r'_+', "_", alphanumderscore_only)
    lowercased = no_multi_underscore.lower()
    return lowercased
