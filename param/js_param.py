import re


def extract_params(file_path):
    with open(file_path, "r") as f:
        file_contents = f.read()

    func_pattern = re.compile(
        # taking those 3 function declaration into account
        # function name(param) | var name = function(param) {} | const name = (param) => {}
        r"(?:(?:const|var|let)\s+(\w+)\s*=\s*function\s*\((.*?)\)|function\s+(\w+)\s*\((.*?)\)\s*\{|const\s+(\w+)\s*=\s*\((.*?)\)\s*=>\s*{)",
        re.DOTALL,
    )
    matches = func_pattern.findall(file_contents)

    func_params = {}
    for match in matches:
        func_name = match[0] or match[2] or match[4]
        params = match[1] or match[3] or match[5]
        param_list = [p.strip() for p in params.split(",")]
        func_params[func_name] = param_list

    return func_params


if __name__ == "__main__":
    file_path = "../robot-shop/catalogue/server.js"
    func_params = extract_params(file_path)
    print(func_params)
