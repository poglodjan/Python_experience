import numpy as np
from matplotlib import pyplot as plt

def eksponencjalna(x, a=1):
    return np.exp(a * x)

def logarytm_naturalny(x):
    return np.log(x)

def hiperbola(x, a=1, b=1):
    return a / x + b

theta = np.linspace(0, 2 * np.pi, 100)
x = 16 * (np.sin(theta) ** 3)
y = 13 * np.cos(theta) - 5 * np.cos(2 * theta) - 2 * np.cos(3 * theta) - np.cos(4 * theta)

plt.plot(x, y, label='Funkcja pierwotna')

x_exp = np.linspace(0.1, 16, 100)
plt.plot(x_exp, eksponencjalna(x_exp), label='Eksponencjalna')

x_ln = np.linspace(0.1, 16, 100)
plt.plot(x_ln, logarytm_naturalny(x_ln), label='Logarytm naturalny')

x_hiperbola = np.linspace(0.1, 16, 100)
plt.plot(x_hiperbola, hiperbola(x_hiperbola), label='Hiperbola')

plt.title('Wizualizacja różnych funkcji')
plt.legend()
plt.show()
