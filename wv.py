import json
import pygraphviz as pgv

out_dir = "."
filename = "robot-shop.dot"

G = pgv.AGraph(strict=False, directed=True)
services = ["rs-load",
            "catalog",
            "user",
            "cart",
            "rs-rabbitmq",
            "rs-mongodb",
            "rs-redis",
            "dispatch",
            "shipping",
            "ratings",
            "payment",
            "rs-web", ]
G.add_nodes_from(services)

G.add_edge("rs-load","payment")
G.add_edge("rs-load","rs-web")
G.add_edge("payment","dispatch")
G.add_edge("dispatch", "rs-rabbitmq")
G.add_edge("rs-rabbitmq", "rs-rabbitmq")
G.add_edge("rs-web", "ratings")
G.add_edge("rs-web", "user")
G.add_edge("rs-web", "cart")
G.add_edge("rs-web", "catalog")
G.add_edge("cart", "rs-redis")
G.add_edge("user", "rs-redis")
G.add_edge("user", "shipping")
G.add_edge("user", "rs-mongodb")
G.add_edge("catalog", "rs-mongodb")
G.layout(prog="dot")
G.write(f'{out_dir}/{filename}')
