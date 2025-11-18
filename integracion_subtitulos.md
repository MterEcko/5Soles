# 🎬 INTEGRACIÓN DE BASE DE DATOS DE SUBTÍTULOS

## 📊 Recursos Disponibles
- **Base de datos:** ~300,000 subtítulos de películas
- **Tamaño:** ~30 GB
- **Formato probable:** SRT, ASS, o base de datos SQL

---

## 🎯 PLAN DE INTEGRACIÓN CON PORTALES DEL QUINTO SOL

### Fase 1: Análisis y Extracción

#### Script 1: Procesador de Subtítulos
```python
# procesar_subtitulos.py
"""
Extrae diálogos de subtítulos y los clasifica por:
- Emociones (alegría, tristeza, ira, miedo, neutral)
- Tipo de interacción (saludo, despedida, negociación, amenaza, petición)
- Personalidad sugerida (valiente, cobarde, generoso, avaro, etc.)
"""
```

**Técnicas a usar:**
- **Sentiment Analysis:** VADER, TextBlob para detectar emociones
- **Named Entity Recognition:** SpaCy para detectar personajes, lugares
- **Topic Modeling:** LDA para categorizar tipos de diálogo
- **Pattern Matching:** Regex para estructuras específicas (preguntas, órdenes, etc.)

#### Datos a extraer:
1. **Saludos contextuales**
   - Formal vs informal
   - Primera vez vs conocido
   - Amigable vs hostil

2. **Negociaciones comerciales**
   - Ofertas de compra/venta
   - Regateo
   - Aceptación/rechazo de tratos

3. **Diálogos emocionales**
   - Alegría (victoria, reencuentro)
   - Tristeza (pérdida, despedida)
   - Ira (confrontación, insultos)
   - Miedo (peligro, incertidumbre)

4. **Estructuras de misión**
   - "Necesito que..."
   - "¿Podrías traerme...?"
   - "Si me ayudas con..."
   - "A cambio de..."

---

### Fase 2: Clasificación por Personalidad

#### Mapeo de Personalidades → Géneros de Película

| Personalidad | Películas Fuente | Tipo de Diálogos |
|--------------|------------------|------------------|
| Valiente | Acción, Guerra, Superhéroes | Enfrentar peligro, desafíos |
| Cobarde | Comedia, Horror | Evitar conflicto, huir |
| Generoso | Drama, Familia | Ofrecer ayuda, compartir |
| Avaro | Thriller, Crimen | Negar ayuda, exigir pago |
| Honesto | Drama, Biográficas | Verdad directa, confesiones |
| Mentiroso | Thriller, Crimen | Engaños, evasivas |
| Amigable | Comedia, Romance | Saludos cálidos, ofrecer ayuda |
| Hostil | Acción, Thriller | Amenazas, rechazos |
| Leal | Acción, Drama | Defender aliados, promesas |
| Traicionero | Thriller, Crimen | Traiciones, falsas promesas |
| Sabio | Fantasía, Sci-Fi | Consejos, enseñanzas |
| Impulsivo | Acción, Comedia | Decisiones rápidas sin pensar |
| Compasivo | Drama, Familia | Empatía, consuelo |
| Cruel | Horror, Thriller | Burlas, amenazas, violencia |

---

### Fase 3: Construcción de Corpus de Diálogos

#### Estructura de Base de Datos
```sql
CREATE TABLE dialogos_entrenamiento (
    id INTEGER PRIMARY KEY,
    texto TEXT NOT NULL,
    pelicula_id INTEGER,
    emocion VARCHAR(50), -- alegria, tristeza, ira, miedo, neutral
    personalidad_sugerida VARCHAR(50), -- valiente, generoso, etc.
    tipo_dialogo VARCHAR(50), -- saludo, comercio, mision, casual, amenaza
    contexto TEXT, -- Qué pasó antes de este diálogo
    genero_pelicula VARCHAR(50), -- accion, drama, comedia, etc.
    idioma VARCHAR(10) -- es, en, etc.
);

CREATE INDEX idx_emocion ON dialogos_entrenamiento(emocion);
CREATE INDEX idx_personalidad ON dialogos_entrenamiento(personalidad_sugerida);
CREATE INDEX idx_tipo ON dialogos_entrenamiento(tipo_dialogo);
```

