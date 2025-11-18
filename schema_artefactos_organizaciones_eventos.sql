-- ================================================================
-- SCHEMAS COMBINADOS: Artefactos + Organizaciones + Eventos Divinos
-- Portales del Quinto Sol - MMORPG
-- ================================================================

-- ================================================================
-- ARTEFACTOS LEGENDARIOS
-- ================================================================

CREATE TABLE IF NOT EXISTS artefactos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(200) NOT NULL UNIQUE,
    tipo VARCHAR(50),  -- 'arma', 'armadura', 'joya', 'reliquia', 'herramienta'
    rareza VARCHAR(20),  -- 'magica', 'rara', 'epica', 'legendaria', 'divina'

    -- Creación
    creador_persona_id INTEGER,
    año_creacion INTEGER,
    lugar_creacion_id INTEGER,
    metodo_creacion VARCHAR(100),  -- 'forjado', 'bendecido', 'ritual', 'encontrado'

    -- Poder
    nivel_poder INTEGER DEFAULT 1,  -- 1-10
    modificadores_stats TEXT,  -- JSON: {fuerza: 10, agilidad: 5}
    habilidades_especiales TEXT,  -- JSON: ['lanzar_rayo', 'invisibilidad']
    maldicion TEXT,  -- Maldición del artefacto

    -- Propietario actual
    propietario_id INTEGER,
    año_adquisicion INTEGER,

    -- Historia
    leyenda TEXT,
    hazañas_realizadas TEXT,  -- JSON
    duelos_ganados INTEGER DEFAULT 0,
    muertes_causadas INTEGER DEFAULT 0,

    -- Estado
    destruido BOOLEAN DEFAULT 0,
    año_destruccion INTEGER,
    perdido BOOLEAN DEFAULT 0,
    ubicacion_desconocida TEXT,

    FOREIGN KEY (creador_persona_id) REFERENCES personas(id),
    FOREIGN KEY (lugar_creacion_id) REFERENCES pueblos_ciudades(id),
    FOREIGN KEY (propietario_id) REFERENCES personas(id)
);

CREATE TABLE IF NOT EXISTS artefactos_historia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    artefacto_id INTEGER NOT NULL,
    año_evento INTEGER NOT NULL,
    tipo_evento VARCHAR(50),  -- 'creacion', 'transferencia', 'robo', 'batalla', 'perdida'
    propietario_anterior_id INTEGER,
    propietario_nuevo_id INTEGER,
    descripcion TEXT,

    FOREIGN KEY (artefacto_id) REFERENCES artefactos(id) ON DELETE CASCADE,
    FOREIGN KEY (propietario_anterior_id) REFERENCES personas(id),
    FOREIGN KEY (propietario_nuevo_id) REFERENCES personas(id)
);

-- ================================================================
-- ORGANIZACIONES
-- ================================================================

CREATE TABLE IF NOT EXISTS organizaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(200) NOT NULL UNIQUE,
    tipo VARCHAR(50),  -- 'gremio', 'culto', 'orden_militar', 'hermandad', 'sociedad_secreta'

    -- Fundación
    año_fundacion INTEGER NOT NULL,
    fundador_id INTEGER,
    lugar_sede_id INTEGER,
    civilizacion_id INTEGER,

    -- Membresía
    miembros_actuales INTEGER DEFAULT 1,
    max_miembros INTEGER,  -- NULL = sin límite
    requisitos_entrada TEXT,  -- JSON

    -- Jerarquía
    lider_actual_id INTEGER,
    estructura_jerarquica TEXT,  -- JSON: ['maestro', 'oficial', 'aprendiz']

    -- Propósito
    proposito VARCHAR(200),
    actividades TEXT,  -- JSON

    -- Recursos
    riqueza INTEGER DEFAULT 0,
    propiedades TEXT,  -- JSON: [lugar_id, lugar_id]
    artefactos_posee TEXT,  -- JSON: [artefacto_id, ...]

    -- Reputación
    reputacion INTEGER DEFAULT 50,  -- 0-100
    fama VARCHAR(20),  -- 'desconocida', 'local', 'regional', 'legendaria'

    -- Estado
    activa BOOLEAN DEFAULT 1,
    año_disolucion INTEGER,
    razon_disolucion TEXT,

    FOREIGN KEY (fundador_id) REFERENCES personas(id),
    FOREIGN KEY (lugar_sede_id) REFERENCES pueblos_ciudades(id),
    FOREIGN KEY (lider_actual_id) REFERENCES personas(id),
    FOREIGN KEY (civilizacion_id) REFERENCES civilizaciones(id)
);

