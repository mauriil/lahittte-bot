# Usar una imagen base ligera de Python
FROM python:3.9-slim

# Configurar directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de requerimientos
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente al contenedor
COPY . .

# Exponer el puerto si es necesario (por ejemplo, para monitoreo o APIs)
# EXPOSE 8080

# Comando para ejecutar el script al iniciar el contenedor
CMD ["python", "main.py"]
