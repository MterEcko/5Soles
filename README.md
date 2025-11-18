# 📜 PORTALES DEL QUINTO SOL

Sistema de Genealogía y Base de Datos Histórica para el MMORPG "Portales del Quinto Sol"

## 📖 Descripción

Este proyecto es un sistema completo de genealogía y simulación histórica que cubre 1500 años de historia (1500-3000) en el mundo de Aztlán Prime. El sistema genera y rastrea:

- **Múltiples especies** (Humanos I, Humanos II, y 5 especies sirvientes de dioses)
- **Árbol genealógico completo** con parentesco, matrimonios e hijos
- **Sistema de oficios y habilidades** para cada individuo
- **Eventos históricos y vitales** detallados
- **17 dioses mesoamericanos** con sus dominios y tecnologías
- **5 civilizaciones principales** con sus ciudades y pueblos
- **Sistema multilingüe** con 13 idiomas (7 indígenas + 6 modernos)

## 🗂️ Estructura del Proyecto

```
5Soles/
├── 📜 PORTALES DEL QUINTO SOL.docx  # Documento de diseño del juego
├── schema.sql                        # Esquema SQLite
├── schema_postgres.sql               # Esquema PostgreSQL
├── quinto_sol.db                     # Base de datos SQLite
├── crear_db.py                       # Script inicial de creación
├── generar_poblacion.py              # Generador de genealogía
├── simular_historia_completa.py      # Simulador histórico
├── actualizar_db.py                  # Actualizar con nuevas tablas
├── consultas.py                      # Sistema de consultas interactivo
└── README.md                         # Este archivo
```

## 🚀 Inicio Rápido

### 1. Crear la Base de Datos Inicial

```bash
# Crear base de datos con dioses, civilizaciones, especies, etc.
python3 crear_db.py

# Generar los 40 humanos iniciales de la Era Alpha
python3 generar_poblacion.py

# Actualizar con idiomas y eventos vitales
python3 actualizar_db.py

# Actualizar con sistema de IA, personalidades y economía
python3 actualizar_sistema_ia.py
```

### 2. Simular Historia Completa (Opcional)

```bash
# Simular 1500 años de historia (1500-3000)
# ADVERTENCIA: Esto generará miles de personas y puede tomar tiempo
python3 simular_historia_completa.py
```

### 3. Consultar la Base de Datos

```bash
# Sistema interactivo de consultas
python3 consultas.py
```

## 🧠 **NUEVO**: Sistema de IA Conversacional

### Características de NPCs Inteligentes

El sistema incluye NPCs con:
- ✅ **34 rasgos de personalidad** (valiente, generoso, avaro, mentiroso, etc.)
- ✅ **Sistema de necesidades** (comida, agua, materiales de trabajo, clientes)
- ✅ **Memoria contextual** - Recuerdan interacciones pasadas
- ✅ **Memoria heredada** - "Mi padre me mencionó sobre ti..."
- ✅ **Diálogos adaptativos** - Responden según personalidad y contexto
- ✅ **Sistema de trueques** - Economía basada en intercambio
- ✅ **Paternidad incierta** - Prostituta con múltiples padres posibles
- ✅ **Sucesión de oficios** - Hijos heredan talleres de padres
- ✅ **Sistema de aprendices** - Maestros entrenan estudiantes

### Ejemplo de Uso

```python
from modelo_ia_conversacional import SistemaConversacionalIA

# Crear sistema
sistema = SistemaConversacionalIA()

# Conversar con un herrero
npc = sistema.obtener_npc(herrero_id)
saludo = npc.generar_saludo(jugador_id, año=1520)
print(f"{npc.nombre}: {saludo}")

# Comprar items
respuesta = npc.generar_dialogo_comercio("Macuahuitl", cantidad=2)
print(f"{npc.nombre}: {respuesta['respuesta']}")
print(f"Precio: {respuesta['precio']} en trueque")

# El NPC recuerda la transacción
npc.registrar_transaccion(jugador_id, "Macuahuitl", 2, precio, 1520)
```

### Nuevos Oficios (53 total)

**Científicos:**
- Alquimista, Matemático, Filósofo, Astrónomo, Naturalista, Cartógrafo

**Sociales:**
- Prostituta/Prostituto, Cantinero, Bardo, Mensajero

**Tecnológicos:**
- Biomecánico, Sintetizador, Ingeniero de Glifos, Cultivador de Cristales

**Guardianes:**
- Guardián, Vigilante Nocturno, Guardaespaldas

