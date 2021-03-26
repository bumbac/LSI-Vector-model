from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, LancasterStemmer, SnowballStemmer


def tokenize(document):
    txt_title_start = document.find('Text: ')
    txt_body_start = txt_title_start + len('Text: ')
    document = document[txt_body_start:]
    tokens = word_tokenize(document, 'english')
    return tokens


def remove_stops(tokens):
    stops = set(stopwords.words("english"))
    clean_tokens = []
    for word in tokens:
        if word not in stops:
            if len(word) > 2:
                clean_tokens.append(word)
    return clean_tokens


def stemmatize(tokens):
    stemmer_techs = [PorterStemmer(), LancasterStemmer(), SnowballStemmer('english')]
    for stemmer in stemmer_techs:
        clean_words = []
        for word in tokens:
            clean_words.append(stemmer.stem(word))
            # word.count()
        return clean_words
