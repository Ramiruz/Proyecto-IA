# Importar las bibliotecas necesarias
from flask import Flask, url_for, render_template, request
import assemblyai as aai
from summarizer import Summarizer
from werkzeug.utils import secure_filename
import os

# Configurar la aplicación Flask
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['ALLOWED_EXTENSIONS'] = {'mp3'}

# Función para realizar la transcripcion de audio utilizando AssemblyAI
def transcribe_audio(api_key, audio_path):

    aai.settings.api_key = api_key      # Establecer la clave API de AssemblyAI
    
    transcriber = aai.Transcriber()     # Inicializar el transcriptor de AssemblyAI
    
    transcript = transcriber.transcribe(audio_path)     # Transcribir el archivo de audio
    
    # Se obtiene el texto del audio por partes y se unen en un solo texto transcrito
    paragraphs = transcript.get_paragraphs()
    text_sentences = [paragraph.text for paragraph in paragraphs]
    transcribed_text = ' '.join(text_sentences)
    
    return transcribed_text


# Ruta para el método GET, que renderiza la página principal
@app.get('/')
def assembly():
    css_url = url_for('static', filename='style.css')
    return render_template("index.html", css_url=css_url)


# Ruta para el método POST, que procesa la carga y transcripción del archivo de audio
@app.post('/')
def index():
    
    css_url = url_for('static', filename='style.css')


    if request.method == 'POST':
        api_key_assemblyai = "46f3fc0a6e364888acf89978f15a5d24"

        # Obtener el archivo de audio desde la solicitud
        file = request.files['audio']
        filename = secure_filename(file.filename)

        # Guardar el archivo de audio en la carpeta de carga
        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(audio_path)

        # Transcribir el audio utilizando AssemblyAI
        transcribed_text = transcribe_audio(api_key_assemblyai, audio_path)

        # Generar un resumen utilizando el modelo de resumen BERT
        bert_model = Summarizer()
        bert_summary = ''.join(bert_model(transcribed_text, min_length=60))
        print(bert_summary)

        # Renderizar la página con el texto transcrito y el resumen BERT
    return render_template('index.html', summary=bert_summary, css_url=css_url)

    # Renderizar la página si no hay una solicitud POST
    #return render_template('index.html', summary="")


# Ejecutar la aplicación si el script se ejecuta directamente
if __name__ == "__main__":

    # Crear la carpeta de carga si no existe
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)