import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

class my_QDA:
    """
    Quadratic Discriminant Analysis (QDA) is a classification method based on Bayes' theorem and a normal (Gaussian) distribution of features in each class.
    The main difference between QDA and LDA is that in QDA:
    - Each class has its own covariance matrix, unlike in LDA, where the covariance matrix is common.
    - The discriminant function is quadratic with respect to the features.
    """
    def __init__(self, epsilon=1e-6):
        self.epsilon_ = epsilon
        self.means_ = {}
        self.covariances_ = {}
        self.cov_inv_ = {}
        self.logdet_ = {}
        self.priors_ = {}
        self.classes_ = None

    def fit(self, X, y):
        self.classes_ = np.unique(y)
        n_samples = X.shape[0]

        for cls in self.classes_:
            X_cls = X[y == cls]
            n_cls = X_cls.shape[0]

            self.priors_[cls] = n_cls / n_samples
            self.means_[cls] = np.mean(X_cls, axis=0)

            cov_matrix = np.cov(X_cls, rowvar=False, ddof=1)
            cov_matrix += self.epsilon_ * np.eye(X.shape[1])
            self.covariances_[cls] = cov_matrix
            self.cov_inv_[cls] = np.linalg.pinv(cov_matrix)

            _, logdet = np.linalg.slogdet(cov_matrix)
            self.logdet_[cls] = logdet
        
    def predict_proba(self, X):
        discriminants = []

        for cls in self.classes_:
            mean_vec = self.means_[cls]
            cov_inv = self.cov_inv_[cls]
            logdet = self.logdet_[cls]
            prior = self.priors_[cls]

            diff = X - mean_vec
            quad_form = np.sum((diff @ cov_inv) * diff, axis=1)
            delta = -0.5*quad_form - 0.5*logdet + np.log(prior)
            discriminants.append(delta)
        
        discriminants = np.array(discriminants).T
        max_delta = np.max(discriminants, axis=1, keepdims=True)
        exp_discriminants = np.exp(discriminants - max_delta)
        prob_matrix = exp_discriminants / np.sum(exp_discriminants, axis=1, keepdims=True)
        return prob_matrix

    def predict(self, X):
        prob_matrix = self.predict_proba(X)
        return np.argmax(prob_matrix, axis=1)

####### main ########

if __name__ == "__main__":
    data = load_iris()
    X = data.data
    y = data.target
    le = LabelEncoder()
    y = le.fit_transform(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # prediction
    lda = my_QDA()
    lda.fit(X_train,y_train)
    probabilities = lda.predict_proba(X_test)
    print(probabilities)