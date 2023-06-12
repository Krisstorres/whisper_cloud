# importaciones de librerias 
import requests
from flask import Flask, request, send_file, jsonify, Response
import os
import openai as ai
from werkzeug.utils import secure_filename
import time
# importaciones de librerias 

##-- Variables
Whisper_01=''
Chatgpt_01=''
ruta_archivos = os.path.abspath('Grabaciones')
if not os.path.exists(ruta_archivos):
    os.mkdir(ruta_archivos)
ruta_textos = os.path.abspath('Textos')
if not os.path.exists(ruta_textos):
    os.mkdir(ruta_textos)
ruta_textos = os.path.abspath('Textos')
lista_archivos = os.listdir('Grabaciones')
soportado = ['mp3', 'flac', 'wav', 'm4a']
##-- Variables


##--Desc_url
def descargar_url(url, ruta_destino):
    try:
        response = requests.get(url)
        response.raise_for_status() 
        
        with open(ruta_destino, 'wb') as archivo:
            archivo.write(response.content)
        
        print('Archivo descargado !')
    
    except requests.exceptions.RequestException as e:
        print('Error descarga :', str(e))
##--Desc_url


##--funcion de limpieza:
def limpieza():
    try:
        if len(lista_archivos) >= 1:
            for col in lista_archivos:
                remove_file(f'Grabaciones/{col}')
        else:
            print('Carpeta Limpia !')
    except Exception as e:
        return print(f'Error : {e}')
##--funcion de limpieza

##--Eliminar audio
def remove_file(path):
    try:
        time.sleep(2)
        os.remove(path)
        print('Se eliminó satisfactoriamente')
        return jsonify({'message': 'Se ha eliminado el archivo original satisfactoriamente'})
    except Exception as e:
        print(f'No se logró eliminar porque: {e}')
        return jsonify({'error': f'No se logró eliminar el archivo: {e}'})
##--Eliminar audio



                        


            


##--Aplicacion Flask:Inicio 
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'Grabaciones'

@app.route('/api/upload', methods=['POST'])
def returndata():    
    ##--Limpiando cartpeta
    limpieza()
    ##--Limpiando cartpeta
    try:        
        if 'file' not in request.files:
            
            ##--                                                                    ##-- Descargando por url 
            try:                
                url = request.form.get('file')
                filename=str(url).split(sep='https://demos.sixbell.com/')[1]         
                ruta_destino = os.path.join(ruta_archivos,filename)
                descargar_url(url,ruta_destino)
                try:
                    ai.api_key = Whisper_01
                    with open(ruta_destino, "rb") as audio_file:
                        transcript = ai.Audio.transcribe("whisper-1", audio_file)
                    
                    transcript_text = transcript['text']
                    text=transcript_text
                    l = len(os.listdir('Textos')) + 1
                    text_file = open(f'Textos/archivo{l}.txt', 'w', encoding='UTF-8')
                    t = str(text).replace('Ã³', 'ó').encode('UTF-8').decode('UTF-8')
                    text_file.write(t.replace('Ã³', 'ó'))
                    text_file.close()
                    remove_file(ruta_destino)                                    
                    ai.api_key = Chatgpt_01
                    rest = ai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Eres un modelo que realiza análisis de sentimientos."},
                        {"role": "user", "content": "Realiza un análisis de sentimientos a este texto "},
                        {"role": "assistant", "content": f"{text}"},
                        {"role": "user", "content": "Muéstrame el resultado del análisis en breves palabras"}
                        ])
                    content = rest['choices'][0]['message']['content']
                    respuesta= ai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                    {"role": "system", "content": "comportate como un modelo que realiza clasificacion de textos segun categoria"},
                    {"role": "user", "content": "Realixa el ananlisis y responde solo con la clasificacion de este texto segun su categoria ejemplo: (servico_tecnico, recursos humanos, contabilidad )"},
                    {"role": "assistant", "content": f"{text}"},
                    {"role": "user", "content": "Muéstrame el resultado del análisis en breves palabras"}
                    ])
                    contenido=respuesta['choices'][0]['message']['content']                                
                    data={
                    #'user_id': userid
                    'filename':filename
                    ,'transcription':str(t)
                    ,'data_analisis':content
                    ,'clasificacion':contenido
                    }
                    #---------------------------------------------------------------------------------------------------------------------------
                    response = jsonify(data)
                    response.headers['Content-Type'] = 'application/json'
                    return response                    
                except Exception as e:
                    return jsonify({'error_descarga' :str(e)})                                                                                                            
            except Exception as e:
                return jsonify({'Request_error' :    str(e) })
            ##--                                                                    ##-- Descargando por url

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No se proporcionó un nombre de archivo válido'})            
        ##--                                                                        ##-- Descargando por archivo         
        filename = secure_filename(file.filename)
        temp_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(temp_filepath)
        ai.api_key = Whisper_01
        with open(temp_filepath, "rb") as audio_file:
            transcript = ai.Audio.transcribe("whisper-1", audio_file)
        transcript_text = transcript['text']
        text=transcript_text
        l = len(os.listdir('Textos')) + 1
        text_file = open(f'Textos/archivo{l}.txt', 'w', encoding='UTF-8')
        t = str(text).replace('Ã³', 'ó').encode('UTF-8').decode('UTF-8')
        text_file.write(t.replace('Ã³', 'ó'))
        text_file.close()
        remove_file(temp_filepath)
        ai.api_key = Chatgpt_01
        texto=text
        rest = ai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un modelo que realiza análisis de sentimientos."},
            {"role": "user", "content": "Realiza un análisis de sentimientos a este texto"},
            {"role": "assistant", "content": f"{t}"},
            {"role": "user", "content": "Muéstrame el resultado del análisis en breves palabras"}
            ])

        content = rest['choices'][0]['message']['content']    

        #---------------------------------------------------------------------------------------------------------------------------
        respuesta= ai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "system", "content": "comportate como un modelo que realiza clasificacion de textos segun categoria"},
            {"role": "user", "content": "Realixa el ananlisis y responde solo con la clasificacion de este texto segun su categorias que podrian estar dentro de cualquier empresa  ejemplo: (servico_tecnico, recursos humanos, contabilidad )"},
            {"role": "assistant", "content": f"{texto}"},
            {"role": "user", "content": "Muéstrame el resultado del análisis en breves palabras"}
            ])
        contenido=respuesta['choices'][0]['message']['content']
        
        data={
        #'user_id': userid
         'filename':filename
        ,'transcription':str(t)
        ,'data_analisis':content
        ,'clasificacion':contenido
        }
        #---------------------------------------------------------------------------------------------------------------------------
        response = jsonify(data)
        response.headers['Content-Type'] = 'application/json'
        return response
    except Exception as e:
        return jsonify({'error': str(e)})
        ##--                                                                        ##-- Descargando por archivo         
   
if __name__ == '__main__':
    app.run()#host='0.0.0.0',port=5000)
##--Aplicacion Flask:Fin