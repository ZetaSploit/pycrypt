from tree_sitter import Query, QueryCursor
import tree_sitter_python as tspython
import hashlib
from treesitter_load import *

query_handler = QueryHandler()

if __name__ == "__main__":

    def run_query(tree, query):
        query = Query(PY_LANGUAGE, """(identifier) @id""")

        cursor = QueryCursor(query)

        for node in cursor.captures(tree.root_node):
            #if node.encode("utf-8") == "md5":
                #print("Found md5")
            print(node)

    run_query(query_handler.get_tree(ftp), "md5") 
