# Imagen base
FROM python:3.11

# Evitar que Python guarde archivos .pyc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Crear y usar el directorio de trabajo
WORKDIR /app

# Copiar los archivos de dependencias
COPY requirements.txt /app/

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código
COPY . /app/

# Exponer el puerto de Django
EXPOSE 8000

# Comando por defecto (se sobreescribe en docker-compose)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
