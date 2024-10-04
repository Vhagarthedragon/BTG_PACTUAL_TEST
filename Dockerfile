# Usa Python 3.9 como imagen base
FROM python:3.12.3

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de dependencias
COPY ./requirements.txt /app/requirements.txt

# Instala las dependencias
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copia todo el código de la aplicación a la carpeta de trabajo
COPY . /app

COPY . .

# Copia el archivo .env
COPY .env .env
# Exponer puerto 8000 para pruebas locales
EXPOSE 80

# Comando para iniciar FastAPI con Mangum (adaptado para Lambda)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
