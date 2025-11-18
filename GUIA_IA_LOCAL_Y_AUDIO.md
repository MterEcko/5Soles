# Guía IA Local y Generación de Audio/Voces
## Portales del Quinto Sol - NPCs con Voz

---

## 🤖 LLM Local para Conversaciones NPC

### ¿Qué tan potente necesito?

**RESPUESTA CORTA:** No necesitas GPU potente. Un modelo **Llama 3.1 8B** o **Mistral 7B** es suficiente para NPCs.

### Especificaciones Recomendadas

#### Opción 1: Solo CPU (Accesible) ✅

**Hardware mínimo:**
- CPU: 4+ cores (Intel i5/Ryzen 5 o superior)
- RAM: 16 GB (8 GB modelo + 8 GB sistema)
- Almacenamiento: 10 GB para modelos

**Modelos recomendados:**
- `llama3.1:8b` - 4.7 GB
- `mistral:7b` - 4.1 GB
- `phi3:mini` - 2.3 GB (muy rápido, suficiente para NPCs)

**Performance:**
- Respuesta: 2-5 segundos
- Tokens/seg: 10-30 (CPU)
- Aceptable para chat de NPCs

#### Opción 2: GPU (Óptimo) 🚀

**Hardware recomendado:**
- GPU: NVIDIA con 6+ GB VRAM (GTX 1660, RTX 3060, etc.)
- RAM: 16 GB
- VRAM: 6-8 GB

**Modelos recomendados:**
- `llama3.1:8b` - 4.7 GB VRAM
- `mistral:7b-instruct` - 4.1 GB VRAM
- `neural-chat:7b` - 4.1 GB VRAM

**Performance:**
- Respuesta: 0.5-2 segundos
- Tokens/seg: 50-100 (GPU)
- Experiencia fluida

### Instalación Ollama (Recomendado)

Ollama es la forma MÁS FÁCIL de correr LLMs localmente.

#### Linux/Mac

```bash
# Instalar Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Iniciar servicio
ollama serve

# Descargar modelo (en otra terminal)
ollama pull llama3.1:8b

# Probar
ollama run llama3.1:8b "Hola, soy un NPC de Portales del Quinto Sol"
```

#### Windows

1. Descargar instalador: https://ollama.com/download/windows
2. Ejecutar instalador
3. Abrir terminal y ejecutar:

```bash
ollama pull llama3.1:8b
ollama run llama3.1:8b
```

### Integración con Python

```bash
# Instalar cliente Python
pip install ollama
```

```python
import ollama

def npc_responder(contexto: str, mensaje_jugador: str) -> str:
    """Genera respuesta de NPC usando LLM local"""

    prompt = f"""Eres un NPC en el MMORPG "Portales del Quinto Sol".

Contexto del NPC: {contexto}

Jugador dice: {mensaje_jugador}

Responde como el NPC (máximo 2-3 oraciones, tono amigable):"""

    response = ollama.chat(
        model='llama3.1:8b',
        messages=[{
            'role': 'user',
            'content': prompt
        }],
        options={
            'temperature': 0.7,
            'max_tokens': 150
        }
    )

    return response['message']['content']

# Ejemplo
contexto = "Herrero tolteca llamado Xolotl, 45 años, sabio y experimentado"
mensaje = "¿Puedes forjarme una espada?"

respuesta = npc_responder(contexto, mensaje)
print(respuesta)
# → "Ah, joven guerrero, por supuesto. Una espada de obsidiana
#    te costará 50 monedas de jade. ¿Qué estilo prefieres?"
```

---

## 🎙️ Generación de Voces (TTS - Text-to-Speech)

### Opciones para Audio Local

#### Opción 1: Coqui TTS (Recomendado) ✅

**Ventajas:**
- ✅ 100% local
- ✅ Voces en español
- ✅ Clonación de voz (puedes crear voces únicas por NPC)
- ✅ Calidad alta

**Instalación:**

```bash
pip install TTS

# Listar modelos disponibles
tts --list_models

# Modelo español recomendado
tts --text "Hola viajero" --model_name "tts_models/es/css10/vits" --out_path output.wav
```

**Uso con Python:**

