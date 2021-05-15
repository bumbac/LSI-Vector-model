import numpy
import numpy as np
from numpy.linalg import norm
import time


class Article:
    """
    Class representing article
    """

    def __init__(self, art_id, category, title, content, sim):
        self.art_id = art_id
        self.category = category
        self.title = title
        self.content = content
        self.sim = sim


def get_article_id(file_name):
    article_id = file_name.replace(".txt", "")
    return article_id


def find_file(doc_filenames, filename):
    """
    Reads console input for document name and finds it.
    :return: tuple(doc_id, doc_filename)
    """
    for item in doc_filenames.items():
        if filename == item[1]:
            return item


def func(matrices_dict, doc_tuple, approx):
    """
    Finds most similar articles from calculated matrices in matrices_dict
    based on query_vector
    :param matrices_dict: matrices from A = USV, D and S inverted
    :param doc_tuple: tuple(doc_id, doc_filename)
    :return: descending list of tuples(doc_number, similarity)
    """
    # v = np.dot(matrices_dict['S_inv'], matrices_dict['D'])
    if approx:
        v = matrices_dict['V']
        v = v[:approx, :]
        print("v shape: ", v.shape)
    else:
        v = matrices_dict['A']
        print("v shape: ", v.shape)
    doc_id = doc_tuple[0]
    print("doc_tuple[0]", doc_tuple[0])
    q_t = v[:, doc_id]
    # dict(doc_id, similarity)
    ranking_of_documents = {}
    print("v[:, doc_id]", v[:, doc_id])
    # iterate all columns = documents in concept space (V)
    start = time.monotonic_ns()
    for d_ in range(v.shape[1]):
        # print("document = ", v[:, d_])
        document = v[:, d_]
        ranking = similarity(q_t, document)
        ranking_of_documents[d_] = ranking
    end = time.monotonic_ns() - start

    sorted_doc_ids = sorted(ranking_of_documents, key=ranking_of_documents.get, reverse=True)
    top_k = 10
    # tuples (doc_id, similarity)
    sorted_doc_similarity = []
    for doc_id in sorted_doc_ids:
        sorted_doc_similarity.append((doc_id, ranking_of_documents[doc_id]))
    return sorted_doc_similarity[:top_k + 1], end


def similarity(query, document):
    """
    Calculates cosine similarity of query to document.
    :param query: document vector transformed to concept space q = S_inv {dot} U^T {dot} q
    :param document: docterm vector from V matrix
    :return: float cosine similarity
    """
    frac_top = np.dot(query, document)
    frac_bottom = (norm(query) * norm(document))
    result = 0
    if frac_bottom != 0:
        result = frac_top / frac_bottom
    return result
