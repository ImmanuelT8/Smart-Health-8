import numpy as np


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
        window = data[i:i + 3]
        mean_value = np.mean(window)
        smoothed_data.append(mean_value)

    return smoothed_data, remainder
