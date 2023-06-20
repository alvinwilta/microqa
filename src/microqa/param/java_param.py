import re


def java_extract_params(file_path):
    with open(file_path, "r") as f:
        file_contents = f.read()

    func_pattern = re.compile(
        # 2 types
        # public type name(param) | public static type name(param)
        r"(?:public\s+(\w+)\s*\((.*?)\)|public\s*static\s*(?:(?!\bclass\b)\b\w+\b)\s*(\w*)\((.*?)\)|public\s*(?:(?!\bclass\b)\b\w+\b)\s*(\w*)\((.*?)\))",
        re.DOTALL,
    )
    matches = func_pattern.findall(file_contents)

    func_params = {}
    for match in matches:
        func_name = match[0] or match[2]
        params = match[1] or match[3]
        param_list = list(
            filter(lambda x: x != '', [
                p.strip().split(" ")[1]
                for p in params.split(",")
                if p.strip()
            ]))
        if len(param_list) != 0:
            func_params[func_name] = param_list

    return func_params
