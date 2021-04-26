import newspaper
from newspaper import Article




#A new article from TOI
filepath = 'app/app/matej/2/'
page_name = "garden"
i = 0
i_max = 200
preventive = 9999999999999999999999999999999999
for page_n in range(2, 20):
# for page_n in range(0, 1):
    url = "https://veggiegardeningtips.com/all-articles/page/" + str(page_n)
    toi_articl = newspaper.build(url, memoize_articles=False, language="en")  # en for English
    k = 0
    for article in toi_articl.articles:
        k += 1
        article.download()
        article.parse()
        # print(filename)
        file = open(filepath + page_name + str(i)+".txt", "w")
        file.write("Title: "+article.title)
        file.write("\n\n")

        text = article.text
        text = text.replace("\n\n", " ")
        file.write("Text: "+text)
        file.close()
        i = i + 1
        print(i, '/', len(toi_articl.articles), article.title)
        if k > preventive or i > i_max:
            break



# # Downloading the HTML for the article
# url = 'https://www.nytimes.com'
# article = Article(url)
# article.download()
# article.parse()
# with open('fox13no.txt', 'w') as fileout:
#    fileout.write(article.title+"\n")
#    fileout.write(article.text)
