-- ================================================================
-- SCHEMA: ESPECIES SIRVIENTES Y SISTEMA DE FAUNA
-- Portales del Quinto Sol - MMORPG
-- ================================================================

-- ================================================================
-- TABLA: Características evolutivas de especies
-- ================================================================
CREATE TABLE IF NOT EXISTS especies_stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    especie_id INTEGER NOT NULL,
    año INTEGER NOT NULL,
    inteligencia_base INTEGER DEFAULT 100,  -- Humanos = 100
    esperanza_vida INTEGER DEFAULT 80,
    resistencia_fisica INTEGER DEFAULT 100,  -- Porcentaje (100 = normal)
    resistencia_magica INTEGER DEFAULT 100,
    fertilidad_min INTEGER DEFAULT 4,  -- Hijos mínimos
    fertilidad_max INTEGER DEFAULT 7,  -- Hijos máximos
    edad_madurez INTEGER DEFAULT 16,
    -- Stats de combate
    fuerza INTEGER DEFAULT 100,
    agilidad INTEGER DEFAULT 100,
    magia INTEGER DEFAULT 100,
    sigilo INTEGER DEFAULT 100,
    FOREIGN KEY (especie_id) REFERENCES especies(id) ON DELETE CASCADE,
    UNIQUE(especie_id, año)
);

-- ================================================================
-- TABLA: Habilidades especiales por especie
-- ================================================================
CREATE TABLE IF NOT EXISTS especies_habilidades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    especie_id INTEGER NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    tipo VARCHAR(50),  -- 'pasiva', 'activa', 'racial'
    potencia INTEGER DEFAULT 100,  -- Escala 0-200
    costo_mana INTEGER DEFAULT 0,
    cooldown_dias INTEGER DEFAULT 0,
    FOREIGN KEY (especie_id) REFERENCES especies(id) ON DELETE CASCADE
);

-- ================================================================
-- TABLA: Guerras inter-especies
-- ================================================================
CREATE TABLE IF NOT EXISTS guerras_especies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(200),
    año_inicio INTEGER NOT NULL,
    año_fin INTEGER,
    especie_atacante_id INTEGER NOT NULL,
    especie_defensora_id INTEGER NOT NULL,
    motivo TEXT,
    ganador_especie_id INTEGER,
    bajas_atacante INTEGER DEFAULT 0,
    bajas_defensor INTEGER DEFAULT 0,
    -- Efectos post-guerra
    territorio_ganado TEXT,  -- JSON con IDs de pueblos/ciudades
    reparaciones INTEGER DEFAULT 0,  -- Oro/recursos
    tratado_paz TEXT,
    FOREIGN KEY (especie_atacante_id) REFERENCES especies(id),
    FOREIGN KEY (especie_defensora_id) REFERENCES especies(id),
    FOREIGN KEY (ganador_especie_id) REFERENCES especies(id)
);

-- ================================================================
-- TABLA: Especies animales (NO genealógicas)
-- ================================================================
CREATE TABLE IF NOT EXISTS especies_animales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_comun VARCHAR(100) NOT NULL UNIQUE,
    nombre_nahuatl VARCHAR(100),
    categoria VARCHAR(50) DEFAULT 'salvaje',  -- 'domestico', 'salvaje', 'mitologico'
    peligrosidad VARCHAR(20) DEFAULT 'baja',  -- 'ninguna', 'baja', 'media', 'alta', 'extrema', 'legendaria'
    valor_mercado INTEGER DEFAULT 0,
    descripcion TEXT,
    -- Características
    tamaño VARCHAR(20),  -- 'pequeño', 'mediano', 'grande', 'gigante'
    dieta VARCHAR(50),  -- 'herbivoro', 'carnivoro', 'omnivoro'
    velocidad INTEGER DEFAULT 100,  -- Relativo (humano = 100)
    -- Habilidades especiales (JSON)
    habilidades_especiales TEXT,  -- JSON: [{"nombre": "Respirar bajo agua", "descripcion": "..."}]
    -- Biomas (JSON)
    biomas_preferidos TEXT,  -- JSON: ['bosque', 'agua', 'montaña', 'ciudad']
    -- Spawn
    rareza FLOAT DEFAULT 1.0,  -- 0.01 (muy raro) - 1.0 (muy común)
    es_vendible BOOLEAN DEFAULT 1,
    es_capturable BOOLEAN DEFAULT 1,
    nivel_min_captura INTEGER DEFAULT 1
);