---

### Fase 4: Integración con modelo_ia_conversacional.py

#### Mejora 1: Generación de Saludos Enriquecida
```python
def generar_saludo_mejorado(self, jugador_id, año_actual):
    """
    Usa corpus de subtítulos para generar saludos más naturales
    según personalidad del NPC
    """
    # Obtener personalidad dominante
    personalidad = self.obtener_personalidad_dominante()

    # Consultar corpus de diálogos
    cursor.execute('''
        SELECT texto FROM dialogos_entrenamiento
        WHERE tipo_dialogo = 'saludo'
        AND personalidad_sugerida = ?
        ORDER BY RANDOM()
        LIMIT 1
    ''', (personalidad,))

    template_saludo = cursor.fetchone()[0]

    # Personalizar con información del NPC
    saludo = template_saludo.format(
        nombre=self.nombre,
        oficio=self.oficio_principal
    )

    return saludo
```

#### Mejora 2: Diálogos de Comercio Más Naturales
```python
def generar_dialogo_comercio_enriquecido(self, item, cantidad):
    """
    Genera diálogos de comercio basados en subtítulos
    """
    personalidad = self.obtener_personalidad_dominante()

    if self.tiene_rasgo('Avaro'):
        # Buscar diálogos de negociación dura
        cursor.execute('''
            SELECT texto FROM dialogos_entrenamiento
            WHERE tipo_dialogo = 'negociacion'
            AND personalidad_sugerida = 'avaro'
            ORDER BY RANDOM() LIMIT 1
        ''')
    elif self.tiene_rasgo('Generoso'):
        # Buscar diálogos amigables
        cursor.execute('''
            SELECT texto FROM dialogos_entrenamiento
            WHERE tipo_dialogo = 'comercio'
            AND emocion = 'alegria'
            ORDER BY RANDOM() LIMIT 1
        ''')

    template = cursor.fetchone()[0]
    return template.format(item=item, cantidad=cantidad, precio=...)
```

---

### Fase 5: Fine-Tuning de Modelo LLM

#### Opción A: Modelo Local (Llama 3, Mistral)
**Ventajas:**
- No depende de APIs externas
- Sin límites de requests
- Privacidad total

**Proceso:**
1. Exportar corpus clasificado a JSONL
2. Fine-tuning con LoRA/QLoRA
3. Integrar modelo en `modelo_ia_conversacional.py`

```python
# Ejemplo de formato JSONL para fine-tuning
{
  "messages": [
    {"role": "system", "content": "Eres un herrero valiente y generoso en el año 1650."},
    {"role": "user", "content": "Hola, ¿vendes espadas?"},
    {"role": "assistant", "content": "¡Buen día, viajero! Sí, tengo espadas de obsidiana recién forjadas. Son las mejores de toda la región."}
  ],
  "metadata": {
    "personalidad": ["valiente", "generoso"],
    "oficio": "herrero",
    "año": 1650
  }
}
```

#### Opción B: Fine-Tuning de GPT-3.5/4
**Ventajas:**
- Mejor calidad de respuestas
- Menos recursos locales

**Desventajas:**
- Coste por request
- Dependencia de API

---

### Fase 6: Sistema de Generación Procedural de Misiones

#### Extraer Estructuras de Quest
```python
# Patrones comunes en subtítulos:
quest_patterns = [
    "Necesito que {accion} {objeto} en {lugar}",
    "¿Podrías traerme {cantidad} {item}?",
    "Si me ayudas con {tarea}, te daré {recompensa}",
    "Alguien robó mi {objeto}, ayúdame a recuperarlo",
    "Hay {enemigo} atacando {lugar}, elimínalos",
]

# Extraer de subtítulos:
- Acciones (buscar, traer, eliminar, construir, etc.)
- Objetos (espada, libro, medicina, etc.)
- Lugares (bosque, cueva, templo, etc.)
- Recompensas (oro, items, información, etc.)
```

