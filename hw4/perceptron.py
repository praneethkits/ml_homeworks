from sklearn.linear_model import Perceptron
from sklearn.datasets import load_svmlight_file

X_train, y_train = load_svmlight_file("./promoters_dataset/training.new")
X_test, y_test = load_svmlight_file( "./promoters_dataset/validation.new")
pr = Perceptron()
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
