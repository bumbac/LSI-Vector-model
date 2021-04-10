from LSI import retrieval


def read_input():
    correct_format = False
    query = {}
    while not correct_format:
        query = {}
        line = input("Write query with weights.\n"
                     "For example: cat 0.4 food 0.5 cheap 0.1\n")
        example_query = "cat 0.4 food 0.5 cheap 0.1"
        tokens = line.split(" ")
        # weight is missing, uneven number of parsed tokens
        if len(tokens) % 2:
            if len(tokens) == 1 and tokens[0] == "exit":
                return {}
            print("Incorrect format")
            continue
        weight = 0
        token = ""
        for i in range(len(tokens)):
            # first name, then weight
            # i % 2 == 1 for weights
            if i % 2:
                try:
                    weight = float(tokens[i])
                    query[token] = weight
                except ValueError:
                    print("Incorrect format.")
                    break
            # i % 2 == 0 for words
            else:
                token = tokens[i]
                # too big token, probably not a word
                if len(token) > 50:
                    print("Incorrect format.")
                    break
        correct_format = True
    return query


def start(matrices_dict):
    while True:
        query = read_input()
        if len(query) == 0:
            break
        print(query)
        retrieval.func(matrices_dict, query)






