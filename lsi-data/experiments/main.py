import os
import time
import pandas as pd
import pickle
import matplotlib.pylab as plt
from lsi import models as lsi


def speed_test():
    # approximation factor
    k_list = [ 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25]
    files = os.listdir('../articles/tmp1/')
    with open('../file.dat', 'rb') as handle:
        data = handle.read()
    matrices_dict = pickle.loads(data)
    doc_filenames = matrices_dict['doc_filenames']
    files_axis = []
    files_sim_axis = []
    for doc_id in range(5):
        files_sim_axis.append([])
        f = doc_filenames[doc_id]
        doc_tuple = (doc_id, f)
        files_axis.append(f)
        files_time_axis = []
        for k in k_list:
            top, time_duration = lsi.func(matrices_dict, doc_tuple, k)
            files_time_axis.append(time_duration)
            files_sim_axis[doc_id].append(top[1][1])
        plt.plot(k_list, files_time_axis, label=f)
        plt.title("Time of sequential and indexed search")
        plt.xlabel('k approximation, 0 is sequential')
        plt.ylabel('Search time in nanoseconds')
        plt.legend()
    plt.savefig('time_search1plus.png')
    plt.show()
    for f in range(len(files_axis)):
        plt.plot(k_list, files_sim_axis[f], label=files_axis[f])
        plt.title("Similarity of top match article with different k")
        plt.ylabel("Similarity of top article")
        plt.xlabel("k approximation, 0 is sequential")
        plt.legend()
    plt.savefig("similarity1-all.png")
    plt.show()



def k_test():
    """
       Runs experiment on concept space. Selects random files from directory and for various k plots the similiarty
       of three most similar articles. For various k, plots histogram of most frequent articles on position 1, 2, 3.
       """
    # select directory with analyzed articles. Chooses one randomly, all need to be processed by LSI before
    files = os.listdir('../articles/tmp1')
    # set how many files you want to analyze, 1-3 recommended
    for i in range(3):
        article_filename = files[i]

        matrix_path = '../'
        matrix_f = open(matrix_path + 'file.dat', 'rb')
        matrix_data = matrix_f.read()
        matrices_dict = pickle.loads(matrix_data)
        # how many articles in top positions should be analyzed
        k_articles = 3 + 1
        similarity_top5 = [[] for i in range(k_articles)]
        order_articles = [[] for i in range(k_articles)]
        # set range for approximation.
        max_approx = 50
        tested_values = []
        # see stepping for faster calculations
        for i in range(1, 30, 5):
            tested_values.append(i)
        for i in range(30, max_approx, 10):
            tested_values.append(i)
        for approx in tested_values:
            doc_filenames = matrices_dict['doc_filenames']
            article_tuple = lsi.find_file(doc_filenames, article_filename)
            top, duration = lsi.func(matrices_dict, article_tuple, approx)
            cnt = 0
            # analyzes 0 to k_articles
            for doc_sim_tuple in top[:k_articles]:
                similar_document_id = doc_sim_tuple[0]
                similar_document_name = str(matrices_dict['doc_filenames'][similar_document_id]).replace('.txt', '')
                similarity_ranking = doc_sim_tuple[1]
                similarity_top5[cnt].append(similarity_ranking)
                order_articles[cnt].append(similar_document_name)
                cnt += 1
        article_filename = article_filename.replace('.txt', '')
        # histogram with frequencies of articles in top positons
        for i in range(1, k_articles):
            ax = pd.Series(order_articles[i]).value_counts().head(5).plot(kind='bar', title=str(i) + '. most similar '
                                                                                               'articles '
                                                                                            'to '
                                                                               + article_filename)
            plt.xticks(rotation=0)
            fig = ax.get_figure()
            fig.savefig('out/5/hist_' + article_filename + str(i) + '.png')
            fig.show()
        # similarities in top positions
        for i in range(1, k_articles):
            plt.plot(tested_values, similarity_top5[i], label=str(i) + '. most similar')
            plt.title("Articles with best match to " + article_filename)
            plt.ylabel('Similarity')
            plt.xlabel('Approximation k')
            plt.legend()


        plt.savefig('out/5/k_' + article_filename + '.png')
        plt.show()


if __name__ == '__main__':
    # speed_test()
    k_test()