-- ================================================================
-- TABLA: Fauna por zona (Sistema de Spawn)
-- ================================================================
CREATE TABLE IF NOT EXISTS fauna_zonas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    zona_id INTEGER NOT NULL,
    especie_animal_id INTEGER NOT NULL,
    densidad_base INTEGER DEFAULT 10,  -- Cantidad base de spawns
    densidad_actual INTEGER DEFAULT 10,  -- Cantidad actual (varía con caza)
    -- Comportamiento en esta zona
    agresividad INTEGER DEFAULT 0,  -- 0-100 (puede variar por zona)
    estado VARCHAR(50) DEFAULT 'salvaje',  -- 'salvaje', 'domestico', 'feral', 'protegido'
    -- Spawn
    probabilidad_spawn FLOAT DEFAULT 1.0,  -- 0.0-1.0
    ultimo_respawn INTEGER,  -- Año del último respawn
    dias_respawn INTEGER DEFAULT 30,  -- Cada cuántos días regenera población
    FOREIGN KEY (zona_id) REFERENCES pueblos_ciudades(id) ON DELETE CASCADE,
    FOREIGN KEY (especie_animal_id) REFERENCES especies_animales(id) ON DELETE CASCADE,
    UNIQUE(zona_id, especie_animal_id)
);

-- ================================================================
-- TABLA: Animales individuales (SOLO importantes)
-- ================================================================
CREATE TABLE IF NOT EXISTS animales_individuales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    especie_id INTEGER NOT NULL,
    nombre VARCHAR(100),  -- Solo si tienen nombre
    dueño_id INTEGER,  -- NULL = salvaje
    zona_actual_id INTEGER,
    año_nacimiento INTEGER NOT NULL,
    año_muerte INTEGER,
    causa_muerte VARCHAR(100),
    -- Clasificación
    es_montura BOOLEAN DEFAULT 0,
    es_mascota BOOLEAN DEFAULT 0,
    es_mitologico BOOLEAN DEFAULT 0,
    es_legendario BOOLEAN DEFAULT 0,  -- Único en el mundo
    -- Stats
    nivel_entrenamiento INTEGER DEFAULT 0,  -- 0-100
    lealtad INTEGER DEFAULT 50,  -- 0-100 (solo mascotas/monturas)
    salud_actual INTEGER DEFAULT 100,
    salud_maxima INTEGER DEFAULT 100,
    -- Características especiales (para mitológicos)
    poderes_especiales TEXT,  -- JSON
    vinculos_espirituales TEXT,  -- JSON: IDs de personas vinculadas
    -- Mercado
    valor_estimado INTEGER DEFAULT 0,
    es_vendible BOOLEAN DEFAULT 1,
    FOREIGN KEY (especie_id) REFERENCES especies_animales(id),
    FOREIGN KEY (dueño_id) REFERENCES personas(id) ON DELETE SET NULL,
    FOREIGN KEY (zona_actual_id) REFERENCES pueblos_ciudades(id)
);

