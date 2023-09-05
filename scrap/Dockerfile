# Utiliza la imagen base de Python
FROM python:3.11

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo requirements.txt a /app
COPY requirements.txt /app

# Instala las dependencias del script de scraping
RUN pip install --no-cache-dir -r requirements.txt

# Copia los archivos de tu script de scraping al directorio de trabajo
COPY . /app

# Comando para ejecutar tu script de scraping cuando se inicie el contenedor
CMD ["python", "scrap.py"]
