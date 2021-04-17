import newspaper
from newspaper import Article

#A new article from TOI
url = 'https://edition.cnn.com'
#For different language newspaper refer above table
toi_articl = newspaper.build(url, memoize_articles=False, language="en") # en for English

i = 0
for article in toi_articl.articles:
    article.download()
    article.parse()
    # print(filename)
    file = open("article"+str(i)+".txt", "w")
    file.write("Title: "+article.title)
    file.write("\n\n")

    text = article.text
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
