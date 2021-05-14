import os
from hashlib import sha256
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from vector.vector import make_docterm_vector


def create_space(path, max_articles=10):
    """
    Parse documents(tokenize, stemmatize, remove stops) and create docterm vectors
    :param path: location of documents
    :param max_articles: number of articles to process
    :return: list of docterm vectors
    """
    files = os.listdir(path)
    print("Number of files: ", len(files))
    # order of documents is important for matrix (m x n_docs), does not change
    doc_id = 0
    docterm_list = []
    unique_doc_hashes = []
    # preprocess
    found_articles = []
    print("TOKENIZE AND STEMMATIZE AND CLEAN WORDS in progress")
    for f in files:
        print(doc_id, f)
        if os.path.isdir(path + f):
            continue
        else:
            found_articles.append(f)
        if doc_id == max_articles+1:
            break
        if f != ".DS_Store" and not os.path.isdir(path + f):
            document_file = open(path + f)
            raw_document = document_file.read()
            # hash used for checking duplicate documents
            doc_hash = sha256(bytearray(raw_document, encoding='utf8')).hexdigest()
            if doc_hash in unique_doc_hashes:
                doc_hash = sha256(bytearray(doc_hash, encoding='utf8')).hexdigest()
                print("same hash as other document", doc_hash, path, f)
            unique_doc_hashes.append(doc_hash)
            tokens = tokenize(raw_document)
            clean_tokens = remove_stops(tokens)
            clean_words = stemmatize(clean_tokens)
            save_path = None  # save_dir + 'm_' + f
            # creates vector of terms with relative weight to this document
            docterm = make_docterm_vector(clean_words, save_path,
                                          doc_hash=str(doc_hash), doc_filename=f,
                                          doc_id=doc_id)
            docterm_list.append(docterm)
            doc_id += 1

    print("Found these articles:", *found_articles, sep=', ')
    return docterm_list


def tokenize(raw_document):
    """
    Create a list of tokens (english words from @document). Tokens are in original form,
    there are stop words, units, names, typos, etc.
    :param raw_document: str
    :return: list[] of tokens
    """
    txt_title_start = raw_document.find('Text: ')
    txt_body_start = txt_title_start + len('Text: ')
    raw_document = raw_document[txt_body_start:]
    tokens = word_tokenize(raw_document, 'english')
    return tokens


def remove_stops(tokens, length_threshold=2):
    """
    Remove stop words and words shorter than 2 from @tokens. Maybe remove units, names, typos, etc.?
    :param tokens: list of tokens, whole document
    :param length_threshold: words with len(word) > @length_threshold are kept
    :return: list[] of tokens, document without stop words
    """
    stops = set(stopwords.words("english"))
    clean_tokens = []
    for word in tokens:
        if word not in stops:
            if len(word) > length_threshold:
                clean_tokens.append(word)
    return clean_tokens


def stemmatize(tokens):
    """
    Shorten words from @tokens to basic word form in english.
    :param tokens:
    :return: list[] of tokens
    """
    # stemmer_techs = [PorterStemmer(), LancasterStemmer(), SnowballStemmer('english')]
    stemmer = PorterStemmer()
    clean_words = []
    for word in tokens:
        clean_words.append(stemmer.stem(word))
        # word.count()
    return clean_words
