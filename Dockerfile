#Imagen base de Python
FROM python:3.9

#Directorio de trabajo en /app
WORKDIR /app

#Copiar requerimientos al contenedor
COPY requirements.txt .

#Instalar requerimientos 
RUN pip install --no-cache-dir -r requirements.txt



#Copiar script al contenedor
COPY Transcriptor.py .

#Exponer el puerto 5000 la ejecucion del proyecto
EXPOSE 5000

#Comando a ejecutar una vez se haga un run en la app 
CMD ["python", "Transcriptor.py"]