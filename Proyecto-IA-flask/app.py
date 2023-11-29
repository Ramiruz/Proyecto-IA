from flask import Flask, url_for, render_template, request
import assemblyai as aai
from summarizer import Summarizer
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './uploads'
app.config['ALLOWED_EXTENSIONS'] = {'mp3'}


def transcribir_audio(api_key, audio_path):
    aai.settings.api_key = api_key
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_path)
    oraciones = transcript.get_paragraphs()
    oraciones_texto = [parrafo.text for parrafo in oraciones]
    texto_transcrito = ' '.join(oraciones_texto)
    return texto_transcrito

@app.get('/')
def assembly():  # put application's code here
    css_url = url_for('static', filename='style.css')
    return render_template("index.html", css_url=css_url)

@app.post('/')
def index():
    if request.method == 'POST':
        api_key_assemblyai = "46f3fc0a6e364888acf89978f15a5d24"


        file = request.files['audio']
        filename= secure_filename(file.filename)

        audio_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(audio_path)

        texto_transcrito = transcribir_audio(api_key_assemblyai, audio_path)

        bert_model = Summarizer()
        bert_summary = ''.join(bert_model(texto_transcrito, min_length=60))

        return render_template('index.html', transcript=texto_transcrito, summary=bert_summary)


    return render_template('index.html', transcript=texto_transcrito, summary=bert_summary)

if __name__ == "__main__":
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(debug=True)
