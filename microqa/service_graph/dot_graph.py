import os
import pygraphviz as pgv
import sys


def dot_extract_connection(filename):
    ext = os.path.splitext(filename)[1]
    if ext == '.dot':
        G = pgv.AGraph()
        G.read(filename)
        return G
    else:
        print('Error: Only .dot file are allowed')
        sys.exit(31)
