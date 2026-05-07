import numpy as np
import matplotlib.pyplot as plt

# Physikalische Konstanten
h = 6.62607015e-34  # Planck-Konstante (J·s)
hbar = h / (2 * np.pi)  # Reduzierte Planck-Konstante
m_e = 9.1093837015e-31  # Elektronenmasse (kg)
c = 299792458  # Lichtgeschwindigkeit (m/s)
e = 1.602176634e-19  # Elementarladung (C)

def energie_photon(wellenlaenge):
    """
    Berechnet die Energie eines Photons bei gegebener Wellenlänge.
    
    Parameter:
    wellenlaenge: Wellenlänge in Metern
    
    Rückgabe:
    Energie in Joule
    """
    return h * c / wellenlaenge

def de_broglie_wellenlaenge(masse, geschwindigkeit):
    """
    Berechnet die de Broglie-Wellenlänge eines Teilchens.
    
    Parameter:
    masse: Masse des Teilchens in kg
    geschwindigkeit: Geschwindigkeit in m/s
    
    Rückgabe:
    Wellenlänge in Metern
    """
    impuls = masse * geschwindigkeit
    return h / impuls

def energie_teilchen_im_kasten(n, L, masse):
    """
    Berechnet die Energie eines Teilchens im eindimensionalen Potentialkasten.
    
    Parameter:
    n: Quantenzahl (n = 1, 2, 3, ...)
    L: Länge des Kastens in Metern
    masse: Masse des Teilchens in kg
    
    Rückgabe:
    Energie in Joule
    """
    return (n**2 * h**2) / (8 * masse * L**2)

def wellenfunktion_teilchen_im_kasten(x, n, L):
    """
    Berechnet die Wellenfunktion eines Teilchens im eindimensionalen Potentialkasten.
    
    Parameter:
    x: Position(en) in Metern (kann Array sein)
    n: Quantenzahl (n = 1, 2, 3, ...)
    L: Länge des Kastens in Metern
    
    Rückgabe:
    Wert der Wellenfunktion bei x
    """
    return np.sqrt(2/L) * np.sin(n * np.pi * x / L)

def visualisiere_teilchen_im_kasten(L=1e-9, n_max=3):
    """
    Visualisiert die Wellenfunktionen eines Teilchens im Potentialkasten.
    
    Parameter:
    L: Länge des Kastens in Metern (Standard: 1 nm)
    n_max: Maximale Quantenzahl zur Visualisierung
    """
    x = np.linspace(0, L, 1000)
    
    plt.figure(figsize=(10, 6))
    for n in range(1, n_max + 1):
        psi = wellenfunktion_teilchen_im_kasten(x, n, L)
        plt.plot(x * 1e9, psi * np.sqrt(1e-9), label=f'n = {n}')
    
    plt.xlabel('Position (nm)')
    plt.ylabel('Wellenfunktion ψ(x)')
    plt.title('Wellenfunktionen eines Teilchens im Potentialkasten')
    plt.legend()
    plt.grid(True)
    plt.show()

def heisenberg_unschaerfe(delta_x):
    """
    Berechnet die minimale Impulsunschärfe nach der Heisenberg'schen Unschärferelation.
    
    Parameter:
    delta_x: Ortsunschärfe in Metern
    
    Rückgabe:
    Minimale Impulsunschärfe in kg·m/s
    """
    return hbar / (2 * delta_x)

def bohr_radius(n=1):
    """
    Berechnet den Bohr'schen Radius für das Wasserstoffatom.
    
    Parameter:
    n: Hauptquantenzahl (Standard: 1 für Grundzustand)
    
    Rückgabe:
    Radius in Metern
    """
    epsilon_0 = 8.8541878128e-12  # Elektrische Feldkonstante (F/m)
    return (4 * np.pi * epsilon_0 * hbar**2 * n**2) / (m_e * e**2)

def energie_wasserstoff(n=1):
    """
    Berechnet die Energie eines Elektrons im Wasserstoffatom.
    
    Parameter:
    n: Hauptquantenzahl (Standard: 1 für Grundzustand)
    
    Rückgabe:
    Energie in Joule (negativ gebunden)
    """
    epsilon_0 = 8.8541878128e-12  # Elektrische Feldkonstante (F/m)
    return -(m_e * e**4) / (8 * epsilon_0**2 * h**2 * n**2)

if __name__ == '__main__':
    print("=== Quantenmechanische Berechnungen ===\n")
    
    # Beispiel 1: Photonenenergie
    wellenlaenge = 500e-9  # 500 nm (grünes Licht)
    E_photon = energie_photon(wellenlaenge)
    print(f"Energie eines Photons (λ = 500 nm): {E_photon:.3e} J = {E_photon/e:.2f} eV")
    
    # Beispiel 2: de Broglie-Wellenlänge eines Elektrons
    v_elektron = 1e6  # 1 Mm/s
    lambda_db = de_broglie_wellenlaenge(m_e, v_elektron)
    print(f"\nde Broglie-Wellenlänge eines Elektrons (v = {v_elektron:.0e} m/s): {lambda_db:.3e} m")
    
    # Beispiel 3: Teilchen im Potentialkasten
    L = 1e-9  # 1 nm Kasten
    n = 1
    E_kasten = energie_teilchen_im_kasten(n, L, m_e)
    print(f"\nEnergie im Potentialkasten (L = 1 nm, n = {n}): {E_kasten:.3e} J = {E_kasten/e:.2f} eV")
    
    # Beispiel 4: Heisenberg-Unschärferelation
    delta_x = 1e-10  # 0.1 nm
    delta_p = heisenberg_unschaerfe(delta_x)
    print(f"\nHeisenberg-Unschärfe (Δx = 0.1 nm): Δp ≥ {delta_p:.3e} kg·m/s")
    
    # Beispiel 5: Wasserstoffatom
    r_bohr = bohr_radius(1)
    E_H = energie_wasserstoff(1)
    print(f"\nBohr'scher Radius (n = 1): {r_bohr:.3e} m")
    print(f"Grundzustandsenergie Wasserstoff: {E_H:.3e} J = {E_H/e:.2f} eV")
    
    # Visualisierung der Wellenfunktionen
    print("\nVisualisierung wird erstellt...")
    visualisiere_teilchen_im_kasten(L=1e-9, n_max=3)