CREATE TABLE IF NOT EXISTS organizaciones_miembros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    organizacion_id INTEGER NOT NULL,
    persona_id INTEGER NOT NULL,

    año_ingreso INTEGER NOT NULL,
    año_salida INTEGER,

    rango VARCHAR(100),
    nivel_jerarquico INTEGER DEFAULT 1,

    contribuciones INTEGER DEFAULT 0,
    leal BOOLEAN DEFAULT 1,

    FOREIGN KEY (organizacion_id) REFERENCES organizaciones(id) ON DELETE CASCADE,
    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE,
    UNIQUE(organizacion_id, persona_id, año_ingreso)
);

CREATE TABLE IF NOT EXISTS organizaciones_relaciones (
    organizacion_1_id INTEGER NOT NULL,
    organizacion_2_id INTEGER NOT NULL,
    tipo_relacion VARCHAR(50),  -- 'aliada', 'neutral', 'rival', 'enemiga'
    nivel_relacion INTEGER DEFAULT 0,  -- -100 a 100

    PRIMARY KEY (organizacion_1_id, organizacion_2_id),
    FOREIGN KEY (organizacion_1_id) REFERENCES organizaciones(id) ON DELETE CASCADE,
    FOREIGN KEY (organizacion_2_id) REFERENCES organizaciones(id) ON DELETE CASCADE
);

-- ================================================================
-- EVENTOS DIVINOS EXPANDIDOS
-- ================================================================

CREATE TABLE IF NOT EXISTS eventos_divinos_mayores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dios_id INTEGER NOT NULL,
    año_evento INTEGER NOT NULL,
    tipo_evento VARCHAR(50),  -- 'bendicion_masiva', 'maldicion', 'milagro', 'castigo', 'manifestacion', 'profecia'

    -- Alcance
    alcance VARCHAR(20),  -- 'persona', 'familia', 'ciudad', 'civilizacion', 'todas_especies'
    objetivo_persona_id INTEGER,
    objetivo_lugar_id INTEGER,
    objetivo_civilizacion_id INTEGER,
    objetivo_especie_id INTEGER,

    -- Efecto
    descripcion TEXT,
    efectos TEXT,  -- JSON: {cosecha: '+300%', natalidad: '+50%'}
    duracion_años INTEGER,  -- NULL = permanente

    -- Consecuencias
    personas_afectadas INTEGER DEFAULT 0,
    muertos INTEGER DEFAULT 0,
    bendecidos INTEGER DEFAULT 0,
    malditos INTEGER DEFAULT 0,

    -- Razón
    razon TEXT,
    fue_merecido BOOLEAN,

    FOREIGN KEY (dios_id) REFERENCES dioses(id),
    FOREIGN KEY (objetivo_persona_id) REFERENCES personas(id),
    FOREIGN KEY (objetivo_lugar_id) REFERENCES pueblos_ciudades(id),
    FOREIGN KEY (objetivo_civilizacion_id) REFERENCES civilizaciones(id),
    FOREIGN KEY (objetivo_especie_id) REFERENCES especies(id)
);

CREATE TABLE IF NOT EXISTS profecias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    dios_id INTEGER NOT NULL,
    profeta_id INTEGER,  -- Quien la recibió
    año_profecia INTEGER NOT NULL,

    texto_profecia TEXT NOT NULL,
    interpretacion TEXT,

    -- Cumplimiento
    cumplida BOOLEAN DEFAULT 0,
    año_cumplimiento INTEGER,
    eventos_cumplimiento TEXT,  -- JSON

    -- Impacto
    conocida_publicamente BOOLEAN DEFAULT 0,
    influencio_decisiones BOOLEAN DEFAULT 0,

    FOREIGN KEY (dios_id) REFERENCES dioses(id),
    FOREIGN KEY (profeta_id) REFERENCES personas(id)
);

-- ================================================================
-- ÍNDICES
-- ================================================================
CREATE INDEX IF NOT EXISTS idx_artefactos_propietario ON artefactos(propietario_id);
CREATE INDEX IF NOT EXISTS idx_artefactos_creador ON artefactos(creador_persona_id);
CREATE INDEX IF NOT EXISTS idx_artefactos_historia_año ON artefactos_historia(año_evento);
CREATE INDEX IF NOT EXISTS idx_organizaciones_tipo ON organizaciones(tipo);
CREATE INDEX IF NOT EXISTS idx_organizaciones_activas ON organizaciones(activa) WHERE activa = 1;
CREATE INDEX IF NOT EXISTS idx_org_miembros_persona ON organizaciones_miembros(persona_id);
CREATE INDEX IF NOT EXISTS idx_org_miembros_org ON organizaciones_miembros(organizacion_id);
CREATE INDEX IF NOT EXISTS idx_eventos_divinos_año ON eventos_divinos_mayores(año_evento);
CREATE INDEX IF NOT EXISTS idx_eventos_divinos_dios ON eventos_divinos_mayores(dios_id);
CREATE INDEX IF NOT EXISTS idx_profecias_año ON profecias(año_profecia);

-- ================================================================
-- FIN DEL SCHEMA
-- ================================================================
