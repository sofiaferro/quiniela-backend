"""Diccionario de La Tirada: símbolo -> número y sinónimos."""

QUINIELA: dict[str, str] = {
    "huevos": "00", "agua": "01", "nino": "02", "san cono": "03", "cama": "04",
    "gato": "05", "perro": "06", "revolver": "07", "incendio": "08", "arroyo": "09",
    "leche": "10", "palito": "11", "soldado": "12", "yeta": "13", "borracho": "14",
    "nina bonita": "15", "anillo": "16", "desgracia": "17", "sangre": "18", "pescado": "19",
    "fiesta": "20", "mujer": "21", "loco": "22", "mariposa": "23", "caballo": "24",
    "gallina": "25", "misa": "26", "peine": "27", "cerro": "28", "san pedro": "29",
    "santa rosa": "30", "luz": "31", "dinero": "32", "cristo": "33", "cabeza": "34",
    "pajarito": "35", "manteca": "36", "dentista": "37", "aceite": "38", "lluvia": "39",
    "cura": "40", "cucha": "41", "zapatilla": "42", "balcon": "43", "carcel": "44",
    "vino": "45", "tomates": "46", "muerto": "47", "muerto habla": "48", "carne": "49",
    "pan": "50", "serrucho": "51", "madre": "52", "barco": "53", "vaca": "54",
    "gallegos": "55", "caida": "56", "jorobado": "57", "ahogado": "58", "planta": "59",
    "virgen": "60", "escopeta": "61", "inundacion": "62", "casamiento": "63", "llanto": "64",
    "cazador": "65", "lombrices": "66", "vibora": "67", "sobrinos": "68", "vicios": "69",
    "muerto suenos": "70", "excremento": "71", "sorpresa": "72", "hospital": "73", "negros": "74",
    "payaso": "75", "llamas": "76", "piernas": "77", "ramera": "78", "ladron": "79",
    "bocha": "80", "flores": "81", "pelea": "82", "mal tiempo": "83", "iglesia": "84",
    "linterna": "85", "humo": "86", "piojos": "87", "papa": "88", "rata": "89",
    "miedo": "90", "excusado": "91", "medico": "92", "enamorado": "93", "cementerio": "94",
    "anteojos": "95", "marido": "96", "mesa": "97", "lavandera": "98", "hermanos": "99",
}

SYNONYMS: dict[str, str] = {
    "gatito": "gato", "gatita": "gato", "gata": "gato", "michi": "gato",
    "perrito": "perro", "perrita": "perro", "perra": "perro", "can": "perro",
    "caballito": "caballo",
    "pajaro": "pajarito", "ave": "pajarito",
    "vaquita": "vaca",
    "ratita": "rata", "raton": "rata", "ratoncito": "rata",
    "florecita": "flores", "flor": "flores", "rosa": "flores",
    "plantita": "planta", "arbolito": "planta", "arbol": "planta",
    "viborita": "vibora", "serpiente": "vibora", "culebra": "vibora",
    "mama": "madre", "mami": "madre", "vieja": "madre",
    "nene": "nino", "chico": "nino", "bebe": "nino", "nena": "nino",
    "plata": "dinero", "billete": "dinero", "pesos": "dinero", "guita": "dinero",
    "mar": "agua", "oceano": "agua", "rio": "agua", "lago": "agua", "pileta": "agua",
    "difunto": "muerto", "fallecido": "muerto", "cadaver": "muerto",
    "hogar": "cama", "departamento": "cama", "casa": "cama",
    "boda": "casamiento", "matrimonio": "casamiento",
    "templo": "iglesia", "capilla": "iglesia",
    "doctor": "medico", "doctora": "medico",
    "esposo": "marido",
    "herman": "hermanos", "hermana": "hermanos", "hermano": "hermanos",
    "susto": "miedo", "terror": "miedo", "panico": "miedo",
    "llorar": "llanto", "lagrima": "llanto", "lagrimas": "llanto",
    "fuego": "incendio", "llama": "llamas",
    "jardin": "flores",
}


def normalizar_simbolo(palabra: str) -> str | None:
    """Dado una palabra, devuelve el símbolo canónico de la quiniela o None."""
    palabra = palabra.lower().strip()
    if palabra in QUINIELA:
        return palabra
    if palabra in SYNONYMS:
        return SYNONYMS[palabra]
    return None