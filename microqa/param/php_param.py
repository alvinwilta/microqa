import re


def php_extract_params(file_path):
    with open(file_path, "r") as f:
        file_contents = f.read()

    func_pattern = re.compile(
        # 3 types
        # name = function(param) | name = fn(param) => { | function name(param)
        r"(?:(\w*)\s*=\s*function\s*\((.*?)\)|(\w+)\s*=\s*fn\((.*?)\)\s*=>|function\s*(\w*)\((.*?)\))",
        re.DOTALL,
    )
    matches = func_pattern.findall(file_contents)

    func_params = {}
    for match in matches:
        func_name = match[0] or match[2] or match[4]
        params = match[1] or match[3] or match[5]
        param_list = [
            p.strip().replace("$", "") if len(
                p.split()) == 1 else p.strip().split(" ")[1].replace("$", "")
            for p in params.split(",")
            if p.strip().replace("$", "")
        ]
        if len(param_list) != 0:
            func_params[func_name] = param_list

    return func_params
