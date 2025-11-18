-- ========================================
-- PORTALES DEL QUINTO SOL - ESQUEMA POSTGRESQL
-- Sistema de Genealogía y Historia (1500-3000)
-- ========================================

-- EXTENSIONES
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- TABLA: ERAS - Períodos históricos
CREATE TABLE IF NOT EXISTS eras (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    año_inicio INTEGER NOT NULL,
    año_fin INTEGER,
    es_actual BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_años CHECK (año_fin IS NULL OR año_fin > año_inicio)
);

-- TABLA: ESPECIES - Razas del mundo
CREATE TABLE IF NOT EXISTS especies (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    tipo VARCHAR(50) NOT NULL, -- 'humano', 'sirviente_divino', 'otra'
    esperanza_vida_min INTEGER DEFAULT 80,
    esperanza_vida_max INTEGER DEFAULT 100,
    hijos_min INTEGER DEFAULT 4,
    hijos_max INTEGER DEFAULT 7,
    dios_creador_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TABLA: DIOSES - Entidades divinas
CREATE TABLE IF NOT EXISTS dioses (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    dominio_principal TEXT,
    culturas TEXT, -- Separadas por comas
    polaridad VARCHAR(50), -- 'Positiva', 'Negativa', 'Neutral'
    eje_tecnologico TEXT,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TABLA: CIVILIZACIONES - Culturas principales
CREATE TABLE IF NOT EXISTS civilizaciones (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    tipo VARCHAR(100), -- 'Mexica de Obsidiana', 'Mayas Celeste', etc.
    dios_patron_id INTEGER REFERENCES dioses(id),
    descripcion TEXT,
    año_fundacion INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TABLA: PUEBLOS Y CIUDADES
CREATE TABLE IF NOT EXISTS pueblos_ciudades (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    tipo VARCHAR(50), -- 'aldea', 'pueblo', 'ciudad', 'capital'
    civilizacion_id INTEGER REFERENCES civilizaciones(id),
    poblacion_aproximada INTEGER,
    nivel_zona INTEGER, -- Para el juego
    año_fundacion INTEGER,
    año_destruccion INTEGER,
    coordenadas_x REAL,
    coordenadas_y REAL,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TABLA: OFICIOS - Profesiones
CREATE TABLE IF NOT EXISTS oficios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    categoria VARCHAR(50), -- 'artesanal', 'religioso', 'militar', 'agricola', etc.
    descripcion TEXT,
    requiere_entrenamiento BOOLEAN DEFAULT TRUE,
    años_aprendizaje INTEGER DEFAULT 5,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TABLA: HABILIDADES - Habilidades especiales
CREATE TABLE IF NOT EXISTS habilidades (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    categoria VARCHAR(50), -- 'combate', 'magia', 'artesanal', 'social', etc.
    descripcion TEXT,
    dios_asociado_id INTEGER REFERENCES dioses(id),
    nivel_poder INTEGER DEFAULT 1, -- 1-10
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TABLA PRINCIPAL: PERSONAS - Individuos del mundo
CREATE TABLE IF NOT EXISTS personas (
    id SERIAL PRIMARY KEY,
    uuid UUID DEFAULT uuid_generate_v4() UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100),
    nombre_completo VARCHAR(200) GENERATED ALWAYS AS (nombre || ' ' || COALESCE(apellido, '')) STORED,

    -- Genealogía
    especie_id INTEGER NOT NULL REFERENCES especies(id),
    padre_id INTEGER REFERENCES personas(id),
    madre_id INTEGER REFERENCES personas(id),

    -- Información básica
    genero VARCHAR(20), -- 'masculino', 'femenino', 'otro'
    año_nacimiento INTEGER NOT NULL,
    año_muerte INTEGER,
    edad_muerte INTEGER GENERATED ALWAYS AS (año_muerte - año_nacimiento) STORED,
    causa_muerte VARCHAR(100), -- 'edad_avanzada', 'combate', 'enfermedad', 'accidente', 'animal_salvaje', etc.

    -- Ubicación y cultura
    lugar_nacimiento_id INTEGER REFERENCES pueblos_ciudades(id),
    lugar_residencia_id INTEGER REFERENCES pueblos_ciudades(id),
    lugar_muerte_id INTEGER REFERENCES pueblos_ciudades(id),
    civilizacion_id INTEGER REFERENCES civilizaciones(id),

    -- Estatus social y religioso
    clase_social VARCHAR(50), -- 'noble', 'sacerdote', 'guerrero', 'artesano', 'campesino'
    dios_patron_id INTEGER REFERENCES dioses(id),
    nivel_devoto INTEGER DEFAULT 1, -- 1-10

    -- Características
    descripcion TEXT,
    notas_especiales TEXT,

    -- Metadata del juego
    es_npc BOOLEAN DEFAULT TRUE,
    es_jugador BOOLEAN DEFAULT FALSE,
    nivel INTEGER DEFAULT 1,

    -- Auditoría
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT check_muerte CHECK (año_muerte IS NULL OR año_muerte >= año_nacimiento),
    CONSTRAINT check_padres CHECK (padre_id IS NULL OR padre_id != id),
    CONSTRAINT check_madres CHECK (madre_id IS NULL OR madre_id != id)
);

-- TABLA: MATRIMONIOS - Uniones entre personas
CREATE TABLE IF NOT EXISTS matrimonios (
    id SERIAL PRIMARY KEY,
    persona1_id INTEGER NOT NULL REFERENCES personas(id),
    persona2_id INTEGER NOT NULL REFERENCES personas(id),
    año_union INTEGER NOT NULL,
    año_separacion INTEGER,
    tipo_union VARCHAR(50) DEFAULT 'matrimonio', -- 'matrimonio', 'union_temporal', etc.
    lugar_union_id INTEGER REFERENCES pueblos_ciudades(id),
    hijos_totales INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT check_personas_diferentes CHECK (persona1_id != persona2_id),
    CONSTRAINT check_separacion CHECK (año_separacion IS NULL OR año_separacion >= año_union)
);

-- TABLA: PERSONA_OFICIOS - Relación muchos a muchos
CREATE TABLE IF NOT EXISTS persona_oficios (
    id SERIAL PRIMARY KEY,
    persona_id INTEGER NOT NULL REFERENCES personas(id) ON DELETE CASCADE,
    oficio_id INTEGER NOT NULL REFERENCES oficios(id),
    año_inicio INTEGER,
    año_fin INTEGER,
    nivel_maestria INTEGER DEFAULT 1, -- 1-10 (aprendiz a maestro)
    es_principal BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(persona_id, oficio_id)
);

-- TABLA: PERSONA_HABILIDADES - Relación muchos a muchos
CREATE TABLE IF NOT EXISTS persona_habilidades (
    id SERIAL PRIMARY KEY,
    persona_id INTEGER NOT NULL REFERENCES personas(id) ON DELETE CASCADE,
    habilidad_id INTEGER NOT NULL REFERENCES habilidades(id),
    año_adquisicion INTEGER,
    nivel_dominio INTEGER DEFAULT 1, -- 1-10
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(persona_id, habilidad_id)
);

-- TABLA: EVENTOS - Eventos históricos importantes
CREATE TABLE IF NOT EXISTS eventos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    tipo VARCHAR(50), -- 'batalla', 'fundacion', 'catastrofe', 'portal', etc.
    año INTEGER NOT NULL,
    era_id INTEGER REFERENCES eras(id),
    lugar_id INTEGER REFERENCES pueblos_ciudades(id),
    civilizacion_afectada_id INTEGER REFERENCES civilizaciones(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TABLA: EVENTOS_VITALES - Historial detallado de vida de personas
CREATE TABLE IF NOT EXISTS eventos_vitales (
    id SERIAL PRIMARY KEY,
    persona_id INTEGER NOT NULL REFERENCES personas(id) ON DELETE CASCADE,
    tipo_evento VARCHAR(50) NOT NULL, -- 'nacimiento', 'muerte', 'matrimonio', 'batalla', 'viaje', 'enfermedad', etc.
    año INTEGER NOT NULL,
    descripcion TEXT NOT NULL,
    lugar_id INTEGER REFERENCES pueblos_ciudades(id),
    evento_relacionado_id INTEGER REFERENCES eventos(id),
    persona_relacionada_id INTEGER REFERENCES personas(id), -- Para eventos que involucran a otra persona
    severidad VARCHAR(20), -- 'leve', 'moderado', 'grave', 'critico' (para heridas, enfermedades)
    resultado VARCHAR(100), -- 'victoria', 'derrota', 'sobrevivio', 'murio', etc.
    metadata JSONB, -- Datos adicionales flexibles
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TABLA: LINAJES - Para rastrear familias importantes
CREATE TABLE IF NOT EXISTS linajes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    fundador_id INTEGER REFERENCES personas(id),
    civilizacion_id INTEGER REFERENCES civilizaciones(id),
    año_fundacion INTEGER,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TABLA: IDIOMAS - Lenguas del mundo
CREATE TABLE IF NOT EXISTS idiomas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    codigo_iso VARCHAR(10), -- 'es', 'en', 'fr', 'ru', 'zh', 'ja', etc.
    tipo VARCHAR(50), -- 'indigena', 'moderno'
    familia_linguistica VARCHAR(100),
    hablantes_nativos INTEGER,
    descripcion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- TABLA: TRADUCCIONES - Frases y textos en múltiples idiomas
CREATE TABLE IF NOT EXISTS traducciones (
    id SERIAL PRIMARY KEY,
    clave VARCHAR(200) NOT NULL, -- Identificador único de la frase
    idioma_id INTEGER NOT NULL REFERENCES idiomas(id),
    texto TEXT NOT NULL,
    contexto VARCHAR(100), -- 'saludo', 'despedida', 'combate', 'comercio', etc.
    es_formal BOOLEAN DEFAULT FALSE,
    metadata JSONB, -- Pronunciación, notas culturales, etc.
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(clave, idioma_id)
);

-- TABLA: PERSONA_IDIOMAS - Idiomas que habla una persona
CREATE TABLE IF NOT EXISTS persona_idiomas (
    id SERIAL PRIMARY KEY,
    persona_id INTEGER NOT NULL REFERENCES personas(id) ON DELETE CASCADE,
    idioma_id INTEGER NOT NULL REFERENCES idiomas(id),
    nivel_dominio INTEGER DEFAULT 1, -- 1-10
    es_nativo BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(persona_id, idioma_id)
);

-- ÍNDICES para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_personas_padre ON personas(padre_id);
CREATE INDEX IF NOT EXISTS idx_personas_madre ON personas(madre_id);
CREATE INDEX IF NOT EXISTS idx_personas_especie ON personas(especie_id);
CREATE INDEX IF NOT EXISTS idx_personas_civilizacion ON personas(civilizacion_id);
CREATE INDEX IF NOT EXISTS idx_personas_nacimiento ON personas(año_nacimiento);
CREATE INDEX IF NOT EXISTS idx_personas_uuid ON personas(uuid);
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

-- Vista: Personas vivas en un año específico (usando función)
CREATE OR REPLACE VIEW personas_vivas AS
SELECT
    p.*,
    e.nombre as especie_nombre,
    c.nombre as civilizacion_nombre,
    d.nombre as dios_patron_nombre,
    COALESCE(p.año_muerte, 3000) - p.año_nacimiento as edad_aparente
FROM personas p
LEFT JOIN especies e ON p.especie_id = e.id
LEFT JOIN civilizaciones c ON p.civilizacion_id = c.id
LEFT JOIN dioses d ON p.dios_patron_id = d.id;

-- Vista: Árbol genealógico básico
CREATE OR REPLACE VIEW arbol_genealogico AS
SELECT
    p.id,
    p.uuid,
    p.nombre_completo,
    p.año_nacimiento,
    p.año_muerte,
    padre.nombre_completo as nombre_padre,
    madre.nombre_completo as nombre_madre,
    p.especie_id,
    p.civilizacion_id,
    p.causa_muerte
FROM personas p
LEFT JOIN personas padre ON p.padre_id = padre.id
LEFT JOIN personas madre ON p.madre_id = madre.id;

-- Vista: Estadísticas de población por civilización
CREATE OR REPLACE VIEW poblacion_por_civilizacion AS
SELECT
    c.nombre as civilizacion,
    COUNT(p.id) as total_personas,
    SUM(CASE WHEN p.año_muerte IS NULL THEN 1 ELSE 0 END) as personas_vivas,
    ROUND(AVG(CASE WHEN p.año_muerte IS NOT NULL THEN p.año_muerte - p.año_nacimiento END)::numeric, 2) as promedio_edad_muerte
FROM civilizaciones c
LEFT JOIN personas p ON c.id = p.civilizacion_id
GROUP BY c.id, c.nombre;

-- Vista: Historial completo de una persona
CREATE OR REPLACE VIEW historial_completo_personas AS
SELECT
    ev.id,
    ev.persona_id,
    p.nombre_completo,
    ev.tipo_evento,
    ev.año,
    ev.descripcion,
    pc.nombre as lugar,
    ev.resultado,
    ev.severidad
FROM eventos_vitales ev
JOIN personas p ON ev.persona_id = p.id
LEFT JOIN pueblos_ciudades pc ON ev.lugar_id = pc.id
ORDER BY ev.persona_id, ev.año;

-- FUNCIONES ÚTILES

-- Función: Obtener edad de una persona en un año específico
CREATE OR REPLACE FUNCTION obtener_edad(persona_id_param INTEGER, año_param INTEGER)
RETURNS INTEGER AS $$
DECLARE
    año_nac INTEGER;
    año_def INTEGER;
BEGIN
    SELECT año_nacimiento, año_muerte INTO año_nac, año_def
    FROM personas WHERE id = persona_id_param;

    IF año_nac IS NULL THEN
        RETURN NULL;
    END IF;

    IF año_def IS NOT NULL AND año_param > año_def THEN
        RETURN NULL; -- La persona ya murió
    END IF;

    RETURN año_param - año_nac;
END;
$$ LANGUAGE plpgsql;

-- Función: Contar descendientes directos
CREATE OR REPLACE FUNCTION contar_descendientes(persona_id_param INTEGER)
RETURNS INTEGER AS $$
BEGIN
    RETURN (
        SELECT COUNT(*)
        FROM personas
        WHERE padre_id = persona_id_param OR madre_id = persona_id_param
    );
END;
$$ LANGUAGE plpgsql;

-- Trigger: Actualizar updated_at automáticamente
CREATE OR REPLACE FUNCTION actualizar_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Aplicar trigger a todas las tablas relevantes
CREATE TRIGGER trigger_personas_updated_at
    BEFORE UPDATE ON personas
    FOR EACH ROW EXECUTE FUNCTION actualizar_updated_at();

CREATE TRIGGER trigger_civilizaciones_updated_at
    BEFORE UPDATE ON civilizaciones
    FOR EACH ROW EXECUTE FUNCTION actualizar_updated_at();

CREATE TRIGGER trigger_especies_updated_at
    BEFORE UPDATE ON especies
    FOR EACH ROW EXECUTE FUNCTION actualizar_updated_at();

-- COMENTARIOS en las tablas
COMMENT ON TABLE personas IS 'Tabla principal de individuos del mundo. Incluye humanos y otras especies.';
COMMENT ON TABLE eventos_vitales IS 'Historial detallado de eventos importantes en la vida de cada persona.';
COMMENT ON TABLE traducciones IS 'Sistema de internacionalización y multilingüe para IA conversacional.';
COMMENT ON COLUMN personas.causa_muerte IS 'Causa de muerte: edad_avanzada, combate, enfermedad, animal_salvaje, accidente, sacrificio, etc.';
COMMENT ON COLUMN eventos_vitales.metadata IS 'Datos adicionales en formato JSON, ej: {"arma": "espada", "enemigo": "Guerrero Jaguar"}';
