import numpy as np
from filter_modul import smooth_data
import time

def generate_random_data(size):
    return np.random.rand(size)

def main():
    previous_remainder = None  # Initialisierung des previous_remainder
    while True:
        # Erzeugung von Dummy-Daten
        dummy_data = generate_random_data(100)
        raw_data_count = len(dummy_data)  # Anzahl der Rohdaten
        print("Rohdaten:", dummy_data)

        # Glättung der Dummy-Daten mit dem Modul
        smoothed_data, remainder = smooth_data(dummy_data, previous_remainder)

        print("Rohdaten  | Geglättete Daten")
        for raw, smoothed in zip(dummy_data, smoothed_data):
            print(f"{raw:.4f} | {smoothed:.4f}")

        # Separate Schleife, um übrig gebliebene Rohdaten zu drucken
        if len(smoothed_data) < len(dummy_data):
            for raw in dummy_data[len(smoothed_data):]:
                print(f"{raw:.4f} | ")

        print("Anzahl der Rohdatenausgaben:", raw_data_count)

        # Ausgabe des remainder
        print(f"Rest: {remainder[0]:.4f}, {remainder[1]:.4f}")

        time.sleep(4)  # Eine Sekunde warten, bevor neue Daten erzeugt werden
        previous_remainder = remainder  # Aktualisierung des previous_remainder

if __name__ == "__main__":
    main()
