import os
ruta_archivos = os.path.abspath('Grabaciones')
ruta_textos = os.path.abspath('Textos')

def crear_carpetas():
    countador=0
    try:
     
        if not os.path.exists(ruta_archivos):
            os.mkdir(ruta_archivos)
            countador+=1
        else:
            print('no se creo la carpeta')
   
        if not os.path.exists(ruta_textos):
            os.mkdir(ruta_textos)
            countador+=1
            
        if countador >= 2:
            
            countador=0
            return print("Dir_message Las carpetas se crearon con exito !!")
        
    except Exception as e: 
        return print( "error" ,e)
    
crear_carpetas()
