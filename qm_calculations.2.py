import numpy as np
import matplotlib.pyplot as plt


def infinite_potential_well(x, L):
    """Wellenfunktion für Teilchen im unendlich hohen Potentialtopf."""
    psi = np.zeros_like(x)
    for i, xi in enumerate(x):
        if 0 < xi < L:
            psi[i] = 1 / np.sqrt(L)
    return psi


x = np.linspace(0, 1, 100)
psi = infinite_potential_well(x, 1)
plt.plot(x, np.abs(psi)**2)
plt.xlabel('Position')
plt.ylabel('Wahrscheinlichkeitsdichte')
plt.title('Wellenfunktion im unendlich hohen Potentialtopf')
plt.show()
