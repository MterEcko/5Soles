-- ================================================================
-- SCHEMA: MATRIMONIOS INTER-ESPECIES E HÍBRIDOS
-- Portales del Quinto Sol - MMORPG
-- ================================================================

-- ================================================================
-- TABLA: Híbridos (Personas con dos especies)
-- ================================================================
CREATE TABLE IF NOT EXISTS personas_hibridas (
    persona_id INTEGER PRIMARY KEY,
    especie_padre_id INTEGER NOT NULL,
    especie_madre_id INTEGER NOT NULL,

    -- Genética
    generacion_hibrida INTEGER DEFAULT 1,  -- 1ra gen, 2da gen, etc.
    porcentaje_especie_1 FLOAT DEFAULT 50.0,
    porcentaje_especie_2 FLOAT DEFAULT 50.0,

    -- Rasgos heredados (JSON)
    rasgos_especie_padre TEXT,  -- JSON: ['plumas', 'ojos_verticales']
    rasgos_especie_madre TEXT,  -- JSON: ['piel_humana', 'estatura_normal']

    -- Stats promedias
    longevidad_esperada INTEGER,  -- Promedio de ambas especies
    fertilidad_mixta BOOLEAN DEFAULT 1,  -- Algunos híbridos son estériles

    -- Identidad y aceptación
    identificacion_cultural VARCHAR(50),  -- 'padre', 'madre', 'hibrido', 'ninguna'
    aceptacion_sociedad_padre INTEGER DEFAULT 50,  -- 0-100
    aceptacion_sociedad_madre INTEGER DEFAULT 50,

    -- Habilidades únicas de híbrido
    habilidades_hibridas TEXT,  -- JSON: habilidades que solo tienen híbridos

    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE,
    FOREIGN KEY (especie_padre_id) REFERENCES especies(id),
    FOREIGN KEY (especie_madre_id) REFERENCES especies(id)
);

-- ================================================================
-- TABLA: Compatibilidad entre Especies
-- ================================================================
CREATE TABLE IF NOT EXISTS compatibilidad_especies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    especie_1_id INTEGER NOT NULL,
    especie_2_id INTEGER NOT NULL,

    -- Biología
    puede_reproducirse BOOLEAN DEFAULT 1,
    probabilidad_concepcion FLOAT DEFAULT 0.3,  -- 30% vs 70% misma especie
    probabilidad_esterilidad_hibrido FLOAT DEFAULT 0.2,  -- 20% de híbridos estériles

    -- Social
    aceptacion_social INTEGER DEFAULT 50,  -- 0-100
    taboo_cultural BOOLEAN DEFAULT 0,
    bendicion_divina_requerida BOOLEAN DEFAULT 0,

    -- Efectos en híbridos
    vigor_hibrido BOOLEAN DEFAULT 1,  -- Stats ligeramente superiores
    debilidad_hibrida BOOLEAN DEFAULT 0,  -- O inferiores

    -- Notas
    notas TEXT,

    FOREIGN KEY (especie_1_id) REFERENCES especies(id),
    FOREIGN KEY (especie_2_id) REFERENCES especies(id),
    UNIQUE(especie_1_id, especie_2_id)
);

-- ================================================================
-- TABLA: Comunidades Híbridas
-- ================================================================
CREATE TABLE IF NOT EXISTS comunidades_hibridas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(200) NOT NULL,
    especie_1_id INTEGER NOT NULL,
    especie_2_id INTEGER NOT NULL,

    -- Ubicación
    lugar_id INTEGER,
    fundacion_año INTEGER NOT NULL,

    -- Población
    poblacion_actual INTEGER DEFAULT 0,
    generacion_maxima INTEGER DEFAULT 1,  -- Hasta qué generación hay

    -- Cultura
    idioma_propio BOOLEAN DEFAULT 0,
    tradiciones TEXT,  -- JSON
    religion_sincretica BOOLEAN DEFAULT 1,  -- Mezcla ambas religiones

    -- Estatus
    reconocimiento_oficial BOOLEAN DEFAULT 0,
    lider_comunidad_id INTEGER,  -- persona_id

    FOREIGN KEY (especie_1_id) REFERENCES especies(id),
    FOREIGN KEY (especie_2_id) REFERENCES especies(id),
    FOREIGN KEY (lugar_id) REFERENCES pueblos_ciudades(id),
    FOREIGN KEY (lider_comunidad_id) REFERENCES personas(id)
);

-- ================================================================
-- TABLA: Eventos de Matrimonios Inter-Especies
-- ================================================================
CREATE TABLE IF NOT EXISTS matrimonios_interespecie_eventos (
    matrimonio_id INTEGER PRIMARY KEY,
    especie_1_id INTEGER NOT NULL,
    especie_2_id INTEGER NOT NULL,

    -- Circunstancias
    año_union INTEGER NOT NULL,
    tipo_ceremonia VARCHAR(50),  -- 'mixta', 'especie_1', 'especie_2', 'secular'

    -- Reacción social
    aprobacion_familia_1 INTEGER DEFAULT 50,  -- 0-100
    aprobacion_familia_2 INTEGER DEFAULT 50,
    escandalo_publico BOOLEAN DEFAULT 0,

    -- Bendición divina
    bendicion_divina BOOLEAN DEFAULT 0,
    dios_bendijo_id INTEGER,
    dios_maldijo_id INTEGER,

    -- Resultado
    exito_matrimonio BOOLEAN DEFAULT 1,
    años_juntos INTEGER,

    FOREIGN KEY (matrimonio_id) REFERENCES matrimonios(id) ON DELETE CASCADE,
    FOREIGN KEY (especie_1_id) REFERENCES especies(id),
    FOREIGN KEY (especie_2_id) REFERENCES especies(id),
    FOREIGN KEY (dios_bendijo_id) REFERENCES dioses(id),
    FOREIGN KEY (dios_maldijo_id) REFERENCES dioses(id)
);

-- ================================================================
-- ÍNDICES
-- ================================================================
CREATE INDEX IF NOT EXISTS idx_hibridos_especies ON personas_hibridas(especie_padre_id, especie_madre_id);
CREATE INDEX IF NOT EXISTS idx_hibridos_generacion ON personas_hibridas(generacion_hibrida);
CREATE INDEX IF NOT EXISTS idx_compatibilidad_especies ON compatibilidad_especies(especie_1_id, especie_2_id);
CREATE INDEX IF NOT EXISTS idx_comunidades_especies ON comunidades_hibridas(especie_1_id, especie_2_id);
CREATE INDEX IF NOT EXISTS idx_matrimonios_inter_año ON matrimonios_interespecie_eventos(año_union);

-- ================================================================
-- FIN DEL SCHEMA
-- ================================================================
