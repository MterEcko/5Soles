-- ================================================================
-- SCHEMA: RELACIONES ESPECIES-CIVILIZACIONES-DIOSES
-- Portales del Quinto Sol - MMORPG
-- ================================================================

-- ================================================================
-- TABLA: Relación entre Especies, Civilizaciones y Dioses
-- ================================================================
CREATE TABLE IF NOT EXISTS especies_civilizaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    especie_id INTEGER NOT NULL,
    civilizacion_id INTEGER NOT NULL,
    dios_patron_id INTEGER,  -- NULL for species that don't serve a specific god

    -- Tipo de relación
    tipo_relacion VARCHAR(50) DEFAULT 'aliado',  -- 'sirviente_directo', 'adorador', 'aliado', 'neutral', 'hostil'

    -- Nivel de devoción/lealtad
    nivel_devocion INTEGER DEFAULT 50,  -- 0-100
    nivel_confianza INTEGER DEFAULT 50,  -- 0-100 entre especie y civilización

    -- Fechas de la relación
    año_inicio_relacion INTEGER NOT NULL,
    año_fin_relacion INTEGER,  -- NULL si sigue activa

    -- Beneficios mutuos
    bonificacion_comercio INTEGER DEFAULT 0,  -- % de descuento en comercio
    bonificacion_diplomacia INTEGER DEFAULT 0,  -- % bonus en negociaciones
    acceso_zonas BOOLEAN DEFAULT 0,  -- Acceso a ciudades/templos

    -- Restricciones
    puede_residir BOOLEAN DEFAULT 1,  -- Puede vivir en ciudades de esta civilización
    puede_comerciar BOOLEAN DEFAULT 1,
    puede_casarse BOOLEAN DEFAULT 0,  -- Matrimonios inter-especies

    -- Historia
    eventos_importantes TEXT,  -- JSON: [{año, evento, impacto}]

    FOREIGN KEY (especie_id) REFERENCES especies(id) ON DELETE CASCADE,
    FOREIGN KEY (civilizacion_id) REFERENCES civilizaciones(id) ON DELETE CASCADE,
    FOREIGN KEY (dios_patron_id) REFERENCES dioses(id) ON DELETE CASCADE,
    UNIQUE(especie_id, civilizacion_id, año_inicio_relacion)
);

-- ================================================================
-- TABLA: Tratados y Alianzas entre Especies
-- ================================================================
CREATE TABLE IF NOT EXISTS tratados_especies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    especie_1_id INTEGER NOT NULL,
    especie_2_id INTEGER NOT NULL,

    tipo_tratado VARCHAR(50),  -- 'paz', 'alianza', 'comercio', 'no_agresion', 'union'

    año_firma INTEGER NOT NULL,
    año_expiracion INTEGER,  -- NULL = indefinido
    año_roto INTEGER,  -- NULL si sigue vigente

    -- Términos del tratado
    terminos TEXT NOT NULL,  -- JSON con detalles

    -- Firmantes
    firmado_por_especie_1 VARCHAR(200),  -- Nombre del líder/representante
    firmado_por_especie_2 VARCHAR(200),

    -- Cumplimiento
    violaciones INTEGER DEFAULT 0,
    estado VARCHAR(20) DEFAULT 'activo',  -- 'activo', 'suspendido', 'roto', 'expirado'

    FOREIGN KEY (especie_1_id) REFERENCES especies(id) ON DELETE CASCADE,
    FOREIGN KEY (especie_2_id) REFERENCES especies(id) ON DELETE CASCADE,
    CHECK (especie_1_id < especie_2_id)  -- Evitar duplicados
);

-- ================================================================
-- TABLA: Diplomacia entre Especies
-- ================================================================
CREATE TABLE IF NOT EXISTS diplomacia_especies (
    especie_id INTEGER NOT NULL,
    especie_objetivo_id INTEGER NOT NULL,

    -- Relación actual
    nivel_relacion INTEGER DEFAULT 0,  -- -100 (guerra) a +100 (aliados perfectos)
    estado_diplomatico VARCHAR(50) DEFAULT 'neutral',  -- 'guerra', 'hostil', 'neutral', 'amistoso', 'aliado'

    -- Historial
    guerras_totales INTEGER DEFAULT 0,
    alianzas_totales INTEGER DEFAULT 0,
    tratados_rotos INTEGER DEFAULT 0,

    -- Última actualización
    ultimo_cambio_año INTEGER,
    ultimo_evento TEXT,  -- Descripción del último evento que afectó la relación

    PRIMARY KEY (especie_id, especie_objetivo_id),
    FOREIGN KEY (especie_id) REFERENCES especies(id) ON DELETE CASCADE,
    FOREIGN KEY (especie_objetivo_id) REFERENCES especies(id) ON DELETE CASCADE
);

-- ================================================================
-- TABLA: Embajadores entre Especies
-- ================================================================
CREATE TABLE IF NOT EXISTS embajadores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    persona_id INTEGER NOT NULL,  -- El embajador
    especie_origen_id INTEGER NOT NULL,
    especie_destino_id INTEGER NOT NULL,
    civilizacion_destino_id INTEGER,

    año_nombramiento INTEGER NOT NULL,
    año_fin_servicio INTEGER,

    -- Efectividad
    nivel_diplomacia INTEGER DEFAULT 50,  -- Skill del embajador
    tratados_exitosos INTEGER DEFAULT 0,
    conflictos_resueltos INTEGER DEFAULT 0,

    estado VARCHAR(20) DEFAULT 'activo',  -- 'activo', 'retirado', 'expulsado', 'fallecido'

    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE,
    FOREIGN KEY (especie_origen_id) REFERENCES especies(id),
    FOREIGN KEY (especie_destino_id) REFERENCES especies(id),
    FOREIGN KEY (civilizacion_destino_id) REFERENCES civilizaciones(id)
);

-- ================================================================
-- ÍNDICES
-- ================================================================
CREATE INDEX IF NOT EXISTS idx_esp_civ_especie ON especies_civilizaciones(especie_id);
CREATE INDEX IF NOT EXISTS idx_esp_civ_civilizacion ON especies_civilizaciones(especie_id);
CREATE INDEX IF NOT EXISTS idx_esp_civ_dios ON especies_civilizaciones(dios_patron_id);
CREATE INDEX IF NOT EXISTS idx_esp_civ_tipo ON especies_civilizaciones(tipo_relacion);
CREATE INDEX IF NOT EXISTS idx_tratados_esp1 ON tratados_especies(especie_1_id);
CREATE INDEX IF NOT EXISTS idx_tratados_esp2 ON tratados_especies(especie_2_id);
CREATE INDEX IF NOT EXISTS idx_tratados_estado ON tratados_especies(estado);
CREATE INDEX IF NOT EXISTS idx_diplomacia_nivel ON diplomacia_especies(nivel_relacion);
CREATE INDEX IF NOT EXISTS idx_embajadores_persona ON embajadores(persona_id);
CREATE INDEX IF NOT EXISTS idx_embajadores_activos ON embajadores(estado);

-- ================================================================
-- FIN DEL SCHEMA
-- ================================================================
