def file_to_list(file_path):
    lines = []
    with open(file_path, "r") as f:
        for line in f:
            lines += [line.replace("\n", "")]
    return lines

def list_to_file(filename, ls):
    with open(filename, "w") as f:
        for i in ls:
            f.write(f"{i}\n")
