# clasificadores.py
#%%
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
#%%
iris_dataset = load_iris()
iris_dataframe = pd.DataFrame(iris_dataset['data'], columns=iris_dataset.feature_names)
iris_dataframe['target'] = iris_dataset['target']
#%%
#X_train, X_test, y_train, y_test = train_test_split(
#    iris_dataset['data'], iris_dataset['target'], random_state=0)
#knn = KNeighborsClassifier(n_neighbors=1)
#knn.fit(X_train, y_train)
#X_new = np.array([[5, 2.9, 1, 0.2]])
#plt.scatter(X_train[:, 1], X_train[:, 3], c=y_train)
#plt.scatter(X_new[:, 1], X_new[:, 3], c='red')
#plt.show()

#prediction = knn.predict(X_new)
#print("Prediccion:", prediction)
#print("Nombre de la especie predicha:",
#      iris_dataset['target_names'][prediction])

#y_pred = knn.predict(X_test)
#print("Predicciones para el conjunto de Test:\n", y_pred)
#print("Etiquetas originales de este conjunto:\n", y_test)
#print(y_pred == y_test)
#print("Test set score: {:.2f}".format(np.mean(y_pred == y_test)))
## metodo score que viene con el clasificador:
#print("Test set score: {:.2f}".format(knn.score(X_test, y_test)))
#%% Random trees
#X_train, X_test, y_train, y_test = train_test_split(
#    iris_dataset['data'], iris_dataset['target'])
#clf = DecisionTreeClassifier()
#clf.fit(X_train, y_train)
#y_pred = clf.predict(X_test)
#print("Test set score: {:.2f}".format(clf.score(X_test, y_test)))
#pd.crosstab(y_test, y_pred, rownames=['Actual'], colnames=['Predicciones']) # Hizo buenas estimaciones
#%%
scores_knn = []
scores_tree = []
scores_rf = []
for _ in range(100):
    X_train, X_test, y_train, y_test = train_test_split(
        iris_dataset['data'], iris_dataset['target'])
    knn = KNeighborsClassifier(n_neighbors=1)
    knn.fit(X_train, y_train)
    scores_knn.append(knn.score(X_test, y_test))
    clf = DecisionTreeClassifier()
    clf.fit(X_train, y_train)
    scores_tree.append(clf.score(X_test, y_test))
    forest = RandomForestClassifier(n_jobs=2, n_estimators=10)
    forest.fit(X_train, y_train)
    scores_rf.append(forest.score(X_test, y_test))

print(f'Promedio de scores para KNN: {round(np.mean(scores_knn),3)}','\n',
      f'Promedio de scores para R. Trees: {round(np.mean(scores_tree),3)}',
      '\n', f'Promedio de scores para R.Forest: {round(np.mean(scores_rf),3)}')