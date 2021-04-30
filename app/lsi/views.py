import pickle
import textwrap
import glob

from django.conf import settings
from django.core.paginator import Paginator
from django.shortcuts import render, redirect

from .models import *


def index(request):
    """
    Default view, when loaded, redirects to home view.
    :param request: django request
    """
    return redirect('home')


def home(request):
    """
    View which displays all articles on the website.
    :param request: django request
    :return: page_obj: array with articles as objects.
    """

    # Load all articles from folder
    files = glob.glob(settings.ARTICLE_URL + "*")
    # Array for articles
    articles = []

    # For every file creates article object which contains title and content
    for f in files:
        file = open(f, 'r')
        file_content = file.read()
        split_content = file_content.splitlines()
        file.close()

        # Extracts article id from its name
        path = f.rsplit('/', 1)[-1]
        article_id = get_article_id(path)

        # Extracts article title from array and removes unnecessary string
        title = split_content[0].replace("Title:", "")

        # Extracts, processes article content and removes unnecessary strings
        content_pos = len(split_content) - 1
        content = split_content[content_pos]
        content = content.replace("Text: ", "")
        content = content.replace("(CNN)", "")

        # Trims content for shore content preview
        content = textwrap.shorten(content, width=100, placeholder="...")
        # Creates article and adds it to the array
        article = Article(article_id, title, content, None)
        articles.append(article)

    # Paginator for showing 9 articles per page
    paginator = Paginator(articles, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'html/index.html', {'page_obj': page_obj})


def article(request, article_id):
    """
    View which displays selected article with similarity of other articles.
    :param request: django request
    :param article_id: selected article id
    :return: article: object that contains title and content.
    """
    # Finds article with id
    file = glob.glob(settings.ARTICLE_URL + str(article_id) + ".txt")

    # Reads content from file
    open_file = open(file[0], 'r')
    obj = open_file.read()
    obj_content = obj.splitlines()
    open_file.close()

    # Extracts title and content and removes unnecessary strings
    title = obj_content[0].replace("Title: ", "")
    content = obj_content[2].replace("Text: ", "")
    content = content.replace("(CNN) ", "")

    # Creates article object
    article = Article(article_id, title, content, None)

    filename = file[0].rsplit('/', 1)[-1]
    with open(settings.BASE_URL + 'file.dat', 'rb') as handle:
        data = handle.read()

    matrices_dict = pickle.loads(data)

    doc_filenames = matrices_dict['doc_filenames']
    docterm_list = matrices_dict['docterm_list']
    article_tuple = find_file(doc_filenames, filename)
    top = func(matrices_dict, article_tuple)

    sim_articles = []

    for doc_sim_tuple in top:
        doc_number = doc_sim_tuple[0]
        similarity_ranking = doc_sim_tuple[1]
        document = docterm_list[doc_number]
        article_id = get_article_id(document['n'])

        file = glob.glob(settings.ARTICLE_URL + article_id + ".txt")

        # Reads content from file
        open_file = open(file[0], 'r')
        obj = open_file.read()
        open_file.close()
        title = obj.splitlines()[0].replace("Title:", "")
        title = textwrap.shorten(title, width=75, placeholder="...")

        sim_articles.append(Article(article_id, title, None, similarity_ranking))

    return render(request, 'html/article.html', {'page_obj': article, 'sim_articles' : sim_articles})
