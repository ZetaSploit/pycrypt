from tree_sitter import Parser, Language, Query, QueryCursor
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


class QueryHandler:
    def __init__(self):
        self.file_parser = FileParser()

    def get_tree(self, file):
        tree = self.file_parser.parse_file(file)

        print("Root node:", tree.root_node.type)

        for child in tree.root_node.children:
            print("Child:", child.type)

        return tree

    def print_tree(self, node, indent=0):
        print("  " * indent + node.type)

        for child in node.children:
            self.print_tree(child, indent + 1)
        

query_handler = QueryHandler()

tree = query_handler.get_tree("test.py")
tree2 = query_handler.print_tree(tree.root_node)

