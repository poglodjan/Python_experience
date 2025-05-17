import numpy as np
import pandas as pd
from boruta import BorutaPy
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from scipy.stats import chi2

def generate_dataset1(n, p, k):
    X = np.random.normal(0, 1, size=(n, p))
    chi2_median = chi2.ppf(0.5, df=k)

    # Calculate the sum of squares of the first k featrures for each sample
    sum_of_squares = np.sum(X[:, :k]**2, axis=1)
    y = (sum_of_squares > chi2_median).astype(int)
    return X, y

def generate_dataset2(n, p, k):
    X = np.random.normal(0, 1, size=(n, p))
    sum_abs = np.sum(np.abs(X[:, :k]), axis=1)
    y = (sum_abs > k).astype(int)
    return X, y

### --- Random Forest Feature Selection ---
def run_rf_importance(X, y, feature_names, title, k, plot=True):
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X, y)
    mdi_importances = rf.feature_importances_
    indices = np.argsort(mdi_importances)[::-1]

    if plot==True:
        plt.figure(figsize=(10, 6))
        plt.bar(range(len(mdi_importances)), 
                mdi_importances[indices], align="center")
        plt.xticks(range(len(mdi_importances)), 
                [feature_names[i] for i in indices], rotation=90)
        plt.title(title)
        plt.xlabel("Feature")
        plt.ylabel("Importance")
        plt.tight_layout()
        plt.show()

    ranked_features = np.argsort(mdi_importances)[::-1] 
    return [idx for idx in ranked_features[:k]]

### --- Boruta Feature Selection ---
def run_boruta(X, y, feature_names, title, k=5, plot=True):
    rf = RandomForestClassifier(n_estimators=100, random_state=1, max_depth=5)

    boruta = BorutaPy(
        estimator=rf,
        n_estimators="auto",
        max_iter=50,
        random_state=1,
        verbose=0
    )

    boruta.fit(X, y)
    selected = boruta.support_
    ranked_features = boruta.ranking_
    print(f"\n {title} - Boruta Results:")
    print(pd.DataFrame({
        "Feature": feature_names,
        "Selected": selected,
        "Ranking": ranked_features,
    }))

    # Plot feature ranking
    if plot==True:
        plt.figure(figsize=(10, 6))
        plt.bar(feature_names, ranked_features, color=[('green' if s else 'red') for s in selected])
        plt.xticks(rotation=90)
        plt.title(f"Boruta Feature Ranking - {title}")
        plt.xlabel("Features")
        plt.ylabel("Ranking (Lower = Better)")
        plt.grid(axis='y', linestyle='--')
        plt.show()
    
    return np.argsort(ranked_features)[:k]


# _____ main _______