**Oscuros:**
- Ladrón, Asesino, Contrabandista, Espía

**Artesanos Especializados:**
- Tatuador, Perfumista, Vidriero

## 📊 Estructura de la Base de Datos

### Nuevas Tablas para IA

#### **rasgos_personalidad** & **persona_personalidad**
Rasgos de personalidad y su asignación a NPCs.

```sql
Categorías: temperamento, etica, social, mental, laboral, espiritual
Ejemplos: Valiente, Honesto, Generoso, Avaro, Carismático, Cruel
Intensidad: 1-10
```

#### **necesidades** & **persona_necesidades**
Sistema de necesidades que afectan comportamiento.

```sql
Básicas: Comida, Agua, Descanso, Refugio
Profesionales: Materiales de Trabajo, Herramientas, Clientes
Sociales: Compañía, Reconocimiento, Amor
```

#### **items** & **persona_inventario**
Items, recursos y inventarios de NPCs.

```sql
28 items: Comida, Armas, Armadura, Materiales, Herramientas
Valores de trueque, peso, perecederos
```

#### **transacciones**
Registro completo de comercio y trueques.

```sql
- Vendedor, Comprador, Items intercambiados
- Precio acordado, satisfacción de ambas partes
- Historial completo de economía
```

#### **memoria_npc**
Memoria contextual para IA conversacional.

```sql
- Memorias de interacciones con jugadores
- Importancia (1-10) - afecta si se recuerda
- Emoción asociada (alegria, tristeza, ira)
- Metadata con contexto adicional
```

#### **paternidad_posible**
Sistema de paternidad múltiple/incierta.

```sql
- Hijo con madre conocida
- Múltiples padres posibles con probabilidad %
- Sistema de confirmación (ADN divino, rasgos, confesión)
```

#### **relaciones**
Relaciones entre personas.

```sql
Tipos: amigo, enemigo, rival, mentor, aprendiz, cliente, amante
Intensidad: 1-10
Es recíproca: True/False
```

#### **sucesion_oficios** & **aprendices**
Sistema de herencia y aprendizaje de oficios.

```sql
- Sucesión: padre → hijo
- Aprendices: maestro → estudiante (sin relación familiar)
- Nivel de maestría heredado/transferido
```

### Tablas Principales

#### **personas**
Tabla central con todos los individuos del mundo.

```sql
- id, nombre, apellido, nombre_completo
- padre_id, madre_id (genealogía)
- especie_id, civilizacion_id
- año_nacimiento, año_muerte, causa_muerte
- clase_social, oficios, habilidades
- dios_patron_id, nivel_devoto
```

**Causas de muerte posibles:**
- `edad_avanzada` - Muerte natural
- `combate` - Muerte en batalla
- `enfermedad` - Muerte por enfermedad
- `animal_salvaje` - Ataque de criatura
- `accidente` - Accidente fatal
- `sacrificio` - Sacrificio ritual

#### **eventos_vitales**
Historial detallado de vida de cada persona.

```sql
- persona_id, tipo_evento, año, descripcion
- lugar_id, severidad, resultado
- metadata (JSON con información adicional)
```

**Tipos de eventos:**
- `nacimiento`, `muerte`, `matrimonio`
- `batalla`, `viaje`, `enfermedad`
- `ritual`, `promocion`, `herida`

#### **especies**
Razas y especies del mundo.

```sql
Humanos I (Era Alpha - siglo XV)
Humanos II (Era del Cataclismo - siglo XXIII)
Tlacatl de Luz (sirvientes de Quetzalcóatl)
Sombra-Coyotes (sirvientes de Tezcatlipoca)
Bio-Constructores (sirvientes de Ixchel)
Acuátiles (sirvientes de Tláloc)
Guerreros Solares (sirvientes de Huitzilopochtli)
```

#### **dioses**
17 deidades mesoamericanas principales.

```sql
Quetzalcóatl - Equilibrio, Viento, Sabiduría
Tezcatlipoca - Conflicto, Sombra, Ilusión
Tláloc - Agua, Lluvia, Fertilidad
Huitzilopochtli - Voluntad, Guerra, Sol
Ixchel - Luna, Sanación, Biogénesis
Mictlantecuhtli - Muerte, Inframundo
... y 11 más
```

#### **civilizaciones**
5 culturas principales de Aztlán Prime.

```sql
Mexica de Obsidiana (guerreros)
Zapotecas del Eco (sanadores)
Mayas Celeste (sabios)
Toltecas del Viento (ingenieros)
Purépecha del Fuego (artesanos)
```

