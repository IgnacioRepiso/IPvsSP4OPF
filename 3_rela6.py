import numpy as np
import matplotlib.pyplot as plt

t = np.arange(0.01, 11)

lambda1 = 2 * t
lambda2 = 2 * t**0.5

plt.figure(figsize=(8, 5))
plt.plot(t, lambda1, marker='o', label=r'$\lambda(t) = 2t$')
plt.plot(t, lambda2, marker='s', label=r'$\lambda(t) = 2t^{1/2}$')

plt.xticks(t)
plt.xlabel('t')
plt.ylabel(r'$\lambda(t)$')
plt.title(r'$\lambda(t) = 2t$ vs $\lambda(t) = 2t^{1/2}$')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
