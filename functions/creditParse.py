def parse(file_name):
    # setup file and return list
    file = open(file_name, "r")
    text_info = []

    for line in file:
        if len(line.strip()) == 0:
            text_info.append("")
        else:
            cur_line = line.strip()
            text_info.append(cur_line)

    return text_info