#### **idiomas**
13 lenguas del mundo (para IA multilingüe).

**Indígenas (7):**
- Náhuatl, Maya Yucateco, Zapoteco, Mixteco
- Purépecha, Otomí, Totonaco

**Modernos (6):**
- Español, Inglés, Francés, Ruso, Chino, Japonés

#### **traducciones**
Frases y textos en múltiples idiomas.

```sql
- clave (identificador único)
- idioma_id, texto, contexto
- es_formal, metadata (pronunciación)
```

### Relaciones

```
personas
├── padre_id → personas(id)
├── madre_id → personas(id)
├── especie_id → especies(id)
├── civilizacion_id → civilizaciones(id)
└── dios_patron_id → dioses(id)

matrimonios
├── persona1_id → personas(id)
└── persona2_id → personas(id)

eventos_vitales
├── persona_id → personas(id)
├── lugar_id → pueblos_ciudades(id)
└── evento_relacionado_id → eventos(id)
```

## 🎮 Sistema de Genealogía

### Características

1. **Población Inicial**: 40 humanos (Era Alpha, año 1500)
2. **Reproducción**: 4-7 hijos por matrimonio
3. **Esperanza de vida variable**:
   - Sacerdotes/Sacerdotisas: 120-300 años
   - Nobles: 100-200 años
   - Guerreros: 80-120 años
   - Artesanos: 90-150 años
   - Campesinos: 80-130 años

4. **Matrimonios**:
   - Preferencia por misma civilización (90%)
   - Edad de matrimonio: 18-40 años
   - Hijos nacen en intervalos de 2-4 años

### Clases Sociales

```python
'sacerdote'   # Líderes espirituales (5%)
'sacerdotisa' # Líderes espirituales femeninas (5%)
'noble'       # Clase alta (10%)
'guerrero'    # Clase militar (20%)
'artesano'    # Clase artesanal (30%)
'campesino'   # Clase trabajadora (30%)
```

## 🛠️ Oficios y Habilidades

### Oficios (28 disponibles)

**Artesanales:** Herrero, Carpintero, Alfarero, Tejedor, Tallador, Joyero

**Religiosos:** Sacerdote, Sacerdotisa, Chamán, Augur

**Militares:** Guerrero, Arquero, Capitán, Estratega

**Agrícolas:** Agricultor, Pastor, Pescador, Cazador

**Especialistas:** Tecnomístico, Geomante, Bio-Ingeniero

### Habilidades (25 disponibles)

**Combate:** Maestría con Espada, Arco, Combate Cuerpo a Cuerpo

**Magia/Divina:** Curación Divina, Invocación de Lluvia, Control de Viento

**Conocimiento:** Lectura de Glifos, Astronomía, Conocimiento de Hierbas

**Social:** Liderazgo Natural, Oratoria Divina, Negociación

## 🌍 Sistema Multilingüe

### Idiomas Indígenas

```yaml
Náhuatl (nah):
  - Hola: "Niltze" (NEEL-tzeh)
  - Adiós: "Ōmpa timonēxtīz"
  - Gracias: "Tlazohcāmati"

Maya Yucateco (yua):
  - Hola: "Bix a beel"
  - Adiós: "Túun túun"
  - Gracias: "Yuum bo'otik"

Zapoteco (zap):
  - Hola: "Naa"
  - Adiós: "Gasti cani"
  - Gracias: "Dios bo chelu"
```

### Estructura para IA

La tabla `traducciones` está diseñada para entrenar modelos de IA multilingües:

```sql
SELECT t.clave, t.texto, i.nombre, t.metadata
FROM traducciones t
JOIN idiomas i ON t.idioma_id = i.id
WHERE t.contexto = 'saludo';
```

**Metadata incluye:**
- Pronunciación fonética
- Notas culturales
- Nivel de formalidad
- Contexto de uso

## 📈 Consultas Útiles

### Buscar una Persona

```python
python3 consultas.py
# Opción 2: Buscar persona por nombre
# Ejemplo: "Dron"
```

### Ver Árbol Genealógico

```sql
SELECT * FROM arbol_genealogico WHERE id = 1;
```

### Estadísticas de Población

```sql
SELECT * FROM poblacion_por_civilizacion;
```

### Historial de una Persona

```sql
SELECT ev.año, ev.tipo_evento, ev.descripcion, ev.resultado
FROM eventos_vitales ev
WHERE ev.persona_id = 1
ORDER BY ev.año;
```

