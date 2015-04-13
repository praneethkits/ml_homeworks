from sklearn.linear_model import Perceptron
from sklearn.datasets import load_svmlight_file
import sys
import argparse

parser = argparse.ArgumentParser(prog='perceptron.py')
parser.add_argument('-tr', nargs=1, required=True,
                    help="training set path.")
parser.add_argument('-te',  nargs=1, required=True,
                    help="test set path.")
parser.add_argument('-a', nargs=1, type=float, required=True,
                    help="alpha")
parser.add_argument('-n', nargs=1, type=int, required=True,
                    help="Initial weights.")
parser.add_argument('-e', nargs=1, type=float, required=True,
                    help="eeta.")
args = parser.parse_args()


X_train, y_train = load_svmlight_file(args.tr[0])
X_test, y_test = load_svmlight_file(args.te[0])
pr = Perceptron(alpha=args.a[0], n_iter=args.n[0], eta0=args.e[0])
pr.fit(X_train, y_train)
y_test_prediction = pr.predict(X_test)
n = len(y_test_prediction)
i = 0
nc = 0
nw = 0
while i < n:
    if y_test_prediction[i] == y_test[i]:
        nc += 1
    else:
        nw += 1

    i += 1

accuracy = (nc * 100.0)/(nw + nc)
print accuracy
