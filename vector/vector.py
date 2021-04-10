import os
import numpy as np


def make_docterm_vector(clean_words, save_path=None, id=0):
    """
    Create occurrence matrix of terms in @clean_document.
    :param clean_words: list[] of tokens, stemmatized, w/o stop words
    :param save_path: save location
    :return: dict{term: occurrence in [0, 1]}
    """
    # unique terms
    terms = set(clean_words)
    total = len(clean_words)
    # 'i' is unique identifier
    # 't' is total number of words in this document
    # always terms length > 1, so no conflicts
    docterm = {'i': id, 't': total}
    for term in terms:
        term_occurrence = 0
        for token in clean_words:
            if token == term:
                term_occurrence += 1
        # f_ij for terms in document j, other terms are not present ~= 0
        docterm[term] = term_occurrence / total
    if save_path:
        save_docterm_vector(docterm, save_path)
    return docterm


def update_docterm_vector(docterm: dict, term: str, term_occurrence: int):
    """
    # TODO: remove? not using it
    Probably useful when adding a new term to language.
    :param docterm: document with the term
    :param term: String term
    :param term_occurrence: number of occurrences
    """
    if term in docterm:
        pass
    else:
        old_total = docterm['t']
        total = old_total + term_occurrence
        docterm['t'] = total
        ratio = old_total / total
        for old_term in docterm:
            docterm[old_term] = docterm[old_term] / ratio
        docterm[term] = term_occurrence / total


def create_matrix(docterm_list):
    unique_terms = set()
    for docterm in docterm_list:
        unique_terms.update(docterm.keys())
    unique_terms.remove("i")
    unique_terms.remove("t")
    frozen_terms, matrix = make_matrix(docterm_list, unique_terms)
    print(frozen_terms, len(frozen_terms))
    print(matrix, matrix.shape)
    return frozen_terms, matrix

def save_docterm_vector(docterm: dict, path: str):
    """
    Saves a single document with indexing.
    :param docterm: Dictionary of terms and occurences
    :param path: save location
    """
    filename = path + str(docterm['i'])
    f = open(filename, 'w')
    f.write(docterm)


def make_idfmatrix(f_matrix):
    """
    Creates inverse document frequency of terms matrix.
    :param f_matrix: np.array(shape(n_terms, m_docs)) frequency matrix
    :return: np.array(shape=(n_terms, 1))
    """
    n_docs = f_matrix.shape[1]
    term_present_mask = np.ma.make_mask(f_matrix, copy=True)
    # 1D array
    df_terms = term_present_mask.sum(axis=1)
    total_matrix = np.full(df_terms.shape, fill_value=n_docs)
    total_matrix = total_matrix / df_terms
    idf_terms = np.log(total_matrix)
    return idf_terms


def make_fmatrix(docterm_list, terms):
    """
    Creates a frequency of terms in documents.
    :param docterm_list: list of docterm vectors
    :param terms: language, set of terms, no duplicates
    :return: np.array(shape=(n_terms, m_docs)
    """
    m_terms = len(terms)
    n_docs = len(docterm_list)
    shape = (m_terms, n_docs)
    f_matrix = np.zeros(shape)
    for term_id in range(m_terms):
        for doc_id in range(n_docs):
            document = docterm_list[doc_id]
            term = terms[term_id]
            if term in document:
                # document['t'] is total number of words in document
                f_matrix[term_id, doc_id] = document[term] / document['t']
    max_f = np.zeros(shape=(m_terms, 1))
    for term_id in range(m_terms):
        max_f[term_id] = np.amax(f_matrix, axis=1)[term_id]
    return f_matrix, max_f


def make_matrix(docterm_list: list, unique_terms: set):
    """
    Creates a term-by-document matrix A. Rather sparse and inefficient computation.
    :param docterm_list: list of docterm vectors
    :param unique_terms: language, set of terms, no duplicates
    :return: ordered list of terms,
             np.array(m_terms, n_documents) with weights_ij of term_i in doc_j
    """
    n_docs = len(docterm_list)
    m_terms = len(unique_terms)
    # TODO: use frozen set everywhere?
    terms = sorted(unique_terms)
    # in rows are unique terms, in columns documents
    shapeA = (m_terms, n_docs)
    # m x n matrix, term-by-document
    A = np.zeros(shapeA, dtype=float)
    # m x n matrix, m x 1 matrix
    f_matrix, max_f = make_fmatrix(docterm_list, terms)
    # 1 x m matrix
    idf_matrix = make_idfmatrix(f_matrix)
    for doc_id in range(n_docs):
        document = docterm_list[doc_id]
        for term_id in range(m_terms):
            term = terms[term_id]
            if term in document:
                # TODO: save matrices for future use
                # TODO: remove for-loops
                # TODO: create class maybe?
                # TODO: solve zero-division
                f_ij = f_matrix[term_id][doc_id]
                tf_ij = 0
                if max_f[term_id] != 0:
                    tf_ij = f_ij / max_f[term_id]
                if tf_ij == 0:
                    print("SHOULD NOT BE ZERO!")
                idf_i = idf_matrix[term_id]
                A[term_id, doc_id] = tf_ij * idf_i
    return terms, A