#### Ejemplo de Misión Generada
```python
def generar_mision_procedural(npc_id):
    """
    Genera misión basada en:
    - Necesidades del NPC
    - Personalidad del NPC
    - Contexto histórico (año, eventos)
    - Templates de subtítulos
    """
    npc = obtener_npc(npc_id)

    # NPC herrero necesita hierro
    if npc.oficio == 'Herrero' and npc.necesidades['materiales_trabajo'] < 30:
        template = random.choice(quest_templates['recoleccion'])

        mision = template.format(
            npc_nombre=npc.nombre,
            item_necesario='hierro',
            cantidad=random.randint(10, 50),
            lugar='minas del norte',
            recompensa='espada de obsidiana'
        )

        return mision
```

---

## 📋 TAREAS DE IMPLEMENTACIÓN

### Tarea 1: Análisis de Subtítulos (Prioridad: Alta)
```bash
# Script a crear: analizar_subtitulos.py
- Leer base de datos de 30GB
- Extraer solo diálogos (eliminar timestamps, formato)
- Detectar idioma (separar español, inglés, etc.)
- Guardar en SQLite/PostgreSQL
```

### Tarea 2: Clasificación con IA (Prioridad: Alta)
```bash
# Script a crear: clasificar_dialogos.py
- Usar modelo de sentiment analysis (VADER, RoBERTa)
- Clasificar por emoción
- Clasificar por tipo de diálogo
- Sugerir personalidad del hablante
```

### Tarea 3: Integración con Sistema Actual (Prioridad: Media)
```bash
# Modificar: modelo_ia_conversacional.py
- Agregar función buscar_dialogo_similar(personalidad, tipo)
- Mejorar generar_saludo() con templates
- Mejorar generar_dialogo_comercio() con variaciones
```

### Tarea 4: Fine-Tuning de Modelo (Prioridad: Baja - Futuro)
```bash
# Requiere GPU potente
- Preparar dataset JSONL
- Fine-tuning Llama 3 8B o Mistral 7B
- Evaluar calidad de respuestas
- Integrar en servidor de juego
```

---

## 🚀 ROADMAP SUGERIDO

### Mes 1: Preparación de Datos
- Semana 1-2: Extraer y limpiar subtítulos
- Semana 3-4: Clasificar emociones y tipos

### Mes 2: Integración Básica
- Semana 1-2: Crear corpus clasificado
- Semana 3-4: Integrar templates en modelo_ia_conversacional.py

### Mes 3: Generación Avanzada
- Semana 1-2: Sistema de misiones procedurales
- Semana 3-4: Evaluación de calidad

### Mes 4+: Fine-Tuning (Opcional)
- Fine-tuning de modelo LLM
- Despliegue en servidor
- Optimización de rendimiento

---

## 💡 VALOR AGREGADO

### Antes (Sistema Actual)
```python
saludo = f"Hola, soy {self.nombre}, {self.oficio_principal}"
```

### Después (Con Subtítulos)
```python
# NPC Valiente + Amigable:
saludo = "¡Saludos, viajero! Es un placer conocer a alguien con aspecto de aventurero. Soy Tonatiuh, el mejor herrero de estas tierras."

# NPC Avaro + Hostil:
saludo = "¿Qué quieres? Si vienes a comprar, tienes que pagar. Si no, vete."

# NPC Sabio + Leal:
saludo = "Bienvenido, joven. He visto muchos como tú pasar por aquí. Permíteme compartir mi conocimiento..."
```

---

## 📊 MÉTRICAS DE ÉXITO

1. **Variedad de Diálogos:** Más de 1000 templates únicos por tipo
2. **Naturalidad:** Diálogos indistinguibles de texto humano
3. **Consistencia:** Personalidad coherente en todas las interacciones
4. **Rendimiento:** Generación < 100ms por diálogo

---

## ⚠️ CONSIDERACIONES

1. **Derechos de Autor:** Usar subtítulos solo para entrenamiento, no redistribuir
2. **Filtrado de Contenido:** Eliminar lenguaje inapropiado si es para audiencia general
3. **Traducción:** Si subtítulos están en inglés, considerar traducción automática
4. **Almacenamiento:** 30GB es mucho, considerar compresión o sampling

---

## 🎯 PRÓXIMO PASO INMEDIATO

**¿Cuál es el formato actual de tu base de datos de subtítulos?**
- ¿Es SQLite, PostgreSQL, MySQL?
- ¿O son archivos .srt / .ass individuales?
- ¿En qué idiomas están?
- ¿Tienes metadatos de películas (género, año)?

Con esta información puedo crear el script de análisis específico para tu caso.
