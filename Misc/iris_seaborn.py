# iris_seaborn.py
import pandas as pd
from sklearn.datasets import load_iris
import seaborn as sns
iris_dataset = load_iris()
iris_dataframe = pd.DataFrame(iris_dataset['data'], columns = iris_dataset.feature_names)
#pd.plotting.scatter_matrix(iris_dataframe, c = iris_dataset['target'], figsize = (15, 15), marker = 'o', hist_kwds = {'bins': 20}, s = 60, alpha = 0.8)
iris_dataframe['target'] = iris_dataset['target']
cols_sel = ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)', 'target']
sns.pairplot(data = iris_dataframe[cols_sel], hue = 'target')