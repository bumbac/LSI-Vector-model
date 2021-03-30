import os
from preprocessing import token as tk
from vector import vector

if __name__ == '__main__':
    path = 'articles/'
    files = os.listdir(path)
    save_dir = 'matrixes'
    cnt = 0
    docterm_list = []
    # preprocess
    unique_terms = set()
    for f in files:
        # testing break
        if cnt > 3:
            break
        cnt += 1
        document_file = open(path + f)
        document = document_file.read()
        tokens = tk.tokenize(document)
        clean_tokens = tk.remove_stops(tokens)
        clean_words = tk.stemmatize(clean_tokens)

        save_path = None # save_dir + 'm_' + f
        docterm = vector.make_docterm_vector(clean_words, save_path, id=cnt)
        docterm_list.append(docterm)
        unique_terms.update(docterm.keys())
    frozen_terms, matrix = vector.make_matrix(docterm_list, unique_terms)
