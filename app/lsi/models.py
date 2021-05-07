import numpy as np
from numpy.linalg import norm


class Article:
    """
    Class representing article
    """

    def __init__(self, art_id, title, content, sim):
        self.art_id = art_id
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


def func(matrices_dict, doc_tuple):
    """
    Finds most similar articles from calculated matrices in matrices_dict
    based on query_vector
    :param matrices_dict: matrices from A = USV, D and S inverted
    :param doc_tuple: tuple(doc_id, doc_filename)
    :return: descending list of tuples(doc_number, similarity)
    """
    u = matrices_dict['U']
    s = matrices_dict['S']
    v = matrices_dict['V']
    d = matrices_dict['D']
    doc_id = doc_tuple[0]
    q_t = v[:, doc_id]
    # dict(doc_id, similarity)
    ranking_of_documents = {}
    # iterate all columns = documents in concept space (V)
    for d_ in range(v.shape[1]):
        document = v[:, d_]
        if d_ == doc_id:
            # ranking should be == 1
            ranking = similarity(q_t, document)
            continue
        ranking = similarity(q_t, document)
        ranking_of_documents[d_] = ranking
    # descending order of most relevant doc_ids
    sorted_doc_ids = sorted(ranking_of_documents, key=ranking_of_documents.get, reverse=True)
    top_k = 5
    # tuples (doc_id, similarity)
    sorted_doc_similarity = []
    for doc_id in sorted_doc_ids:
        sorted_doc_similarity.append((doc_id, ranking_of_documents[doc_id]))
    return sorted_doc_similarity[:top_k]


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
