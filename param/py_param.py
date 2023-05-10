import os
import ast


def extract_params(node):
    params = []
    for arg in node.args.args:
        if arg.arg != "self":
            params.append(arg.arg)
    return params


def extract_params_from_file(file_path):
    with open(file_path) as f:
        tree = ast.parse(f.read())
        params_dict = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_name = node.name
                params = extract_params(node)
                params_dict[func_name] = params
        return params_dict


def extract_params_from_dir(dir_path):
    params_dict = {}
    for dirpath, _, filenames in os.walk(dir_path):
        for filename in filenames:
            if filename.endswith(".py"):
                file_path = os.path.join(dirpath, filename)
                params_dict.update(extract_params_from_file(file_path))
    return params_dict


params_dict = extract_params_from_dir("../robot-shop/payment")
for func_name, params in params_dict.items():
    print(f"Function {func_name} has arguments: {params}")