if __name__ == "__main__":
    # a) - b) Try different values of n, p and k. 
    n = [500,1000]  # number of samples
    p = [20,50]    # total number of features
    k = [5,10]     # number of significant features

    for ni in n:
        for pi in p:
            for ki in k:
                print(f"\n___ Experiment for n={ni}, k={ki}, p={pi}\n __")
                X1, y1 = generate_dataset1(ni, pi, ki)
                X2, y2 = generate_dataset2(ni, pi, ki)

                feature_names = [f"X{i+1}" for i in range(pi)]
                _ = run_boruta(X1, y1, feature_names, "Dataset 1 - boruta", ki, plot=True)
                _ = run_boruta(X2, y2, feature_names, "Dataset 2 - boruto", ki, plot=False) # if show a plot then change to true
                _ = run_rf_importance(X1, y1, feature_names, "Dataset 1 - RF", ki, plot=True)
                _ = run_rf_importance(X2, y2, feature_names, "Dataset 2 - RF", ki, plot=False)

    # c) estimation on the probabilities of correct ordering L=25 experiments
    L = 25
    results_boruta_d1 = []
    results_boruta_d2 = []
    results_rf_d1 = []
    results_rf_d2 = []

    for ex in range(L):
        X1, y1 = generate_dataset1(n[0], p[0], k[0])
        X2, y2 = generate_dataset2(n[0], p[0], k[0])
        feature_names = [f"X{i+1}" for i in range(p[0])]

        # Run Boruta on Dataset 1 and Dataset 2
        boruta_ranking_d1 = run_boruta(X1, y1, feature_names, title="Dataset 1", k=k[0], plot=False)
        boruta_ranking_d2 = run_boruta(X2, y2, feature_names, title="Dataset 2", k=k[0], plot=False)
        
        # Run RF importance on Dataset 1 and Dataset 2
        rf_top_d1 = run_rf_importance(X1, y1, feature_names, title="Dataset 1", k=k[0], plot=False)
        rf_top_d2 = run_rf_importance(X2, y2, feature_names, title="Dataset 2", k=k[0], plot=False)
        
        correct_boruta_d1 = all(feat_idx < k[0] for feat_idx in boruta_ranking_d1)
        correct_boruta_d2 = all(feat_idx < k[0] for feat_idx in boruta_ranking_d1)
        correct_rf_d1 = all(feat_idx < k[0] for feat_idx in rf_top_d1)
        correct_rf_d2 = all(feat_idx < k[0] for feat_idx in rf_top_d1)

        # Store results
        results_boruta_d1.append(correct_boruta_d1)
        results_boruta_d2.append(correct_boruta_d2)
        results_rf_d1.append(rf_top_d1)
        results_rf_d2.append(rf_top_d2)

    prob_boruta_d1 = np.mean(results_boruta_d1)
    prob_boruta_d2 = np.mean(results_boruta_d2)
    prob_rf_d1 = np.mean(results_rf_d1)
    prob_rf_d2 = np.mean(results_rf_d2)

    print("\c) Probability of Correct Ordering (Top k features):")
    print(f"Boruta (Dataset 1): {prob_boruta_d1:.2%}")
    print(f"Boruta (Dataset 2): {prob_boruta_d2:.2%}")
    print(f"RF Importance (Dataset 1): {prob_rf_d1:.2%}")
    print(f"RF Importance (Dataset 2): {prob_rf_d2:.2%}")

    # d) Experiment with t - number of top-ranked features

    def get_boruta_features(X, y):
        rf = RandomForestClassifier(n_estimators=100, max_depth=5, random_state=1)
        boruta = BorutaPy(estimator=rf, n_estimators='auto', max_iter=50, random_state=1, verbose=0)
        boruta.fit(X, y)
        return np.argsort(boruta.ranking_)
    
    def get_rf_features(X, y):
        rf = RandomForestClassifier(n_estimators=100, random_state=42)
        rf.fit(X, y)
        return np.argsort(rf.feature_importances_)[::-1]

    def evaluate_accuracy(X_train, X_test, y_train, y_test, features, t_values):
        accuracies = []
        for t in t_values:
            selected = features[:t]
            rf = RandomForestClassifier(n_estimators=100, random_state=1)
            rf.fit(X_train[:, selected], y_train)
            y_pred = rf.predict(X_test[:, selected])
            acc = accuracy_score(y_test, y_pred)
            accuracies.append(acc)
        return accuracies
    
    n = 200
    p = 500
    k = 20
    t_values = [5, 10, 15, 20, 50, 100, 200, 300, 400, 500]  # number of top features to test

    X1, y1 = generate_dataset1(n, p, k)
    X2, y2 = generate_dataset2(n, p, k)

    X1_train, X1_test, y1_train, y1_test = train_test_split(X1, y1, test_size=0.3, random_state=1)
    X2_train, X2_test, y2_train, y2_test = train_test_split(X2, y2, test_size=0.3, random_state=1)

    boruta_features_d1 = get_boruta_features(X1_train, y1_train)
    boruta_features_d2 = get_boruta_features(X2_train, y2_train)
    rf_features_d1 = get_rf_features(X1_train, y1_train)
    rf_features_d2 = get_rf_features(X2_train, y2_train)

    acc_boruta_d1 = evaluate_accuracy(X1_train, X1_test, y1_train, y1_test, boruta_features_d1, t_values)
    acc_boruta_d2 = evaluate_accuracy(X2_train, X2_test, y2_train, y2_test, boruta_features_d2, t_values)
    acc_rf_d1 = evaluate_accuracy(X1_train, X1_test, y1_train, y1_test, rf_features_d1, t_values)
    acc_rf_d2 = evaluate_accuracy(X2_train, X2_test, y2_train, y2_test, rf_features_d2, t_values)

    plt.figure(figsize=(12, 8))
    plt.plot(t_values, acc_boruta_d1, 'o-', label='Boruta (Dataset 1)')
    plt.plot(t_values, acc_boruta_d2, 'o-', label='Boruta (Dataset 2)')
    plt.plot(t_values, acc_rf_d1, 'o-', label='RF Importance (Dataset 1)')
    plt.plot(t_values, acc_rf_d2, 'o-', label='RF Importance (Dataset 2)')
    plt.axvline(x=k, color='gray', linestyle='--', label='True number of features (k=20)')
    plt.xscale('log')
    plt.xlabel('Number of top features used (t)')
    plt.ylabel('Classification accuracy')
    plt.title('Accuracy vs Number of Top Features Used\n(n=200, p=500, k=20)')
    plt.legend()
    plt.grid(True, which="both", ls="-")
    plt.show()
