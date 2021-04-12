import os
from hashlib import sha256
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, LancasterStemmer, SnowballStemmer
from vector.vector import make_docterm_vector


def create_space(path, max_articles=5):
    """
    Parse documents(tokenize, stemmatize, remove stops) and create docterm vectors/
    :param path: location of documents
    :param max_articles: number of articles to process
    :return: list of docterm vectors
    """
    files = os.listdir(path)
    save_dir = 'matrices'
    cnt = 0
    docterm_list = []
    unique_doc_ids = []
    # preprocess
    found_articles = []
    print("TOKENIZE AND STEMMATIZE AND CLEAN WORDS in progress")
    for f in files:
        if os.path.isdir(path + f):
            continue
        else:
            found_articles.append(f)
        if cnt > max_articles:
            break
        cnt += 1
        document_file = open(path + f)
        document = document_file.read()
        doc_id = sha256(bytearray(document, encoding='utf8')).hexdigest()
        if doc_id in unique_doc_ids:
            print("same hash as other article", doc_id, path, f)
        else:
            unique_doc_ids.append(doc_id)
        tokens = tokenize(document)
        clean_tokens = remove_stops(tokens)
        clean_words = stemmatize(clean_tokens)
        save_path = None  # save_dir + 'm_' + f
        # creates vector of terms with relative weight to this document
        docterm = make_docterm_vector(clean_words, save_path, doc_id=str(doc_id), article_filename=f)
        docterm_list.append(docterm)
        print(".", end='')
    print("\n\n\nFound these articles:", *found_articles, sep=', ')
    return docterm_list


def tokenize(document):
    """
    Create a list of tokens (english words from @document). Tokens are in original form,
    there are stop words, units, names, typos, etc.
    :param document: str
    :return: list[] of tokens
    """
    txt_title_start = document.find('Text: ')
    txt_body_start = txt_title_start + len('Text: ')
    document = document[txt_body_start:]
    tokens = word_tokenize(document, 'english')
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
