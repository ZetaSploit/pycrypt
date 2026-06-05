from tree_sitter import Query, QueryCursor
import tree_sitter_python as tspython
from treesitter_load import *


qh = QueryHandler()
tree = qh.get_tree(ftp)
tree_print = qh.print_tree(tree.root_node)

if __name__ == "__main__":

    def run_query(tree):
        query = Query(PY_LANGUAGE, "(identifier) @function.name")

        cursor = QueryCursor(query)

        for node in cursor.captures(tree.root_node):
            print(node)

    run_query(tree)
