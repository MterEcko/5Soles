# ¿Necesito LLM Potente? NO ❌

## Respuesta Rápida

### Hardware Suficiente

**✅ Esto funciona perfectamente:**
- CPU: i5 / Ryzen 5 (4 cores)
- RAM: **16 GB**
- GPU: **NO necesaria**
- Disco: 10 GB

**¿Por qué NO necesitas mucho?**

Los NPCs solo dicen frases cortas:
```
Jugador: "¿Vendes espadas?"
NPC: "Sí, tengo espadas de obsidiana por 50 jade"
     ↑ Solo 9 palabras
```

No es ChatGPT escribiendo ensayos, es un NPC en un juego 🎮

---

## ⚡ Instalación Rápida (5 minutos)

### LLM (Ollama)

```bash
# Instalar Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Descargar modelo (elige uno)
ollama pull llama3.1:8b      # Recomendado (4.7 GB)
ollama pull phi3:mini        # Más rápido (2.3 GB)
ollama pull mistral:7b       # Muy bueno (4.1 GB)

# Instalar Python client
pip install ollama
```

### TTS (Voces)

```bash
pip install TTS
```

---

## 🧪 Prueba Ahora (2 minutos)

### Test LLM

```bash
python3 demo_llm_local.py
```

**Qué verás:**
- ✅ Conversación con NPC
- ✅ NPC con memoria
- ✅ Múltiples personalidades
- ✅ Medición de velocidad

**Tiempo esperado:**
- Sin GPU: 2-5 segundos/respuesta ✅ ACEPTABLE
- Con GPU: 0.5-2 segundos/respuesta ✅ EXCELENTE

### Test Audio

```bash
python3 demo_audio_voces.py
```

**Qué verás:**
- ✅ Generación de voz en español
- ✅ Múltiples voces
- ✅ Sistema con caché
- ✅ Archivos WAV generados en `audio_demo/`

---

## 📊 Comparativa

### Modelos Recomendados

| Modelo | RAM | GPU | Calidad NPCs | Velocidad CPU |
|--------|-----|-----|--------------|---------------|
| **phi3:mini** | 8 GB | No | ⭐⭐⭐ Buena | ⭐⭐⭐⭐⭐ Muy rápido |
| **llama3.1:8b** | 16 GB | No | ⭐⭐⭐⭐⭐ Excelente | ⭐⭐⭐ Bueno |
| **mistral:7b** | 16 GB | No | ⭐⭐⭐⭐ Muy buena | ⭐⭐⭐⭐ Rápido |

**Recomendación:** `llama3.1:8b` si tienes 16 GB RAM

### TTS (Voces)

| Sistema | GPU | Calidad | Velocidad | Español |
|---------|-----|---------|-----------|---------|
| **Coqui TTS** | No | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ |
| Piper | No | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ✅ |
| Bark | Sí | ⭐⭐⭐⭐⭐ | ⭐⭐ | ✅ |

**Recomendación:** Coqui TTS (balance perfecto)

---

## 💰 Costos

### Opción Cloud ❌

**Con 100,000 NPCs conversando:**
- OpenAI: ~$500-1,000/mes
- ElevenLabs: ~$300-500/mes
- **TOTAL AL AÑO: $6,000-18,000** 💸

### Opción Local ✅

**Hardware:**
- PC que ya tienes: $0
- Electricidad: ~$5-10/mes
- **TOTAL AL AÑO: $60-120** 💰

**AHORRO: $5,880-17,880/año** 🎉

---

## 🎯 Ejemplo Completo

```python
import ollama
from TTS.api import TTS

# 1. NPC genera respuesta con LLM
response = ollama.chat(
    model='llama3.1:8b',
    messages=[{
        'role': 'user',
        'content': 'Eres Xolotl el herrero. Jugador pregunta: ¿Vendes armas?'
    }]
)

texto = response['message']['content']
# → "Sí viajero, tengo espadas de obsidiana por 50 jade"

# 2. Generar voz
tts = TTS(model_name='tts_models/es/css10/vits')
tts.tts_to_file(text=texto, file_path='xolotl_respuesta.wav')

# 3. Enviar al jugador
return {
    'texto': texto,
    'audio': 'xolotl_respuesta.wav'
}
```

**Tiempo total:** 3-6 segundos (aceptable para juego)

---

## ✅ Checklist

- [ ] Tengo 16 GB RAM
- [ ] CPU de 4+ cores
- [ ] Ollama instalado (`curl -fsSL https://ollama.com/install.sh | sh`)
- [ ] Modelo descargado (`ollama pull llama3.1:8b`)
- [ ] TTS instalado (`pip install TTS`)
- [ ] Probé demos (`python3 demo_llm_local.py`)

---

## ❓ FAQ

**P: ¿Necesito NVIDIA?**
R: NO. Funciona en CPU. GPU solo acelera.

**P: ¿Funciona en Mac/AMD?**
R: SÍ. Ollama funciona en Mac (M1/M2 excelente) y AMD.

**P: ¿Qué tan buena es la calidad?**
R: Suficiente para NPCs. Pruébalo: `python3 demo_llm_local.py`

**P: ¿Cuántos NPCs soporta?**
R: Miles. Es procesamiento secuencial (1 a la vez).

**P: ¿Funciona offline?**
R: 100% offline después de descargar modelos.

**P: ¿Qué tan difícil es integrarlo?**
R: Muy fácil. Ver `sistema_conversaciones_npcs.py`

---

## 🚀 Siguiente Paso

**Prueba ahora:**

```bash
# 1. Instalar Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Descargar modelo
ollama pull llama3.1:8b

# 3. Instalar TTS
pip install TTS ollama

# 4. Probar
python3 demo_llm_local.py
python3 demo_audio_voces.py
```

**Tiempo total:** 10-15 minutos (incluye descarga de 4.7 GB)

---

## 💡 Conclusión

### ❌ NO NECESITAS:
- GPU potente
- Más de 16 GB RAM
- Pagar servicios cloud
- Internet después de setup

### ✅ SÍ NECESITAS:
- PC normal (16 GB RAM)
- 10 GB espacio disco
- 15 minutos para setup
- Probar con las demos

**¡Es más fácil de lo que pensabas!** 🎉

---

_Prueba las demos y verás que funciona perfectamente_ 😊
