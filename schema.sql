-- ========================================
-- PORTALES DEL QUINTO SOL - ESQUEMA DE BASE DE DATOS
-- Sistema de Genealogía y Historia (1500-3000)
-- ========================================

-- TABLA: ERAS - Períodos históricos
CREATE TABLE IF NOT EXISTS eras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    año_inicio INTEGER NOT NULL,
    año_fin INTEGER,
    es_actual BOOLEAN DEFAULT 0,
    CONSTRAINT check_años CHECK (año_fin IS NULL OR año_fin > año_inicio)
);

-- TABLA: ESPECIES - Razas del mundo
CREATE TABLE IF NOT EXISTS especies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    tipo VARCHAR(50) NOT NULL, -- 'humano', 'sirviente_divino', 'otra'
    esperanza_vida_min INTEGER DEFAULT 80,
    esperanza_vida_max INTEGER DEFAULT 100,
    hijos_min INTEGER DEFAULT 4,
    hijos_max INTEGER DEFAULT 7,
    dios_creador_id INTEGER,
    FOREIGN KEY (dios_creador_id) REFERENCES dioses(id)
);

-- TABLA: DIOSES - Entidades divinas
CREATE TABLE IF NOT EXISTS dioses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    dominio_principal TEXT,
    culturas TEXT, -- Separadas por comas
    polaridad VARCHAR(50), -- 'Positiva', 'Negativa', 'Neutral'
    eje_tecnologico TEXT,
    descripcion TEXT
);

-- TABLA: CIVILIZACIONES - Culturas principales
CREATE TABLE IF NOT EXISTS civilizaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    tipo VARCHAR(100), -- 'Mexica de Obsidiana', 'Mayas Celeste', etc.
    dios_patron_id INTEGER,
    descripcion TEXT,
    año_fundacion INTEGER,
    FOREIGN KEY (dios_patron_id) REFERENCES dioses(id)
);

-- TABLA: PUEBLOS Y CIUDADES
CREATE TABLE IF NOT EXISTS pueblos_ciudades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(200) NOT NULL,
    tipo VARCHAR(50), -- 'aldea', 'pueblo', 'ciudad', 'capital'
    civilizacion_id INTEGER,
    poblacion_aproximada INTEGER,
    nivel_zona INTEGER, -- Para el juego
    año_fundacion INTEGER,
    año_destruccion INTEGER,
    coordenadas_x REAL,
    coordenadas_y REAL,
    descripcion TEXT,
    FOREIGN KEY (civilizacion_id) REFERENCES civilizaciones(id)
);

-- TABLA: OFICIOS - Profesiones
CREATE TABLE IF NOT EXISTS oficios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    categoria VARCHAR(50), -- 'artesanal', 'religioso', 'militar', 'agricola', etc.
    descripcion TEXT,
    requiere_entrenamiento BOOLEAN DEFAULT 1,
    años_aprendizaje INTEGER DEFAULT 5
);

-- TABLA: HABILIDADES - Habilidades especiales
CREATE TABLE IF NOT EXISTS habilidades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    categoria VARCHAR(50), -- 'combate', 'magia', 'artesanal', 'social', etc.
    descripcion TEXT,
    dios_asociado_id INTEGER,
    nivel_poder INTEGER DEFAULT 1, -- 1-10
    FOREIGN KEY (dios_asociado_id) REFERENCES dioses(id)
);

-- TABLA PRINCIPAL: PERSONAS - Individuos del mundo
CREATE TABLE IF NOT EXISTS personas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100),
    nombre_completo VARCHAR(200) GENERATED ALWAYS AS (nombre || ' ' || COALESCE(apellido, '')) STORED,

    -- Genealogía
    especie_id INTEGER NOT NULL,
    padre_id INTEGER,
    madre_id INTEGER,

    -- Información básica
    genero VARCHAR(20), -- 'masculino', 'femenino', 'otro'
    año_nacimiento INTEGER NOT NULL,
    año_muerte INTEGER,
    edad_actual INTEGER, -- Se calcula
    causa_muerte VARCHAR(100), -- 'edad_avanzada', 'combate', 'enfermedad', 'accidente', 'animal_salvaje', etc.

    -- Ubicación y cultura
    lugar_nacimiento_id INTEGER,
    lugar_residencia_id INTEGER,
    civilizacion_id INTEGER,

    -- Estatus social y religioso
    clase_social VARCHAR(50), -- 'noble', 'sacerdote', 'guerrero', 'artesano', 'campesino'
    dios_patron_id INTEGER,
    nivel_devoto INTEGER DEFAULT 1, -- 1-10

    -- Características
    descripcion TEXT,
    notas_especiales TEXT,

    -- Metadata del juego
    es_npc BOOLEAN DEFAULT 1,
    es_jugador BOOLEAN DEFAULT 0,
    nivel INTEGER DEFAULT 1,

    FOREIGN KEY (especie_id) REFERENCES especies(id),
    FOREIGN KEY (padre_id) REFERENCES personas(id),
    FOREIGN KEY (madre_id) REFERENCES personas(id),
    FOREIGN KEY (lugar_nacimiento_id) REFERENCES pueblos_ciudades(id),
    FOREIGN KEY (lugar_residencia_id) REFERENCES pueblos_ciudades(id),
    FOREIGN KEY (civilizacion_id) REFERENCES civilizaciones(id),
    FOREIGN KEY (dios_patron_id) REFERENCES dioses(id),
    CONSTRAINT check_muerte CHECK (año_muerte IS NULL OR año_muerte >= año_nacimiento),
    CONSTRAINT check_padres CHECK (padre_id IS NULL OR padre_id != id),
    CONSTRAINT check_madres CHECK (madre_id IS NULL OR madre_id != id)
);

