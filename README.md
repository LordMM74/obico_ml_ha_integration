# Obico ML Home Assistant Integration (Docker Fork)

Eine angepasste Home-Assistant-Integration zur lokalen KI-Fehlererkennung (Spaghetti-Erkennung) beim 3D-Druck mittels **Obico ML**.

> **Hinweis zu diesem Fork:**  
> Dies ist ein angepasster Fork von [nobodyguy/obico_ml_ha_integration](https://github.com/nobodyguy/obico_ml_ha_integration). Anstelle des nicht mehr gepflegten Home Assistant Add-ons kommuniziert diese Version direkt mit der ML-API eines selbstgehosteten Obico-Docker-Containers über das Image von [imagegenius/docker-obico](https://github.com/imagegenius/docker-obico#readme).

## Funktionsweise & Änderungen gegenüber dem Original

* **GET statt POST:** Die Integration sendet keine Base64-kodierten Bilddaten mehr per `POST`-Request, sondern nutzt den nativen `/detect`-Endpunkt der Obico ML API per `GET`-Request.
* **Direkte Bild-URL (`image_url`):** Anstatt das Bild lokal in Home Assistant zu verarbeiten, wird die direkte Snapshot-URL der Kamera (z. B. von Moonraker/OctoPrint) als Parameter an den ML-Server übergeben, der das Bild eigenständig abruft.

## Voraussetzungen

1. **Laufender Obico-Server / ML-API:** Ein eingerichteter Container auf Basis von [imagegenius/docker-obico](https://github.com/imagegenius/docker-obico#readme), dessen ML-API-Endpunkt (Standardport `3333` bzw. `/detect`) aus dem Netzwerk erreichbar ist.
2. **Direkte Snapshot-URL der Kamera:** Eine per HTTP erreichbare URL, die ein aktuelles Einzelbild (JPEG) des 3D-Druckers liefert (z. B. `http://<DRUCKER-IP>/webcam/?action=snapshot`). *Wichtig: Der Docker-Container muss diese URL ohne Login-Abfrage direkt erreichen können.*

## Installation

### Über HACS (Empfohlen)

1. Öffne **HACS** in Home Assistant.
2. Klicke oben rechts auf das Drei-Punkte-Menü und wähle **Benutzerdefinierte Repositories** (Custom repositories).
3. Füge folgende URL hinzu: `https://github.com/LordMM74/obico_ml_ha_integration`
4. Wähle als Kategorie **Integration** aus und klicke auf **Hinzufügen**.
5. Suche nach **Obico ML**, installiere die Integration und starte Home Assistant neu.

### Manuelle Installation

1. Lade dieses Repository herunter und kopiere den Ordner `custom_components/obico_ml` in das Verzeichnis `config/custom_components/` deiner Home-Assistant-Instanz.
2. Starte Home Assistant neu.

## Konfiguration

1. Gehe in Home Assistant zu **Einstellungen** > **Geräte & Dienste**.
2. Klicke unten rechts auf **Integration hinzufügen** und suche nach **Obico ML**.
3. Trage die erforderlichen Verbindungsdaten ein:
   * **ML API URL:** Die URL zum `/detect`-Endpunkt deines Obico-Containers (z. B. `http://<SERVER-IP>:3333/detect`).
   * **Kamera Snapshot URL:** Die direkte HTTP-URL zum Kamerabild deines Druckers.
   * **Threshold (Schwellenwert):** Empfindlichkeit der Fehlererkennung (Standardwert meist zwischen `0.25` und `0.5`).

## Bereitgestellte Entitäten

* **Binary Sensor (`error_detected`):** Schaltet auf `Erkannt` (`on`), sobald die KI ein Druckproblem (z. B. Spaghetti) feststellt.
* **Sensor (`avg_confidence`):** Gibt die durchschnittliche Erkennungssicherheit (Confidence) in Prozent an.
* **Camera / Image (`image_with_errors`):** Zeigt das zuletzt geprüfte Bild inklusive der von der KI eingezeichneten Erkennungsrahmen (Bounding Boxes) an.
