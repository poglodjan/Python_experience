# Exploring data frame using machine learning functions and modeling accurancy

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.model_selection import train_test_split
%matplotlib inline

columns = ['Sepal length', 'Sepal width', 'Petal length', 'Petal width', 'Class_labels'] 

df = pd.read_csv('iris.data', names=columns)
df.head()

# analiza statystyczna danych
df.describe() 

# wizualizacja całej ramki
sns.pairplot(df, hue='Class_labels')

# separownie kodu po grupach
data = df.values
X = data[:,0:4]
Y = data[:,4]

separacja = np.array([np.average(X[:, i][Y==j].astype('float32')) for i in range (X.shape[1])
 for j in (np.unique(Y))])
seperated = separacja.reshape(4, 3)
seperated = np.swapaxes(seperated, 0, 1)
X_axis = np.arange(len(columns)-1)
width = 0.25

# Wykres średniej arytmetycznej dla każdej z grupy w ramce danych 
plt.bar(X_axis, seperated[0], width, label = 'Setosa')
plt.bar(X_axis+width, seperated[1], width, label = 'Versicolour')
plt.bar(X_axis+width*2, seperated[2], width, label = 'Virginica')
plt.xticks(X_axis, columns[:4])
plt.xlabel("Features")
plt.ylabel("Value in cm.")
plt.legend(bbox_to_anchor=(1.3,1))
plt.show()

# Modelowanie i testy
X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)

# Wykorzystanie train do testowania
from sklearn.svm import SVC
svn = SVC()

# Badanie precyzyjności
svn.fit(X_train, y_train)
predictions = svn.predict(X_test)
from sklearn.metrics import accuracy_score
accuracy_score(y_test, predictions)

# Otrzymujemy wynik 97% - dokładność badanego modelu


