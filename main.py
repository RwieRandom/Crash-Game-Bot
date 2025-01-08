import ctypes
import pyautogui
from PIL import ImageGrab
import time
from threading import Thread
import tkinter as tk
import datetime
import os
import json

# >>> DPI-AWARENESS aktivieren (nur Windows, hilft bei Skalierungsproblemen) <<<.
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(2)  # 2 = PROCESS_PER_MONITOR_DPI_AWARE
except Exception as e:
    print(f"SetProcessDpiAwareness fehlgeschlagen: {e}")
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception as e2:
        print(f"SetProcessDPIAware fehlgeschlagen: {e2}")
# -----------------------------------------------
# >>> Standard-Startwerte
Input_Einsatz = (801, 900)
INPUT_CASHOUT = (944, 900)
BTN_Confirm = (1138, 923)
Box_Green_Cashout = ((1465, 327), (1541, 342))
Box_Red_Score = ((1127, 525), (1333, 580))
Box_Next_Round = ((1167, 513), (1206, 521))
GREEN = (27, 205, 73)
RED = (226, 30, 77)
GOLD = (254, 182, 42)
START_NUMBER = 0.01

WIN_MULTIPLIER = 2.1
stop_flag = False
start_time = None


# Stats
CURRENT_BALANCE = 20.23
ROUNDS_PLAYED = 0
TOTAL_GAMES_WON = 0
TOTAL_GAMES_LOST = 0
BET = 0

def input_number(number):
    """Automatische Eingabe der Zahl an der definierten Position und Abziehen des Einsatzes."""
    global CURRENT_BALANCE  # Zugriff auf die globale Balance
    try:

        if number > 4 * CURRENT_BALANCE:
            message(f"Einsatz {number} ist mehr als das 4-fache der Balance {CURRENT_BALANCE}.")
            
            message("Lade Chrome-Seite neu....")
            pyautogui.hotkey('ctrl', 'r')
            root.after(30000, restart_program)
            return


        # Abziehen des Einsatzes von der Balance
        CURRENT_BALANCE -= number
        message(f"Einsatz von {number} abgezogen. Neuer Kontostand: {CURRENT_BALANCE}")
        # Gewohnte Eingabe-Prozedur
        message(f"Versuche, Zahl {number} an Position {Input_Einsatz} einzugeben.")  # DEBUG
        pyautogui.click(Input_Einsatz)
        time.sleep(0.1)
        message("Hotkey: Strg + A")  # DEBUG
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        message(f"Gebe nun die Zahl ein: {number}")  # DEBUG
        pyautogui.typewrite(str(number), interval=0.1)
        message(f"Bestätige mit Klick auf: {BTN_Confirm}")  # DEBUG
        pyautogui.click(BTN_Confirm)
    except Exception as e:
        message(f"Fehler beim Eingeben der Zahl: {e}")
        stop_program()

def check_color_in_box(box, colors):
    """Überprüfen, ob eine der angegebenen Farben im gegebenen Bereich vorhanden ist."""
    try:
        screen = ImageGrab.grab(bbox=(box[0][0], box[0][1], box[1][0], box[1][1]))
        color_counts = screen.getcolors(screen.size[0] * screen.size[1])
        found_color = False
        for count, color in color_counts:
            if color in colors:
                found_color = True
                break
        return found_color
    except Exception as e:
        message(f"Fehler bei der Farberkennung: {e}")
        return False

