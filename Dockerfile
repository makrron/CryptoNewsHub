# Utiliza la imagen base de Python 3.11
FROM python:3.11

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia el código fuente del backend al contenedor
COPY . /app

# Instala las dependencias desde requirements.txt
RUN pip install -r requirements.txt

# Expone el puerto en el que se ejecuta tu backend (por ejemplo, 8000)
EXPOSE 8000

# Comando para iniciar el servidor de Django
CMD ["python", "manage.py", "runserver"]
