import sys
import os
import yaml
import subprocess
import pygraphviz as pgv
import shutil
import argparse

from microqa.param import java_param, go_param, js_param, php_param, py_param
from microqa.service_graph import dot_graph, weavescope_graph
from microqa.rules import ACS, ALCOM, TCM, interface

default_config_filepath = "./microqa-config.yaml"
graph_output_dir = "./graph"

allowed_lang = ["js", "py", "go", "java", "php"]
lang_function_parser = {
    "java": java_param.java_extract_params,
    "py": py_param.py_extract_params,
    "go": go_param.go_extract_params,
    "js": js_param.js_extract_params,
    "php": php_param.php_extract_params,
}
rule_functions = {
    'ACS': ACS.ACS,
    'ALCOM': ALCOM.ALCOM,
    'TCM': TCM.TCM
}


class Microservice:
    def __init__(self, config):
        self.config = config
        self.param = _parse_parameter_from_config(config)
        self.call_graph = _generate_graph_from_config(config)
        self.total_services = len(self.call_graph)
        # self.service_graph = parse_weavescope('alt' if self.config["name"] == "tns" else "robot")
        self.service_graph = self._import_service_graph()
        self.list_services = list(self.config['services'])

    def _import_service_graph(self):
        # adjust according to the options. Currently supported options are:
        # - file with .dot
        # - file with .json obtained from the weavescope API
        # - direct connection with weavescope API
        # add more on service_graph/ directory
        if self.config['service_connection_type'] == 'file':
            if self.config['service_connection_source'] == 'dot':
                return dot_graph.dot_extract_connection(self.config['service_connection_param'])
            elif self.config['service_connection_source'] == 'weavescope':
                return weavescope_graph.weavescope_extract_connection(list(self.config["services"]), self.config['service_connection_type'], self.config['service_connection_filename'] or '', graph_output_dir)
            else:
                print("Error: Unrecognized service connection source, current available source for 'file' type is 'dot' or 'weavescope'.")
                sys.exit(11)
        elif self.config['service_connection_type'] == 'api':
            return weavescope_graph.weavescope_extract_connection(list(self.config["services"]), self.config['service_connection_type'], self.config['service_connection_hostname'] or '', graph_output_dir)
        else:
            print(
                "Error: Unrecognized connection type, make sure that the input is either 'file' or 'api'.")
            sys.exit(12)

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

    def total_unique_param(self) -> dict:
        list_total_unique_param = {}
        for service in self.param:
            param_set = set()
            for function in self.param[service]:
                for param in self.param[service][function]:
                    param_set.add(param)
            list_total_unique_param[service] = len(param_set)
        return list_total_unique_param

    def total_service_ops(self) -> dict:
        # Graph nodes
        list_total_service_ops = {}
        for service in self.call_graph:
            graph = pgv.AGraph()
            graph.read(self.call_graph[service])
            list_total_service_ops[service] = len(graph.nodes())
        return list_total_service_ops

    def total_edges(self) -> dict:
        # Graph edges
        list_total_one_service_edges = {}
        for service in self.call_graph:
            graph = pgv.AGraph()
            graph.read(self.call_graph[service])
            list_total_one_service_edges[service] = len(graph.edges())
        return list_total_one_service_edges

    def in_node(self) -> dict:
        list_in_service_count = {}
        for target in self.service_graph.nodes():
            in_count = 0
            for node in self.service_graph.nodes():
                if self.service_graph.has_edge(node, target):
                    in_count += 1
            list_in_service_count[target] = in_count
        return list_in_service_count

    def out_node(self) -> dict:
        list_out_service_count = {}
        for target in self.service_graph.nodes():
            out_count = 0
            for node in self.service_graph.nodes():
                if self.service_graph.has_edge(target, node):
                    out_count += 1
            list_out_service_count[target] = out_count
        return list_out_service_count

    def indirect_call(self) -> dict:
        list_indirect_call = {}
        for node in self.service_graph.nodes():
            list_indirect_call[node] = self._count_indirect_node(
                self.service_graph, node)
        return list_indirect_call

    def _count_indirect_node(self, graph: pgv.AGraph, node: str):
        queue = list(dict.fromkeys(graph.out_neighbors(node)))
        visited = set(node)  # avoid cyclic counting
        indirect_count = len(graph.out_edges(node))
        while queue:
            current = queue.pop()
            neighbors = list(dict.fromkeys(graph.out_neighbors(current)))
            indirect_count += len(graph.out_edges(current))
            for node in neighbors:
                if node not in visited:
                    visited.add(node)
                    queue.append(node)
        return indirect_count


def import_config(filepath):
    # read yaml configuration
    config = {}
    with open(filepath, "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            print(e)

    return config


def create_dir(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
    except OSError:
        print('Error: Creating directory. ' + path)


def clean_dir(path):
    try:
        if os.path.exists(path):
            shutil.rmtree(path)
    except Exception:
        print('Error: Cleaning directory. ' + path)


def _generate_graph_from_config(config):
    """
    manage commands for running the perl script
    """
    # clean graph output directory
    clean_dir(graph_output_dir)
    create_dir(graph_output_dir)
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
            ["perl", "microqa/callGraph", full_dir, "-language", lang, "-output", out_file]
        )

    # run multiple process simultaneously
    procs = [subprocess.Popen(i) for i in commands]
    for p in procs:
        p.wait()
    return service_graph_filename


def _extract_params_from_dir(dir_path, parser, lang):
    params_dict = {}
    for dirpath, _, filenames in os.walk(dir_path):
        for filename in filenames:
            if filename.endswith(f".{lang}"):
                file_path = os.path.join(dirpath, filename)
                params_dict.update(parser(file_path))
    return params_dict


def _parse_parameter_from_config(config):
    list_param = {}
    for service in config["services"]:
        lang = config["services"][service]["lang"]
        full_dir = config["root_dir"] + config["services"][service]["dir"]
        params = _extract_params_from_dir(
            full_dir, lang_function_parser[lang], lang)
        list_param[service] = params
    return list_param


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c","--config", help="directory to configuration file", default=default_config_filepath)
    parsed_config = parser.parse_args()
    config = import_config(parsed_config.config)
    ms = Microservice(config)
    print()
    ruleinput = interface.RuleInterface(ms.total_services, ms.list_services, ms.total_param(), ms.total_unique_param(
    ), ms.total_service_ops(), ms.total_edges(), ms.in_node(), ms.out_node(), ms.indirect_call())
    # print the metrics
    for rule in config['rules']:
        if rule_functions[rule]:
            rule_functions[rule](ruleinput).print()
    # clean up directory
    clean_dir(graph_output_dir)


if __name__ == "__main__":
    main()
