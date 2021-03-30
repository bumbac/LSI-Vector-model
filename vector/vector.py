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


def save_docterm_vector(docterm: dict, path: str):
    """
    Saves a single document with indexing.
    :param docterm: Dictionary of terms and occurences
    :param path: save location
    """
    filename = path + str(docterm['i'])
    f = open(filename, 'w')
    f.write(docterm)


def make_matrix(docterm_list: list, unique_terms: set):
    """
    Creates a term-by-document matrix A. Rather sparse
    :param docterm_list: list of docterm vectors
    :param unique_terms: language, set of terms, no duplicates
    :return: frozen set of terms,
             np.array(m_terms, n_documents) with weights_ij of term_i in doc_j
    """
    n_docs = len(docterm_list)
    m_terms = len(unique_terms)
    terms = sorted(unique_terms)
    # in rows are documents, in columns unique terms
    shapeA = (m_terms, n_docs)
    A = np.zeros(shapeA, dtype=float)
    for doc_id in range(n_docs):
        document = docterm_list[doc_id]
        for term_id in range(m_terms):
            term = terms[term_id]
            if terms[term_id] in document:
                A[term_id, doc_id] = document[term]
    return frozenset(terms), A


def size_of_space(tmatrix_list):
    sum_of_totals = 0
    for tmatrix in tmatrix_list:
        sum_of_totals += tmatrix['t']
    return sum_of_totals
