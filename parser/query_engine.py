from tree_sitter import Query, QueryCursor
import hashlib
from treesitter_load import FileParser


class QueryHandler(FileParser):
    def get():
        file_parser1 = FileParser()
        tree = file_parser1.parse_file("test.py")
        for i in tree.root_node:
            pass

