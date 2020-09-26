import matplotlib.pyplot as plt


RESULTS_FILE_A = r'time_diff.csv'
RESULTS_FILE_B = r'time_diff_b.csv'


def get_results(filename):
    xs, ys = [], []
    with open(filename, 'r') as f:
        for line in f.readlines():
            line = line.rstrip('\n')
            if line:
                x, y = line.split(',')
                xs.append(int(x))
                ys.append(int(y.rstrip('\n')))
    return xs, ys


def plot_results_a(xs, ys):
    plt.xlabel('Run #')
    plt.ylabel('Time difference in ns')
    plt.title('Time differences Exercise 8a')
    plt.scatter(xs, ys, s=10)
    plt.show()


def plot_results_b(xs, ys):
    plt.xlabel('Run #')
    plt.ylabel('Time difference in ns')
    plt.title('Time differences Exercise 8b')
    plt.scatter(xs, ys, s=10)
    plt.show()


if __name__ == '__main__':
    res_a = get_results(RESULTS_FILE_A)
    res_b = get_results(RESULTS_FILE_B)
    plot_results_a(*res_a)
    plot_results_b(*res_b)