def process_color_detection():
    """Überwacht kontinuierlich die Farben und führt entsprechende Aktionen durch."""
    global stop_flag
    global CURRENT_BALANCE
    global WIN_MULTIPLIER
    global ROUNDS_PLAYED, TOTAL_GAMES_WON, TOTAL_GAMES_LOST, BET
    number = START_NUMBER
    gold_detected = False

    while not stop_flag:
        if check_color_in_box(Box_Next_Round, [GOLD]) and not gold_detected:
            gold_detected = True
            ROUNDS_PLAYED += 1
            message("Neue Runde erkannt (Gold) -> Überprüfung auf rot/grün beginnt...")
            save_to_stats()
            time.sleep(1)
        if gold_detected:
            message("Suche nach Rot oder Grün im definierten Bereich...")
            if check_color_in_box(Box_Red_Score, [RED]):
                # --- Verlust-Logik ---
                message("Rote Farbe erkannt! -> Einsatz verloren.")
                number *= 2
                TOTAL_GAMES_LOST += 1
                BET = number
                message(f"Aktueller Einsatz (verdoppelt): {number}")
                # Nächsten Einsatz eingeben
                input_number(number)
                gold_detected = False
                save_to_stats()
                save_to_history()
                time.sleep(1)
            elif check_color_in_box(Box_Green_Cashout, [GREEN]):
                # --- Gewinn-Logik ---
                message("Grüne Farbe erkannt! -> Einsatz gewonnen.")
                # Gewinn hinzufügen (Einsatz * Multiplikator)
                gewinn = number * WIN_MULTIPLIER
                CURRENT_BALANCE += gewinn
                TOTAL_GAMES_WON += 1
                message(f"Gewinn von {gewinn} hinzugefügt. Neuer Kontostand: {CURRENT_BALANCE}")
                
                number = START_NUMBER
                BET = number
                message(f"Aktueller Einsatz (zurückgesetzt): {number}")
                # Nächsten Einsatz eingeben
                input_number(number)
                gold_detected = False
                save_to_stats()
                save_to_history()
                time.sleep(1)
        time.sleep(0.5)

def restart_program():
    """
    Stoppt zunächst das laufende Programm und startet es nach kurzer Wartezeit erneut.
    So ist ein 'echter' Neustart innerhalb derselben GUI-Sitzung möglich.
    """
    stop_program()
    time.sleep(2)
    start_program()

def update_mouse_position():
    """Aktualisiert die Mausposition in den Entry-Feldern."""
    x, y = pyautogui.position()
    x_pos.set(f"{x}")
    y_pos.set(f"{y}")

def on_key_press(event):
    """Reagiert auf Tastendruck, um die Mausposition zu aktualisieren."""
    if event.char.lower() == 'r':
        message("R-Taste erkannt. Mausposition wird aktualisiert.")
        update_mouse_position()