### Linajes Importantes

```python
# Familias con más de 20 descendientes
python3 consultas.py
# Opción 6: Linajes importantes
```

## 🔄 Migración a PostgreSQL

El proyecto incluye un esquema completo para PostgreSQL en `schema_postgres.sql`.

### Características Adicionales en PostgreSQL

- UUIDs para identificadores únicos
- Tipo JSONB para metadata
- Funciones y triggers automáticos
- Índices optimizados
- Auditoría con timestamps

### Migrar de SQLite a PostgreSQL

```bash
# 1. Crear base de datos PostgreSQL
createdb quinto_sol

# 2. Ejecutar esquema
psql quinto_sol < schema_postgres.sql

# 3. Exportar datos de SQLite (script personalizado necesario)
# O usar herramientas como pgloader
```

## 📝 Ejemplos de Uso

### Ejemplo 1: Crear Historia de un Personaje

```python
from generar_poblacion import GeneradorGenealogico
import json

gen = GeneradorGenealogico()

# Crear un nuevo héroe
heroe_id = gen.crear_persona(
    nombre="Cuauhtémoc",
    genero="masculino",
    año_nacimiento=1520,
    civilizacion_id=1  # Mexica de Obsidiana
)

# Registrar evento de batalla
gen.cursor.execute('''
    INSERT INTO eventos_vitales
    (persona_id, tipo_evento, año, descripcion, severidad, resultado, metadata)
    VALUES (?, 'batalla', 1550,
            'Participó en la defensa de la Ciudad del Quinto Sol',
            'grave', 'victoria',
            ?)
''', (heroe_id, json.dumps({
    'enemigos_derrotados': 12,
    'arma': 'Macuahuitl de Obsidiana',
    'aliados': ['Guerreros Jaguar', 'Guerreros Águila']
})))

gen.conn.commit()
```

### Ejemplo 2: Consultar Hablantes de un Idioma

```sql
SELECT p.nombre_completo, pi.nivel_dominio, pi.es_nativo
FROM personas p
JOIN persona_idiomas pi ON p.id = pi.persona_id
JOIN idiomas i ON pi.idioma_id = i.id
WHERE i.nombre = 'Náhuatl'
ORDER BY pi.nivel_dominio DESC;
```

### Ejemplo 3: Eventos Históricos por Era

```sql
SELECT e.nombre as era, ev.nombre, ev.año, ev.descripcion
FROM eventos ev
JOIN eras e ON ev.era_id = e.id
ORDER BY ev.año;
```

### Ejemplo 4: Historial Comercial de un NPC

```sql
SELECT * FROM historial_comercial
WHERE vendedor = 'Ichtaca del Viento'
ORDER BY año;
```

### Ejemplo 5: Líneas de Sucesión de Oficios

```sql
SELECT * FROM lineas_sucesion
WHERE oficio = 'Herrero'
ORDER BY año_sucesion;
```

## 🎮 Ejemplos Avanzados

El proyecto incluye `ejemplos_avanzados.py` que demuestra:

### 1. Paternidad Incierta

```bash
python3 ejemplos_avanzados.py
```

**Escenario:**
- Prostituta tiene un hijo
- 3 posibles padres con probabilidades: Herrero (40%), Pescador (35%), Guardián (25%)
- Sistema permite resolver paternidad mediante: ADN divino, rasgos físicos, confesión

### 2. Sucesión de Taller

**Escenario:**
- Herrero maestro muere
- Hijo hereda el taller
- Hijo recuerda clientes de su padre
- Primera conversación: *"Mi padre me mencionó sobre ti..."*

```python
💬 Cuauhtémoc: Espera... Ichtaca del Viento me habló de ti.
   Decía que eras un viajero que siempre paga bien y trata con respeto.

💬 Cuauhtémoc: Mi padre falleció en el año 1550.
   He heredado su taller y sus conocimientos.
```

### 3. Aprendiz No Familiar

**Escenario:**
- Maestro Alquimista entrena a estudiante sin relación familiar
- Relación maestro-aprendiz con progreso (65%)
- Aprendiz puede eventualmente superar al maestro

## 🤖 Entrenamiento de IA con Wikipedia

El proyecto incluye un sistema para extraer conocimientos de Wikipedia y entrenar modelos de IA multilingües.

### ¿Por qué Wikipedia?

Wikipedia es una excelente fuente para entrenar IA porque:

