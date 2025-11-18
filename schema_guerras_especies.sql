-- ================================================================
-- SCHEMA: SISTEMA DE GUERRAS INTER-ESPECIES
-- Portales del Quinto Sol - MMORPG
-- ================================================================

-- ================================================================
-- TABLA: Guerras entre Especies
-- ================================================================
CREATE TABLE IF NOT EXISTS guerras_especies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    especie_atacante_id INTEGER NOT NULL,
    especie_defensora_id INTEGER NOT NULL,

    -- Temporalidad
    año_inicio INTEGER NOT NULL,
    año_fin INTEGER,  -- NULL si sigue activa
    duracion_años INTEGER,  -- calculado al finalizar

    -- Causa y contexto
    causa VARCHAR(100),  -- 'territorial', 'religiosa', 'recursos', 'venganza', 'expansion', 'defensa'
    descripcion TEXT,

    -- Intensidad
    intensidad VARCHAR(50) DEFAULT 'media',  -- 'escaramuza', 'batalla', 'guerra', 'guerra_total'

    -- Ubicación
    territorio_disputa VARCHAR(200),  -- Nombre del territorio en conflicto
    civilizacion_afectada_id INTEGER,  -- Civilización donde ocurre

    -- Resultados
    vencedor_especie_id INTEGER,  -- NULL si empate/paz negociada
    tipo_victoria VARCHAR(50),  -- 'aniquilacion', 'rendicion', 'tratado', 'empate', 'retirada'

    -- Bajas
    bajas_atacante INTEGER DEFAULT 0,
    bajas_defensora INTEGER DEFAULT 0,
    civiles_muertos INTEGER DEFAULT 0,
    prisioneros INTEGER DEFAULT 0,

    -- Consecuencias
    territorios_ganados TEXT,  -- JSON: lista de territorios
    recursos_saqueados TEXT,   -- JSON: {oro, comida, armas, etc}
    artefactos_capturados TEXT,  -- JSON: lista de artefactos

    -- Impacto diplomático
    cambio_relacion_diplomatica INTEGER DEFAULT 0,  -- -50, -20, etc.
    aliados_involucrados TEXT,  -- JSON: [{especie_id, rol: 'atacante'/'defensor'}]

    -- Intervención divina
    dios_favorecio_id INTEGER,  -- Dios que intervino
    intervencion_divina TEXT,  -- JSON: descripción de la intervención

    -- Metadatos
    eventos_importantes TEXT,  -- JSON: [{año, evento, descripcion}]
    heroes_destacados TEXT,  -- JSON: [{persona_id, hazañas}]

    FOREIGN KEY (especie_atacante_id) REFERENCES especies(id),
    FOREIGN KEY (especie_defensora_id) REFERENCES especies(id),
    FOREIGN KEY (vencedor_especie_id) REFERENCES especies(id),
    FOREIGN KEY (civilizacion_afectada_id) REFERENCES civilizaciones(id),
    FOREIGN KEY (dios_favorecio_id) REFERENCES dioses(id)
);

-- ================================================================
-- TABLA: Batallas de una Guerra
-- ================================================================
CREATE TABLE IF NOT EXISTS batallas_guerras (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guerra_id INTEGER NOT NULL,

    -- Temporalidad
    año_batalla INTEGER NOT NULL,
    duracion_dias INTEGER DEFAULT 1,

    -- Ubicación
    lugar_nombre VARCHAR(200),
    lugar_id INTEGER,  -- pueblo/ciudad

    -- Fuerzas
    fuerzas_atacante INTEGER,  -- número de combatientes
    fuerzas_defensora INTEGER,

    -- Resultados
    vencedor VARCHAR(20),  -- 'atacante', 'defensor', 'empate'
    bajas_atacante INTEGER DEFAULT 0,
    bajas_defensora INTEGER DEFAULT 0,

    -- Descripción
    tipo_batalla VARCHAR(50),  -- 'asedio', 'campo_abierto', 'emboscada', 'naval', 'aerea'
    descripcion TEXT,
    tacticas_usadas TEXT,  -- JSON

    -- Héroes y eventos
    comandante_atacante_id INTEGER,  -- persona_id
    comandante_defensor_id INTEGER,
    heroes_batalla TEXT,  -- JSON: [{persona_id, hazaña}]

    FOREIGN KEY (guerra_id) REFERENCES guerras_especies(id) ON DELETE CASCADE,
    FOREIGN KEY (lugar_id) REFERENCES pueblos_ciudades(id),
    FOREIGN KEY (comandante_atacante_id) REFERENCES personas(id),
    FOREIGN KEY (comandante_defensor_id) REFERENCES personas(id)
);

-- ================================================================
-- TABLA: Conflictos Menores (Escaramuzas)
-- ================================================================
CREATE TABLE IF NOT EXISTS escaramuzas_especies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    especie_1_id INTEGER NOT NULL,
    especie_2_id INTEGER NOT NULL,

    año_incidente INTEGER NOT NULL,
    lugar_id INTEGER,

    -- Tipo de conflicto
    tipo VARCHAR(50),  -- 'fronterizo', 'comercial', 'honor', 'robo', 'asesinato'
    gravedad VARCHAR(20) DEFAULT 'menor',  -- 'menor', 'media', 'grave'

    -- Resultados
    muertos INTEGER DEFAULT 0,
    heridos INTEGER DEFAULT 0,

    -- Resolución
    resuelto BOOLEAN DEFAULT 0,
    forma_resolucion VARCHAR(100),  -- 'compensacion', 'disculpa', 'venganza', 'ignorado', 'escalado'
    escalo_a_guerra_id INTEGER,  -- Si escaló a guerra

    -- Impacto
    cambio_relacion INTEGER DEFAULT -5,  -- pequeño cambio en relación
    descripcion TEXT,

    FOREIGN KEY (especie_1_id) REFERENCES especies(id),
    FOREIGN KEY (especie_2_id) REFERENCES especies(id),
    FOREIGN KEY (lugar_id) REFERENCES pueblos_ciudades(id),
    FOREIGN KEY (escalo_a_guerra_id) REFERENCES guerras_especies(id)
);