```python
from TTS.api import TTS

# Inicializar (una vez)
tts = TTS(model_name="tts_models/es/css10/vits")

# Generar audio
tts.tts_to_file(
    text="Bienvenido a Tenochtitlan, viajero",
    file_path="npc_saludo.wav"
)
```

**Clonación de Voz (Voces Únicas por NPC):**

```python
# Usar modelo multi-speaker
tts = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts")

# Generar con voz específica
tts.tts_to_file(
    text="Soy Xolotl el herrero",
    speaker="speaker_1",  # Cada NPC puede tener su speaker_id
    file_path="xolotl_voz.wav"
)
```

#### Opción 2: Piper (Más Rápido)

**Ventajas:**
- ✅ MUY rápido (tiempo real)
- ✅ Bajo uso de recursos
- ✅ Voces en español

**Instalación:**

```bash
pip install piper-tts

# Descargar modelo español
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_ES/carlfm/medium/es_ES-carlfm-medium.onnx
wget https://huggingface.co/rhasspy/piper-voices/resolve/main/es/es_ES/carlfm/medium/es_ES-carlfm-medium.onnx.json
```

**Uso:**

```bash
echo "Bienvenido aventurero" | piper \
  --model es_ES-carlfm-medium.onnx \
  --output_file output.wav
```

#### Opción 3: Bark (Voz Más Natural)

**Ventajas:**
- ✅ Voz MUY natural
- ✅ Emociones (risa, suspiro, etc.)
- ✅ Multilingüe

**Desventaja:**
- ❌ Más lento (no tiempo real)
- ❌ Requiere GPU

**Instalación:**

```bash
pip install bark
```

**Uso:**

```python
from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav

# Cargar modelos
preload_models()

# Generar con emoción
text_prompt = "[es_speaker_5] Bienvenido viajero, ¿buscas comerciar? [laughs]"
audio_array = generate_audio(text_prompt)

# Guardar
write_wav("npc_comerciante.wav", SAMPLE_RATE, audio_array)
```

---

## 🎮 Integración Completa: LLM + TTS

### Sistema Completo NPC con Voz

```python
import ollama
from TTS.api import TTS
import uuid

class NPCConVoz:
    """NPC con IA local y generación de voz"""

    def __init__(self, npc_id: int, nombre: str, contexto: str):
        self.npc_id = npc_id
        self.nombre = nombre
        self.contexto = contexto

        # LLM para texto
        self.llm_model = "llama3.1:8b"

        # TTS para voz
        self.tts = TTS(model_name="tts_models/es/css10/vits")

    def responder_con_voz(self, mensaje_jugador: str) -> tuple[str, str]:
        """
        Genera respuesta de texto + audio

        Returns:
            (texto_respuesta, ruta_audio)
        """
        # 1. Generar respuesta con LLM
        prompt = f"""Eres {self.nombre}, un NPC en Portales del Quinto Sol.

Contexto: {self.contexto}

Jugador: {mensaje_jugador}

Responde brevemente (máximo 2 oraciones):"""

        response = ollama.chat(
            model=self.llm_model,
            messages=[{'role': 'user', 'content': prompt}],
            options={'temperature': 0.7, 'max_tokens': 100}
        )

        texto = response['message']['content']

        # 2. Generar audio con TTS
        audio_path = f"audio/npc_{self.npc_id}_{uuid.uuid4().hex[:8]}.wav"
        self.tts.tts_to_file(text=texto, file_path=audio_path)

        return texto, audio_path

# Uso
npc = NPCConVoz(
    npc_id=123,
    nombre="Xolotl",
    contexto="Herrero tolteca de 45 años, sabio y experimentado"
)

texto, audio = npc.responder_con_voz("¿Puedes forjarme una espada?")

print(f"Texto: {texto}")
print(f"Audio: {audio}")
# → Texto: "Claro guerrero, una espada de obsidiana te costará 50 jade..."
# → Audio: audio/npc_123_a4f8b2c1.wav
```

---

## 📊 Comparativa de Opciones

### LLMs

| Modelo | Tamaño | RAM | GPU | Velocidad CPU | Calidad |
|--------|--------|-----|-----|---------------|---------|
| phi3:mini | 2.3 GB | 8 GB | No | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| mistral:7b | 4.1 GB | 8 GB | No | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| llama3.1:8b | 4.7 GB | 16 GB | No | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| llama3.1:8b | 4.7 GB | 16 GB | Sí (6GB) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |

