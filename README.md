# InterpolAI

Un'applicazione web per l'ingrandimento avanzato delle immagini oltre i limiti classici dello zoom, utilizzando tecniche sofisticate di interpolazione e super-risoluzione.

## Caratteristiche

- Caricamento di immagini (JPG, JPEG, PNG)
- Interfaccia interattiva per selezionare aree specifiche dell'immagine
- Zoom avanzato fino a 15x con tecniche di interpolazione:
  - Interpolazione bicubica
  - Interpolazione Lanczos
  - Super-risoluzione (se disponibile modello EDSR)
- Miglioramento dei dettagli e riduzione degli artefatti
- **Pannello di controllo** per:
  - Luminosità
  - Contrasto
  - Nitidezza
  - Saturazione
- **Tutte le regolazioni sono applicate in tempo reale**
- Layout moderno: immagine originale e area ingrandita affiancate, controlli sotto

## Requisiti

- Python 3.7+
- Flask
- OpenCV
- NumPy
- Pillow
- (Opzionale) Modello EDSR per super-risoluzione

## Installazione manuale

1. Clona il repository:
   ```bash
   git clone https://github.com/tuoutente/InterpolAI.git
   cd InterpolAI
   ```

2. (Opzionale) Crea e attiva un ambiente virtuale:
   ```bash
   python -m venv env
   # Su Windows
   env\Scripts\activate
   # Su Linux/Mac
   source env/bin/activate
   ```

3. Installa le dipendenze:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. (Opzionale) Scarica il modello EDSR pre-addestrato e posizionalo in `app/models/EDSR_x4.pb` per la super-risoluzione avanzata.

5. Avvia l'applicazione:
   ```bash
   python run.py
   ```

6. Apri il browser su [http://127.0.0.1:5000](http://127.0.0.1:5000)

## Struttura del progetto

```
InterpolAI/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── models/
│   │   └── super_resolution.py
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   ├── img/
│   │   └── uploads/
│   └── templates/
│       └── index.html
├── requirements.txt
├── run.py
└── README.md
```

## Funzionalità principali

- **Zoom selettivo**: clicca su un punto dell'immagine per ingrandirlo
- **Controlli in tempo reale**: modifica luminosità, contrasto, nitidezza, saturazione e vedi subito il risultato
- **Layout responsive**: immagini affiancate, controlli sotto
- **Nessun reload manuale**: ogni modifica aggiorna subito l'area ingrandita

## Note
- Se vuoi usare la super-risoluzione EDSR, scarica il modello pre-addestrato e posizionalo in `app/models/EDSR_x4.pb`.
- Se hai problemi con Pillow su Windows, aggiorna pip e installa Pillow separatamente:
  ```bash
  python -m pip install --upgrade pip
  pip install Pillow
  ```