-- ================================================================
-- TABLA: Alianzas Militares
-- ================================================================
CREATE TABLE IF NOT EXISTS alianzas_militares (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nombre VARCHAR(200) NOT NULL,
    año_formacion INTEGER NOT NULL,
    año_disolucion INTEGER,

    -- Miembros (JSON: [especie_id, especie_id, ...])
    miembros_especies TEXT NOT NULL,

    -- Propósito
    proposito VARCHAR(100),  -- 'defensa_mutua', 'expansion', 'contra_especie_X', 'comercial'
    descripcion TEXT,

    -- Activación
    activada_veces INTEGER DEFAULT 0,
    guerras_participadas TEXT,  -- JSON: [guerra_id, guerra_id, ...]

    -- Estado
    estado VARCHAR(20) DEFAULT 'activa',  -- 'activa', 'suspendida', 'disuelta', 'violada'
    violada_por_especie_id INTEGER,

    FOREIGN KEY (violada_por_especie_id) REFERENCES especies(id)
);

-- ================================================================
-- TABLA: Impacto de Guerras en Poblaciones
-- ================================================================
CREATE TABLE IF NOT EXISTS impacto_guerra_poblaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guerra_id INTEGER,
    batalla_id INTEGER,  -- NULL si es impacto general de guerra

    -- Ubicación afectada
    lugar_id INTEGER NOT NULL,

    -- Población afectada
    poblacion_antes INTEGER,
    poblacion_despues INTEGER,
    muertos_combate INTEGER DEFAULT 0,
    muertos_hambre INTEGER DEFAULT 0,
    muertos_enfermedad INTEGER DEFAULT 0,
    refugiados INTEGER DEFAULT 0,
    esclavizados INTEGER DEFAULT 0,

    -- Daños
    edificios_destruidos INTEGER DEFAULT 0,
    cosechas_perdidas INTEGER DEFAULT 0,
    saqueo_recursos INTEGER DEFAULT 0,

    -- Recuperación
    años_recuperacion INTEGER,
    ayuda_recibida TEXT,  -- JSON

    FOREIGN KEY (guerra_id) REFERENCES guerras_especies(id) ON DELETE CASCADE,
    FOREIGN KEY (batalla_id) REFERENCES batallas_guerras(id) ON DELETE CASCADE,
    FOREIGN KEY (lugar_id) REFERENCES pueblos_ciudades(id)
);

-- ================================================================
-- TABLA: Crímenes de Guerra
-- ================================================================
CREATE TABLE IF NOT EXISTS crimenes_guerra (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    guerra_id INTEGER NOT NULL,
    batalla_id INTEGER,

    año_crimen INTEGER NOT NULL,

    -- Perpetrador
    especie_perpetradora_id INTEGER NOT NULL,
    comandante_id INTEGER,  -- persona responsable

    -- Tipo de crimen
    tipo_crimen VARCHAR(100),  -- 'masacre', 'tortura', 'esclavitud', 'saqueo_templos', 'envenenamiento', 'profanacion'
    gravedad VARCHAR(20),  -- 'leve', 'grave', 'atroz'

    -- Víctimas
    victimas_especies_id INTEGER,
    numero_victimas INTEGER,
    descripcion TEXT,

    -- Consecuencias
    juicio_realizado BOOLEAN DEFAULT 0,
    castigo TEXT,
    impacto_diplomatico INTEGER DEFAULT -20,

    FOREIGN KEY (guerra_id) REFERENCES guerras_especies(id) ON DELETE CASCADE,
    FOREIGN KEY (batalla_id) REFERENCES batallas_guerras(id) ON DELETE CASCADE,
    FOREIGN KEY (especie_perpetradora_id) REFERENCES especies(id),
    FOREIGN KEY (comandante_id) REFERENCES personas(id),
    FOREIGN KEY (victimas_especies_id) REFERENCES especies(id)
);

-- ================================================================
-- ÍNDICES
-- ================================================================
CREATE INDEX IF NOT EXISTS idx_guerras_año ON guerras_especies(año_inicio);
CREATE INDEX IF NOT EXISTS idx_guerras_atacante ON guerras_especies(especie_atacante_id);
CREATE INDEX IF NOT EXISTS idx_guerras_defensora ON guerras_especies(especie_defensora_id);
CREATE INDEX IF NOT EXISTS idx_guerras_activas ON guerras_especies(año_fin) WHERE año_fin IS NULL;
CREATE INDEX IF NOT EXISTS idx_batallas_guerra ON batallas_guerras(guerra_id);
CREATE INDEX IF NOT EXISTS idx_batallas_año ON batallas_guerras(año_batalla);
CREATE INDEX IF NOT EXISTS idx_escaramuzas_especies ON escaramuzas_especies(especie_1_id, especie_2_id);
CREATE INDEX IF NOT EXISTS idx_escaramuzas_año ON escaramuzas_especies(año_incidente);
CREATE INDEX IF NOT EXISTS idx_alianzas_activas ON alianzas_militares(estado) WHERE estado = 'activa';
CREATE INDEX IF NOT EXISTS idx_impacto_lugar ON impacto_guerra_poblaciones(lugar_id);
CREATE INDEX IF NOT EXISTS idx_crimenes_guerra ON crimenes_guerra(guerra_id);

-- ================================================================
-- FIN DEL SCHEMA
-- ================================================================