-- TABLA: MATRIMONIOS - Uniones entre personas
CREATE TABLE IF NOT EXISTS matrimonios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    persona1_id INTEGER NOT NULL,
    persona2_id INTEGER NOT NULL,
    año_union INTEGER NOT NULL,
    año_separacion INTEGER,
    tipo_union VARCHAR(50) DEFAULT 'matrimonio', -- 'matrimonio', 'union_temporal', etc.
    lugar_union_id INTEGER,
    hijos_totales INTEGER DEFAULT 0,
    FOREIGN KEY (persona1_id) REFERENCES personas(id),
    FOREIGN KEY (persona2_id) REFERENCES personas(id),
    FOREIGN KEY (lugar_union_id) REFERENCES pueblos_ciudades(id),
    CONSTRAINT check_personas_diferentes CHECK (persona1_id != persona2_id),
    CONSTRAINT check_separacion CHECK (año_separacion IS NULL OR año_separacion >= año_union)
);

-- TABLA: PERSONA_OFICIOS - Relación muchos a muchos
CREATE TABLE IF NOT EXISTS persona_oficios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    persona_id INTEGER NOT NULL,
    oficio_id INTEGER NOT NULL,
    año_inicio INTEGER,
    año_fin INTEGER,
    nivel_maestria INTEGER DEFAULT 1, -- 1-10 (aprendiz a maestro)
    es_principal BOOLEAN DEFAULT 0,
    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE,
    FOREIGN KEY (oficio_id) REFERENCES oficios(id),
    UNIQUE(persona_id, oficio_id)
);

-- TABLA: PERSONA_HABILIDADES - Relación muchos a muchos
CREATE TABLE IF NOT EXISTS persona_habilidades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    persona_id INTEGER NOT NULL,
    habilidad_id INTEGER NOT NULL,
    año_adquisicion INTEGER,
    nivel_dominio INTEGER DEFAULT 1, -- 1-10
    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE,
    FOREIGN KEY (habilidad_id) REFERENCES habilidades(id),
    UNIQUE(persona_id, habilidad_id)
);

-- TABLA: EVENTOS - Eventos históricos importantes
CREATE TABLE IF NOT EXISTS eventos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    tipo VARCHAR(50), -- 'batalla', 'fundacion', 'catastrofe', 'portal', etc.
    año INTEGER NOT NULL,
    era_id INTEGER,
    lugar_id INTEGER,
    civilizacion_afectada_id INTEGER,
    FOREIGN KEY (era_id) REFERENCES eras(id),
    FOREIGN KEY (lugar_id) REFERENCES pueblos_ciudades(id),
    FOREIGN KEY (civilizacion_afectada_id) REFERENCES civilizaciones(id)
);

-- TABLA: LINAJES - Para rastrear familias importantes
CREATE TABLE IF NOT EXISTS linajes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    fundador_id INTEGER,
    civilizacion_id INTEGER,
    año_fundacion INTEGER,
    descripcion TEXT,
    FOREIGN KEY (fundador_id) REFERENCES personas(id),
    FOREIGN KEY (civilizacion_id) REFERENCES civilizaciones(id)
);

-- TABLA: EVENTOS_VITALES - Historial detallado de vida de personas
CREATE TABLE IF NOT EXISTS eventos_vitales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    persona_id INTEGER NOT NULL,
    tipo_evento VARCHAR(50) NOT NULL, -- 'nacimiento', 'muerte', 'matrimonio', 'batalla', 'viaje', 'enfermedad', etc.
    año INTEGER NOT NULL,
    descripcion TEXT NOT NULL,
    lugar_id INTEGER,
    evento_relacionado_id INTEGER,
    persona_relacionada_id INTEGER, -- Para eventos que involucran a otra persona
    severidad VARCHAR(20), -- 'leve', 'moderado', 'grave', 'critico' (para heridas, enfermedades)
    resultado VARCHAR(100), -- 'victoria', 'derrota', 'sobrevivio', 'murio', etc.
    metadata TEXT, -- JSON en texto para SQLite
    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE,
    FOREIGN KEY (lugar_id) REFERENCES pueblos_ciudades(id),
    FOREIGN KEY (evento_relacionado_id) REFERENCES eventos(id),
    FOREIGN KEY (persona_relacionada_id) REFERENCES personas(id)
);

