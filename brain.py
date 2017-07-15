import numpy as np
import matplotlib.pyplot as plt
import time
from matplotlib import style
from matplotlib.colors import ListedColormap
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons
from sklearn.neighbors import KNeighborsClassifier

style.use('ggplot')


class Brain:

	def __init__(self):
		self.k = 20
		self.clf = KNeighborsClassifier(self.k)
		self.X = np.array([])
		self.y = np.array([])

		print("Brain inititiated")

	def addData(self, X_new, y_new):
		# turn into list
		self.X = self.X.tolist()
		self.y = self.y.tolist()

		# add new data
		for X_entry in X_new:
			self.X.append([X_entry[0], X_entry[1]])

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
		xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

		# plot setup
		plt.figure(figsize=(6,6))
		cm_list = ["#FFAAAA", "#FFCCCC", "#CCFFCC", "#AAFFAA"]
		cm = ListedColormap(cm_list)
		cm_bold = ListedColormap(["#FF0000", "#00FF00"])
		ax = plt.subplot(1, 1, 1)

		# get predictions
		self.Z = self.clf.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1]
		self.Z = self.Z.reshape(xx.shape)

		# plot Z as contour
		ax.contourf(xx, yy, self.Z, cmap=cm, alpha=1)

		# plot X as scatter
		ax.scatter(self.X[:, 0], self.X[:, 1], c=self.y, cmap=cm_bold, marker="x")
		ax.set_xlim(xx.min(), xx.max())
		ax.set_ylim(yy.min(), yy.max())
		ax.set_xticks(())
		ax.set_yticks(())
		ax.text(xx.max() - 0.1, yy.min() + 0.1, "k={}".format(self.k), size=24, horizontalalignment='right')

		end_time = time.time() - start_time
		print("Prepared visualization in {}s".format(round(end_time,5)))		

		plt.savefig("media/brain-visualization-example-k={}.png".format(self.k), bbox_inches="tight")

		# show graph
		plt.show()


brain = Brain()

X_new, y_new = make_moons(n_samples=100, noise=0.5, random_state=2)
brain.addData(X_new, y_new)

brain.learn()
brain.visualize()