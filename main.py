import sys
import os
import yaml
import subprocess
import pygraphviz as pgv
from tqdm import tqdm

sys.path.insert(0, "./param/")
# fmt: off
import lang_parser as lp
from parse_weavescope import parse_weavescope
sys.path.insert(0, "./rules/")
import rules as ru


config_filepath = "./config.yaml"
graph_output_dir = "./graph"

allowed_lang = ["js", "py", "go", "java", "php"]
lang_function_parser = {
    "java": lp.java_extract_params,
    "py": lp.py_extract_params,
    "go": lp.go_extract_params,
    "js": lp.js_extract_params,
    "php": lp.php_extract_params,
}

class Rule:
    def __init__(self, val, name, param_min, param_max, is_best_left, max):
        self.val = val
        self.name = name
        self.param_min = param_min
        self.param_max = param_max
        self.is_best_left = is_best_left
        self.max = max

    def printValue(self):
        print(f"{self.name} Value: " + str(self.val))

    def printProgress(self):
        left = "better" if self.is_best_left else "worse"
        right = "worse" if self.is_best_left else "better"

        print(f"({left}) {self.param_min} 0 ", end='')
        self.progress(self.max,self.val) if self.max != '+' else print('-', end='')
        print(f" {self.max} {self.param_max} ({right})")

    def progress(self, max, value):
        value = int((value / max) * 15)
        max = 15
        remaining = max - value
        filled = chr(0x2588) + chr(0x2502)
        empty = chr(0x2591) + chr(0x2502)
        filled_char = filled * value
        empty_char = empty * remaining
        print(filled_char + empty_char,end='')

    def print(self):
        self.printValue()
        self.printProgress()

class Microservice:
    def __init__(self, config):
        self.config = config
        self.param = parse_parameter_from_config(config)
        self.call_graph = generate_graph_from_config(config)
        self.total_services = len(self.call_graph)
        # self.service_graph = parse_weavescope('alt' if self.config["name"] == "tns" else "robot")
        self.service_graph = parse_weavescope(list(self.config["services"]), self.config['service_connection_type'], self.config['service_connection_param'] or '')
        self.list_services = list(self.config['services'])

    def total_param(self) -> dict:
        list_total_param = {}
        for service in self.param:
            total_elements = 0
            for function in self.param[service]:
                total_elements += (
                    len(self.param[service][function])
                    if self.param[service][function] != ""
                    else 0
                )
            list_total_param[service] = total_elements
        return list_total_param

    def total_unique_param(self):
        list_total_unique_param = {}
        for service in self.param:
            param_set = set()
            for function in self.param[service]:
                for param in self.param[service][function]:
                    param_set.add(param)
            list_total_unique_param[service] = len(param_set)
        return list_total_unique_param

    def total_operations(self):
        # Graph nodes
        list_total_service_ops = {}
        for service in self.call_graph:
            graph = pgv.AGraph()
            graph.read(self.call_graph[service])
            list_total_service_ops[service] = len(graph.nodes())
        return list_total_service_ops

    def total_edges(self):
        # Graph edges
        list_total_one_service_edges = {}
        for service in self.call_graph:
            graph = pgv.AGraph()
            graph.read(self.call_graph[service])
            list_total_one_service_edges[service] = len(graph.edges())
        return list_total_one_service_edges

    def in_node(self):
        list_in_service_count = {}
        for target in self.service_graph.nodes():
            in_count = 0
            for node in self.service_graph.nodes():
                if self.service_graph.has_edge(node, target):
                    in_count += 1
            list_in_service_count[target] = in_count
        return list_in_service_count

    def out_node(self):
        list_out_service_count = {}
        for target in self.service_graph.nodes():
            out_count = 0
            for node in self.service_graph.nodes():
                if self.service_graph.has_edge(target, node):
                    out_count += 1
            list_out_service_count[target] = out_count
        return list_out_service_count

    def indirect_call(self):
        return self.out_node()


def import_config(filepath):
    config = {}
    with open(filepath, "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(e)

    return config


def clean_directory(path):
    files = os.listdir(path)
    # Iterate over the files and remove them
    for file in files:
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)


def generate_graph_from_config(config):
    # manage commands for running the perl script
    clean_directory(graph_output_dir)
    commands = []
    service_graph_filename = {}
    for service in config["services"]:
        # check lang
        lang = config["services"][service]["lang"]
        if lang not in allowed_lang:
            print(f"language {lang} is not allowed")
            exit()
        # check path
        full_dir = config["root_dir"] + config["services"][service]["dir"]
        out_file = f'{graph_output_dir}/{config["name"]}-{service}.dot'
        service_graph_filename[service] = out_file
        commands.append(
            ["perl", "callGraph", full_dir, "-language", lang, "-output", out_file]
        )

    # run multiple process simultaneously
    procs = [subprocess.Popen(i) for i in commands]
    for p in procs:
        p.wait()
    return service_graph_filename



def extract_params_from_dir(dir_path, parser, lang):
    params_dict = {}
    for dirpath, _, filenames in os.walk(dir_path):
        for filename in filenames:
            if filename.endswith(f".{lang}"):
                file_path = os.path.join(dirpath, filename)
                params_dict.update(parser(file_path))
    return params_dict


def parse_parameter_from_config(config):
    list_param = {}
    for service in config["services"]:
        lang = config["services"][service]["lang"]
        full_dir = config["root_dir"] + config["services"][service]["dir"]
        params = extract_params_from_dir(
            full_dir, lang_function_parser[lang], lang)
        list_param[service] = params
    return list_param


if __name__ == "__main__":
    config = import_config(config_filepath)
    ms = Microservice(config)
    # debug
    # print(ms.total_param())
    # print(ms.total_unique_param())
    # print(ms.total_operations())
    # print(ms.total_edges())
    # print(ms.service_count)
    # print(ms.out_node())
    # print(ms.in_node())
    print()
    alcom = ru.ALCOM(ms.list_services, ms.total_param(),ms.total_unique_param(),ms.total_operations())
    c_alcom = Rule(alcom,"ALCOM","Less Cohesive","Highly Cohesive",False,1)
    c_alcom.print()
    acs = ru.ACS(ms.list_services,ms.in_node(),ms.out_node())
    c_acs = Rule(acs, "ACS", "Loosely Coupled","Tightly Coupled",True,1)
    c_acs.print()
    tcm = ru.TCM(ms.list_services,ms.total_services,ms.total_operations(),ms.total_edges(),ms.indirect_call())
    c_tcm = Rule(tcm,"TCM","Low Complexity","High Complexity",True,"+")
    c_tcm.print()