# -*- coding: latin-1 -*-

# data_manager.py

import os
import pandas as pd
import datetime

def create_or_update_excel_file(folder_path, filename, red_list, ir_list):
    """
    Erstellt oder aktualisiert eine Excel-Datei mit den gegebenen Red- und IR-Listen.
    
    :param folder_path: Der Pfad zum Ordner, in dem die Datei gespeichert werden soll.
    :param filename: Der Name der Datei.
    :param red_list: Die Liste der Red-Werte.
    :param ir_list: Die Liste der IR-Werte.
    """
    full_path = os.path.join(folder_path, filename)

    # Synchronisieren der Längen der Listen
    min_length = min(len(red_list), len(ir_list))
    red_list = red_list[:min_length]
    ir_list = ir_list[:min_length]

    # Neues DataFrame mit den neuen Daten erstellen
    df_new = pd.DataFrame({'Red': red_list, 'IR': ir_list})

    if os.path.exists(full_path):
        # Öffnen und Anhängen der neuen Daten, wenn die Datei bereits existiert
        df_existing = pd.read_excel(full_path)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_excel(full_path, index=False)
    else:
        # Erstellen und Speichern der Datei, wenn sie noch nicht existiert
        df_new.to_excel(full_path, index=False)

    print(f"Excel file {filename} updated")

def generate_timestamped_filename(folder_path):
    """
    Generiert einen Dateinamen mit Zeitstempel.
    
    :param folder_path: Der Pfad zum Ordner, in dem die Datei gespeichert werden soll.
    :return: Tuple (filename, full_path)
    """
    current_time = datetime.datetime.now()
    timestamp = current_time.strftime("%d-%m-%Y_%H-%M-%S")
    filename = f"{timestamp}.xlsx"
    full_path = os.path.join(folder_path, filename)
    return filename, full_path

def is_data_available(red_list, ir_list):
    """
    Prüft, ob Daten in beiden Listen vorhanden sind.
    
    :param red_list: Die Liste der Red-Werte.
    :param ir_list: Die Liste der IR-Werte.
    :return: Boolescher Wert, der angibt, ob Daten vorhanden sind.
    """
    return len(red_list) > 0 and len(ir_list) > 0
