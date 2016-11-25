import numpy as np
from sklearn.datasets import load_iris
from sklearn import tree
from random import rantint
#visualize classifier
from sklearn.externals.six import StringIO
import pydot

from sklearn.cross_validation import train_test_split

iris = load_iris()
u = randint(1,3)
X1 = iris.data[0:50]
y1 = iris.target[0:50]
X2 = iris.data[50:100]
y2 = iris.target[50:100]
X3 = iris.data[100:]
y3 = iris.target[100:]

for i in range(10):
	t = (1 - ( ((i+1)*0.1)-0.05 ))
	
	X1_train, X2_test, y2_train, y2_test = train_test_split(X2, y2, test_size = t )
	X3_train, X3_test, y3_train, y3_test = train_test_split(X3, y3, test_size = t )
	
	clf = tree.DecisionTreeClassifier()
	
	if u == 1 
		X1_train, X1_test, y1_train, y1_test = train_test_split(X1, y1, test_size = t )
		X_train = X1_train + X2 + X3
		y_train = y1_train + y2 + y3
		X_test = X1_test
	else if == 2
		X_train = X1_train + X3_train
		X_test = X1_test + X3_test
		y_train = y1_train + y3_train
		y_test = y1_test + y3_test
	else
		X_train = X1_train + X2_train
		X_test = X1_test + X2_test
		y_train = y1_train + y2_train
		y_test = y1_test + y2_test


	
	clf.fit(X_train, y_train)
	predictions = clf.predict(X_test)

	from sklearn.metrics import accuracy_score
	print accuracy_score(y_test, predictions)

	if ( (i%5) == 0 ):
		#print test_target
		#print clf.predict(test_data)
		dot_data = StringIO()
		tree.export_graphviz(clf,
								out_file=dot_data,
								feature_names=iris.feature_names,
								class_names=iris.target_names,
								filled=True, rounded=True,
								impurity=False)
		fname = "iris"+str(i)+".pdf"
		graph = pydot.graph_from_dot_data(dot_data.getvalue())
		graph.write_pdf(fname)