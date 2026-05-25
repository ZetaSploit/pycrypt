from tree_sitter import Parser, Language
import tree_sitter_python as tspython
from pathlib import Path


PY_LANGUAGE = Language(tspython.language())


class FileParser:
    def __init__(self):
        self.parser = Parser(PY_LANGUAGE)

    def read_file(self, path: str) -> str:
        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        return file_path.read_text(encoding="utf-8")

    def parse_source(self, source: str):
        return self.parser.parse(source.encode("utf-8"))

    def parse_file(self, path: str):
        source = self.read_file(path)
        return self.parse_source(source)

file_parser1 = FileParser()
tree = file_parser1.parse_file("test.py")
print(tree.root_node)

