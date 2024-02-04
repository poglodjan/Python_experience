import matplotlib.pyplot as plt

counts, bins, ignored  = plt.hist(MC_beta_hats, 20, density = True, color = 'purple', label = 'MC sampling beta')
plt.title("Monte Carlo Simulation for LR beta estimate M = 10000")
plt.axvline(beta, 0,40, color = 'y', label = 'Population beta')
plt.xlabel("beta")
plt.ylabel("Probability")
plt.legend()
plt.show()
