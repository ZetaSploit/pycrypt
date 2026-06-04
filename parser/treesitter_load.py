from tree_sitter import Parser, Language
import tree_sitter_python as tspython
from pathlib import Path


PY_LANGUAGE = Language(tspython.language())
ftp = input("File to be parsed: ")

class FileParser:
    def __init__(self):
        self.parser = Parser(PY_LANGUAGE)

    def read_file(self, ftp) -> str:
        file_path = Path(ftp)

        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {ftp}")

        return file_path.read_text(encoding="utf-8")

    def parse_source(self, source: str):
        return self.parser.parse(source.encode("utf-8"))

    def parse_file(self, ftp):
        source = self.read_file(ftp)
        return self.parse_source(source)


class QueryHandler:
    def __init__(self):
        self.file_parser = FileParser()

    def get_tree(self, ftp):
        return self.file_parser.parse_file(ftp)

    def print_tree(self, node, indent=0):
        print("  " * indent + node.type)

        for child in node.children:
            self.print_tree(child, indent + 1)
        
if __name__ == "__main__":
    query_handler = QueryHandler()

    tree = query_handler.get_tree(ftp)
    query_handler.print_tree(tree.root_node)

