# InterpolAI

Un'applicazione web per l'ingrandimento avanzato delle immagini oltre i limiti classici dello zoom, utilizzando tecniche sofisticate di interpolazione e super-risoluzione.

## Caratteristiche

- Caricamento di immagini (JPG, JPEG, PNG)
- Interfaccia interattiva per selezionare aree specifiche dell'immagine
- Zoom avanzato con multiple tecniche di interpolazione:
  - Interpolazione bicubica
  - Interpolazione Lanczos
  - Super-risoluzione basata su reti neurali (EDSR)
- Elaborazione di bordi migliorata con maschera di contrasto
- Interfaccia utente intuitiva e responsive

## Requisiti

- Python 3.7+
- Flask
- OpenCV
- TensorFlow
- NumPy
- Pillow

## Installazione

1. Clonare il repository:
   ```
   git clone https://github.com/tuoutente/InterpolAI.git
   cd InterpolAI
   ```

2. Creare e attivare un ambiente virtuale (opzionale ma raccomandato):
   ```
   python -m venv env
   # Su Windows
   env\Scripts\activate
   # Su Linux/Mac
   source env/bin/activate
   ```

3. Installare le dipendenze:
   ```
   pip install -r requirements.txt
   ```

4. Scaricare i modelli pre-addestrati (opzionale):
   - Per utilizzare la funzionalità di super-risoluzione avanzata, scaricare il modello pre-addestrato EDSR e posizionarlo nella cartella `app/models/`.
   - Il percorso del modello dovrebbe essere `app/models/EDSR_x4.pb` o `app/models/edsr_model.h5`
   - Se non disponibile, l'app utilizzerà tecniche di interpolazione tradizionali.

## Utilizzo

1. Avviare l'applicazione:
   ```
   python run.py
   ```

2. Aprire un browser e navigare a `http://127.0.0.1:5000`

3. Caricare un'immagine usando il pulsante "Carica"

4. Fare clic su qualsiasi punto dell'immagine per ingrandire quell'area

5. Utilizzare lo slider per regolare il livello di zoom

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

## Tecnologie di interpolazione

L'applicazione utilizza diverse tecniche di interpolazione a seconda del livello di zoom:

1. **Zoom basso (≤ 2x)**: Interpolazione bicubica
2. **Zoom medio (≤ 4x)**: Interpolazione Lanczos (alta qualità)
3. **Zoom alto (> 4x)**: Super-risoluzione basata su reti neurali (EDSR)

Se i modelli di super-risoluzione non sono disponibili, l'applicazione utilizzerà automaticamente le tecniche di interpolazione tradizionali.

## Licenza

MIT 