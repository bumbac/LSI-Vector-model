import bisect
import numpy as np
from LSI import retrieval


def read_input(doc_filenames):
    """
    Reads console input for document name and finds it.
    :return: tuple(doc_id, doc_filename)
    """
    correct_format = False
    while not correct_format:
        test = False
        line = ""
        if test:
            line = 'article2.txt'
        else:
            line = input("Write filename of article to find similar."
                         "For example: article2.txt\n")
        # item = (doc_id, doc_filename)
        for item in doc_filenames.items():
            if line == item[1]:
                return item


def start(matrices_dict):
    """
    CLI interface for fetching similar documents.
    :param matrices_dict: dict of calculated matrices U, S, V, D, S_inv
    :return: descending list of tuples(doc_number, similarity)
    """
    doc_filenames = matrices_dict['doc_filenames']
    while True:
        article_tuple = read_input(doc_filenames)
        return retrieval.func(matrices_dict, article_tuple)

