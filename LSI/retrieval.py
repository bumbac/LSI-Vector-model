import numpy as np
from numpy.linalg import norm


def func(matrices_dict, query_vector):
    """
    Finds most similar articles from calculated matrices in matrices_dict
    based on query_vector
    :param matrices_dict: matrices from A = USV, D and S inverted
    :param query_vector: dict{term: weight}
    :return: descending list of tuples(doc_number, similarity)
    """
    u = matrices_dict["U"]
    s = matrices_dict["S"]
    v = matrices_dict["V"]
    d = matrices_dict["D"]
    v = np.transpose(v)
    s_inv = matrices_dict["S_inv"]
    q_t = np.transpose(query_vector)
    q_new = np.linalg.multi_dot([q_t, u, s_inv])
    ranking_of_documents = {}
    for d_ in range(v.shape[1]):
        document = v[:][d_]
        ranking = similarity(q_new, document)
        ranking_of_documents[d_] = ranking
    sorted_documents = sorted(ranking_of_documents, key=ranking_of_documents.get, reverse=True)
    top_k = 3
    sorted_doc_similarity = []
    for doc_number in sorted_documents:
        sorted_doc_similarity.append((doc_number, ranking_of_documents[doc_number]))
    return sorted_doc_similarity[:top_k]


def similarity(query, document):
    """
    Calculates cosine similarity of query to document.
    :param query: dict{term: weight}
    :param document: docterm vector from V matrice - transformed by SVD concepts
    :return: float cosine similarity
    """
    frac_top = np.dot(query, document)
    frac_bottom = (norm(query) * norm(document))
    # TODO
    # WHAT DOES IT MEAN???
    result = [0]
    if frac_bottom != 0:
        result = frac_top / frac_bottom
    return result[0]
