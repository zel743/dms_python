from flask import Flask, render_template, request, jsonify
import os
import sys
from pathlib import Path
import webbrowser
from threading import Timer

def resolver_ruta(ruta_relativa):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, ruta_relativa)
    return os.path.join(os.path.abspath("."), ruta_relativa)

app = Flask(__name__, template_folder=resolver_ruta('templates'))

def buscar_pdfs_optimizado(carpeta_raiz, palabra):
    palabra_clave = palabra.lower()
    archivos_encontrados = []
    
    for directorio_actual, subdirectorios, archivos in os.walk(carpeta_raiz):
        subdirectorios[:] = [d for d in subdirectorios if not d.startswith('.') and d not in ['AppData', 'node_modules', 'venv', '$Recycle.Bin']]
        
        for archivo in archivos:
            if archivo.lower().endswith('.pdf') and palabra_clave in archivo.lower():
                ruta_completa = Path(directorio_actual) / archivo
                
                archivos_encontrados.append({
                    "nombre": archivo,
                    "ruta": str(ruta_completa),
                    "tamaño": round(ruta_completa.stat().st_size / 1024, 1)
                })
                
    return archivos_encontrados

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/buscar', methods=['POST'])
def buscar():
    datos = request.get_json()
    palabra = datos.get('palabra', '')
    
    if not palabra:
        return jsonify({"error": "Por favor ingresa una palabra."}), 400
        
    ruta_busqueda = str(Path.home())
    
    resultados = buscar_pdfs_optimizado(ruta_busqueda, palabra)
    return jsonify({"resultados": resultados})

@app.route('/abrir', methods=['POST'])
def abrir():
    datos = request.get_json()
    ruta = datos.get('ruta', '')
    
    if not ruta or not os.path.exists(ruta):
        return jsonify({"error": "El archivo no existe o fue movido."}), 400
        
    try:
        os.startfile(ruta)
        return jsonify({"status": "ok"})
    except Exception as e:
        return jsonify({"error": f"No se pudo abrir: {str(e)}"}), 500

def abrir_navegador():
    webbrowser.open_new('http://127.0.0.1:5000/')

if __name__ == '__main__':
    Timer(1, abrir_navegador).start()
    app.run(debug=True)