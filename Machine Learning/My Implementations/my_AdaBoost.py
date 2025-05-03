import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_breast_cancer, load_wine
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, log_loss
from sklearn.base import clone
from sklearn.model_selection import StratifiedKFold
from collections import defaultdict
from scipy.stats import chi2
# for comparison with AdaBoost
from my_bagging import My_BaggingClassifier 
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier

class MyAdaBoost:
    def __init__(self, base_estimator=DecisionTreeClassifier(max_depth=3), n_estimators=10):
        self.base_estimator = base_estimator
        self.n_estimators = n_estimators
        self.models = []
        self.betas = []

    def fit(self, X, y):
        n = X.shape[0]
        w = np.ones(n) / n # i. weights initialization

        # ii. iterations
        for k in range(self.n_estimators):
            #A build clf with weights w_i
            model = clone(self.base_estimator)
            model.fit(X, y, sample_weight=w)
            
            #B compute weitghed error 
            pred = model.predict(X)
            incorrect = (pred != y)
            epsilon = np.dot(w, incorrect)

            #C calculate Beta
            if epsilon == 0: beta=1e-10         # divide by 0 protection
            elif epsilon >= 0.5: continue       # weak classificators
            else: beta = epsilon / (1-epsilon)

            #D save clf and his weight
            self.models.append(model)
            self.betas.append(beta)

            # F. weights normalization
            w *= np.where(pred == y, beta, 1)
            w /= np.sum(w)
    
    def predict(self, X):
        if not self.models: 
            raise ValueError("Model has not been trained")
    
        all_prds = [model.predict(X) for model in self.models]
        final_prds = []

        for i in range(X.shape[0]):
            vote_count  = defaultdict(float)
            for k in range(len(self.models)):
                label = all_prds[k][i]
                vote_count[label] += np.log(1 / self.betas[k])
            
            # class with the biggest weighted sum log(1/beta)
            final_label = max(vote_count.items(), key=lambda x: x[1])[0]
            final_prds.append(final_label)
        
        return np.array(final_prds)


