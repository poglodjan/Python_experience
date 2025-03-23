import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class my_LogisticRegression:
    def __init__(self, penalty=None, alpha=0.01, max_iter=1000, tol=1e-4):
        self.penalty = penalty
        self.alpha = alpha
        self.max_iter = max_iter
        self.tol = tol
        self.classes_ = None
        self.weights_ = None
    
    def _softmax(self, Z):
        expZ = np.exp(Z - np.max(Z, axis=1, keepdims=True))
        return expZ / np.sum(expZ, axis=1, keepdims=True)
    
    def _loss(self, X, y, weights):
        m = X.shape[0]
        logits = X @ weights
        probs = self._softmax(logits)
        loss = -np.sum(np.log(probs[np.arange(m), y])) / m

        if self.penalty == "l2":
            loss += (self.alpha / 2) * np.sum(weights ** 2)
        if self.penalty == "l1":
            loss += (self.alpha) * np.sum(np.abs(weights))
        
        return loss

    def _gradient(self, X, y, weights):
        m = X.shape[0]
        logits = X @ weights
        probs = self._softmax(logits)
        one_hot_y = np.zeros_like(probs)
        one_hot_y[np.arange(m), y] = 1
        grad = X.T @ (probs - one_hot_y) / m

        if self.penalty == "l2":
            grad += self.alpha * weights
        elif self.penalty == "l1":
            grad += self.alpha * np.sign(weights)

        return grad
    
    def fit(self, X, y):
        self.classes_ = np.unique(y)
        n_classes = len(self.classes_)
        n_features = X.shape[1]
        # adding bias column
        X = np.hstack([np.ones((X.shape[0],1)),X])
        self.weights_ = np.random.randn(X.shape[1], n_classes)

        for iteration in range(self.max_iter):
            grad = self._gradient(X, y, self.weights_)
            prev_weights = self.weights_.copy()
            self.weights_ -= self.alpha * grad

            if np.linalg.norm(self.weights_ - prev_weights, ord=1) < self.tol:
                print(f"Stopped after {iteration} iterations")
                break
    
    def predict_proba(self, X):
        X = np.hstack([np.ones((X.shape[0], 1)), X])
        logits = X @ self.weights_
        probs = self._softmax(logits)
        return probs

    def predict(self, X):
        probs = self.predict_proba(X)
        return np.argmax(probs, axis=1)

    def get_params(self):
        return {"weights": self.weights_, "penalty": self.penalty, "alpha": self.alpha}

if __name__ == "__main__":
    data = load_iris()
    X = data.data
    y = data.target

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    penalties = [None, "l1", "l2"]
    for penalty in penalties:
        model = my_LogisticRegression(penalty=penalty, alpha=0.01, max_iter=1000)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Penalty: {penalty}, Accuracy: {accuracy:.4f}")
