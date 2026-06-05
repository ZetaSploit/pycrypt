from tree_sitter import Query, QueryCursor
import tree_sitter_python as tspython
import hashlib
from treesitter_load import *


if __name__ == "__main__":

    def run_query(tree_obj, query):
        query_string = "(identifier) @function.name"
        query = Query(PY_LANGUAGE, query_string)
        qcursor = QueryCursor()

        for node, capture_name in qcursor.captures(query, tree.root_node):


    
