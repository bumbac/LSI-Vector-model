import time
from run import create_index
import matplotlib.pylab as plt


def speed_test():
    # number of articles
    n_list = [200]
    # approximation factor
    k_list = [10, 20, 30, 40, 50]
    print(n_list, k_list)
    article_filepath = "../articles/tmp/"

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
    # k, k+1 zvysuju rozpty
    pass


def similarity_test():
    pass


if __name__ == '__main__':
    speed_test()
    k_test()
    similarity_test()
