import cupy as cp
import numpy as np
import time
import matplotlib.pyplot as plt

# Funktion: z.B. Potenzialberechnung auf GPU
def compute_potential_on_gpu(grid_x, grid_y, mass_density, a, b):
    # Erzeuge auf GPU
    X_gpu = cp.asarray(grid_x)
    Y_gpu = cp.asarray(grid_y)
    # Beispiel: Newtonsche Potentialberechnung (vereinfachte Annäherung)
    r = cp.sqrt(X_gpu**2 + Y_gpu**2 + 1e-5)  # Vermeide Division durch Null
    G = 6.67430e-11
    M = mass_density  # hier als Konstanten-Dichte, ggf. anpassen
    potential = -G * M / r
    return potential

# Beispielhafte Simulation
if __name__ == "__main__":
    # Gitter definieren
    size = 500
    a, b = 10, 8  # Halbachsen
    x = np.linspace(-a * 1.2, a * 1.2, size)
    y = np.linspace(-b * 1.2, b * 1.2, size)
    X, Y = np.meshgrid(x, y)

    # Konstanten
    mass_density = 1e12  # Beispiel für Massendichte
    start_time = time.time()

    # Potential auf GPU berechnen
    potential = compute_potential_on_gpu(X, Y, mass_density, a, b)

    duration = time.time() - start_time
    print(f"Potentialberechnung auf GPU in {duration:.4f} Sekunden")

    # Visualisierung
    plt.imshow(cp.asnumpy(potential), extent=(-a*1.2, a*1.2, -b*1.2, b*1.2))
    plt.colorbar(label='Potential')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Vereinfachte Potentialsimulation (GPU)')
    plt.show()
