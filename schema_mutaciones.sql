-- ================================================================
-- SCHEMA: SISTEMA DE MUTACIONES GENÉTICAS
-- Portales del Quinto Sol - MMORPG
-- ================================================================

-- ================================================================
-- TABLA: Catálogo de Mutaciones
-- ================================================================
CREATE TABLE IF NOT EXISTS mutaciones_catalogo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    tipo VARCHAR(50),  -- 'fisica', 'mental', 'magica', 'divina', 'maldicion'

    -- Rareza y obtención
    rareza VARCHAR(20) DEFAULT 'comun',  -- 'comun', 'rara', 'epica', 'legendaria'
    probabilidad_natural FLOAT DEFAULT 0.001,  -- 0.1% natural

    -- Causas posibles (JSON: ['divina', 'radiacion', 'magia', 'herencia'])
    causas_posibles TEXT,

    -- Efectos en stats
    modificador_fuerza INTEGER DEFAULT 0,
    modificador_agilidad INTEGER DEFAULT 0,
    modificador_inteligencia INTEGER DEFAULT 0,
    modificador_resistencia INTEGER DEFAULT 0,
    modificador_carisma INTEGER DEFAULT 0,
    modificador_longevidad INTEGER DEFAULT 0,  -- años extras

    -- Efectos especiales (JSON)
    habilidades_especiales TEXT,  -- JSON: ['vision_nocturna', 'regeneracion', 'telepatia']
    debilidades TEXT,  -- JSON: ['luz_solar', 'agua_bendita']

    -- Genética
    es_heredable BOOLEAN DEFAULT 0,
    probabilidad_herencia FLOAT DEFAULT 0.5,  -- 50% si heredable
    dominante BOOLEAN DEFAULT 0,  -- Si es dominante sobre versión normal

    -- Visual
    cambios_fisicos TEXT,  -- JSON: {color_ojos: 'dorado', piel: 'brillante'}
    es_visible BOOLEAN DEFAULT 1
);

-- ================================================================
-- TABLA: Mutaciones de Personas
-- ================================================================
CREATE TABLE IF NOT EXISTS personas_mutaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    persona_id INTEGER NOT NULL,
    mutacion_id INTEGER NOT NULL,

    -- Origen
    año_adquisicion INTEGER NOT NULL,
    causa VARCHAR(50),  -- 'nacimiento', 'divina', 'accidente', 'ritual', 'maldicion'
    evento_origen TEXT,  -- Descripción del evento

    -- Genética
    heredada_de_id INTEGER,  -- persona_id del padre/madre que la transmitió

    -- Estado
    activa BOOLEAN DEFAULT 1,
    nivel_manifestacion INTEGER DEFAULT 1,  -- 1-10, qué tan fuerte es

    -- Control
    controlada BOOLEAN DEFAULT 0,  -- Si la persona la controla
    años_para_control INTEGER,  -- Tiempo entrenando

    -- Efectos acumulados (calculados)
    stats_modificados TEXT,  -- JSON con modificadores totales

    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE,
    FOREIGN KEY (mutacion_id) REFERENCES mutaciones_catalogo(id),
    FOREIGN KEY (heredada_de_id) REFERENCES personas(id),
    UNIQUE(persona_id, mutacion_id)  -- No tener la misma mutación dos veces
);

-- ================================================================
-- TABLA: Linajes de Mutaciones
-- ================================================================
CREATE TABLE IF NOT EXISTS linajes_mutaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_linaje VARCHAR(150) NOT NULL,
    mutacion_id INTEGER NOT NULL,

    -- Fundador del linaje
    fundador_persona_id INTEGER NOT NULL,
    año_origen INTEGER NOT NULL,

    -- Estadísticas
    generaciones INTEGER DEFAULT 1,
    miembros_totales INTEGER DEFAULT 1,
    miembros_actuales INTEGER DEFAULT 1,

    -- Evolución
    ha_evolucionado BOOLEAN DEFAULT 0,
    mutacion_evolucionada_id INTEGER,  -- Si mutó a algo más

    -- Localización
    civilizacion_origen_id INTEGER,
    lugares_predominantes TEXT,  -- JSON: [lugar_id, lugar_id]

    -- Reputación
    reputacion VARCHAR(50) DEFAULT 'desconocido',  -- 'bendicion', 'maldicion', 'temido', 'venerado'

    FOREIGN KEY (mutacion_id) REFERENCES mutaciones_catalogo(id),
    FOREIGN KEY (fundador_persona_id) REFERENCES personas(id),
    FOREIGN KEY (mutacion_evolucionada_id) REFERENCES mutaciones_catalogo(id),
    FOREIGN KEY (civilizacion_origen_id) REFERENCES civilizaciones(id)
);

-- ================================================================
-- TABLA: Eventos de Mutación
-- ================================================================
CREATE TABLE IF NOT EXISTS eventos_mutacion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    persona_id INTEGER NOT NULL,
    mutacion_id INTEGER NOT NULL,

    año_evento INTEGER NOT NULL,
    tipo_evento VARCHAR(50),  -- 'manifestacion', 'evolucion', 'perdida', 'control'

    descripcion TEXT,

    -- Contexto
    lugar_id INTEGER,
    testigos TEXT,  -- JSON: [persona_id, persona_id]

    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE,
    FOREIGN KEY (mutacion_id) REFERENCES mutaciones_catalogo(id),
    FOREIGN KEY (lugar_id) REFERENCES pueblos_ciudades(id)
);

-- ================================================================
-- ÍNDICES
-- ================================================================
CREATE INDEX IF NOT EXISTS idx_personas_mutaciones_persona ON personas_mutaciones(persona_id);
CREATE INDEX IF NOT EXISTS idx_personas_mutaciones_mutacion ON personas_mutaciones(mutacion_id);
CREATE INDEX IF NOT EXISTS idx_mutaciones_heredables ON mutaciones_catalogo(es_heredable) WHERE es_heredable = 1;
CREATE INDEX IF NOT EXISTS idx_linajes_mutacion ON linajes_mutaciones(mutacion_id);
CREATE INDEX IF NOT EXISTS idx_eventos_mutacion_año ON eventos_mutacion(año_evento);

-- ================================================================
-- FIN DEL SCHEMA
-- ================================================================
