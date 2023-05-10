import re


def extract_params(file_path):
    with open(file_path, "r") as f:
        file_contents = f.read()

    func_pattern = re.compile(
        # taking those 3 function declaration into account
        # name = function(param) | name = fn(param) => { |
        r"(?:(\w*)\s*=\s*function\s*\((.*?)\)|(\w+)\s*=\s*fn\((.*?)\)\s*=>|function\s*(\w*)\((.*?)\))",
        re.DOTALL,
    )
    matches = func_pattern.findall(file_contents)

    func_params = {}
    for match in matches:
        func_name = match[0] or match[2] or match[4]
        params = match[1] or match[3] or match[5]
        param_list = [
            p.strip().split(" ")[1].replace("$", "")
            for p in params.split(",")
            if p.strip()
        ]
        func_params[func_name] = param_list

    return func_params


if __name__ == "__main__":
    file_path = "../robot-shop/ratings/html/src/Kernel.php"
    func_params = extract_params(file_path)
    print(func_params)
