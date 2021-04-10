import os
from hashlib import sha256
from preprocessing import token as tk
from vector import vector
from LSI import lsi
from app import console
if __name__ == '__main__':
    path = 'articles/'
    docterm_list = tk.create_space(path)
    terms, matrix = vector.create_matrix(docterm_list)
    matrices_dict = lsi.svd(matrix)
    console.start(matrices_dict)
