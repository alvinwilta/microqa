import os
import pygraphviz as pgv


def dot_extract_connection(filename):
    ext = os.path.splitext(filename)[1]
    if ext == '.dot':
        G = pgv.AGraph()
        G.read(filename)
        return G
    else:
        print('only .dot file are allowed')
        quit()
