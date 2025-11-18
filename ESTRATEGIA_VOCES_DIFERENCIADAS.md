# Estrategia de Voces Diferenciadas
## 270,000 NPCs con Voces Únicas

---

## 🎯 Tu Propuesta vs Solución Optimizada

### ❌ Propuesta Inicial: 200 voces fijas

```
200 voces (100 hombres, 100 mujeres)
270,000 NPCs / 200 voces = 1,350 NPCs por voz
```

**Problemas:**
- Muy repetitivo (1,350 NPCs idénticos)
- Sin variación de edad/tono
- Limitado para NPCs importantes

### ✅ Solución Optimizada: Sistema de 3 Tiers

```
Base: 30 voces (15M, 15F)
Variaciones: pitch × 5, speed × 5
Total: 30 × 5 × 5 = 750 combinaciones diferentes

+ Clonación de voz para NPCs únicos
= Voces prácticamente infinitas
```

---

## 🎭 Sistema de 3 Tiers

### Tier 1: NPCs Únicos (1-5% del total que hablan)

**¿Quiénes?**
- Quest-givers principales
- Personajes de historia
- Jefes de facción
- NPCs únicos con nombre

**Tecnología:** Clonación de voz (XTTS v2)

**¿Cómo funciona?**
```python
# Requiere solo 6 segundos de audio de referencia
referencia_audio = "samples/xolotl_sample.wav"  # 6 segundos

xtts.tts_to_file(
    text="Soy Xolotl el Herrero",
    speaker_wav=referencia_audio,  # Clona esta voz
    file_path="xolotl_voz.wav"
)
```

**Resultado:** Voz completamente única, imposible de confundir

**Cantidad:** ~100-500 NPCs (los más importantes)

---

### Tier 2: NPCs Importantes (10-15% del total que hablan)

**¿Quiénes?**
- Comerciantes principales
- Guardias con misiones
- NPCs con funciones específicas
- Líderes locales

**Tecnología:** Pool de 50-100 voces diferentes

**¿Cómo funciona?**
```python
# Combinación de voz base + variaciones
30 voces base × 5 pitch × 5 speed = 750 combinaciones

# Ejemplo:
voz = 'hombre_05'           # Voz base
pitch = 1.15               # 15% más agudo
speed = 0.95               # 5% más lento

→ Voz única y diferente
```

**Cantidad:** ~1,000-5,000 NPCs

---

### Tier 3: NPCs Comunes (80-85% del total que hablan)

**¿Quiénes?**
- Campesinos genéricos
- Guardias sin misión
- Población de fondo

**Tecnología:** 20-30 voces con variaciones menores

**¿Cómo funciona?**
```python
# Subset de voces base + variaciones limitadas
10 voces base × 3 pitch × 3 speed = 90 combinaciones

→ Suficiente variedad para NPCs comunes
```

**Cantidad:** ~8,000-40,000 NPCs (del total que hablan)

---

## 📊 Distribución Real

### De 270,000 NPCs:

```
┌──────────────────────────────────────────────────┐
│  NO HABLAN CON JUGADORES (90%)     243,000       │
│  ████████████████████████████████████████████    │
│  Sin voz (solo población simulada)               │
└──────────────────────────────────────────────────┘

┌────────────────────────┐
│  COMUNES (8%)  21,600  │
│  ████████████████      │
│  20-30 voces base      │
└────────────────────────┘

┌──────────┐
│  IMPORT  │
│  (1.5%)  │
│  4,000   │
│  ████    │
│  50-100  │
│  voces   │
└──────────┘

┌──┐
│Ú │
│N │
│I │
│C │
│O │
│S │
│  │
│400│
│⭐│
└──┘
```

**Voces necesarias:**
- NPCs únicos: 400 voces clonadas
- NPCs importantes: ~100 combinaciones diferentes
- NPCs comunes: ~30 combinaciones

**Total efectivo: ~530 voces diferentes** (no 200 fijas)

---

## 🎤 Voces Base Recomendadas

### 15 Voces Masculinas

