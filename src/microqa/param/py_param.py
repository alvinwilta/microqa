import os
import ast


def extract_params(node):
    params = []
    for arg in node.args.args:
        if arg.arg != "self":
            params.append(arg.arg)
    return params


def py_extract_params(file_path):
    with open(file_path) as f:
        tree = ast.parse(f.read())
        params_dict = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_name = node.name
                params = extract_params(node)
                if len(params) != 0:
                    params_dict[func_name] = params
        return params_dict


def extract_params_from_dir(dir_path):
    params_dict = {}
    for dirpath, _, filenames in os.walk(dir_path):
        for filename in filenames:
            if filename.endswith(".py"):
                file_path = os.path.join(dirpath, filename)
                params_dict.update(py_extract_params(file_path))
    return params_dict
