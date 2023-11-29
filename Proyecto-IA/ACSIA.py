# Importar las bibliotecas de Assemblyai y el modelo summarizer de BERT
import assemblyai as aai
from summarizer import Summarizer


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


def main():

    # Clave API de AssemblyAI y ruta del archivo de audio seleccionado
    api_key_assemblyai = "46f3fc0a6e364888acf89978f15a5d24"
    audio_path = "Audio001.mp3"  

    # Transcribir audio utilizando AssemblyAI
    transcribed_text = transcribe_audio(api_key_assemblyai, audio_path)
    print("Audio transcrito:\n", transcribed_text)

    # Inicializar el modelo de resumen BERT
    bert_model = Summarizer()
    
    # Generar un resumen utilizando el modelo de resumen BERT
    bert_summary = ''.join(bert_model(transcribed_text, min_length=60))
    print("Resumen del audio:\n", bert_summary) 


if __name__ == "__main__":
    main()