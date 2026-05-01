from fastapi import FastAPI, UploadFile, File
from fastapi.responses import Response
from openai import OpenAI
import os

from quiniela.interprete import interpretar_sueno, construir_respuesta_hablada

app = FastAPI()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/voice")
async def voice(audio: UploadFile = File(...)):
    # 1. STT: audio -> texto
    audio_bytes = await audio.read()
    
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=("audio.wav", audio_bytes, "audio/wav"),
        language="es",
    )
    sueno = transcription.text
    print(f"\n🌙 Sueño: {sueno}")
    
    # 2. Interpretar con LLM + diccionario
    resultado = interpretar_sueno(sueno, client)
    print(f"🎯 Símbolos: {resultado['simbolos']}")
    print(f"🔢 Números: {resultado['numeros']}")
    print(f"🎲 Jugada: {resultado['jugada']}")
    print(f"💭 {resultado['razonamiento']}\n")
    
    # 3. Texto de respuesta
    respuesta_texto = construir_respuesta_hablada(resultado)
    
    # 4. TTS: texto -> audio
    audio_respuesta = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=respuesta_texto,
        response_format="wav",
    )
    
    return Response(
        content=audio_respuesta.content,
        media_type="audio/wav",
    )