-- TABLA: IDIOMAS - Lenguas del mundo
CREATE TABLE IF NOT EXISTS idiomas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    codigo_iso VARCHAR(10), -- 'es', 'en', 'fr', 'ru', 'zh', 'ja', etc.
    tipo VARCHAR(50), -- 'indigena', 'moderno'
    familia_linguistica VARCHAR(100),
    hablantes_nativos INTEGER,
    descripcion TEXT
);

-- TABLA: TRADUCCIONES - Frases y textos en múltiples idiomas
CREATE TABLE IF NOT EXISTS traducciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    clave VARCHAR(200) NOT NULL, -- Identificador único de la frase
    idioma_id INTEGER NOT NULL,
    texto TEXT NOT NULL,
    contexto VARCHAR(100), -- 'saludo', 'despedida', 'combate', 'comercio', etc.
    es_formal BOOLEAN DEFAULT 0,
    metadata TEXT, -- JSON: pronunciación, notas culturales, etc.
    FOREIGN KEY (idioma_id) REFERENCES idiomas(id),
    UNIQUE(clave, idioma_id)
);

-- TABLA: PERSONA_IDIOMAS - Idiomas que habla una persona
CREATE TABLE IF NOT EXISTS persona_idiomas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    persona_id INTEGER NOT NULL,
    idioma_id INTEGER NOT NULL,
    nivel_dominio INTEGER DEFAULT 1, -- 1-10
    es_nativo BOOLEAN DEFAULT 0,
    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE,
    FOREIGN KEY (idioma_id) REFERENCES idiomas(id),
    UNIQUE(persona_id, idioma_id)
);

-- ÍNDICES para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_personas_padre ON personas(padre_id);
CREATE INDEX IF NOT EXISTS idx_personas_madre ON personas(madre_id);
CREATE INDEX IF NOT EXISTS idx_personas_especie ON personas(especie_id);
CREATE INDEX IF NOT EXISTS idx_personas_civilizacion ON personas(civilizacion_id);
CREATE INDEX IF NOT EXISTS idx_personas_nacimiento ON personas(año_nacimiento);
CREATE INDEX IF NOT EXISTS idx_matrimonios_persona1 ON matrimonios(persona1_id);
CREATE INDEX IF NOT EXISTS idx_matrimonios_persona2 ON matrimonios(persona2_id);
CREATE INDEX IF NOT EXISTS idx_eventos_año ON eventos(año);
CREATE INDEX IF NOT EXISTS idx_eventos_vitales_persona ON eventos_vitales(persona_id);
CREATE INDEX IF NOT EXISTS idx_eventos_vitales_año ON eventos_vitales(año);
CREATE INDEX IF NOT EXISTS idx_eventos_vitales_tipo ON eventos_vitales(tipo_evento);
CREATE INDEX IF NOT EXISTS idx_traducciones_clave ON traducciones(clave);
CREATE INDEX IF NOT EXISTS idx_traducciones_idioma ON traducciones(idioma_id);
CREATE INDEX IF NOT EXISTS idx_traducciones_contexto ON traducciones(contexto);

-- VISTAS ÚTILES

-- Vista: Personas vivas en un año específico
CREATE VIEW IF NOT EXISTS personas_vivas AS
SELECT
    p.*,
    e.nombre as especie_nombre,
    c.nombre as civilizacion_nombre,
    d.nombre as dios_patron_nombre
FROM personas p
LEFT JOIN especies e ON p.especie_id = e.id
LEFT JOIN civilizaciones c ON p.civilizacion_id = c.id
LEFT JOIN dioses d ON p.dios_patron_id = d.id;

-- Vista: Árbol genealógico básico
CREATE VIEW IF NOT EXISTS arbol_genealogico AS
SELECT
    p.id,
    p.nombre_completo,
    p.año_nacimiento,
    p.año_muerte,
    padre.nombre_completo as nombre_padre,
    madre.nombre_completo as nombre_madre,
    p.especie_id,
    p.civilizacion_id
FROM personas p
LEFT JOIN personas padre ON p.padre_id = padre.id
LEFT JOIN personas madre ON p.madre_id = madre.id;

-- Vista: Estadísticas de población por civilización y era
CREATE VIEW IF NOT EXISTS poblacion_por_civilizacion AS
SELECT
    c.nombre as civilizacion,
    COUNT(p.id) as total_personas,
    SUM(CASE WHEN p.año_muerte IS NULL THEN 1 ELSE 0 END) as personas_vivas,
    AVG(CASE WHEN p.año_muerte IS NOT NULL THEN p.año_muerte - p.año_nacimiento END) as promedio_edad_muerte
FROM civilizaciones c
LEFT JOIN personas p ON c.id = p.civilizacion_id
GROUP BY c.id, c.nombre;
