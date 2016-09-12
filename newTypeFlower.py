import numpy as np
from sklearn.datasets import load_iris
from sklearn import tree
#visualize classifier
from sklearn.externals.six import StringIO
import pydot

iris = load_iris()
train_idx = 100

for i in range(train_idx, len(iris.data)):
	train_target = iris.target[0:i]
	train_data = iris.data[0:i]

	test_target = iris.target[i:]
	test_data = iris.data[i:]

	clf = tree.DecisionTreeClassifier()
	clf.fit(train_data, train_target)

	#print test_target
	#print clf.predict(test_data)
	dot_data = StringIO()
	tree.export_graphviz(clf,
							out_file=dot_data,
							feature_names=iris.feature_names,
							class_names=iris.target_names,
							filled=True, rounded=True,
							impurity=False)
	fname = "iris"+str(i)+".pdf";
	graph = pydot.graph_from_dot_data(dot_data.getvalue())
	graph.write_pdf(fname)