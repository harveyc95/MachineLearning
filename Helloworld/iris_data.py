import numpy as np
from sklearn.datasets import load_iris
from sklearn import tree

iris = load_iris()
print iris.feature_names
print iris.target_names

test_idx = [0, 50, 100]

# training data
train_data = np.delete(iris.data, test_idx, axis=0)
train_target = np.delete(iris.target, test_idx)

# testing data
testing_data = iris.data[test_idx]
testing_target = iris.target[test_idx]


clf = tree.DecisionTreeClassifier()
clf = clf.fit(train_data, train_target)

print testing_target
print clf.predict(testing_data)