def start_program():
    """Startet das Programm, wenn es nicht bereits läuft."""
    global stop_flag, Input_Einsatz, BTN_Confirm, INPUT_CASHOUT
    global Box_Green_Cashout, Box_Red_Score, Box_Next_Round, START_NUMBER
    global CURRENT_BALANCE
    global WIN_MULTIPLIER  # <-- Falls wir ihn aus dem GUI lesen wollen
    global multiplier_input_pos

    stop_flag = False
    global start_time
    start_time = time.time()
    text_widget.delete(1.0, tk.END)
    message("Programm gestartet...")
    time.sleep(0.2)
    start_button.pack_forget()
    stop_button.pack(side=tk.RIGHT, padx=10, pady=10)

    # Koordinaten und Start-Parameter aus den Eingabefeldern holen
    try:
        Input_Einsatz = (int(input_einsatz_x.get()), int(input_einsatz_y.get()))
        BTN_Confirm = (int(btn_confirm_x.get()), int(btn_confirm_y.get()))
        Box_Green_Cashout = ((int(green_x1.get()), int(green_y1.get())), (int(green_x2.get()), int(green_y2.get())))
        Box_Red_Score = ((int(red_x1.get()), int(red_y1.get())), (int(red_x2.get()), int(red_y2.get())))
        Box_Next_Round = ((int(next_x1.get()), int(next_y1.get())), (int(next_x2.get()), int(next_y2.get())))
        START_NUMBER = float(start_number_entry.get())
        WIN_MULTIPLIER = float(multiplier_entry.get())
        INPUT_CASHOUT = (int(multiplier_input_x.get()), int(multiplier_input_y.get()))

        multiplier_input_pos = (int(multiplier_input_x.get()), int(multiplier_input_y.get()))

        start_money = float(start_money_entry.get())

        if abs(start_money) < 1e-6:
            stats = read_stats()
            CURRENT_BALANCE = stats.get("CURRENT_BALANCE")
            if CURRENT_BALANCE is not None:
                message(f"Statistik geladen: CURRENT_BALANCE {CURRENT_BALANCE}")
            else:
                message("Fehler: CURRENT_BALANCE nicht gefunden in den Statistiken.")
        else:
            try:
                CURRENT_BALANCE = float(start_money_entry.get())
                message(f"CURRENT_BALANCE nicht geladen: {CURRENT_BALANCE}")
            except ValueError:
                message("Fehler: Ungültiger Wert für start_money_entry.")

    except ValueError as ve:
        message(f"Eingabefehler: {ve}")
        stop_program()
        return

    # --- NEU: Automatische Eingabe des Win Multipliers ---
    try:
        pyautogui.click(INPUT_CASHOUT)
        time.sleep(0.1)
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.typewrite(str(WIN_MULTIPLIER), interval=0.1)
        message(f"Cashout {WIN_MULTIPLIER} wurde eingegeben.")
    except Exception as e:
        message(f"Fehler bei der automatischen Eingabe des Cashout: {e}")
        stop_program()
        return

    # Ersten Einsatz eingeben
    message("Bet wird eingegeben...")  # DEBUG
    input_number(START_NUMBER)
    # Thread starten, der permanent die Farberkennung durchführt
    Thread(target=process_color_detection, daemon=True).start()

