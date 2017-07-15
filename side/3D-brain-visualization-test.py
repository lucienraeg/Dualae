import numpy as np
import matplotlib.pyplot as plt
import time
from matplotlib import style
from matplotlib.colors import ListedColormap
from matplotlib import cm
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_classification
from sklearn.neighbors import KNeighborsClassifier

style.use('ggplot')


class Brain:

	def __init__(self):
		k = 20
		self.clf = KNeighborsClassifier(k)
		self.X = np.array([])
		self.y = np.array([])

		print("Brain inititiated")

	def addData(self, X_new, y_new):
		# turn into list
		self.X = self.X.tolist()
		self.y = self.y.tolist()

		# add new data
		for X_entry in X_new:
			print(X_entry)
			self.X.append([X_entry[0], X_entry[1], X_entry[2]])

		for y_entry in y_new:
			self.y.append(y_entry)

		# turn into numpy array
		self.X = np.array(self.X)
		self.y = np.array(self.y)

		print("Added data [{} entries]".format(len(X_new), len(y_new)))

	def check(self):
		print("X: shape={}".format(np.shape(self.X)))
		print("y: shape={}".format(np.shape(self.y)))

	def learn(self):
		start_time = time.time()

		self.clf.fit(self.X, self.y)

		end_time = time.time() - start_time

		print("Fitted in {}s".format(round(end_time,5)))

	def visualize(self):
		# step size in the mesh
		h = 0.02

		start_time = time.time()

		x_min, x_max = self.X[:, 0].min() - 0.2, self.X[:, 0].max() + 0.2
		y_min, y_max = self.X[:, 1].min() - 0.2, self.X[:, 1].max() + 0.2
		z_min, z_max = self.X[:, 2].min() - 0.2, self.X[:, 2].max() + 0.2
		xx, yy, zz = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h), np.arange(z_min, z_max, h))

		# plot setup
		plt.figure(figsize=(6,6))
		cm = ListedColormap(["#FFAAAA", "#FFCCCC", "#CCFFCC", "#AAFFAA"])
		cm_bold = ListedColormap(["#FF0000", "#00FF00"])
		ax = plt.subplot(1, 1, 1, projection="3d")

		# get predictions
		self.V = self.clf.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]
		self.V = self.V.reshape(xx.shape)

		print(self.V)

		# plot Z as 3d contour
		ax.plot_surface(self.V)

		# plot X as scatter
		ax.scatter(self.X[:, 0], self.X[:, 1], c=self.y, cmap=cm_bold, marker="x")
		ax.set_xlim(xx.min(), xx.max())
		ax.set_ylim(yy.min(), yy.max())
		ax.set_xticks(())
		ax.set_yticks(())

		end_time = time.time() - start_time
		print("Prepared visualization in {}s".format(round(end_time,5)))

		# show graph
		plt.show()


brain = Brain()

X_new, y_new = make_classification(n_features=3, n_redundant=0, n_informative=3, random_state=1, n_clusters_per_class=1)
brain.addData(X_new, y_new)

brain.learn()
brain.visualize()