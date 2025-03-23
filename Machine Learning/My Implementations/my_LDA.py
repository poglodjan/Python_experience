import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

class my_LDA:
    """
    - LDA assumes a linear decision boundary, resulting from the equality of the covariance matrices in all classes.
    - This makes LDA fast and stable, but it does not handle nonlinearly separable data well.
    - With the fit_transform implementation, it handle with dimensionality reduction to min(n_components, number of classes - 1)
    """
    def __init__(self):
        self.classes_ = None
        self.means_ = {}
        self.covariance_ = None
        self.priors_ = {}
        self.coef_ = {}
        self.intercepts_ = {}
        self.W_ = None  # matrix for dimensionality reduction
    
    def fit(self, X, y):
        self.classes_ = np.unique(y)
        n_samples, n_features = X.shape
        n_classes = len(self.classes_)
        pooled_cov = np.zeros((n_features, n_features))

        # computing means, priors and covariances for each class
        for cls in self.classes_:
            X_cls = X[y == cls]
            n_cls = X_cls.shape[0]
            mean_vec = np.mean(X_cls, axis=0)
            self.means_[cls] = mean_vec
            self.priors_[cls] = n_cls / n_samples

            # Pooled covariance
            if n_cls > 1:
                cov_matrix = np.cov(X_cls, rowvar=False, ddof=1)
            else: cov_matrix = np.zeros((n_features, n_features))
            pooled_cov += (n_cls-1) * cov_matrix

        pooled_cov /= (n_samples - n_classes)
        self.covariance_ = pooled_cov
        self.sigma_inv_ = np.linalg.pinv(pooled_cov) # (Moore-Penrose) pseudo-inverse of a matrix

        # computing coeficiants for each class
        for cls in self.classes_:
            delta_mu = self.means_[cls]
            self.coef_[cls] = self.sigma_inv_ @ delta_mu
            self.intercepts_[cls] = -0.5 * delta_mu @ self.sigma_inv_ @ delta_mu + np.log(self.priors_[cls])

    def fit_transform(self, X, y, n_components=2):
        """ transforming data for dimensionality reduction """
        self.fit(X, y)

        overall_mean = np.mean(X, axis=0)
        S_b = np.zeros((X.shape[1], X.shape[1]))

        for cls in self.classes_:
            n_cls = np.sum(y == cls)
            mean_vec = self.means_[cls].reshape(-1,1)
            overall_mean_vec = overall_mean.reshape(-1,1)
            S_b += n_cls * (mean_vec - overall_mean_vec) @ (mean_vec - overall_mean_vec).T
        
        eigvals, eigvecs = np.linalg.eig(np.linalg.pinv(self.covariance_) @ S_b)
        sorted_indices = np.argsort(eigvals)[::-1]
        self.W_ = eigvecs[:, sorted_indices[:n_components]]

        X_reduced = X @ self.W_
        return X_reduced

    def predict_proba(self, X):
        linear_predictors = {}
        for cls in self.classes_:
            linear_predictors[cls] = X @ self.coef_[cls] + self.intercepts_[cls]
        
        linear_predictors = np.array([linear_predictors[cls] for cls in self.classes_]).T
        exp_scores = np.exp(linear_predictors)
        prob_matrix = exp_scores / np.sum(exp_scores, axis=1, keepdims=True) # softmax
        return prob_matrix

    def predict(self, X):
        prob_matrix = self.predict_proba(X)
        return np.argmax(prob_matrix, axis=1)
    
    def get_params(self):
        print(f"LDA coefs: \n{self.coef_},\n intercept:\n {self.intercepts_},\n priors: \n{self.priors_},\n means: \n{self.means_}")

####### main ########

if __name__ == "__main__":
    data = load_iris()
    X = data.data
    y = data.target
    le = LabelEncoder()
    y = le.fit_transform(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # prediction
    lda = my_LDA()
    lda.fit(X_train,y_train)
    probabilities = lda.predict_proba(X_test)
    print(probabilities)

    # dimensionality reduction
    original_variance = np.sum(np.var(X_train, axis=0))
    X_reduced = lda.fit_transform(X_train, y_train, n_components=2)
    reduced_variance = np.sum(np.var(X_reduced, axis=0)) 
    variance_retained = (reduced_variance / original_variance) * 100
    
    # chart 1: Dimensionality reduction with LDA
    plt.figure(figsize=(12, 5))
    plt.subplot(1, 3, 1)
    colors = ['red', 'green', 'blue']
    for i, color in enumerate(colors):
        plt.scatter(X_reduced[y_train == i, 0], X_reduced[y_train == i, 1], color=color, label=data.target_names[i], alpha=0.8)
    plt.title('Dimensionality reduction with LDA')
    plt.legend()

    # Chart 2: Variance explianed with LDA components
    plt.subplot(1, 3, 2)
    variance_explained = np.var(X_reduced, axis=0) / np.sum(np.var(X_reduced, axis=0))
    plt.bar(range(len(variance_explained)), variance_explained, color=['blue', 'orange'])
    plt.title('Variance explianed with LDA components')
    plt.xlabel('LDA components')
    plt.ylabel('Variance explained')
    plt.xticks([0, 1], ['LDA 1', 'LDA 2'])

    # Chart 3: Comparison of variance before and after reduction
    plt.subplot(1, 3, 3)
    plt.bar(['Original data', 'Data after reduction'], [original_variance, reduced_variance], color=['green', 'red'])
    plt.title('Comparison of variance before and after reduction')
    plt.ylabel('Total variance')
    plt.text(0, original_variance, f'{original_variance:.2f}', ha='center', va='bottom')
    plt.text(1, reduced_variance, f'{reduced_variance:.2f} ({variance_retained:.2f}%)', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()