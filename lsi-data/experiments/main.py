import os
import time
import pandas as pd
import pickle
from run import create_index
import matplotlib.pylab as plt
from app.lsi import models as lsi


def speed_test():
    # number of articles
    n_list = [200]
    # approximation factor
    k_list = [10, 20, 30, 40, 50]
    print(n_list, k_list)
    article_filepath = "../articles/tmp4/"

    for n in n_list:
        durations = []
        for k in k_list:
            print(n, k)
            start = time.monotonic()
            create_index(article_filepath=article_filepath, max_articles=n, approx=k)
            t = time.monotonic() - start
            print("Duration:", t)
            durations.append(t)
        print(durations)
        plt.plot(k_list, durations)
        plt.xlabel("Value k")
        plt.ylabel("Time in seconds")
        plt.title('Appr. on ' + str(n) + " articles")
        plt.show()


def k_test():
    """
       View which displays selected article with similarity of other articles.
       :param request: django request
       :param article_id: selected article id
       :return: article: object that contains title and content.
       """
    files = os.listdir('../articles/tmp4')
    for i in range(3):
        article_filename = files[i]

        matrix_path = '../'
        matrix_f = open(matrix_path + 'file.dat', 'rb')
        matrix_data = matrix_f.read()
        matrices_dict = pickle.loads(matrix_data)
        k_articles = 3 + 1
        similarity_top5 = [[] for i in range(k_articles)]
        order_articles = [[] for i in range(k_articles)]
        max_approx = 490
        tested_values = []
        for i in range(1, 30, 5):
            tested_values.append(i)
        for i in range(30, max_approx, 10):
            tested_values.append(i)
        for approx in tested_values:
            doc_filenames = matrices_dict['doc_filenames']
            article_tuple = lsi.find_file(doc_filenames, article_filename)
            top = lsi.func(matrices_dict, article_tuple, approx)
            cnt = 0
            for doc_sim_tuple in top[:k_articles]:
                similar_document_id = doc_sim_tuple[0]
                similar_document_name = str(matrices_dict['doc_filenames'][similar_document_id]).replace('.txt', '')
                similarity_ranking = doc_sim_tuple[1]
                similarity_top5[cnt].append(similarity_ranking)
                order_articles[cnt].append(similar_document_name)
                cnt += 1
        article_filename = article_filename.replace('.txt', '')
        for i in range(1, k_articles):
            ax = pd.Series(order_articles[i]).value_counts().head(5).plot(kind='bar', title=str(i) + '. most similar '
                                                                                               'articles '
                                                                                            'to '
                                                                               + article_filename)
            plt.xticks(rotation=0)
            fig = ax.get_figure()
            fig.savefig('out/4/hist_' + article_filename + str(i) + '.png')
            fig.show()

        for i in range(1, k_articles):
            plt.plot(tested_values, similarity_top5[i], label=str(i) + '. most similar')
            plt.title("Articles with best match to " + article_filename)
            plt.ylabel('Similarity')
            plt.xlabel('Approximation k')
            plt.legend()


        plt.savefig('out/4/k_' + article_filename + '.png')
        plt.show()


def similarity_test():
    pass


if __name__ == '__main__':
    # speed_test()
    k_test()
    # similarity_test()