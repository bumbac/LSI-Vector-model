import pickle
import time

from preprocessing import token as tk
from vector import vector
from LSI import lsi


if __name__ == '__main__':

    filepath = 'lsi-data/articles/tmp2/'
    max_articles = 368
    # create_index(filepath, max_articles=max_articles)
    start = time.monotonic()
    docterm_list = tk.create_space(filepath, max_articles=max_articles)
    terms, matrix = vector.create_matrix(docterm_list)
    matrices_dict = lsi.svd(matrix)
    matrices_dict["Terms"] = terms
    # dictionary of doc_number: document filename
    doc_filenames = {}
    for docterm in docterm_list:
        doc_filenames[docterm['i']] = docterm['n']
    matrices_dict["doc_filenames"] = doc_filenames

    matrices_dict["docterm_list"] = docterm_list
    # Save matrices_dict to file
    filehandler = open('file.dat', 'wb')
    pickle.dump(matrices_dict, filehandler)
    filehandler.close()

    res = time.monotonic() - start
    print("Time:", res)

