from tree_sitter import Query, QueryCursor
import tree_sitter_python as tspython
import hashlib
from treesitter_query import *


tree_object = QueryHandler()
language = PY_LANGUAGE

tree = tree_object.get_tree(ftp)
#tree_printed = tree_object.print_tree(tree.root_node)


if __name__ == "__main__":
    
    def skim_tree():
        cursor = tree.walk()
        print(cursor.node.type)

    skim_tree()
