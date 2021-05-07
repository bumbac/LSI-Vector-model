from langdetect import detect


def is_eng(article):
    return detect(article) == 'en'