import numpy as np
import time

def smooth_data(data, previous_remainder=None):
    """
    Glättet eine Sequenz von Datenpunkten, indem für jedes Fenster von drei aufeinanderfolgenden Datenpunkten der Mittelwert berechnet wird.

    Parameter:
    - data: Eine Sequenz von Datenpunkten, die geglättet werden sollen.
    - previous_remainder: Die letzten beiden Datenpunkte des vorherigen Arrays, die in das aktuelle Array integriert werden sollen.

    Rückgabewerte:
    - smoothed_data: Eine Liste mit den geglätteten Daten.
    - remainder: Die letzten beiden Datenpunkte des verarbeiteten Arrays, die für den nächsten Durchlauf verwendet werden sollen.
    """
    if previous_remainder is not None:
        data = np.concatenate((previous_remainder, data))
    
    smoothed_data = []
    remainder = data[-2:]
    
    for i in range(len(data) - 2):
        window = data[i:i+3]
        mean_value = np.mean(window)
        smoothed_data.append(mean_value)
    
    return smoothed_data, remainder

# Initialisierung
previous_remainder = None
last_data = None
time_window = 3.0  # Zeitfenster in Sekunden
Sensordaten_last = None  # Vorherige Sensordaten initialisieren

# Endlosschleife für die kontinuierliche Datenverarbeitung
while True:
    # Hier prüfen wir auf neue Sensordaten (ersetze dies mit deiner eigenen Logik)
    Sensordaten_aktuell = np.random.rand(100)  # Beispiel: Neue Sensordaten mit 100 Zufallswerten
    
    # Überprüfen, ob neue Sensordaten vorliegen und das Zeitfenster überschritten wurde
    current_time = time.time()
    if Sensordaten_aktuell is not None and Sensordaten_last is not None and not np.array_equal(Sensordaten_last, Sensordaten_aktuell):
        if last_data is not None and current_time - last_data > time_window:
            previous_remainder = None  # Verwerfe vorherige Reste, wenn das Zeitfenster überschritten wird
        
        # Glätten und verarbeiten der neuen Daten
        print("Geglättete Sensordaten:", smooth_data(Sensordaten_aktuell, previous_remainder))
        
        # Aktualisiere den letzten Datenzeitpunkt und die verbleibenden Daten
        last_data = current_time
        previous_remainder = remainder
        Sensordaten_last = Sensordaten_aktuell
    
    # Simuliere eine Zeitverzögerung zwischen den Datenankünften
    time.sleep(0.5)  # Beispiel: 0.5 Sekunden Pause zwischen den Datenankünften
