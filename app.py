import os
from flask import Flask, url_for, render_template, request
from Proyecto_IA.ACSIA import transcribir_audio, generar_respuesta 
from transformers import GPT2LMHeadModel, GPT2Tokenizer
app = Flask(__name__)


@app.get('/')
def assembly():  # put application's code here
    css_url = url_for('static', filename='style.css')
    return render_template("index.html", css_url=css_url)

@app.post('/')
def pene():
   audio = request.form['audio']

   audio.save(os.path.join(app.config['UPLOAD_FOLDER'], audio.filename))
   ruta_archivo = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], audio.filename))


   texto_transcrit = transcribir_audio("46f3fc0a6e364888acf89978f15a5d24", ruta_archivo)
   modelo_gpt2 = GPT2LMHeadModel.from_pretrained('gpt2')
   tokenizer_gpt2 = GPT2Tokenizer.from_pretrained('gpt2')
   pregunta = "\nTell me about the content of the transcribed text. Who is the patrick?"
   respuesta_generada = generar_respuesta(pregunta, modelo_gpt2, tokenizer_gpt2)
   return render_template("index.html", respuesta_generada= respuesta_generada)

if __name__ == '__main__':
    app.run()
