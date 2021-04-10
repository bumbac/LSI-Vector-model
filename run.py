import os
from hashlib import sha256
from preprocessing import token as tk
from vector import vector
from LSI import lsi
from app import console

if __name__ == '__main__':
    path = 'articles/example/'
    docterm_list = tk.create_space(path)
    terms, matrix = vector.create_matrix(docterm_list)
    matrices_dict = lsi.svd(matrix)
    matrices_dict["Terms"] = terms
    flag = True
    while flag:
        top = console.start(matrices_dict)
        print("top doc ids:", top)
        for id in top:
            document = docterm_list[id]
            filename = path + document['n']
            print(id, document['i'], filename)
            f = open(filename)
            print(f.read())
        flag = False
