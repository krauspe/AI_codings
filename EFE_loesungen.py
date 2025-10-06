import numpy as np
import matplotlib.pyplot as plt

# Parameter der ellipsoidalen Masseverteilung
a = 5  # Halbachse in x-Richtung
b = 3  # Halbachse in y-Richtung
mass = 1e5  # Gesamtmasse

# Rastergrid für die Visualisierung
nx, ny = 100, 100
x = np.linspace(-a*1.5, a*1.5, nx)
y = np.linspace(-b*1.5, b*1.5, ny)
X, Y = np.meshgrid(x, y)

# Funktion, um den Gravitationspotenzial im Newtonschen Sinne zu approximieren
def gravitational_potential(x, y, a, b, M):
    # Position in Ellipsoidkoordinaten transformieren
    # Annahme: Massenverteilung im Ellipsoid
    # Für eine vereinfachte Annäherung verwenden wir eine homogene Ellipsoidmasse
    # - Berechnung des Abstandes von jedem Punkt zum Mittelpunkt
    r = np.sqrt(x**2 + y**2)
    # Annahme: Potential proportional zu M/r (Newtonischer Ansatz)
    # Ligth: Für Punkte außerhalb des Ellipsoids
    # erfolgt eine Approximation, da das echte Potential komplexer ist
    potential = -G * M / (r + 1e-5)
    return potential

# Gravitationskonstante
G = 6.67430e-11  # m^3 kg^-1 s^-2

# Potential berechnen
phi = gravitational_potential(X, Y, a, b, mass)

# Visualisierung
plt.contourf(X, Y, phi, levels=50, cmap='viridis')
plt.colorbar(label='Potenzial (m^2/s^2)')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Vereinfachtes gravitationspotential einer ellipsoiden Masseverteilung')
plt.show()