| ID | Tono | Edad | Modelo | Uso |
|----|------|------|--------|-----|
| hombre_01 | Grave | Adulto | Coqui | Guerreros, herreros |
| hombre_02 | Normal | Adulto | Coqui | Comerciantes |
| hombre_03 | Agudo | Adulto | Coqui | Escribas |
| hombre_04 | Grave | Joven | Coqui | Aprendices |
| hombre_05 | Normal | Joven | Coqui | Mensajeros |
| hombre_06 | Grave | Anciano | Coqui | Sabios |
| hombre_07 | Normal | Anciano | Coqui | Sacerdotes |
| hombre_08 | Agudo | Joven | XTTS | Nobles jóvenes |
| hombre_09 | Normal | Adulto | XTTS | Capitanes |
| hombre_10 | Grave | Adulto | XTTS | Líderes |
| hombre_11 | Agudo | Adulto | Bark | Artistas |
| hombre_12 | Normal | Joven | Bark | Exploradores |
| hombre_13 | Grave | Joven | Bark | Soldados |
| hombre_14 | Agudo | Anciano | Coqui | Maestros |
| hombre_15 | Normal | Anciano | XTTS | Consejeros |

### 15 Voces Femeninas

| ID | Tono | Edad | Modelo | Uso |
|----|------|------|--------|-----|
| mujer_01 | Grave | Adulto | Coqui | Guerreras |
| mujer_02 | Normal | Adulto | Coqui | Comerciantes |
| mujer_03 | Agudo | Adulto | Coqui | Curanderas |
| mujer_04 | Grave | Joven | Coqui | Aprendices |
| mujer_05 | Normal | Joven | Coqui | Mensajeras |
| mujer_06 | Grave | Anciano | Coqui | Sabias |
| mujer_07 | Normal | Anciano | Coqui | Sacerdotisas |
| mujer_08 | Agudo | Joven | XTTS | Nobles jóvenes |
| mujer_09 | Normal | Adulto | XTTS | Líderes |
| mujer_10 | Grave | Adulto | XTTS | Comandantes |
| mujer_11 | Agudo | Adulto | Bark | Artistas |
| mujer_12 | Normal | Joven | Bark | Exploradoras |
| mujer_13 | Grave | Joven | Bark | Soldadas |
| mujer_14 | Agudo | Anciano | Coqui | Maestras |
| mujer_15 | Normal | Anciano | XTTS | Consejeras |

---

## 🔧 Variaciones de Voz

### Pitch (Tono)

```python
pitch_variations = {
    0.85: 'Muy grave',
    0.95: 'Grave',
    1.00: 'Normal',
    1.05: 'Agudo',
    1.15: 'Muy agudo'
}

# Ejemplo:
voz_base = 'hombre_02'  # Tono normal
pitch = 1.15            # +15% = Más agudo
→ Suena diferente pero natural
```

### Speed (Velocidad)

```python
speed_variations = {
    0.90: 'Lento (anciano, cansado)',
    0.95: 'Pausado',
    1.00: 'Normal',
    1.05: 'Rápido',
    1.10: 'Muy rápido (joven, nervioso)'
}

# Ejemplo:
voz_base = 'mujer_07'   # Anciana
speed = 0.90            # -10% = Más lento
→ Suena como anciana hablando
```

### Combinaciones

```
1 voz base × 5 pitch × 5 speed = 25 variaciones diferentes

30 voces base × 25 variaciones = 750 combinaciones totales
```

---

## 💻 Implementación

### Asignación Determinista

**Crítico:** El MISMO NPC siempre debe tener la MISMA voz

```python
def asignar_voz(npc_id, npc_genero, npc_edad):
    """
    Usa npc_id como seed para determinismo
    Mismo NPC = Misma voz siempre
    """

    # Seed basado en ID
    seed = npc_id

    # Seleccionar voz base (determinista)
    voces_genero = filtrar_por_genero_edad(npc_genero, npc_edad)
    voz_base = random.Random(seed).choice(voces_genero)

    # Seleccionar variaciones (determinista)
    pitch = random.Random(seed + 1).choice([0.85, 0.95, 1.0, 1.05, 1.15])
    speed = random.Random(seed + 2).choice([0.90, 0.95, 1.0, 1.05, 1.10])

    return ConfiguracionVoz(voz_base, pitch, speed)
```

### Clonación de Voz (NPCs Únicos)

```python
from TTS.api import TTS

# Inicializar XTTS v2 (soporta clonación)
tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")

# Clonar voz de Xolotl
tts.tts_to_file(
    text="Bienvenido a mi herrería, viajero",
    speaker_wav="samples/xolotl_6seg.wav",  # Solo 6 segundos de referencia
    language="es",
    file_path="xolotl_saludo.wav"
)

# Resultado: Voz única de Xolotl
# Todas sus frases sonarán con la MISMA voz única
```

