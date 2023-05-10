import re


def extract_params(file_path):
    with open(file_path, "r") as f:
        file_contents = f.read()

    func_pattern = re.compile(
        # Taking 2 function declaration
        # func name(param) | name := func(param)
        r"(?:func\s+(\w+)\s*\((.*?)\)|(\w*)\s*:=\s*func\s*\((.*?)\))",
        re.DOTALL,
    )
    matches = func_pattern.findall(file_contents)

    func_params = {}
    for match in matches:
        func_name = match[0] or match[2]
        params = match[1] or match[3]
        param_list = [p.strip().split(" ")[0] for p in params.split(",") if p.strip()]
        func_params[func_name] = param_list

    return func_params


if __name__ == "__main__":
    file_path = "./test/example.go"
    func_params = extract_params(file_path)
    print(func_params)