- ✅ **Licencia Creative Commons** (CC-BY-SA) - Uso permitido
- ✅ **Múltiples idiomas** - Incluye náhuatl, español, inglés, y más
- ✅ **Contenido verificado** - Artículos con referencias
- ✅ **Cobertura extensa** - Mitología, historia, lenguas indígenas
- ✅ **Actualización constante** - Contenido mantenido por la comunidad

### Uso del Extractor

```bash
# Extraer artículos de Wikipedia sobre mitología mesoamericana
python3 entrenar_ia_wikipedia.py
```

Esto genera:
1. **conocimientos_ia** (tabla en BD) - Artículos completos almacenados
2. **dataset_entrenamiento.jsonl** - Dataset listo para fine-tuning

### Fuentes de Datos Adicionales

**Corpus Lingüísticos:**
- [INALI](https://www.inali.gob.mx/) - Instituto Nacional de Lenguas Indígenas
- [Wikcionario](https://es.wiktionary.org/) - Diccionarios multilingües
- [OLAC](http://www.language-archives.org/) - Open Language Archives

**Recursos Académicos:**
- Proyecto Gutenberg (libros históricos)
- Corpus del español del siglo XXI
- Digital resources for náhuatl

### Modelos Recomendados

```python
# Traducción: Helsinki-NLP/opus-mt (multilingüe)
# Generación: GPT-4, Claude, LLaMA fine-tuned
# NER: spaCy con modelos custom para náhuatl
```

## 🎯 Roadmap

### ✅ Completado (v1.0)

- [x] Sistema de genealogía básico
- [x] Generación de población inicial (40 humanos)
- [x] Sistema de matrimonios e hijos
- [x] 53 oficios y 25 habilidades
- [x] Eventos vitales con historial detallado
- [x] Sistema multilingüe (13 idiomas)
- [x] Extractor de Wikipedia para IA
- [x] **Sistema de personalidades** (34 rasgos)
- [x] **Sistema de necesidades y economía**
- [x] **28 items y recursos**
- [x] **Sistema de trueques y transacciones**
- [x] **Memoria de NPCs** (contextual y heredada)
- [x] **IA conversacional** con diálogos adaptativos
- [x] **Paternidad incierta** (prostituta, padres múltiples)
- [x] **Sucesión de oficios** (herencia familiar)
- [x] **Sistema de aprendices** (maestro/estudiante)
- [x] **Relaciones entre personas** (amigo, enemigo, mentor, amante)

### 🔄 En Progreso (v2.0)

- [ ] Simulación completa 1500-3000 (generación masiva)
- [ ] Integración con modelos LLM (GPT, Claude, Llama)
- [ ] Sistema de combate y batallas
- [ ] Eventos históricos procedurales

### 📋 Planeado (v3.0)

- [ ] Migración a PostgreSQL
- [ ] API REST para consultas
- [ ] Dashboard web para visualización
- [ ] Generador de narrativas automáticas
- [ ] Sistema de facciones y política
- [ ] Economía avanzada (inflación, comercio inter-ciudades)
- [ ] Sistema de magia y habilidades divinas
- [ ] Generación procedural de misiones

## 📚 Documentación Adicional

### Documento de Diseño

Ver `📜 PORTALES DEL QUINTO SOL.docx` para:
- Narrativa completa del juego
- Diseño de gameplay
- Sistemas de progresión
- Tecnología simbólica (glifos)
- Mobs y fauna mitológica

### Esquemas de Base de Datos

- `schema.sql` - SQLite (desarrollo)
- `schema_postgres.sql` - PostgreSQL (producción)

## 🤝 Contribuciones

Este es un proyecto de worldbuilding para un MMORPG. Las áreas principales de trabajo son:

1. **Datos históricos**: Añadir más eventos y personajes
2. **Traducciones**: Expandir el diccionario multilingüe
3. **IA conversacional**: Entrenar modelos de lenguaje natural
4. **Visualización**: Crear dashboards y árboles genealógicos
5. **Optimización**: Mejorar el rendimiento de consultas

## 📜 Licencia

Este proyecto es parte del desarrollo del MMORPG "Portales del Quinto Sol".

## 🙏 Créditos

**Mitología y Cultura Mesoamericana:**
- Basado en las tradiciones de las culturas Mexica, Maya, Zapoteca, Mixteca, Purépecha, Tolteca y Olmeca
- Diseño respetuoso de lenguas indígenas

**Tecnologías:**
- Python 3
- SQLite / PostgreSQL
- Sistemas de genealogía procedural

---

**Cuando los dioses regresaron, no trajeron milagros… trajeron memoria.**
