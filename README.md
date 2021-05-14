# LSI Vector Model
### Latent semantic indexing model

Semestral project at Czech technical university in Prague.
Course **BI-VWM**, summer **2021**

## Introduction

In this project @sutymate and @makarada focused on creating a model, that finds
similar articles based on article content. This model is based on LSI model, 
also knows as latent semantic indexing model. The main idea is that articles are
indexed by frequency and importance of various words in the articles.


## Quick guide:
In order to be able to run our project you need to install dependecies found
in `requirements.txt`. You can install them with `pip` or `anaconda`.

1.  Install dependencies from `requirements.txt`
2.  Download your own set of articles or extract the recommended set of articles
(around 3000) from `articles/all_articles.zip`.
3.  Move all articles to `articles/`
4.  Run latent semantic indexing by executing `run.py`
5.  Launch the web server to view the results by executing `python3 app/manage.py runserver`
6.  Go to `localhost:8000` and find how the articles are similar to each other 
