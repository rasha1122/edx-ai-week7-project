import sys
import numpy as np
import matplotlib.pyplot as plt


def open_input(input_file):
    fo = open(input_file, "r")
    return fo


def open_output(output_file):
    fo = open(output_file, "w")
    return fo


class Perceptron:
    def __init__(self, outputter, num_features=2, alpha=0.1):
        self.alpha = alpha
        self.outputter = outputter
        self.weights = np.zeros(num_features + 1)

    def predict_all(self, data: np.array, labels: np.array):
        right, wrong = 0, 0
        for row, expected in zip(data, labels):
            actual = self.predict(row)
            if actual != expected:
                wrong += 1
            else:
                right += 1
        return right, wrong

    def predict(self, data: np.array):
        dot = np.dot(data, self.weights)
        if dot > 0:
            return 1
        else:
            return 0

    def run(self, training_set: np.array, d: np.array, labels: np.array):
        w = self.weights
        for (x, y) in zip(training_set, d):
            tmp = self.predict(x)
            f = labels[tmp]
            adjustment = self.alpha * (y - f)
            for i, w_i in enumerate(w):  # for each weight, j
                w[i] += adjustment * x[i]
        self.outputter.process(self, training_set, d, labels)

    def score(self, data, labels):
        r, w = self.predict_all(data, labels)
        return (r/(r+w)) * 100


class Outputter:
    def process(self, p: Perceptron, data: np.array, expected_labels: np.array, labels: np.array):
        pass


class CompositeOutputter(Outputter):
    def __init__(self, outputters):
        super().__init__()
        self.outputters = outputters

    def process(self, p: Perceptron, data: np.array, expected_labels: np.array, labels: np.array):
        for outputter in self.outputters:
            outputter.process(p, data, labels)


class ConsoleOutputter(Outputter):
    def process(self, p: Perceptron, data: np.array, expected_labels: np.array, labels: np.array):
        print(p.weights)
        # print("Prediction " + str(p.predict(data)))
        # print("Actual     " + str(labels))
        # print("Accuracy   " + str(p.score(data, labels) * 100) + "%")

    def __init__(self):
        super().__init__()


class FileOutputter(Outputter):
    def process(self, p: Perceptron, data: np.array, expected_labels: np.array, labels: np.array):
        pass

    def __init__(self, file_path):
        super().__init__()
        self.fo = open_output(file_path)


class GraphOutputter(Outputter):
    def __init__(self):
        super().__init__()

    def process(self, p: Perceptron, data: np.array, expected_labels: np.array, labels: np.array):
        colormap = np.array(['r', 'k'])
        ixs = [0 if x == 1 else 1 for x in expected_labels]
        xs = data[:, [1]]
        ys = data[:, [2]]
        plt.scatter(xs.flatten(), ys.flatten(), c=colormap[ixs], s=40)

        xmin, xmax = min(xs), max(xs)
        w = p.weights
        x = np.arange(xmin, xmax)
        y = w[0] + w[1] / w[2] * x
        p = plt.plot(x, y, 'k-')

        # ymin, ymax = min(ys), max(ys)
        # xx = np.linspace(ymin, ymax)
        # a = -w[1] / w[2]
        # yy = a * xx - (w[0]) / w[2]
        # yy
        # plt.plot(yy, xx, 'k-')
        plt.show()


def main():
    p = Perceptron(ConsoleOutputter())
    raw_data = np.loadtxt(sys.argv[1], delimiter=',')
    data = raw_data[:, [0, 1]]
    rows = raw_data.shape[0]
    bias_column = np.ones(rows)
    bias_column.shape = (rows, 1)
    data = np.hstack((bias_column, data))
    labels = raw_data[:, [2]].flatten()
    r = w = None
    while w != 0:
        p.run(data, labels.T, list(set(labels)))
        r,w = p.predict_all(data, labels.T)
        print("(right=%d, wrong=%d)" % (r,w))
    return 0


if __name__ == "__main__":
    main()

# # RESOURCES
# - https://www.tutorialspoint.com/python/python_files_io.htm (file handling)
# - https://en.wikipedia.org/wiki/Perceptron (WP article on perceptron)
# - http://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Perceptron.html#sklearn.linear_model.Perceptron (basic perceptron learning algorithm)
# - https://docs.scipy.org/doc/numpy/reference/generated/numpy.genfromtxt.html (loading text from csv into numpy array)
