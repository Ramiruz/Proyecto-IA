import assemblyai as aai
from transformers import GPT2LMHeadModel, GPT2Tokenizer

def transcribir_audio(api_key, audio_path):
    aai.settings.api_key = api_key
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_path)
    oraciones = transcript.get_paragraphs()
    oraciones_texto = [parrafo.text for parrafo in oraciones]
    texto_transcrito = ' '.join(oraciones_texto)
    return texto_transcrito

def generar_respuesta(prompt, modelo, tokenizer, max_length=500, min_length=20):
    entrada_codificada = tokenizer.encode(prompt, return_tensors='pt')
    salida = modelo.generate(
        entrada_codificada,
        max_length=max_length,
        min_length=min_length,
        num_beams=10,
        use_cache= True,
        no_repeat_ngram_size=1,
        top_k=50,
        top_p=0.95,
        temperature=0.1,
    )
    texto_generado = tokenizer.decode(salida[0], skip_special_tokens=True)
    texto_generado = texto_generado.strip()
    return texto_generado


def main():
    api_key_assemblyai = "46f3fc0a6e364888acf89978f15a5d24"
    audio_path = "onlymp3.to - Speech recognition in Python made easy Python Tutorial-YdYTSxEW5bA-192k-1700264266.mp3"  

    texto_transcrito = transcribir_audio(api_key_assemblyai, audio_path)

    print(texto_transcrito)

    modelo_gpt2 = GPT2LMHeadModel.from_pretrained('gpt2')
    tokenizer_gpt2 = GPT2Tokenizer.from_pretrained('gpt2')

    pregunta = "\nTell me about the content of the transcribed text. Who is the patrick?"

    respuesta_generada = generar_respuesta(pregunta, modelo_gpt2, tokenizer_gpt2)

    print("\nRespuesta generada:")
    print(respuesta_generada)

if __name__ == "__main__":
    main()

