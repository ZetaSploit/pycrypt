from pathlib import Path
from treesitter_load import ftp

LANGUAGES = {
    ".py": "python",
}

def get_language_from_file(path: str) -> str | None:
    return LANGUAGES.get(Path(path).suffix)

lang = get_language_from_file(ftp)

if lang:
    print(lang)
