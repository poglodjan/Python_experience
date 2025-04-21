import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class Node:
    def __init__(self, feature=None, threshold=None,
                 left=None, right=None, *, value=None):
        self.feature = feature   # indice
        self.threshold = threshold 
        self.left = left   # left sub-tree       
        self.right = right # right sub-tree
        self.value = value 

class my_DecisionTreeClassifier:
    def __init__(self, max_depth = 3):
        self.max_depth = max_depth
        self.root = None

    def gini(self, y):
        classes = set(y)
        impurity = 1
        for c in classes:
            p = sum(y == c) / len(y)
            impurity -= p**2
        return impurity
    
    def fit(self, X, y):
        self.root = self._build_tree(X, y, depth=0)
    
    def _build_tree(self, X, y, depth):
        num_samples_per_class = [np.sum(y == i) for i in np.unique(y)] # e.g [53, 45]
        predicted_class = np.argmax(num_samples_per_class)

        # stop condition
        if depth >= self.max_depth or len(np.unique(y)) == 1:
            return Node(value=predicted_class)
        
        feature, threshold, sets = self.best_split(X, y)
        if sets is None:
            return Node(value=predicted_class)

        left_idx, right_idx = sets
        left = self._build_tree(X[left_idx], y[left_idx], depth+1)
        right = self._build_tree(X[right_idx], y[right_idx], depth+1)
        return Node(feature, threshold, left, right)

    def best_split(self, X, y):
        m, n = X.shape
        best_feature, best_thresh, best_gain = None, None, 0
        best_sets = None
        parent_gini = self.gini(y)

        for feature in range(n):
            thresholds = np.unique(X[:, feature])
            for t in thresholds:
                left_idx = X[:, feature] <= t
                right_idx = X[:, feature] > t
            if len(y[left_idx]) == 0 or len(y[right_idx]) == 0:
                continue

            left_gini = self.gini(y[left_idx])
            right_gini = self.gini(y[right_idx])
            gain = parent_gini - (len(y[left_idx]) / len(y)) * left_gini - (len(y[right_idx]) / len(y)) * right_gini

            if gain > best_gain:
                best_gain = gain
                best_feature = feature
                best_thresh = t
                best_sets = (left_idx, right_idx)

        return best_feature, best_thresh, best_sets
    
    def predict_one(self, x, node):
        if node.value is not None:
            return node.value
        if x[node.feature] <= node.threshold:
            return self.predict_one(x, node.left)
        else:
            return self.predict_one(x, node.right)

    def predict(self, X):
        return np.array([self.predict_one(x, self.root) for x in X])
    

# _____ Analyze self implementation _______
data = load_breast_cancer()
X,y = data.data, data.target
feature_names = data.feature_names
class_names = data.target_names
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=20)

my_tree = my_DecisionTreeClassifier(max_depth=3)
my_tree.fit(X_train, y_train)
y_pred = my_tree.predict(X_test)

print("My tree Accuracy:", accuracy_score(y_test, y_pred))

# _____ Analyze sklearn implementation _______ 

# 1) Analyze parameter impact
criteria = ['gini', 'entropy']
splitters = ['best', 'random']
depths = [None, 3, 5]
min_samples = [2, 10, 20]

results = []
for crit in criteria:
    for split in splitters:
        for depth in depths:
            for min_split in min_samples:
                model = DecisionTreeClassifier(criterion=crit,
                               splitter=split,
                               max_depth=depth,
                               min_samples_split=min_split,
                               random_state=20)
                model.fit(X_train, y_train)
                results.append({
                    "criterion": crit,
                    "splitter": split,
                    "max_depth": depth,
                    "min_samples_split": min_split,
                    "n_nodes": model.tree_.node_count,
                    "train_acc": model.score(X_train, y_train),
                    "test_acc": model.score(X_test, y_test)
                })

df_results = pd.DataFrame(results)
print("Parameter Impact Analysis:\n", df_results.head())

# 2) Plot default tree
clf = DecisionTreeClassifier(random_state=20)
clf.fit(X_train, y_train)

plt.figure(figsize=(20,10))
plot_tree(clf, filled=True,
          feature_names=feature_names,
          class_names=class_names)
plt.title("Decision Tree")
plt.show()

# 3) Cost-Cemplexity Pruning
path = clf.cost_complexity_pruning_path(X_train, y_train)
ccp_alphas = path.ccp_alphas

pruned_models = []
for alpha in ccp_alphas:
    pruned_tree = DecisionTreeClassifier(random_state=20, ccp_alpha=alpha)
    pruned_tree.fit(X_train, y_train)
    pruned_models.append({
        "alpha": alpha,
        "n_nodes": pruned_tree.tree_.node_count,
        "train_acc": pruned_tree.score(X_train, y_train),
        "test_acc": pruned_tree.score(X_test, y_test)
    })

df_pruning = pd.DataFrame(pruned_models)
print("\nCost-Complexity Pruning Results:\n", df_pruning.tail())

# Plot pruning effect
plt.figure(figsize=(8, 5))
plt.plot(df_pruning["alpha"], df_pruning["test_acc"], marker='o', label="Test Accuracy")
plt.plot(df_pruning["alpha"], df_pruning["train_acc"], marker='o', label="Train Accuracy")
plt.xlabel("ccp_alpha")
plt.ylabel("Accuracy")
plt.title("Effect of Cost-Complexity Pruning")
plt.legend()
plt.grid(True)
plt.show()

