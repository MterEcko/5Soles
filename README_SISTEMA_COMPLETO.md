# 🌅 Portales del Quinto Sol - Sistema Completo
## MMORPG Mesoamericano con Simulación Histórica 1500-3000

---

## 📖 Índice

1. [Visión General](#-visión-general)
2. [Arquitectura del Sistema](#-arquitectura-del-sistema)
3. [Instalación](#-instalación)
4. [Configuración Base de Datos](#-configuración-base-de-datos)
5. [Flujo de Ejecución](#-flujo-de-ejecución)
6. [Sistemas Implementados](#-sistemas-implementados)
7. [NPCs y Conversaciones](#-npcs-y-conversaciones)
8. [Economía Dual](#-economía-dual-físicacripto)
9. [Servidor de Tiempo Real](#-servidor-de-tiempo-real)
10. [Estadísticas Esperadas](#-estadísticas-esperadas)

---

## 🌟 Visión General

**Portales del Quinto Sol** es un MMORPG ambientado en Mesoamérica con una característica única: **1500 años de historia simulada** antes de que los jugadores entren al mundo.

### Concepto Único

**FASE 1: Simulación Histórica (1500-3000)** ⚙️
- Generación procedural de 270,000+ NPCs
- Genealogías completas de 6 especies
- 1500 años de guerras, alianzas, mutaciones
- NPCs conversando entre sí, generando cultura
- Rumores que se propagan y distorsionan
- Conocimiento cultural que se transmite

**FASE 2: Mundo Vivo (3000+)** 🎮
- Jugadores entran a un mundo con 1500 años de historia
- NPCs recuerdan eventos históricos
- 1 hora real = 1 día del juego
- Conversaciones con NPCs que tienen memoria
- Economía dual: Dinero físico + Criptomonedas
- Mundo sigue evolucionando en tiempo real

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    FASE 1: SIMULACIÓN (Offline)              │
│                        1500 → 3000 (1500 años)               │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
            ┌──────────────────────────────────┐
            │  16 SISTEMAS PRINCIPALES         │
            ├──────────────────────────────────┤
            │ 1. Relaciones Especies-Civs      │
            │ 2. Flora (777 especies)          │
            │ 3. Fauna (315 especies)          │
            │ 4. Genealogías Especies (300a)   │
            │ 5. Longevidad por Oficio (200a)  │
            │ 6. Guerras Inter-Especies        │
            │ 7. Mutaciones (16 tipos)         │
            │ 8. Híbridos Inter-Especies       │
            │ 9. Artefactos Legendarios        │
            │ 10. Organizaciones               │
            │ 11. Eventos Divinos              │
            │ 12. Migraciones                  │
            │ 13. Sistema de Justicia          │
            │ 14. Clima (1500 años)            │
            │ 15. Economía Dual                │
            │ 16. CONVERSACIONES NPC ✨ NUEVO  │
            └──────────────────────────────────┘
                               │
                               ▼
            ┌──────────────────────────────────┐
            │  BASE DE DATOS COMPLETA          │
            ├──────────────────────────────────┤
            │ • 270,000 NPCs con historia      │
            │ • 75,000+ conversaciones         │
            │ • Rumores y leyendas             │
            │ • Conocimiento cultural          │
            │ • Guerras y alianzas             │
            │ • Mutantes e híbridos            │
            └──────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                  FASE 2: SERVIDOR VIVO (Online)              │
│                         Año 3000+                            │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
            ┌──────────────────────────────────┐
            │  SERVIDOR TIEMPO REAL            │
            ├──────────────────────────────────┤
            │ • 1 hora real = 1 día juego      │
            │ • Procesamiento diario NPCs      │
            │ • Conversaciones continuas       │
            │ • Cultura evoluciona             │
            └──────────────────────────────────┘
                               │
                               ▼
            ┌──────────────────────────────────┐
            │  JUGADORES INTERACTÚAN           │
            ├──────────────────────────────────┤
            │ • Chat con NPCs (memoria)        │
            │ • Comercio con criptomonedas     │
            │ • Mundo con historia de 1500a    │
            │ • NPCs con personalidad única    │
            └──────────────────────────────────┘
```

---

## 💿 Instalación

### Requisitos

- **Python 3.7+**
- **Base de datos:** SQLite (dev) o PostgreSQL (producción)
- **Espacio en disco:** 10-15 GB
- **RAM:** 8 GB recomendado
- **CPU:** Multi-core recomendado

### Dependencias Python

```bash
# Básicas
pip install numpy

# PostgreSQL (opcional, para producción)
pip install psycopg2-binary

# IA Local (para FASE 2)
pip install ollama sentence-transformers chromadb
```

### Clonar Repositorio

```bash
git clone https://github.com/usuario/5Soles.git
cd 5Soles
```

---

## 🗄️ Configuración Base de Datos

### Opción 1: SQLite (Desarrollo/Testing)

✅ **Recomendado para:** Desarrollo, testing, máquinas con pocos recursos

```bash
# No requiere configuración adicional
# Los scripts crearán automáticamente quinto_sol.db
```

### Opción 2: PostgreSQL (Producción)

✅ **Recomendado para:** Producción, servidor de juego, múltiples jugadores

Ver guía completa: **[CONFIGURACION_POSTGRESQL.md](CONFIGURACION_POSTGRESQL.md)**

**Resumen rápido:**

```bash
# 1. Instalar PostgreSQL
sudo apt install postgresql postgresql-contrib
pip install psycopg2-binary

# 2. Crear base de datos
sudo -u postgres psql
CREATE DATABASE quinto_sol;
CREATE USER quinto_sol_user WITH PASSWORD 'tu_password';
GRANT ALL PRIVILEGES ON DATABASE quinto_sol TO quinto_sol_user;
\q

# 3. Configurar variables de entorno
export DB_TYPE=postgres
export PG_HOST=localhost
export PG_PORT=5432
export PG_DATABASE=quinto_sol
export PG_USER=quinto_sol_user
export PG_PASSWORD=tu_password

# 4. Verificar conexión
python3 database_connector.py
```

---

## 🚀 Flujo de Ejecución

### PASO 1: Simulación Principal (2-6 horas)

Genera genealogías, guerras, longevidad, etc.

```bash
python3 simulacion_completa_1500_3000.py
```

**Incluye:**
- Relaciones especies-civilizaciones
- Genealogías especies sirvientes (300 años)
- Longevidad por oficios (200 años humanos)
- Guerras inter-especies
- Resumen estadístico

### PASO 2: Sistemas Adicionales (1-2 horas)

Mutaciones, híbridos, artefactos, clima, economía, etc.

```bash
python3 sistemas_adicionales_integrados.py
```

**Incluye:**
- Mutaciones genéticas (16 tipos)
- Matrimonios inter-especies e híbridos
- Artefactos legendarios (5 iniciales)
- Organizaciones (gremios, cultos, órdenes)
- Eventos divinos expandidos
- Migraciones poblacionales
- Sistema de justicia (crímenes, juicios)
- Clima y estaciones (1500 años)
- Economía dual (5 monedas + cripto)

### PASO 3: Simulación Mundo Completo ✨ NUEVO (30-60 minutos)

Integra todo + conversaciones NPC

```bash
python3 simulacion_mundo_completo.py
```

**Añade:**
- Sistema de conversaciones NPC-to-NPC
- Generación de rumores (efecto teléfono descompuesto)
- Conocimiento cultural
- Estadísticas finales completas
- Optimización para producción

### PASO 4: Servidor de Tiempo Real (Continuo)

Inicia servidor para jugadores (año 3000+)

```bash
python3 servidor_tiempo_juego.py
```

**Características:**
- 1 hora real = 1 día del juego
- Procesamiento diario de NPCs
- Conversaciones NPCs continúan
- Admin console (comandos: /time, /npcs, /events, /quit)
- Modo fast (1 min = 1 día) para testing

---

## 🎯 Sistemas Implementados

### Sistema 1-6: Principales ✅

| # | Sistema | Descripción | Archivo |
|---|---------|-------------|---------|
| 1 | Relaciones Especies-Civilizaciones | Mapeo especies↔civilizaciones↔dioses | `schema_relaciones_especies_civilizaciones.sql` |
| 2 | Flora | 777 especies vegetales clasificadas | `schema_flora.sql`, `flora_1000_especies.py` |
| 3 | Fauna | 315 especies animales + sistema spawn | `schema_especies_fauna.sql`, `fauna_300_especies.py` |
| 4 | Genealogías Especies | 5 especies sirvientes, 300 años vida | `generar_genealogias_especies.py` |
| 5 | Longevidad Oficios | 53 oficios, humanos hasta 200 años | `sistema_longevidad_oficios.py` |
| 6 | Guerras Inter-Especies | Guerras, batallas, alianzas | `sistema_guerras_especies.py` |

### Sistema 7-15: Adicionales ✅

| # | Sistema | Descripción | Archivo |
|---|---------|-------------|---------|
| 7 | Mutaciones | 16 mutaciones (físicas, mentales, mágicas) | `sistema_mutaciones.py` |
| 8 | Híbridos | Matrimonios inter-especies, hijos híbridos | `sistema_matrimonios_interespecie.py` |
| 9 | Artefactos | Items legendarios con poderes | `schema_artefactos_organizaciones_eventos.sql` |
| 10 | Organizaciones | Gremios, cultos, órdenes militares | `schema_artefactos_organizaciones_eventos.sql` |
| 11 | Eventos Divinos | Bendiciones, maldiciones, profecías | `schema_artefactos_organizaciones_eventos.sql` |
| 12 | Migraciones | Refugiados, migraciones masivas | `schema_migraciones_justicia_clima_economia.sql` |
| 13 | Justicia | Crímenes, juicios, prisiones | `schema_migraciones_justicia_clima_economia.sql` |
| 14 | Clima | 1500 años de clima, afecta guerras | `schema_migraciones_justicia_clima_economia.sql` |
| 15 | Economía Dual | 5 monedas (física + cripto) | `schema_migraciones_justicia_clima_economia.sql` |

### Sistema 16: Conversaciones NPC ✨ NUEVO

**Características:**

🗣️ **Conversaciones NPC-to-NPC**
- ~50 conversaciones por año durante simulación
- 8 categorías: saludo, comercio, familia, guerra, religión, chisme, conflicto, alianza
- Generación con templates (rápido, no requiere LLM)

📢 **Sistema de Rumores**
- 10% de conversaciones generan rumores
- Propagación con "efecto teléfono descompuesto"
- Veracidad degrada con el tiempo
- Rumores se extinguen tras 50+ propagaciones

📚 **Conocimiento Cultural**
- Leyendas, tradiciones, tabúes, rituales, técnicas
- Generado orgánicamente por NPCs
- Vinculado a civilizaciones
- Transmisión oral y escrita

**Archivos:**
- `sistema_conversaciones_npcs.py`
- `simulacion_mundo_completo.py` (integración)

---

## 🗣️ NPCs y Conversaciones

### Durante Simulación (FASE 1)

**Templates rápidos:**
```python
"{p1} negocia con {p2} sobre {tema} en {lugar}"
"{p1} discute estrategias de guerra con {p2} en {lugar}"
"{p1} comparte rumores con {p2} en {lugar}"
```

**Resultado:**
- 75,000+ conversaciones generadas
- Historia social completa
- Rumores que se propagan
- Cultura que emerge

### Con Jugadores (FASE 2)

**LLM Local + Memoria:**
```python
# Sistema de 3 capas
- Memoria de trabajo: Conversación actual
- Memoria episódica: Eventos con jugador (ChromaDB)
- Memoria semántica: Conocimiento cultural (RAG)

# NPC recuerda:
- Conversaciones previas con jugador
- Eventos compartidos
- Grupo de jugadores presente
- Historia del mundo (1500 años)
```

**Tecnología:**
- Ollama (Llama 3 8B) - 100% local
- ChromaDB - Vector database
- sentence-transformers - Embeddings
- RAG - Retrieval Augmented Generation

---

## 💰 Economía Dual (Física/Cripto)

### 5 Monedas Implementadas

| Moneda | Símbolo | Tipo | Usado Por | Valor Relativo |
|--------|---------|------|-----------|----------------|
| Cacao | 🌰 | Física | NPCs | 1.0 |
| Jade | 💎 | Física | NPCs | 10.0 |
| Oro | 🟡 | Física | NPCs | 100.0 |
| **QuintoSol Coin (QSC)** | **QSC** | **CRIPTO** | **Jugadores** | **1000.0** |
| Bendición Divina | ✨ | Divina | Especial | 10000.0 |

### Modelo de Negocio

**Drops de Mobs:**
```python
mob_normal.drop() → Cacao, Jade, Oro (monedas físicas)
```

**Compra de Cripto:**
```python
# Jugador compra QSC desde tienda del juego
jugador.comprar_qsc(cantidad_real_money)
→ genera_revenue_para_desarrollador
```

**Ventajas QSC:**
```python
# NPCs aceptan QSC para mejores items
npc_herrero.vender_espada_legendaria()
→ acepta: QSC ✅
→ no acepta: Cacao ❌

# Animales míticos solo con QSC
npc_criador.vender_quetzalcoatl_bebe()
→ precio: 1000 QSC (no vendible por oro)
```

**Tablas:**
- `monedas` - Definición de monedas
- `wallets` - Saldo por persona
- `transacciones` - Histórico de pagos
- `mercado_precios` - Precios dinámicos

---

## ⏰ Servidor de Tiempo Real

### Características

**Tiempo:**
- **Producción:** 1 hora real = 1 día juego (3600 segundos)
- **Testing:** 1 minuto real = 1 día juego (60 segundos)

**Procesamiento Diario:**
```python
def process_daily_events():
    # Cada "día del juego" (cada hora real)
    - NPCs envejecen
    - Conversaciones NPCs continúan
    - Eventos aleatorios (5% probabilidad)
    - Actualizar estado del mundo
    - Guardar estado en BD
```

**Admin Console:**
```bash
/time    # Ver tiempo actual del juego
/npcs    # Ver NPCs vivos
/events  # Ver eventos recientes
/quit    # Detener servidor
```

**Archivo:** `servidor_tiempo_juego.py`

---

## 📊 Estadísticas Esperadas

### Población (Año 3000)

| Especie | Inicial | Final Estimado |
|---------|---------|----------------|
| Humanos I | 0 (generados) | 150,000 - 250,000 |
| Tlacatl de Luz | 150 | 1,500 - 2,500 |
| Sombra-Coyotes | 100 | 800 - 1,500 |
| Bio-Constructores | 180 | 2,000 - 3,500 |
| Acuátiles | 140 | 1,500 - 2,500 |
| Guerreros Solares | 200 | 2,500 - 4,000 |
| **TOTAL** | **770** | **~160,000 - 270,000** |

### Genética

- **Mutaciones:** ~100-500 personas (0.1% población)
- **Híbridos:** ~500-2,000 individuos
- **Linajes mutantes:** 20-50 familias

### Conflictos

- **Guerras inter-especies:** 4-6
- **Escaramuzas:** 20-30
- **Batallas totales:** 50-150
- **Bajas acumuladas:** ~50,000-150,000

### Conversaciones ✨ NUEVO

- **Conversaciones NPC-to-NPC:** ~75,000
- **Rumores generados:** ~7,500
- **Conocimiento cultural:** ~75 piezas

### Objetos y Organizaciones

- **Artefactos legendarios:** 5 iniciales + ~10-20 creados
- **Organizaciones activas:** 5 iniciales + ~15-30 formadas

---

## 🔧 Troubleshooting

### Error: "No se encuentra archivo X.sql"
```bash
# Verifica directorio
pwd  # Debe estar en /home/user/5Soles
ls -la *.sql
```

### Error: "Database is locked" (SQLite)
```bash
# Cierra otros procesos
lsof quinto_sol.db
kill -9 <PID>
```

### Simulación muy lenta
```bash
# Opciones:
1. Reducir poblaciones iniciales en scripts
2. Aumentar RAM disponible
3. Usar PostgreSQL (mejor performance)
4. Reducir años de simulación (testing)
```

### Error PostgreSQL: "role does not exist"
```bash
# Ver CONFIGURACION_POSTGRESQL.md
sudo -u postgres createuser quinto_sol_user
```

---

## 📚 Documentación Adicional

- **[RESUMEN_SISTEMAS_COMPLETOS.md](RESUMEN_SISTEMAS_COMPLETOS.md)** - Guía completa de todos los sistemas
- **[CONFIGURACION_POSTGRESQL.md](CONFIGURACION_POSTGRESQL.md)** - Setup PostgreSQL paso a paso
- **[SISTEMAS_COMPLETADOS.md](SISTEMAS_COMPLETADOS.md)** - Detalles sistemas principales
- **[MAPEO_ESPECIES_CIVILIZACIONES.md](MAPEO_ESPECIES_CIVILIZACIONES.md)** - Relaciones especies
- **[DISENO_ESPECIES_ANIMALES.md](DISENO_ESPECIES_ANIMALES.md)** - Sistema de fauna

---

## 🎮 Para el Juego

### Integración con Game Server

**1. Base de Datos:**
```python
# Conectar desde game server
from database_connector import DatabaseConnector

db = DatabaseConnector(db_type='postgres')
conn = db.connect()
```

**2. NPCs:**
```python
# Obtener NPCs vivos en año actual
npcs = db.execute("""
    SELECT * FROM personas
    WHERE año_nacimiento <= ? AND (año_muerte IS NULL OR año_muerte > ?)
""", (current_year, current_year))
```

**3. Chat con NPCs:**
```python
# Sistema de memoria
from npc_memory_system import NPCMemorySystem

memory = NPCMemorySystem(npc_id, player_id)
response = memory.get_response(player_message)
```

**4. Economía:**
```python
# Transacción con QSC
from economia import realizar_transaccion

realizar_transaccion(
    pagador_id=player_id,
    receptor_id=npc_id,
    moneda='QSC',
    cantidad=100,
    tipo='compra'
)
```

---

## 🚀 Roadmap

### ✅ Completado

- [x] 16 sistemas principales y adicionales
- [x] Simulación histórica 1500-3000
- [x] Sistema de conversaciones NPC
- [x] Soporte PostgreSQL
- [x] Servidor de tiempo real
- [x] Economía dual con criptomonedas

### 🔄 En Desarrollo

- [ ] Sistema IA conversacional con LLM
- [ ] Interface web para admin
- [ ] API REST para game client
- [ ] Sistema de quests generadas

### 📋 Planeado

- [ ] Migración automática SQLite → PostgreSQL
- [ ] Dashboard de estadísticas en tiempo real
- [ ] Backup automático
- [ ] Sistema de achievements
- [ ] Eventos dinámicos multiplayer

---

## 🤝 Contribuir

```bash
# Fork del repositorio
git clone https://github.com/tu-usuario/5Soles.git

# Crear branch
git checkout -b feature/nueva-caracteristica

# Commit y push
git commit -m "Añade nueva característica"
git push origin feature/nueva-caracteristica

# Crear Pull Request
```

---

## 📄 Licencia

[MIT License](LICENSE)

---

## 👥 Créditos

**Concepto y Desarrollo:** MterEcko
**Documentación:** Claude (Anthropic)
**Tecnologías:** Python, SQLite/PostgreSQL, Ollama

---

## 📞 Soporte

- **Issues:** https://github.com/usuario/5Soles/issues
- **Documentación:** Ver archivos .md en el repositorio
- **Discord:** [Invitación al servidor]

---

_Última actualización: 2025_
_Portales del Quinto Sol - MMORPG Mesoamericano_

**¡Disfruta de tu mundo simulado con 1500 años de historia!** 🌍⚔️🧬
