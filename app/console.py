import bisect
import numpy as np
from LSI import retrieval


def read_input():
    """
    Reads console input in specific form and returns parsed query
    :return: dict{term: weight}
    """
    correct_format = False
    query = {}
    while not correct_format:
        query = {}
        test = False
        line = ""
        if test:
            line = "'poor 0.7 're 0.3"
        else:
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
    """
    CLI interface for fetching similar documents to query
    :param matrices_dict: dict of calculated matrices U, S, V, D, S_inv
    :return: descending list of tuples(doc_number, similarity)
    """
    terms = matrices_dict["Terms"]
    while True:
        tokens = read_input()
        if len(tokens) == 0:
            break
        print(tokens)
        query_vector = np.zeros((len(terms), 1), dtype=float)
        # assign weight to all terms
        for term in tokens.keys():
            term_id = bisect.bisect_left(terms, term)
            # term in query is not present in language space
            if term_id == len(terms):
                continue
            # term is present in the language space, update query vector
            if terms[term_id] == term:
                query_vector[term_id, 0] = tokens[term]
            # term in query is not present in language space
            if terms[term_id] != term:
                continue
        return retrieval.func(matrices_dict, query_vector)
