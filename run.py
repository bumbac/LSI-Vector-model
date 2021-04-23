import pickle

from preprocessing import token as tk
from vector import vector
from LSI import lsi
from app import console

if __name__ == '__main__':
    path = 'newarticles/'

    max_articles = 50
    docterm_list = tk.create_space(path, max_articles=max_articles)
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

    flag = False
    while flag:
        top = console.start(matrices_dict)
        if len(top) == 0:
            break
        print("top doc ids:", top)
        for doc_sim_tuple in top:
            doc_number = doc_sim_tuple[0]
            similarity_ranking = doc_sim_tuple[1]
            document = docterm_list[doc_number]
            filename = path + document['n']
            print('document:', doc_number, '||', filename, document['i'])
            # f = open(filename)
            print("SIMILARITY:", similarity_ranking)
            # print(f.read())