-- ================================================================
-- TABLA: Eventos de spawn de mitológicos
-- ================================================================
CREATE TABLE IF NOT EXISTS eventos_spawn_mitologicos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    especie_animal_id INTEGER NOT NULL,
    zona_id INTEGER NOT NULL,
    año INTEGER NOT NULL,
    tipo_evento VARCHAR(100),  -- 'tormenta', 'eclipse', 'erupcion', 'ritual'
    fue_capturado BOOLEAN DEFAULT 0,
    capturado_por_id INTEGER,  -- ID de persona
    animal_individual_id INTEGER,  -- Si fue capturado
    FOREIGN KEY (especie_animal_id) REFERENCES especies_animales(id),
    FOREIGN KEY (zona_id) REFERENCES pueblos_ciudades(id),
    FOREIGN KEY (capturado_por_id) REFERENCES personas(id),
    FOREIGN KEY (animal_individual_id) REFERENCES animales_individuales(id)
);

-- ================================================================
-- TABLA: Comercio de animales
-- ================================================================
CREATE TABLE IF NOT EXISTS mercado_animales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    animal_id INTEGER NOT NULL,
    vendedor_id INTEGER,
    comprador_id INTEGER,
    zona_id INTEGER NOT NULL,
    año_venta INTEGER NOT NULL,
    precio INTEGER NOT NULL,
    tipo_venta VARCHAR(50),  -- 'compra_normal', 'subasta', 'mercado_negro', 'intercambio'
    estado_animal VARCHAR(50),  -- 'sano', 'herido', 'enfermo', 'entrenado'
    FOREIGN KEY (animal_id) REFERENCES animales_individuales(id),
    FOREIGN KEY (vendedor_id) REFERENCES personas(id),
    FOREIGN KEY (comprador_id) REFERENCES personas(id),
    FOREIGN KEY (zona_id) REFERENCES pueblos_ciudades(id)
);

-- ================================================================
-- TABLA: Vínculo Nagual (Animal espiritual)
-- ================================================================
CREATE TABLE IF NOT EXISTS vinculos_nagual (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    persona_id INTEGER NOT NULL,
    animal_nagual_id INTEGER NOT NULL,
    año_vinculo INTEGER NOT NULL,
    tipo_vinculo VARCHAR(50),  -- 'nacimiento', 'ritual', 'vision'
    fuerza_vinculo INTEGER DEFAULT 50,  -- 0-100
    habilidades_compartidas TEXT,  -- JSON
    estado VARCHAR(50) DEFAULT 'activo',  -- 'activo', 'debilitado', 'roto'
    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE,
    FOREIGN KEY (animal_nagual_id) REFERENCES animales_individuales(id) ON DELETE CASCADE,
    UNIQUE(persona_id)  -- Solo 1 nagual por persona
);

-- ================================================================
-- ÍNDICES para optimización
-- ================================================================
CREATE INDEX IF NOT EXISTS idx_especies_stats_año ON especies_stats(especie_id, año);
CREATE INDEX IF NOT EXISTS idx_guerras_especies_año ON guerras_especies(año_inicio, año_fin);
CREATE INDEX IF NOT EXISTS idx_fauna_zonas_zona ON fauna_zonas(zona_id);
CREATE INDEX IF NOT EXISTS idx_fauna_zonas_especie ON fauna_zonas(especie_animal_id);
CREATE INDEX IF NOT EXISTS idx_animales_ind_especie ON animales_individuales(especie_id);
CREATE INDEX IF NOT EXISTS idx_animales_ind_dueño ON animales_individuales(dueño_id);
CREATE INDEX IF NOT EXISTS idx_animales_ind_zona ON animales_individuales(zona_actual_id);
CREATE INDEX IF NOT EXISTS idx_animales_ind_mitologico ON animales_individuales(es_mitologico);
CREATE INDEX IF NOT EXISTS idx_eventos_spawn_año ON eventos_spawn_mitologicos(año);
CREATE INDEX IF NOT EXISTS idx_mercado_año ON mercado_animales(año_venta);
CREATE INDEX IF NOT EXISTS idx_vinculos_nagual_persona ON vinculos_nagual(persona_id);

-- ================================================================
-- FIN DEL SCHEMA
-- ================================================================
