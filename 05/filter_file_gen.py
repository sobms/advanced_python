def filter_file(file, words_list):
    words_dict = dict.fromkeys([word.lower() for word in words_list])
    if isinstance(file, str):
        file = open(file, "r")
    while True:
        line = file.readline().lower()
        for word in line.split():
            if word in words_dict:
                yield line
        if not line:
            break

    file.close()


if __name__ == "__main__":
    file_obj = open("input2", "r")
    for string in filter_file(file_obj, ["abc", "sTu", "DEF"]):
        print(string, end="")
