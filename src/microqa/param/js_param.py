import re


def js_extract_params(file_path):
    with open(file_path, "r") as f:
        file_contents = f.read()

    func_pattern = re.compile(
        # 3 types
        # function name(param) | var name = function(param) {} | const name = (param) => {}
        r"(?:(?:const|var|let)\s+(\w+)\s*=\s*function\s*\((.*?)\)|function\s+(\w+)\s*\((.*?)\)\s*\{|const\s+(\w+)\s*=\s*\((.*?)\)\s*=>\s*{)",
        re.DOTALL,
    )
    matches = func_pattern.findall(file_contents)

    func_params = {}
    for match in matches:
        func_name = match[0] or match[2] or match[4]
        params = match[1] or match[3] or match[5]
        param_list = list(
            filter(lambda x: x != '', [p.strip() for p in params.split(",")]))
        if len(param_list) != 0:
            func_params[func_name] = param_list

    return func_params
