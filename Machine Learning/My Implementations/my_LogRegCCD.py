import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.datasets import load_iris
from sklearn.metrics import (recall_score, precision_score, f1_score, 
                             balanced_accuracy_score, roc_auc_score, average_precision_score) # for optimal lambda value

class my_LogRegCCD:
    def __init__(self, alpha=1.0, n_lambdas=100, eps=1e-3, tol=1e-4, max_iter=100, max_outer_iter=50):
        """
        alpha: parameter for mixing in the Elastic Net (1.0 means just the LASSO, 0.0 means L2)
        n_lambdas: number of lambda values in the path
        eps: lambda_min = eps * lambda_max
        tol: toleration for the convergence in coeficiant actualization
        max_iter: maximum number of iteration in CCD (inner loop) - coefficiant actualization
        max_outer_iter: IRLS maximum iteration number
        """
        self.alpha = alpha
        self.n_lambdas = n_lambdas
        self.eps = eps
        self.tol = tol
        self.max_iter = max_iter
        self.max_outer_iter = max_outer_iter
        self.lambdas = None
        self.coef_path = None
        self.intercept_path = None
        self.best_lambda = None
        self.best_coef = None
        self.best_intercept = None
        self.validation_scores = None

    def _soft_threshold(self, z, gamma):
        """ S(z,y) is the soft-thresholding operator with value: """
        if abs(z) > gamma and z>0: return z - gamma
        elif abs(z) > gamma and z<0: return z + gamma #I'm changing here so it'll fit formula (6) from the paper,
        else: return 0.0

    def _compute_lambda_max(self, X, y):
        """
        Computing lambda_max for which coefficiants equals 0 
        (claiming p_i = 0.5) 
        """
        N = X.shape[0]
        grad = np.abs(np.dot(X.T, (y - 0.5))) / N
        return np.max(grad) / self.alpha if self.alpha != 0 else np.max(grad)

    def fit(self, X_train, y_train):
        """
        Fits logistic regression model using CCD (with IRLS method)
        for the whole regularization path
        """
        N, p = X_train.shape 
        self.coef_path = []
        self.intercept_path = []
        
        lambda_max = self._compute_lambda_max(X_train, y_train) # computes max_lambda
        lambda_min = self.eps * lambda_max
        self.lambdas = np.logspace(np.log10(lambda_max), np.log10(lambda_min), self.n_lambdas) # generate lambdas for given n_lambdas, min and max

        # Warm start: coefficiants set to zero, intercept set to average logit fucntion
        beta = np.zeros(p)
        avg_y = np.mean(y_train)
        if (0 < avg_y < 1): #added change for avg_y ==1
            beta0 = np.log(avg_y / (1 - avg_y))
        elif (avg_y ==1):  
            beta0 = 1
        else: beta0 = 0
        
        # FOR EACH lambda we fit the model
        for lam in self.lambdas:
            # IRLS algorithm (outer loop)
            for outer_iter in range(self.max_outer_iter):
                eta = beta0 + np.dot(X_train, beta)
                eta = np.clip(eta, -500, 500) # protection for dividing by 0 
                p_vec = 1.0 / (1.0 + np.exp(-eta))
                p_vec = np.clip(p_vec, 1e-5, 1 - 1e-5) # protection for dividing by 0 
                w = p_vec * (1 - p_vec)

                # Calculating z - working response
                z = eta + (y_train - p_vec) / w
                # Coping beta to check covergance
                beta_old = beta.copy()
                beta0_old = beta0
                # Intercept actualization (without regularization)
                beta0 = np.sum(w * (z - np.dot(X_train, beta))) / np.sum(w) # where did you find this formula?

                # inner CCD loop – coefs actualization
                for iter_cd in range(self.max_iter):
                    beta_prev = beta.copy()
                    for j in range(p):
                        # residual wector for j-feature (without it itself) like in formula
                        r_j = z - beta0 - np.dot(X_train, beta) + X_train[:, j] * beta[j] #formula 5?
                        numerator = np.sum(w * X_train[:, j] * r_j)
                        denom = np.sum(w * X_train[:, j]**2) + lam * (1 - self.alpha) ##np.sum(w * X_train[:, j]**2) ??? the formula isn't (1+lambda(1-alfa)
                        beta[j] = self._soft_threshold(numerator, lam * self.alpha) / denom
                    if np.max(np.abs(beta - beta_prev)) < self.tol:
                        break

                # Checking IRLS convergance
                if np.max(np.abs(beta - beta_old)) < self.tol and abs(beta0 - beta0_old) < self.tol:
                    break

            self.coef_path.append(beta.copy())
            self.intercept_path.append(beta0)
        
        self.coef_path = np.array(self.coef_path) # shape: (n_lambdas, p)
        self.intercept_path = np.array(self.intercept_path)
    
    def predict_proba(self, X_test):
        """
        using best coefficient returns probabilities for X data
        """
        eta = self.best_intercept + np.dot(X_test, self.best_coef)
        return 1.0 / (1.0 + np.exp(-eta))
    
    def validate(self, X_valid, y_valid, measure='f1'):
        """
        Model scores on validation set for each lambda value 
        - choose best one with given measure
          - 'recall'
          - 'precision'
          - 'f1'
          - 'balanced_accuracy'
          - 'roc_auc'
          - 'average_precision'
        """
        scores = []
        for i, lam in enumerate(self.lambdas):
            beta = self.coef_path[i]
            beta0 = self.intercept_path[i]
            eta = beta0 + np.dot(X_valid, beta)
            eta = np.clip(eta, -500, 500) 
            p_pred = 1.0 / (1.0 + np.exp(-eta))
            y_pred = (p_pred >= 0.5).astype(int)
            if measure == 'recall': score = recall_score(y_valid, y_pred)
            elif measure == 'precision': score = precision_score(y_valid, y_pred)
            elif measure == 'f1': score = f1_score(y_valid, y_pred)
            elif measure == 'balanced_accuracy': score = balanced_accuracy_score(y_valid, y_pred)
            elif measure == 'roc_auc': score = roc_auc_score(y_valid, p_pred)
            elif measure == 'average_precision': score = average_precision_score(y_valid, p_pred)
            else: raise ValueError("Unsupported measure")
            scores.append(score)

        self.validation_scores = np.array(scores)
        best_index = np.argmax(self.validation_scores)
        self.best_lambda = self.lambdas[best_index]
        self.best_coef = self.coef_path[best_index]
        self.best_intercept = self.intercept_path[best_index]
        print(f"Optimal lambda: {self.best_lambda}, best {measure}: {self.validation_scores[best_index]}")
        return self.validation_scores # returns scores of given measure

    def plot(self, measure='f1'):
        """
        Plot of log10(lambda) vs given measure
        """
        if self.validation_scores is None:
            raise ValueError("Validation scores not computed. Run validate() first.")
        plt.figure(figsize=(8,6))
        plt.plot(np.log10(self.lambdas), self.validation_scores, marker='o')
        plt.xlabel('log10(lambda)')
        plt.ylabel(measure)
        plt.title(f'{measure} vs log10(lambda)')
        plt.grid(True)
        plt.show()

    def plot_coefficients(self):
        """
        Plot of coeficiants paths in lambda logarithm function
        """
        plt.figure(figsize=(8,6))
        for j in range(self.coef_path.shape[1]):
            plt.plot(np.log10(self.lambdas), self.coef_path[:, j], label=f'coef {j}')
        plt.xlabel('log10(lambda)')
        plt.ylabel('Value of coefficiants')
        plt.title('Coefficiant paths')
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.grid(True)
        plt.show()
    
###### main ######

if __name__ == "__main__":
    data = load_iris()
    X = data.data
    y = data.target
    le = LabelEncoder()
    scaler = StandardScaler()
    y = le.fit_transform(y)

    X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.2, random_state=42)
    X_train = scaler.fit_transform(X_train)
    X_valid = scaler.transform(X_valid)

    model = my_LogRegCCD(alpha=1.0, n_lambdas=50, eps=1e-3, tol=1e-4) 
    model.fit(X_train, y_train)
    # search for optimal lambda value on the validation set (here f1 score)
    model.validate(X_valid, y_valid, measure='f1')
    # Plot for F1-score in relation to lambda values
    model.plot(measure='f1')
    model.plot_coefficients()
    y_proba = model.predict_proba(X_valid)
    y_pred = (y_proba >= 0.5).astype(int)
    f1 = f1_score(y_valid, y_pred)
    print(f"Final F1-score on validation set: {f1:.4f}")