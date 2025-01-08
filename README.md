# Crash-Game-Bot

## Übersicht

Der **Crash-Game-Bot** ist ein automatisiertes Python-Skript, das entwickelt wurde, um Wetten in Crash-Spielen zu platzieren und Gewinne sowie Verluste basierend auf den Bildschirmfarben zu erkennen. Der Bot simuliert menschliche Eingaben, um Einsätze zu tätigen, Cashouts zu verwalten und Spielrunden zu überwachen. Dieses Tool richtet sich an Benutzer, die ihre Interaktionen mit Crash-Spielen automatisieren möchten.

**Hinweis:** Dieses Skript dient ausschließlich zu Bildungs- und Demonstrationszwecken. Glücksspiel birgt erhebliche Risiken, und es ist **nicht möglich**, das Glücksspiel zu schlagen. Casinos und Wettanbieter haben stets einen mathematischen Vorteil, der langfristig zu Verlusten führt.

## Funktionen

- **Automatisierte Wetteingabe:** Der Bot platziert automatisch Einsätze an definierten Bildschirmpositionen.
- **Farbüberwachung:** Erkennt gewonnene (grüne) oder verlorene (rote) Runden durch Farbanalyse bestimmter Bildschirmbereiche.
- **Einsatzverwaltung:** Verdoppelt den Einsatz nach einem Verlust und setzt bei einem Gewinn den Einsatz zurück.
- **Statistik-Tracking:** Protokolliert Rundenanzahl, Gewinne, Verluste und aktuellen Kontostand.
- **GUI-Oberfläche:** Ein benutzerfreundliches grafisches Interface zur Konfiguration und Überwachung des Bots.
- **Log- und Verlaufsdateien:** Speichert Ereignisse und Spielverläufe zur späteren Analyse.

## Voraussetzungen

- **Betriebssystem:** Windows
- **Python:** Version 3.6 oder höher
- **Benötigte Bibliotheken:**
  - `ctypes`
  - `pyautogui`
  - `Pillow`
  - `tkinter`
  - `json`

## Installation

1. **Python installieren:**
   Stellen Sie sicher, dass Python auf Ihrem System installiert ist. Sie können Python von der [offiziellen Website](https://www.python.org/downloads/) herunterladen und installieren.

2. **Benötigte Bibliotheken installieren:**
   Öffnen Sie die Eingabeaufforderung (CMD) und führen Sie die folgenden Befehle aus:

   ```bash
   pip install pyautogui
   pip install Pillow
   
3. **Skript herunterladen:**
Laden Sie das Skript crash_game_bot.py herunter und speichern Sie es an einem gewünschten Ort auf Ihrem Computer.

## Nutzung

1. **Skript starten:**
   Navigieren Sie im Terminal oder in der Eingabeaufforderung zum Verzeichnis des Skripts und führen Sie es aus:

   ```bash
   python crash_game_bot.py

2.	**GUI-Konfiguration:**
	•	Start und Stop: Nutzen Sie die Schaltflächen „Start“ und „Stop“, um den Bot zu starten oder zu beenden.
	•	Mausposition aktualisieren: Drücken Sie die Taste R, um die aktuelle Mausposition in die Eingabefelder zu übernehmen.
	•	Einstellungen: Passen Sie die Positionen der Einsatzfelder, Bestätigungsbuttons, Indikatorboxen (Grün für Gewinn, Rot für Verlust, Gold für nächste Runde) sowie den Startbetrag und den Multiplikator nach Bedarf an.

3.	**Bot ausführen:**
  Nach der Konfiguration klicken Sie auf „Start“, um den Bot zu aktivieren. Der Bot beginnt automatisch, Einsätze zu platzieren und überwacht die Ergebnisse basierend auf den festgelegten Farben.

4.	**Statistiken und Logs:**
	•	Live-Logs: Sehen Sie sich Echtzeit-Logs im Textfeld des GUI an.
	•	Log-Dateien: Überprüfen Sie logfile.txt für eine detaillierte Aufzeichnung der Ereignisse.
	•	Statistiken: Die Datei stats.json speichert die aktuellen Spielstatistiken.
	•	Verlauf: Die Datei history.json enthält eine Historie der Einsätze und Ergebnisse.

## Erfahrungsbericht

In einem Testlauf wurden 4.000 Runden mit einem Startbetrag von 0.01 Euro und einem Multiplikator von 2,05 gespielt. Während dieser Simulation konnte der Bot Einsätze effizient verwalten und Ergebnisse protokollieren. 
Es ist jedoch wichtig zu betonen, dass solche Tests nicht die langfristigen Risiken und Verluste des Glücksspiels widerspiegeln.

## Wichtiger Hinweis

Glücksspiel kann süchtig machen und zu erheblichen finanziellen Verlusten führen. Dieses Skript ist nicht dazu gedacht, Glücksspielsysteme zu schlagen oder Gewinne zu garantieren. Casinos und Wettanbieter verfügen über mathematische Vorteile, die langfristig zu Verlusten führen. Nutzen Sie dieses Tool verantwortungsbewusst und seien Sie sich der Risiken bewusst.

## Haftungsausschluss

Der Autor dieses Skripts übernimmt keinerlei Verantwortung für Verluste oder Schäden, die durch die Nutzung dieses Bots entstehen. Die Nutzung erfolgt auf eigenes Risiko.

## Lizenz

Dieses Projekt steht unter der MIT-Lizenz.