def stop_program():
    """Stoppt das Programm."""
    global stop_flag
    stop_flag = True
    end_time = time.time()
    elapsed_time = end_time - start_time
    hours = int(elapsed_time // 3600)
    minutes = int((elapsed_time % 3600) // 60)
    seconds = int(elapsed_time % 60)
    message("Programm wird gestoppt...")
    time.sleep(0.5)
    message("Programm beendet")
    message(f"Das Spiel lief für {hours} Stunden, {minutes} Minuten und {seconds} Sekunden.")
    start_button.pack(side=tk.LEFT, padx=10, pady=10)
    stop_button.pack_forget()

def message(msg):
    """Funktion zum Schreiben von Nachrichten in das Text-Widget."""
    print(msg) 
    save_log_entry(msg)
    if text_widget:
        text_widget.insert(tk.END, msg + "\n")
        text_widget.yview(tk.END)


def get_last_log_message(log_file_path):
    """Liest die Nachricht der letzten Zeile der Log-Datei."""
    if not os.path.exists(log_file_path):
        return None
    with open(log_file_path, 'rb') as f:
        try:
            f.seek(-2, os.SEEK_END)
            while f.tell() > 0:
                byte = f.read(1)
                if byte == b'\n':
                    break
                f.seek(-2, os.SEEK_CUR)
        except OSError:
            f.seek(0)
        last_line = f.read().decode().strip()
    
    if ']' in last_line:
        _, message = last_line.split(']', 1)
        return message.strip()
    else:
        return last_line

def save_log_entry(msg):
    """Funktion zum Speichern von Log-Einträgen in eine Datei."""
    log_file_path = 'logfile.txt'
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f'[{timestamp}] {msg}'

    try:
        last_message = get_last_log_message(log_file_path)
        if last_message == msg:
            return
        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(log_entry + '\n')
    except Exception as e:
        print(f"Fehler beim Schreiben in die Log-Datei: {e}")

def save_to_stats():
    """Speichert die aktuellen Statistiken in einer JSON-Datei."""

    playtime_seconds = time.time() - start_time
    playtime_formatted = format_playtime(playtime_seconds)

    stats = {
        "BET": BET,
        "CURRENT_BALANCE": round(CURRENT_BALANCE, 2),
        "ROUNDS_PLAYED": ROUNDS_PLAYED,
        "TOTAL_GAMES_WON": TOTAL_GAMES_WON,
        "TOTAL_GAMES_LOST": TOTAL_GAMES_LOST,
        "START_BALANCE": float(start_money_entry.get()),
        "PLAYTIME": playtime_formatted
    }
    
    try:
        with open('stats.json', 'w', encoding='utf-8') as f:
            json.dump(stats, f, ensure_ascii=False, indent=4)
        
    except Exception as e:
        message(f"Fehler beim Speichern der Statistiken: {e}")

def save_to_history():
    """Speichert die aktuellen Statistiken in einer JSON-Datei als History."""
    playtime_seconds = time.time() - start_time
    playtime_formatted = format_playtime(playtime_seconds)

    stats = {
        datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'): {
            'BET': BET,
            "CURRENT_BALANCE": round(CURRENT_BALANCE, 2),
        }
    }

    try:
        # Versuchen, bestehende Datei zu laden
        try:
            with open('history.json', 'r', encoding='utf-8') as f:
                history = json.load(f)  # Laden der bestehenden JSON-Daten
        except FileNotFoundError:
            # Falls die Datei nicht existiert, starten wir mit einem leeren Dictionary
            history = {}

        # Neues Objekt zur History hinzufügen
        history.update(stats)

        # JSON-Datei aktualisieren
        with open('history.json', 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=4)

    except Exception as e:
        message(f"Fehler beim Speichern der History: {e}")
    
    

def format_playtime(seconds):
    days, remainder = divmod(int(seconds), 86400)        # 86400 Sekunden pro Tag
    hours, remainder = divmod(remainder, 3600)          # 3600 Sekunden pro Stunde
    minutes, seconds = divmod(remainder, 60)            # 60 Sekunden pro Minute
    return f"{days} Tage, {hours} Stunden, {minutes} Minuten, {seconds} Sekunden"

def read_stats():
    """Liest die Statistiken aus der JSON-Datei und gibt sie zurück."""
    try:
        with open('stats.json', 'r', encoding='utf-8') as f:
            stats = json.load(f)
        return stats
    except FileNotFoundError:
        print("Die Datei 'stats.json' wurde nicht gefunden.")
    except json.JSONDecodeError:
        print("Fehler beim Dekodieren der JSON-Datei.")
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

def create_gui():
    """Erstellt das GUI-Fenster und initialisiert die Steuerelemente."""
    global text_widget, start_button, stop_button
    global input_einsatz_x, input_einsatz_y, btn_confirm_x, btn_confirm_y
    global green_x1, green_y1, green_x2, green_y2
    global red_x1, red_y1, red_x2, red_y2
    global next_x1, next_y1, next_x2, next_y2
    global start_number_entry, x_pos, y_pos, root
    global start_money_entry
    global multiplier_entry
    global multiplier_input_x, multiplier_input_y

    root = tk.Tk()
    root.title("Easy-Money Bot")
    root.geometry("400x950")

    # Frame für "Start" und "Stop"
    button_frame = tk.Frame(root)
    button_frame.pack(side=tk.TOP, fill=tk.X)
    button_container = tk.Frame(button_frame)
    button_container.pack(side=tk.TOP, pady=10)
    start_button = tk.Button(button_container, text="Start", command=start_program)
    start_button.pack(side=tk.LEFT, padx=10)
    stop_button = tk.Button(button_container, text="Stop", command=stop_program)
    stop_button.pack(side=tk.LEFT, padx=10)
    stop_button.pack_forget()

    # Label für Mausposition und Hinweistext
    instruction_label = tk.Label(root, text="Drücke 'R' für Mausposition")
    instruction_label.pack(side=tk.TOP, padx=10, pady=5)

    # Frame für Mausposition
    position_frame = tk.Frame(root)
    position_frame.pack(side=tk.TOP, padx=10, pady=5)
    tk.Label(position_frame, text="X:").pack(side=tk.LEFT)
    x_pos = tk.StringVar()
    x_pos_entry = tk.Entry(position_frame, textvariable=x_pos, width=10)
    x_pos_entry.pack(side=tk.LEFT, padx=5)

    tk.Label(position_frame, text="Y:").pack(side=tk.LEFT)
    y_pos = tk.StringVar()
    y_pos_entry = tk.Entry(position_frame, textvariable=y_pos, width=10)
    y_pos_entry.pack(side=tk.LEFT, padx=5)

    # Initialisiere Mausposition
    update_mouse_position()

    # Einstellungs-Frame
    settings_frame = tk.LabelFrame(root, text="Einstellungen", padx=10, pady=10)
    settings_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10, expand=True)

    entry_frame = tk.Frame(settings_frame)
    entry_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
    pady_value = 5
    padx_value = 5

    # Input Einsatz
    tk.Label(entry_frame, text="Position - Einsatz:", anchor="w").grid(row=0, column=0, sticky="w", pady=pady_value)
    input_einsatz_x = tk.Entry(entry_frame, width=5)
    input_einsatz_x.grid(row=0, column=1, padx=(0, padx_value))
    input_einsatz_x.insert(0, Input_Einsatz[0])
    input_einsatz_y = tk.Entry(entry_frame, width=5)
    input_einsatz_y.grid(row=0, column=2)
    input_einsatz_y.insert(0, Input_Einsatz[1])
    tk.Label(entry_frame, text="").grid(row=1, column=0)

    # Confirm Button
    tk.Label(entry_frame, text="Position - Einsatz plazieren:", anchor="w").grid(row=2, column=0, sticky="w", pady=pady_value)
    btn_confirm_x = tk.Entry(entry_frame, width=5)
    btn_confirm_x.grid(row=2, column=1, padx=(0, padx_value))
    btn_confirm_x.insert(0, BTN_Confirm[0])
    btn_confirm_y = tk.Entry(entry_frame, width=5)
    btn_confirm_y.grid(row=2, column=2)
    btn_confirm_y.insert(0, BTN_Confirm[1])
    tk.Label(entry_frame, text="").grid(row=3, column=0)

    # --- NEU: Multiplier Input Position (verschoben nach oben) ---
    tk.Label(entry_frame, text="Position - Auto-Cashout:", anchor="w").grid(row=4, column=0, sticky="w", pady=pady_value)
    multiplier_input_x = tk.Entry(entry_frame, width=5)
    multiplier_input_x.grid(row=4, column=1, padx=(0, padx_value))
    multiplier_input_x.insert(0, INPUT_CASHOUT[0])  # <-- GEÄNDERT: Verwendung von Input_Cashout

    multiplier_input_y = tk.Entry(entry_frame, width=5)
    multiplier_input_y.grid(row=4, column=2)
    multiplier_input_y.insert(0, INPUT_CASHOUT[1])  # <-- GEÄNDERT: Verwendung von Input_Cashout
    tk.Label(entry_frame, text="").grid(row=5, column=0)

    # Grün Box
    tk.Label(entry_frame, text="Indikator - Gewonnen:", anchor="w").grid(row=6, column=0, sticky="w", pady=pady_value)
    green_x1 = tk.Entry(entry_frame, width=5)
    green_x1.grid(row=6, column=1, padx=(0, padx_value))
    green_x1.insert(0, Box_Green_Cashout[0][0])
    green_y1 = tk.Entry(entry_frame, width=5)
    green_y1.grid(row=6, column=2)
    green_y1.insert(0, Box_Green_Cashout[0][1])
    green_x2 = tk.Entry(entry_frame, width=5)
    green_x2.grid(row=7, column=1, padx=(0, padx_value))
    green_x2.insert(0, Box_Green_Cashout[1][0])
    green_y2 = tk.Entry(entry_frame, width=5)
    green_y2.grid(row=7, column=2)
    green_y2.insert(0, Box_Green_Cashout[1][1])
    tk.Label(entry_frame, text="").grid(row=8, column=0)

    # Rot Box
    tk.Label(entry_frame, text="Indikator - Verloren:", anchor="w").grid(row=9, column=0, sticky="w", pady=pady_value)
    red_x1 = tk.Entry(entry_frame, width=5)
    red_x1.grid(row=9, column=1, padx=(0, padx_value))
    red_x1.insert(0, Box_Red_Score[0][0])
    red_y1 = tk.Entry(entry_frame, width=5)
    red_y1.grid(row=9, column=2)
    red_y1.insert(0, Box_Red_Score[0][1])
    red_x2 = tk.Entry(entry_frame, width=5)
    red_x2.grid(row=10, column=1, padx=(0, padx_value))
    red_x2.insert(0, Box_Red_Score[1][0])
    red_y2 = tk.Entry(entry_frame, width=5)
    red_y2.grid(row=10, column=2)
    red_y2.insert(0, Box_Red_Score[1][1])
    tk.Label(entry_frame, text="").grid(row=11, column=0)

    # Next Round
    tk.Label(entry_frame, text="Indikator - Nächste Runde:", anchor="w").grid(row=12, column=0, sticky="w", pady=pady_value)
    next_x1 = tk.Entry(entry_frame, width=5)
    next_x1.grid(row=12, column=1, padx=(0, padx_value))
    next_x1.insert(0, Box_Next_Round[0][0])
    next_y1 = tk.Entry(entry_frame, width=5)
    next_y1.grid(row=12, column=2)
    next_y1.insert(0, Box_Next_Round[0][1])
    next_x2 = tk.Entry(entry_frame, width=5)
    next_x2.grid(row=13, column=1, padx=(0, padx_value))
    next_x2.insert(0, Box_Next_Round[1][0])
    next_y2 = tk.Entry(entry_frame, width=5)
    next_y2.grid(row=13, column=2)
    next_y2.insert(0, Box_Next_Round[1][1])
    tk.Label(entry_frame, text="").grid(row=14, column=0)

    # Start Number
    tk.Label(entry_frame, text="Einsatz:", anchor="w").grid(row=15, column=0, sticky="w", pady=pady_value)
    start_number_entry = tk.Entry(entry_frame, width=10)
    start_number_entry.grid(row=15, column=1, columnspan=2)
    start_number_entry.insert(0, START_NUMBER)
    tk.Label(entry_frame, text="").grid(row=16, column=0)

    # Start Money
    tk.Label(entry_frame, text="bisheriges Geld:", anchor="w").grid(row=17, column=0, sticky="w", pady=pady_value)
    start_money_entry = tk.Entry(entry_frame, width=10)
    start_money_entry.grid(row=17, column=1, columnspan=2)
    start_money_entry.insert(0, "0.0")
    tk.Label(entry_frame, text="").grid(row=18, column=0)

    # --- NEU: Multiplikator-Feld ---
    tk.Label(entry_frame, text="Cashout-Betrag:", anchor="w").grid(row=19, column=0, sticky="w", pady=pady_value)
    multiplier_entry = tk.Entry(entry_frame, width=10)
    multiplier_entry.grid(row=19, column=1, columnspan=2)
    multiplier_entry.insert(0, WIN_MULTIPLIER)
    tk.Label(entry_frame, text="").grid(row=20, column=0)

    # Text-Widget für Log-Ausgaben
    text_widget = tk.Text(root, wrap=tk.WORD)
    text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Event-Bindung fürs Tastatur-Event (r/R drücken -> Mausposition updaten)
    root.bind('<KeyPress>', on_key_press)

    root.attributes("-topmost", True)

    root.mainloop()

if __name__ == "__main__":
    create_gui()