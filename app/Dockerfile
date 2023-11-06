FROM registry.access.redhat.com/ubi8/ubi

# Actualizar el sistema y configurar los repositorios
RUN dnf update -y && \
    dnf install -y python3

# Copiar los archivos de la aplicación a la imagen
COPY . /app

# Establecer el directorio de trabajo
WORKDIR /app

# Instalar las dependencias de la aplicación (si las hay)
RUN pip3 install -r requirements.txt

# Comando para ejecutar la aplicación
CMD ["python3", "app.py"]