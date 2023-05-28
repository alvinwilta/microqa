import json
import re
import pygraphviz as pgv
import requests
import os


def _match_regex_list(test_list, regex_list):
    # the test list will be tested in any of the regex list
    # [el1, el2, el3]
    for i in range(len(test_list)):
        for regex in regex_list:
            if (re.match(regex, test_list[i])):
                test_list[i] = re.compile(
                    regex, re.DOTALL).findall(test_list[i])[0]
                break
    return test_list


def weavescope_extract_connection(service_list, type, arg, out_dir):
    # repo = repository name to differentiate the container from other container in the machine
    # type = options <file/api> to determine service graph source, file is .json type (from weave)
    # arg = arguments for each opt. file = filepath, api = hostname
    if type == 'file':
        ext = os.path.splitext(arg)[1]
        if ext == ".json":
            with open(arg, 'r') as f:
                raw_data = json.load(f)
        else:
            print('only .json output from weavescope is allowed')
            quit()
    elif type == 'api':
        if arg is None or arg == '':
            arg = 'localhost:4040'
        url = f'http://{arg}/api/topology/containers-by-image'
        response = requests.get(url)
        raw_data = json.loads(response.text)
    else:
        print('parse option for weavescope not recognized.')
        quit()
    try:
        # use repo name
        pattern = []
        for service in service_list:
            pattern.append(f'.*({service}).*')

        # sample one service, check the repo name, the repo name will be the base regex to determine which is actually the microservice
        sample = ''
        for i in range(len(raw_data['nodes'])):
            if (re.match(re.compile(f'.*{service_list[0]}.*'), list(raw_data['nodes'])[i])):
                sample = list(raw_data['nodes'])[i]
        repo = sample.split('/')[0]

        data = {'nodes': {}}
        # remove all elements that is not included in the repo
        for container in raw_data['nodes']:
            if (re.match(re.compile(f'.*{repo}.*'), container)):
                data['nodes'][container] = raw_data['nodes'][container]

        filtered_container = {}

        # Parse data, rename image name into service name
        for container in data["nodes"]:
            found = False
            for service in service_list:
                if (re.match(re.compile(f'.*({service}).*'), container)):
                    if ('adjacency' in data['nodes'][container]):
                        # if there is attribute named adjacency
                        filtered_container[service] = _match_regex_list(
                            data['nodes'][container]['adjacency'], pattern)
                    else:
                        filtered_container[service] = []
                    found = True
                    break
            if not found:
                if 'adjacency' in data['nodes'][container]:
                    filtered_container[container] = _match_regex_list(
                        data['nodes'][container]['adjacency'], pattern)
                else:
                    filtered_container[container] = []

        G = pgv.AGraph(strict=False, directed=True)

        G.add_nodes_from(filtered_container)

        for target_container in filtered_container:
            for container in filtered_container:
                for adjacency in filtered_container[container]:
                    if (adjacency == target_container):
                        G.add_edge(container, target_container)
                        break

        G.layout(prog="dot")
        G.write(out_dir + '/service-graph.dot')
        return G
    except:
        if type == 'api':
            print('api error, is the weavescope running?')
        else:
            print('json parse error, is the json file from weavescope?')
        quit()
