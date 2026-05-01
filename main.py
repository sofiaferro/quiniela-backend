from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from openai import OpenAI
import os
import time

from quiniela.interprete import interpretar_sueno, construir_respuesta_hablada

app = FastAPI()

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/voice")
async def voice(audio: UploadFile = File(...)):
    t_start = time.time()

    # 1. STT
    audio_bytes = await audio.read()
    t_stt_start = time.time()
    transcription = client.audio.transcriptions.create(
        model="whisper-1",
        file=("audio.wav", audio_bytes, "audio/wav"),
        language="es",
    )
    t_stt = time.time() - t_stt_start
    sueno = transcription.text
    print(f"\n⏱️  STT (whisper-1): {t_stt:.2f}s")
    print(f"🌙 Sueño: {sueno}")

    # 2. LLM
    t_llm_start = time.time()
    resultado = interpretar_sueno(sueno, client)
    t_llm = time.time() - t_llm_start
    print(f"⏱️  LLM (gpt-4o-mini): {t_llm:.2f}s")
    print(f"🎯 Símbolos: {resultado['simbolos']} → {resultado['numeros']}")
    print(f"🎲 Jugada: {resultado['jugada']}")

    # 3. TTS streaming
    respuesta_texto = construir_respuesta_hablada(resultado)
    t_tts_start = time.time()

    def stream_audio():
        state = {"first_chunk_time": None}
        with client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice="nova",
            input=respuesta_texto,
            response_format="mp3",
        ) as response:
            for chunk in response.iter_bytes(chunk_size=4096):
                if state["first_chunk_time"] is None:
                    state["first_chunk_time"] = time.time() - t_tts_start
                    print(f"⏱️  TTS primer chunk: {state['first_chunk_time']:.2f}s")
                    print(f"⏱️  TOTAL hasta primer chunk: {time.time() - t_start:.2f}s")
                yield chunk
        print(f"⏱️  TTS streaming completo: {time.time() - t_tts_start:.2f}s")

    return StreamingResponse(
        stream_audio(),
        media_type="audio/mpeg",
    )