import os

def make_tmatrix(clean_document):
    terms = set(clean_document)
    tmatrix = {}
    total = len(clean_document)
    for term in terms:
        term_occurence = 0
        for token in clean_document:
            if token == term:
                term_occurence += 1
        tmatrix[term] = term_occurence / total
    return tmatrix