if __name__ == "__main__":
    """
    Experiment I:
    (a) Compare the following ensemble methods:
    • Single tree
    • Bagging
    • Boosting (AdaBoost), your implementation.
    • XGBoost
    • Random Forest
    Experiment include: 3 datasets, 3 seeds, 10-cross validation
    """

    def generate_syntetic_dataset(n_samples, n_features, threshold):
        X = np.random.normal(loc=0, scale=1, size=(n_samples, n_features))
        X_squared_sum = np.sum(X**2, axis=1)
        y = np.where(X_squared_sum > threshold, 1, 0)
        return X, y
    
    # Median of chi-squared distribution with 10 degrees of freedom
    chi2_median = chi2.ppf(0.5, df=10)
    X_train_syntetic, y_train_syntetic = generate_syntetic_dataset(n_samples = 2000, n_features = 10, threshold = chi2_median)
    X_test_syntetic, y_test_syntetic = generate_syntetic_dataset(n_samples = 10000, n_features = 10, threshold = chi2_median)
    data_syntetic = X_train_syntetic, y_train_syntetic, X_test_syntetic, y_test_syntetic 
    
    #1) load datasets
    wine_data = load_wine()
    X_wine,y_wine = wine_data.data,wine_data.target
    mask = (y_wine == 0) | (y_wine == 1) # keep 0|1
    X_wine,y_wine = X_wine[mask], y_wine[mask]

    cancer_data = load_breast_cancer()
    X_cancer, y_cancer = cancer_data.data, cancer_data.target
    datasets = {
        "breast_cancer": (X_cancer, y_cancer),
        "wine": (X_wine,y_wine),
        "syntetic": data_syntetic
    }
    seeds = [320575, 111, 5]
    my_base_tree = DecisionTreeClassifier(max_depth=3)
    models = {
    "AdaBoost": lambda: MyAdaBoost(base_estimator=DecisionTreeClassifier(max_depth=1), n_estimators=20),
    "Bagging": lambda: My_BaggingClassifier(base_estimator=DecisionTreeClassifier(), n_estimators=20),
    "DecisionTree": lambda: DecisionTreeClassifier(max_depth=3),
    "RandomForest": lambda: RandomForestClassifier(n_estimators=20, max_depth=3),
    "XGBoost": lambda: XGBClassifier(n_estimators=20, max_depth=3, learning_rate=0.1, eval_metric='logloss')
    }
    
    results = []
    for dataset_name, dataset in datasets.items():
        if dataset_name == "syntetic":
            X_train, y_train, X_test, y_test = dataset
            print("Unique values in y_train:", np.unique(y_train))
            for seed in seeds:
                for model_name, model_func in models.items():
                    model = model_func()
                    if hasattr(model, 'random_state'): model.set_params(random_state=seed)  
                    if model_name == "AdaBoost":
                        y_train_converted = np.where(y_train==0, -1,1)
                        y_test_converted = np.where(y_test==0, -1,1)
                    else:
                        y_train_converted = y_train
                        y_test_converted = y_test

                    # training on x_train, evaluating on the x_test
                    model.fit(X_train, y_train_converted)
                    y_pred = model.predict(X_test)
                    acc = accuracy_score(y_test_converted, y_pred)
                
                    results.append({
                        "dataset": dataset_name,
                        "seed": seed,
                        "model": model_name,
                        "mean_accuracy": acc,
                        "std_accuracy": 0.0 
                    })
        else:
            X, y = dataset
            print("Unique values in y:", np.unique(y))
            for seed in seeds:
                skf = StratifiedKFold(n_splits=10, shuffle=True, random_state=seed) # using 10-cross for statistic significant reesults
                for model_name, model_func in models.items():
                    acc_scores = []
                    if model_name == "AdaBoost":
                        y_converted = np.where(y==0, -1,1)
                    else: y_converted = y

                    for train_idx, test_idx in skf.split(X, y_converted):
                        model = model_func()
                        model.fit(X[train_idx], y[train_idx])
                        y_pred = model.predict(X[test_idx])
                        acc_scores.append(accuracy_score(y[test_idx], y_pred))
                    results.append({
                        "dataset": dataset_name,
                        "seed": seed,
                        "model": model_name,
                        "mean_accuracy": np.mean(acc_scores),
                        "std_accuracy": np.std(acc_scores)
                    })

    df_results = pd.DataFrame(results)
    print(df_results[["model","mean_accuracy"]])

    # plots

    # Boxplot
    plt.figure(figsize=(14, 6))
    sns.boxplot(x='model', y='mean_accuracy', hue='dataset', data=df_results)
    plt.title('Boxplot: Accuracy per Model per Dataset (10-fold CV)')
    plt.ylabel('Accuracy')
    plt.xlabel('Model')
    plt.legend(title='Dataset')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Barplot of mean accuracies with error bars (std)
    plt.figure(figsize=(14, 6))
    sns.barplot(x='model', y='mean_accuracy', hue='dataset', data=df_results, errorbar='sd', capsize=0.1)
    plt.title('Barplot: Mean Accuracy +- STD per Model per Dataset')
    plt.ylabel('Mean Accuracy')
    plt.xlabel('Model')
    plt.legend(title='Dataset')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    # Faceted barplot per dataset
    g = sns.catplot(x='model', y='mean_accuracy', col='dataset', kind='bar', data=df_results,
                    errorbar='sd', height=5, aspect=1.2, capsize=0.1)
    g.figure.suptitle('Accuracy Comparison per Dataset', y=1.05)
    g.set_axis_labels("Model", "Mean Accuracy")
    g.set_titles("{col_name}")
    for ax in g.axes.flat:
        ax.grid(True)
        for label in ax.get_xticklabels():
            label.set_rotation(45)
    plt.tight_layout()
    plt.show()

    """
    Experiment II
    Making a plot showing how the error changes with the number of iterations/trees (for
    boosting, bagging, Random Forest, XGBoost).
    """
    max_iter = 20  # number of estimators
    plt.figure(figsize=(14, 8))

    X,y = datasets["breast_cancer"]
    X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=320575)

    dt = DecisionTreeClassifier(max_depth=3)
    dt.fit(X_train, y_train)
    dt_error = 1 - accuracy_score(y_test, dt.predict(X_test))
    plt.axhline(y=dt_error, color='gray', linestyle='--', label='Single DecisionTree')

    # Calculating and saving error for each model
    for name, model_func in models.items():
        test_errors = []
        model = model_func()  # model init
        
        if name == "DecisionTree":
            continue

        # label convertion for adaboost
        y_train_current = np.where(y_train == 0, -1, 1) if name == "AdaBoost" else y_train

        # xbboost special approach 
        if name == "XGBoost":
            for i in range(1, max_iter + 1):
                model.n_estimators = i
                model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=False)
                y_pred = model.predict(X_test)
                test_error = 1 - accuracy_score(y_test, y_pred)
                test_errors.append(test_error)
            plt.plot(range(1, max_iter + 1), test_errors, label=name, linewidth=2)
            continue

        # For other models
        for i in range(1, max_iter + 1):
            if name == "RandomForest":
                model.n_estimators = i
            elif name in ["AdaBoost", "Bagging"]:
                model.n_estimators = i
            
            model.fit(X_train, y_train_current)
            y_pred = model.predict(X_test)
            
            if name == "AdaBoost": y_pred = np.where(y_pred == -1, 0, 1)
            
            test_error = 1 - accuracy_score(y_test, y_pred)
            test_errors.append(test_error)
        
        plt.plot(range(1, max_iter + 1), test_errors, label=name, linewidth=2)

# Plotting Error vs. Number of Iterations/Trees
plt.title('Error vs. Number of Iterations/Trees', fontsize=16)
plt.xlabel('Number of Iterations/Trees', fontsize=14)
plt.ylabel('Test Error (1 - Accuracy)', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)
plt.xticks(range(1, max_iter+1))
plt.ylim(0, 0.5)
plt.tight_layout()
plt.show()
