import numpy as np
from numpy.linalg import norm


def func(matrices_dict, query_vector):
    u = matrices_dict["U"]
    s = matrices_dict["S"]
    v = matrices_dict["V"]
    d = matrices_dict["D"]
    s_inv = matrices_dict["S_inv"]
    q_t = np.transpose(query_vector)
    q_new = np.linalg.multi_dot([q_t, u, s_inv])
    doc_by_concept_list = []
    ranking_of_documents = {}
    for d_ in range(v.shape[1]):
        document = v[:][d_]
        ranking = similarity(q_new, document)
        ranking_of_documents[d_] = ranking
    sorted_documents = sorted(ranking_of_documents, key=ranking_of_documents.get)
    top_k = 2

    return sorted_documents[:top_k]


def similarity(query, document):
    frac_top = np.dot(query, document)
    frac_bottom = (norm(query) * norm(document))
    return frac_top / frac_bottom
