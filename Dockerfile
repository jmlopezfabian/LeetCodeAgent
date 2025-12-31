# Imagen base
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar archivos
COPY . .

# Instalar dependencias (si las hay)
RUN pip install --no-cache-dir -r requirements.txt

# Comando por defecto
CMD ["python", "app.py"]
