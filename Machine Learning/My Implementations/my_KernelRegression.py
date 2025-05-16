import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline

def g(x):
    return 4.26 * (np.exp(-x) - 4 * np.exp(-2*x) + 3 * np.exp(-3*x))

class NadarayaWatsonRegressor:
    def __init__(self, kernel="gaussian", bandwidth=0.5):
        """
        kernel: ['gaussian', 'epanechnikov', 'uniform']
        badwith: float (parametr wygladzania)
        """
        self.kernel = kernel
        self.bandwidth = bandwidth
        self.x_train = None
        self.y_train = None
    
    def _compute_kernel(self, u):
        """ computes kernel for vector u """
        if self.kernel == "gaussian":
            return np.exp(-0.5 * u**2) / np.sqrt(2 * np.pi)
        elif self.kernel == "epanechnikov":
            return np.where(np.abs(u) <= 1, 0.75 * (1 - u**2), 0)
        elif self.kernel == "uniform":
            return np.where(np.abs(u) <= 1, 0.5, 0)
        else:
            raise ValueError("Nieznane jądro. Wybierz: 'gaussian', 'epanechnikov', 'uniform'.")
    
    def fit(self, x_train, y_train):
        self.x_train = np.array(x_train).reshape(-1)
        self.y_train = np.array(y_train).reshape(-1)
    
    def predict(self, x_test):
        x_test = np.array(x_test).reshape(-1)
        y_pred = np.zeros_like(x_test, dtype=float)

        for i, x in enumerate(x_test):
            u = (x - self.x_train) / self.bandwidth
            weights = self._compute_kernel(u)

            if np.sum(weights) == 0:
                y_pred[i] == np.mean(self.y_train)
            else:
                y_pred[i] = np.sum(weights * self.y_train) / np.sum(weights)
        
        return y_pred

if __name__ == "__main__":
    np.random.seed(320575)
    n_samples = 200
    x_train = np.random.uniform(0,4, n_samples)

    epsilon = np.random.normal(0,0.1,n_samples)
    y_train = g(x_train) + epsilon

    # Nadaraya-Watson kernel regression - Test
    nwr = NadarayaWatsonRegressor(kernel="gaussian", bandwidth=0.5)
    nwr.fit(x_train, y_train)

    x_test = np.linspace(0, 4, 200)
    y_nw = nwr.predict(x_test)

    sort_idx = np.argsort(x_train)
    x_sorted = x_train[sort_idx]
    y_sorted = y_train[sort_idx]
    spline = UnivariateSpline(x_sorted, y_sorted, s=0.99)
    y_spline = spline(x_test)
    
    # Nadaraya-Watson Plot
    plt.figure(figsize=(12, 6))
    plt.scatter(x_train, y_train, alpha=0.3, label='Noisy data')
    plt.plot(x_test, g(x_test), 'k--', label='True g(x)')
    plt.plot(x_test, y_nw, 'r-', label='Nadaraya-Watson (h=0.5)')
    plt.legend()
    plt.show()

    # Plot Smoothing spline
    plt.figure(figsize=(12, 6))
    plt.scatter(x_train, y_train, alpha=0.3, label='Noisy data')
    plt.plot(x_test, g(x_test), 'k--', label='True g(x)')
    plt.plot(x_test, y_spline, 'b-', label='Smoothing Spline (λ=0.1)')
    plt.ylim(-1.5,1)
    plt.legend()
    plt.show()

    print("MSE g - spline: ", np.mean(g(x_test)-y_spline) / n_samples)
    print("MSE g - Nadaraya-Watson: ", np.mean(g(x_test)-y_nw)/ n_samples)

    # MSE for different n samples
    sample_sizes = np.arange(50, 1001, 50)  
    mse_nw = []
    mse_spline = []

    for n in sample_sizes:
        x_train = np.random.uniform(0, 4, n)
        epsilon = np.random.normal(0, 0.1, n)
        y_train = g(x_train) + epsilon
        
        x_test = np.linspace(0, 4, 200)
        
        # Nadaraya-Watson
        nwr = NadarayaWatsonRegressor(kernel="gaussian", bandwidth=0.5)
        nwr.fit(x_train, y_train)
        y_nw = nwr.predict(x_test)
        
        # Smoothing Spline
        sort_idx = np.argsort(x_train)
        spline = UnivariateSpline(x_train[sort_idx], y_train[sort_idx], s=0.99)
        y_spline = spline(x_test)
        
        # Calculate MSE
        mse_nw.append(np.mean((g(x_test) - y_nw)**2) / n)
        mse_spline.append(np.mean((g(x_test) - y_spline)**2) / n)

    # Plot results
    plt.figure(figsize=(10, 6))
    plt.plot(sample_sizes, mse_nw, 'r-', label='Nadaraya-Watson (h=0.5)')
    plt.xlabel('Sample Size (n)')
    plt.ylabel('Mean Squared Error (MSE)')
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(sample_sizes, mse_spline, 'b-', label='Smoothing Spline (s=0.99)')
    plt.xlabel('Sample Size (n)')
    plt.ylabel('Mean Squared Error (MSE)')
    plt.legend()
    plt.grid(True)
    plt.show()
