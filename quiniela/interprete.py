"""Interpreta sueños usando GPT y los mapea al diccionario de La Tirada."""

import json
from openai import OpenAI
from .diccionario import QUINIELA, SYNONYMS, normalizar_simbolo


def construir_prompt() -> str:
    """Arma el system prompt con el diccionario completo."""
    simbolos_validos = sorted(QUINIELA.keys())
    
    return f"""Sos un experto en La Tirada, la tradición argentina de interpretar sueños para jugar a la quiniela.

Te voy a contar un sueño. Tu trabajo es identificar **exactamente DOS símbolos** del sueño que aparezcan en este diccionario de la quiniela:

{', '.join(simbolos_validos)}

Reglas estrictas:
1. Devolvés SOLO los dos símbolos más importantes/centrales del sueño.
2. Si el sueño usa una palabra distinta pero conceptualmente equivalente (ej: "boda" en vez de "casamiento", "fuego" en vez de "incendio"), devolvé el símbolo canónico del diccionario.
3. Si en el sueño aparecen menos de dos símbolos claros, podés inferir el segundo del tono general (ej: si el sueño es angustiante, "miedo" o "desgracia").
4. Si aparecen más de dos, elegí los dos MÁS centrales/frecuentes de la narrativa.

Devolvé EXACTAMENTE este JSON, sin texto adicional:
{{
  "simbolos": ["simbolo1", "simbolo2"],
  "razonamiento": "una oración breve explicando por qué esos dos"
}}"""


def interpretar_sueno(sueno: str, client: OpenAI) -> dict:
    """
    Recibe un sueño en texto, devuelve dict con símbolos, números y jugada.
    
    Returns:
        {
          "sueno": str,
          "simbolos": [str, str],
          "numeros": [str, str],
          "jugada": str,
          "razonamiento": str,
        }
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": construir_prompt()},
            {"role": "user", "content": sueno},
        ],
        response_format={"type": "json_object"},
        temperature=0.7,
    )
    
    data = json.loads(response.choices[0].message.content)
    simbolos_raw = data.get("simbolos", [])
    razonamiento = data.get("razonamiento", "")
    
    # Mapear símbolos a números, usando sinónimos si hace falta
    simbolos_canonicos = []
    numeros = []
    for s in simbolos_raw[:2]:
        canonico = normalizar_simbolo(s)
        if canonico and canonico in QUINIELA:
            simbolos_canonicos.append(canonico)
            numeros.append(QUINIELA[canonico])
    
    if len(numeros) < 2:
        # Fallback: si el LLM falló, devolver algo válido
        simbolos_canonicos = ["yeta", "miedo"]
        numeros = ["13", "90"]
        razonamiento = "No pude identificar símbolos claros en tu sueño."
    
    jugada = numeros[0] + numeros[1]
    
    return {
        "sueno": sueno,
        "simbolos": simbolos_canonicos,
        "numeros": numeros,
        "jugada": jugada,
        "razonamiento": razonamiento,
    }


def construir_respuesta_hablada(resultado: dict) -> str:
    """Arma el texto que va a leer el TTS."""
    s1, s2 = resultado["simbolos"]
    n1, n2 = resultado["numeros"]
    jugada = resultado["jugada"]
    
    return (
        f"En tu sueño veo dos símbolos: {s1}, que es el {n1}, "
        f"y {s2}, que es el {n2}. "
        f"Tu jugada para la quiniela: {jugada}. "
        f"O en pares: {n1} y {n2}."
    )