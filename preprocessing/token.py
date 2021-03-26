from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, LancasterStemmer, SnowballStemmer


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
            if len(word) > 2:
                clean_tokens.append(word)
    return clean_tokens


def stemmatize(tokens):
    """
    Shorten words from @tokens to basic word form in english.
    :param tokens:
    :return: list[] of tokens
    """
    stemmer_techs = [PorterStemmer(), LancasterStemmer(), SnowballStemmer('english')]
    for stemmer in stemmer_techs:
        clean_words = []
        for word in tokens:
            clean_words.append(stemmer.stem(word))
            # word.count()
        return clean_words