### Aplicar Variaciones

```python
def generar_con_variaciones(texto, config_voz, output_path):
    """Genera audio aplicando pitch y speed"""

    # 1. Generar audio base
    tts.tts_to_file(
        text=texto,
        speaker=config_voz.voz_base,
        file_path=temp_path
    )

    # 2. Aplicar pitch (librosa)
    import librosa
    import soundfile as sf

    y, sr = librosa.load(temp_path)

    # Aplicar pitch shift
    n_steps = (config_voz.pitch - 1.0) * 12  # Convertir a semitonos
    y_pitched = librosa.effects.pitch_shift(y, sr=sr, n_steps=n_steps)

    # Aplicar time stretch (speed)
    y_final = librosa.effects.time_stretch(y_pitched, rate=config_voz.speed)

    # Guardar
    sf.write(output_path, y_final, sr)
```

---

## 📈 Escalabilidad

### ¿Funciona con 270,000 NPCs?

**SÍ ✅**

**Por qué:**
1. Solo ~27,000 NPCs hablarán con jugadores (10%)
2. De esos:
   - 400 son únicos (clonación)
   - 4,000 son importantes (100 voces)
   - 22,600 son comunes (30 voces)

3. **Total voces necesarias: ~530**

### Distribución Real

Con 1000 jugadores online simultáneos:

```
NPCs hablados en sesión: ~10,000
Voces únicas usadas: ~300-400

Promedio NPCs por voz: 25-33
→ Suficiente variedad ✅
```

---

## 🎯 Comparativa Final

### Opción A: 200 Voces Fijas (Tu propuesta inicial)

```
✅ Simple de implementar
❌ 1,350 NPCs por voz (muy repetitivo)
❌ Sin variaciones de edad/tono
❌ Todos suenan muy similares
```

### Opción B: Sistema de 3 Tiers (Recomendado)

```
✅ 750 combinaciones posibles
✅ NPCs únicos tienen voces únicas
✅ Variaciones naturales (edad, tono)
✅ Escalable a 270,000 NPCs
✅ Promedio 25-33 NPCs por voz
✅ Experiencia inmersiva
```

---

## 🚀 Instalación

### Modelos TTS Necesarios

```bash
# Coqui TTS (voces base)
pip install TTS

# XTTS v2 (clonación de voz para únicos)
# Ya incluido en TTS

# Librosa (pitch/speed)
pip install librosa soundfile

# Descargar modelo
python -c "from TTS.api import TTS; TTS('tts_models/multilingual/multi-dataset/xtts_v2')"
```

### Crear Samples de Referencia

Para NPCs únicos, necesitas audio de 6+ segundos:

```bash
# Grabar o usar TTS para crear sample base
python -c "
from TTS.api import TTS
tts = TTS('tts_models/es/css10/vits')
tts.tts_to_file('Soy Xolotl el herrero, maestro de la obsidiana', 'xolotl_sample.wav')
"

# Usar ese sample para clonar
```

---

## 💡 Recomendaciones

### Para NPCs Únicos (400)
- ✅ Usar XTTS v2 con clonación
- ✅ Crear samples de 6-10 segundos
- ✅ Cachear permanentemente

### Para NPCs Importantes (4,000)
- ✅ Pool de 50-100 voces
- ✅ Variaciones de pitch/speed
- ✅ Cache LRU

### Para NPCs Comunes (22,000)
- ✅ 20-30 voces base
- ✅ Variaciones menores
- ✅ Fallback a texto si ocupado

---

## ✅ Conclusión

**Tu idea de 200 voces está bien para empezar, pero:**

### Mejor estrategia:

1. **Base:** 30 voces (15M + 15F)
2. **Variaciones:** pitch × 5, speed × 5 = **750 combinaciones**
3. **NPCs únicos:** Clonación de voz = **voces infinitas**
4. **Total efectivo:** ~530 voces diferentes realmente necesarias

**Resultado:**
- 🎭 Voces prácticamente únicas para NPCs importantes
- ⚡ Escalable a 270,000 NPCs
- 💰 Sin costos cloud
- 🎮 Experiencia inmersiva

**Archivo implementado:** `sistema_voces_diferenciadas.py`

**Prueba:** `python3 sistema_voces_diferenciadas.py`

---

_Última actualización: 2025_
_Portales del Quinto Sol - MMORPG_
