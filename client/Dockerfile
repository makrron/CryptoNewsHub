# Utiliza la imagen base de Node.js con la versión que necesites
FROM node:14

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia los archivos del frontend al contenedor
COPY . /app
# Copiar la configuración de Nginx al contenedor
COPY nginx.conf /etc/nginx/nginx.conf

# Instala las dependencias utilizando npm
RUN npm install

# Construye la aplicación React
RUN npm run build

# Exponer el puerto en el que se ejecutará la aplicación (por ejemplo, 80)
EXPOSE 5173

# Comando para iniciar el servidor web (en este caso, Nginx)
CMD ["npm", "run", "dev"]