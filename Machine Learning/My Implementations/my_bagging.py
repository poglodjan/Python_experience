import matplotlib.pyplot as plt
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.base import clone
from collections import Counter
import numpy as np

data = load_breast_cancer()
X,y = data.data, data.target

X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=42)

class My_BaggingClassifier:
    def __init__(self, base_estimator, n_estimators=10):
        self.base_estimator = base_estimator
        self.n_estimators = n_estimators
        self.models = []
    
    def bootstrap_sample(self, X, y):
        """ returns generated boostrap sample """
        n_samples = X.shape[0]
        indices = np.random.choice(n_samples, size=n_samples, replace=True)
        return X[indices], y[indices]
    
    def _clone_estimator(self):
        """ returns new DecisionTree instance """
        return clone(self.base_estimator)

    def fit(self, X, y):
        self.models = []
        for _ in range(self.n_estimators):
            X_sample, y_sample = self.bootstrap_sample(X, y)
            model = self._clone_estimator()
            model.fit(X_sample, y_sample)
            self.models.append(model)
    
    def predict(self, X):
        predictions = np.array([model.predict(X) for model in self.models])
        final_predictions = [Counter(pred).most_common(1)[0][0] for pred in predictions.T]
        return final_predictions

bagging = My_BaggingClassifier(base_estimator=DecisionTreeClassifier(), n_estimators=20)
bagging.fit(X_train, y_train)
y_pred = bagging.predict(X_test)

acc = accuracy_score(y_test, y_pred)
print("Bagging accuracy:", acc)