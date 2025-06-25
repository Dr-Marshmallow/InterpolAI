# Usa una immagine Python ufficiale come base
FROM python:3.10-slim

# Imposta la directory di lavoro
WORKDIR /app

# Copia requirements e installa le dipendenze
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copia il resto del codice dell'app
COPY . .

# Espone la porta su cui gira Flask
EXPOSE 5000

# Variabile d'ambiente per Flask
ENV FLASK_APP=run.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

# Comando di avvio
CMD ["flask", "run"] 