### TTS

| Sistema | Velocidad | Calidad | GPU | Voces ES | Clonación |
|---------|-----------|---------|-----|----------|-----------|
| Piper | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | No | ✅ | ❌ |
| Coqui TTS | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | No | ✅ | ✅ |
| Bark | ⭐⭐ | ⭐⭐⭐⭐⭐ | Sí | ✅ | ✅ |

---

## 🚀 Recomendación para Tu Proyecto

### Setup Óptimo (Balanceado)

**Para NPCs:**

1. **LLM:** `llama3.1:8b` con Ollama
   - Suficiente para conversaciones de NPCs
   - Funciona bien en CPU
   - Con GPU: experiencia fluida

2. **TTS:** Coqui TTS (`tts_models/es/css10/vits`)
   - Buen balance velocidad/calidad
   - Voces en español
   - No requiere GPU

3. **Caché de Audio:**
   - Pre-generar frases comunes
   - Ejemplo: "Bienvenido", "Adiós", "¿En qué te ayudo?"
   - Genera solo respuestas dinámicas

### Optimización para Producción

```python
class SistemaVocesOptimizado:
    """Sistema optimizado con caché de audio"""

    def __init__(self):
        self.tts = TTS(model_name="tts_models/es/css10/vits")
        self.cache_audio = {}  # {texto: ruta_audio}

        # Pre-generar frases comunes
        self.frases_comunes = [
            "Bienvenido viajero",
            "Adiós, que los dioses te acompañen",
            "No tengo eso en stock",
            "Eso cuesta mucho oro"
        ]

        self.pregenerar_comunes()

    def pregenerar_comunes(self):
        """Pre-genera audio de frases comunes"""
        for frase in self.frases_comunes:
            audio_path = f"audio/cache/{hash(frase)}.wav"
            self.tts.tts_to_file(text=frase, file_path=audio_path)
            self.cache_audio[frase] = audio_path

    def obtener_audio(self, texto: str) -> str:
        """Obtiene audio (desde caché o genera nuevo)"""
        if texto in self.cache_audio:
            return self.cache_audio[texto]  # Instantáneo

        # Generar nuevo
        audio_path = f"audio/dynamic/{uuid.uuid4().hex}.wav"
        self.tts.tts_to_file(text=texto, file_path=audio_path)
        return audio_path
```

---

## 💰 Costos

### Opción Cloud (Para Comparar)

- **OpenAI TTS:** $15/millón de caracteres
- **ElevenLabs:** $22/mes (30k caracteres)
- **Azure TTS:** $16/millón de caracteres

**Con 100k NPCs conversando:**
- Costo mensual: $500-1000+ 💸

### Opción Local (Tu Caso)

- **Hardware:** Una vez ($0 si ya tienes PC)
- **Electricidad:** ~$5-10/mes
- **Mantenimiento:** $0
- **Escalabilidad:** Ilimitada

**Ahorros:** ~$5,000-10,000/año 💰✅

---

## 📝 Resumen Ejecutivo

### Para Portales del Quinto Sol:

**LLM:** `llama3.1:8b` (Ollama)
- ✅ Gratis, local, suficiente calidad
- ✅ No necesitas GPU potente
- ✅ 16 GB RAM suficiente

**TTS:** Coqui TTS
- ✅ Voces en español
- ✅ Clonación de voz (NPCs únicos)
- ✅ No requiere GPU

**Optimización:**
- Pre-generar frases comunes
- Caché de audio
- Generar solo respuestas dinámicas

**Hardware mínimo:**
- CPU: 4+ cores
- RAM: 16 GB
- GPU: Opcional (mejora velocidad)
- Almacenamiento: 20 GB

---

## 🔗 Referencias

- **Ollama:** https://ollama.com
- **Coqui TTS:** https://github.com/coqui-ai/TTS
- **Piper:** https://github.com/rhasspy/piper
- **Bark:** https://github.com/suno-ai/bark
- **Llama 3.1:** https://ollama.com/library/llama3.1

---

_Última actualización: 2025_
_Portales del Quinto Sol - MMORPG_
