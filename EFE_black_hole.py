import numpy as np
import matplotlib.pyplot as plt

# Physikalische Konstanten
G = 6.67430e-11  # m^3 kg^-1 s^-2
c = 3e8  # m/s
M = 1e30  # Masse in kg (z.B. Sonnenmasse)

# Schwarzschild-Radius
r_s = 2 * G * M / c**2

# Gitter für Raumlinie
r = np.linspace(r_s * 1.1, 10 * r_s, 200)
theta = np.linspace(0, 2*np.pi, 200)

# Visualisierung: Verzerrung der Raumzeit
X = r * np.cos(theta)
Y = r * np.sin(theta)

# Plot
plt.figure(figsize=(8,8))
plt.plot(X, Y, color='k')
plt.scatter(0, 0, color='red', label='Massenzentrum\nSchwarzschild-Radius')
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.title('Raumkrümmung um ein schwarzes Loch (Schwarzschild-Metrik)')
plt.legend()
plt.grid(True)
plt.axis('equal')
plt.show()
