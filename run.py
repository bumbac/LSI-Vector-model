import os
from hashlib import sha256
from preprocessing import token as tk
from vector import vector
from LSI import lsi

if __name__ == '__main__':
    path = 'articles/'
    files = os.listdir(path)
    save_dir = 'matrixes'
    cnt = 0
    docterm_list = []
    unique_doc_ids = []
    # preprocess
    unique_terms = set()
    for f in files:
        # testing break
        if cnt > 6:
            break
        cnt += 1
        document_file = open(path + f)
        document = document_file.read()
        id = sha256(bytearray(document, encoding='utf8'))
        if not id in unique_doc_ids:
            unique_doc_ids.append(id)
        else:
            print("double document", id, path, f)
        tokens = tk.tokenize(document)
        clean_tokens = tk.remove_stops(tokens)
        clean_words = tk.stemmatize(clean_tokens)
        save_path = None # save_dir + 'm_' + f
        # creates vector of terms with relative weight to this document
        docterm = vector.make_docterm_vector(clean_words, save_path, id=str(id))
        docterm_list.append(docterm)
        unique_terms.update(docterm.keys())
    unique_terms.remove("i")
    unique_terms.remove("t")
    frozen_terms, matrix = vector.make_matrix(docterm_list, unique_terms)
    print(frozen_terms, matrix)
    lsi.svd(matrix)
