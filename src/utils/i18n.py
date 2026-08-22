"""
src/utils/i18n.py
Utility functions for loading and managing application translations.
"""
import json
import os


def load_translations(lang_code="en_us"):
    """
    Loads the translation dictionary for the given language code.
    Defaults to 'en_us' if the file is not found.
    """
    # Navigate up from src/utils/i18n.py to the project root
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    file_path = os.path.join(base_dir, "locales", f"{lang_code}.json")

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(
            f"Warning: Translation file for '{lang_code}' not found. Falling back to en_us.")
        fallback_path = os.path.join(base_dir, "locales", "en_us.json")
        with open(fallback_path, 'r', encoding='utf-8') as fallback_file:
            return json.load(fallback_file)

# Example usage (can be imported in your Dash layout callbacks):
# t = load_translations("pt_br")
# print(t["nav"]["overview"])
