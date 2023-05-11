import json
import pygraphviz as pgv

out_dir = "./graph"
filename = "robot-shop.dot"


# TODO: Parse from json file and API
def parse_weavescope(arg):
    # with open('data.json') as f:
    #     data = json.load(f)
    # return data
    G = pgv.AGraph(strict=False, directed=True)
    if arg != 'alt':
        services = ["catalog",
                    "user",
                    "cart",
                    "rabbitmq",
                    "mongodb",
                    "redis",
                    "dispatch",
                    "shipping",
                    "ratings",
                    "payment",
                    "web", ]
        G.add_nodes_from(services)
        # manual input
        G.add_edge("catalog", "mongodb")
        G.add_edge("user", "mongodb")
        G.add_edge("user", "redis")
        G.add_edge("cart", "redis")
        G.add_edge("rabbitmq", "rabbitmq")
        G.add_edge("dispatch", "rabbitmq")
        G.add_edge("web", "payment")
        G.add_edge("web", "user")
        G.layout(prog="dot")
        G.write(f'{out_dir}/{filename}')
        return G
    else:
        services = ["app", "lb"]
        G.add_nodes_from(services)
        G.add_edge("lb", "app")
        G.layout(prog="dot")
        G.write(f'{out_dir}/{filename}')
        return G
