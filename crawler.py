import os
import shutil
import newspaper
from newspaper import Article
from preprocessing.language import is_eng


def crawl():
    #A new article from TOI
    filepath = 'articles/matej2/'
    url = "https://fashionmagazine.com/style"
    #For different language newspaper refer above table
    toi_articl = newspaper.build(url, memoize_articles=False, language="en") # en for English
    category = 'fashion4_'
    i = 0

    for article in toi_articl.articles:
        if i > 200:
            break
        article.download()
        article.parse()
        # print(filename)
        file = open(filepath + category + str(i)+".txt", "w")
        file.write("Title: "+article.title)
        file.write("\n\n")

        text = article.text
        print(len(text), article.title)
        text = text.replace("\n\n", " ")
        file.write("Text: "+text)
        file.close()
        i = i + 1



    # # Downloading the HTML for the article
    # url = 'https://www.nytimes.com'
    # article = Article(url)
    # article.download()
    # article.parse()
    # with open('fox13no.txt', 'w') as fileout:
    #    fileout.write(article.title+"\n")
    #    fileout.write(article.text)

def preprocess():
    articles_folder = 'matej2/'
    error_folder = 'matej2/error/'
    path = 'articles/' + articles_folder
    error_path = 'articles/' + error_folder
    for filename in os.listdir(path):
        if filename.endswith(".txt"):
            f = open(path + filename, 'r')
            article_text = f.read()
            f.close()
            if is_eng(article_text):
                continue
            else:
                shutil.move(path + filename, error_path + filename)
                print(filename, 'moved to', error_folder)


if __name__ == '__main__':
    preprocess()
    #crawl()
