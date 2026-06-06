from tree_sitter import Query, QueryCursor
from treesitter_load import *


parser = FileParser()

with open(ftp, "rb") as f:
    source = f.read()

tree = parser.parse_file(ftp)

query = Query(
    PY_LANGUAGE,
    "(identifier) @function.name"
)

if __name__ == "__main__":

    def run_query(tree, source):
        cursor = QueryCursor(query)

        captures = cursor.captures(tree.root_node)

        for node in captures["function.name"]:
            text = source[node.start_byte:node.end_byte].decode("utf-8")
            print(text)

    run_query(tree, source)
