from sklearn import tree

# features: [weight, bumpy/smooth(0/1)]
# labels: 0 = apple, 1 = orange
features = [[140, 1], [130, 1], [150, 0], [170, 0]]
labels = [0, 0, 1, 1]

clf = tree.DecisionTreeClassifier()
clf = clf.fit(features, labels)


# predict 160g and bumpy texture
print clf.predict([[160, 0]])