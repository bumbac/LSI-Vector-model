import time
from run import create_index
import matplotlib.pylab as plt


def speed_test():
    # number of articles
    n_list = [i for i in range(20, 61, 10)]
    # approximation factor
    k_list = [i for i in range(5, 25, 5)]
    article_filepath = "/home/sutymate/School/VWM/LSI/articles/tmp4/"

    for n in n_list:
        durations = []
        for k in k_list:
            start = time.perf_counter_ns()
            create_index(article_filepath=article_filepath, max_articles=n, approx=k)
            t = time.perf_counter_ns() - start
            durations.append(t)
        plt.plot(k_list, durations)
        plt.title('Appr. on ' + str(n) + " articles")
        plt.show()



def k_test():
    # k, k+1 zvysuju rozpty
    pass


def similarity_test():
    pass


if __name__ == '__main__':
    speed_test()
    k_test()
    similarity_test()
