import os


def make_tmatrix(clean_document, save_path=None):
    """
    Create occurrence matrix of terms in @clean_document.
    :param clean_document: list[] of tokens, stemmatized, w/o stop words
    :param save_path: save location
    :return: dict{term: occurrence in [0, 1]}
    """
    # unique terms
    terms = set(clean_document)
    tmatrix = {}
    total = len(clean_document)
    for term in terms:
        term_occurence = 0
        for token in clean_document:
            if token == term:
                term_occurence += 1
        tmatrix[term] = term_occurence / total
    if save_path:
        save_tmatrix(tmatrix, save_path)
    return tmatrix


def save_tmatrix(tmatrix, path):
    f = open(path, 'w')
    f.write(tmatrix)
