import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from scipy.stats import gaussian_kde

class my_NB:
    """
    Naive Bayes (NB) is a classification method that assumes:
    - Independence of features within each class.
    - Normal (Gaussian) distribution of features within each class.
    - Added feature to operate with KDE estimator
    """
    def __init__(self, method="gaussian"):
        self.means_ = {}
        self.variances_ = {}
        self.priors_ = {}
        self.classes_ = None
        self.method_ = method  # "gaussian", "kde"
        self.kde_ = {}  # For KDE method
    
    """ logarithms of pdf for selected method """
    def _log_gaussian_pdf(self, X, mu, var):
        log_prob = -0.5 * np.log(2 * np.pi * var) - 0.5 * ((X - mu) ** 2) / var
        return np.sum(log_prob, axis=1)
    
    def _log_kde_pdf(self, X, kde):
        log_prob = [np.log(kde[i](X[:,i])) for i in range(X.shape[1])]
        return np.sum(log_prob, axis=0)


    """ fit with data """
    def fit(self, X, y):
        self.classes_ = np.unique(y)
        n_samples = X.shape[0]

        for cls in self.classes_:
            X_cls = X[y == cls]
            n_cls = X_cls.shape[0]
            self.priors_[cls] = n_cls / n_samples

            # parameters computing
            if self.method_ == "gaussian":
                self.means_[cls] = np.mean(X_cls, axis=0)
                self.variances_[cls] = np.var(X_cls, axis=0, ddof=1)
            if self.method_ == "kde":
                self.kde_[cls] = [gaussian_kde(X_cls[:,j]) for j in range(X.shape[1])]

    def predict_proba(self, X):
        log_probs = []

        for cls in self.classes_:
            prior = np.log(self.priors_[cls])

            if self.method_ == "gaussian":
                mu = self.means_[cls]
                var = self.variances_[cls]
                log_prob = self._log_gaussian_pdf(X, mu, var) + prior
            if self.method_ == "kde":
                kde = self.kde_[cls]
                log_prob = self._log_kde_pdf(X, kde) + prior

            log_probs.append(log_prob)

        # numerical stability and softmax
        log_probs = np.array(log_probs).T
        max_log = np.max(log_probs, axis=1, keepdims=True)
        exp_log_probs = np.exp(log_probs - max_log)
        prob_matrix = exp_log_probs / np.sum(exp_log_probs, axis=1, keepdims=True)
        return prob_matrix
    
    def predict(self, X):
        prob_matrix = self.predict_proba(X)
        return np.argmax(prob_matrix, axis=1)
    
    def get_params(self):
        return {'means': self.means_, 'variances': self.variances_, 'priors': self.priors_}

####### main ########

if __name__ == "__main__":
    data = load_iris()
    X = data.data
    y = data.target
    le = LabelEncoder()
    y = le.fit_transform(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Test for each method and plotting results
    methods = ["gaussian", "kde"]
    accuracies = []
    for method in methods:
        nb = my_NB(method=method)
        nb.fit(X_train, y_train)
        y_pred = nb.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        accuracies.append(acc)
        print(f"Accuracy for {method}: {acc:.4f}")
    plt.figure(figsize=(8, 5))
    plt.bar(methods, accuracies, color=["blue", "green", "orange"])
    plt.title("Accuracy of Different Naive Bayes Methods on Iris")
    plt.xlabel("Method")
    plt.ylabel("Accuracy")
    plt.ylim(0, 1)
    for i, acc in enumerate(accuracies):
        plt.text(i, acc + 0.02, f"{acc:.2f}", ha="center")
    plt.show()