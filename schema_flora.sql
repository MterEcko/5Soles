-- ================================================================
-- SCHEMA: SISTEMA DE FLORA (1000+ ESPECIES DE PLANTAS)
-- Portales del Quinto Sol - MMORPG
-- ================================================================

-- ================================================================
-- TABLA: Especies de Flora
-- ================================================================
CREATE TABLE IF NOT EXISTS especies_flora (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre_comun VARCHAR(150) NOT NULL,
    nombre_nahuatl VARCHAR(150),
    nombre_cientifico VARCHAR(200),  -- Nombre latino opcional

    -- Clasificación botánica
    tipo_planta VARCHAR(50),  -- 'arbol', 'arbusto', 'hierba', 'enredadera', 'hongo', 'cactus', 'helecho', 'palmera', 'flor'
    familia VARCHAR(100),

    -- Clasificación por uso (puede tener múltiples usos)
    es_alimento BOOLEAN DEFAULT 0,
    es_veneno BOOLEAN DEFAULT 0,
    es_curativo BOOLEAN DEFAULT 0,
    es_alucinogeno BOOLEAN DEFAULT 0,
    es_adorno BOOLEAN DEFAULT 0,
    es_recurso BOOLEAN DEFAULT 0,

    -- Propiedades detalladas (JSON)
    propiedades_alimento TEXT,     -- JSON: {"parte_comestible": "fruto", "valor_nutricional": 80, "sabor": "dulce"}
    propiedades_veneno TEXT,       -- JSON: {"toxicidad": "alta", "sintomas": ["paralisis", "muerte"], "antidoto": "planta_X"}
    propiedades_curativo TEXT,     -- JSON: {"enfermedades_cura": ["fiebre", "heridas"], "efectividad": 85}
    propiedades_alucinogeno TEXT,  -- JSON: {"potencia": "alta", "duracion_horas": 6, "efectos": ["visiones", "euforia"]}
    propiedades_adorno TEXT,       -- JSON: {"color_flor": "rojo", "epoca_floracion": "primavera", "aroma": "intenso"}
    propiedades_recurso TEXT,      -- JSON: {"tipo_recurso": "madera", "dureza": 80, "usos": ["construccion", "muebles"]}

    -- Características físicas
    altura_min_cm INTEGER,
    altura_max_cm INTEGER,
    color_principal VARCHAR(50),
    descripcion TEXT,

    -- Ubicación y rareza
    biomas_preferidos TEXT,  -- JSON: ['bosque', 'selva', 'montaña']
    rareza FLOAT DEFAULT 1.0,  -- 0.01 (muy raro) - 1.0 (muy común)
    epoca_disponible TEXT,  -- JSON: ['primavera', 'verano'] o null si todo el año

    -- Economía
    valor_mercado INTEGER DEFAULT 0,
    es_vendible BOOLEAN DEFAULT 1,
    es_cultivable BOOLEAN DEFAULT 0,
    tiempo_crecimiento_dias INTEGER,  -- Días para madurar si cultivable

    -- Peligrosidad
    nivel_peligro VARCHAR(20) DEFAULT 'ninguno',  -- 'ninguno', 'bajo', 'medio', 'alto', 'extremo'

    -- Requerimientos
    nivel_min_recoleccion INTEGER DEFAULT 1,
    herramienta_requerida VARCHAR(50)  -- null, 'hacha', 'machete', 'pico', etc.
);

-- ================================================================
-- TABLA: Flora por zona (Sistema de Spawn)
-- ================================================================
CREATE TABLE IF NOT EXISTS flora_zonas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    zona_id INTEGER NOT NULL,
    especie_flora_id INTEGER NOT NULL,
    densidad_base INTEGER DEFAULT 10,  -- Cantidad base por zona
    densidad_actual INTEGER DEFAULT 10,  -- Cantidad actual (varía con recolección)

    -- Spawn
    probabilidad_spawn FLOAT DEFAULT 1.0,  -- 0.0-1.0
    ultimo_respawn INTEGER,  -- Año del último respawn
    dias_respawn INTEGER DEFAULT 30,  -- Cada cuántos días regenera

    -- Ubicación específica
    tipo_terreno VARCHAR(50),  -- 'llano', 'ladera', 'cerca_agua', 'rocoso'

    FOREIGN KEY (zona_id) REFERENCES pueblos_ciudades(id) ON DELETE CASCADE,
    FOREIGN KEY (especie_flora_id) REFERENCES especies_flora(id) ON DELETE CASCADE,
    UNIQUE(zona_id, especie_flora_id)
);

-- ================================================================
-- TABLA: Plantas individuales (SOLO plantas especiales/únicas)
-- ================================================================
CREATE TABLE IF NOT EXISTS plantas_individuales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    especie_id INTEGER NOT NULL,
    nombre VARCHAR(150),  -- Solo si es planta legendaria/nombrada
    zona_actual_id INTEGER,
    año_plantado INTEGER,
    año_muerte INTEGER,

    -- Estado
    edad_años INTEGER DEFAULT 0,
    salud_actual INTEGER DEFAULT 100,
    salud_maxima INTEGER DEFAULT 100,

    -- Clasificación especial
    es_sagrado BOOLEAN DEFAULT 0,
    es_legendario BOOLEAN DEFAULT 0,
    es_cultivado BOOLEAN DEFAULT 0,
    propietario_id INTEGER,  -- ID de persona que la plantó/cuida

    -- Características especiales (para plantas únicas)
    poderes_especiales TEXT,  -- JSON
    bendiciones TEXT,  -- JSON: bendiciones divinas

    -- Mercado
    valor_estimado INTEGER DEFAULT 0,

    FOREIGN KEY (especie_id) REFERENCES especies_flora(id),
    FOREIGN KEY (zona_actual_id) REFERENCES pueblos_ciudades(id),
    FOREIGN KEY (propietario_id) REFERENCES personas(id) ON DELETE SET NULL
);

-- ================================================================
-- TABLA: Recetas y combinaciones de plantas
-- ================================================================
CREATE TABLE IF NOT EXISTS recetas_herbolaria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(150) NOT NULL,
    tipo VARCHAR(50),  -- 'pocion', 'ungüento', 'te', 'polvo', 'incienso'
    descripcion TEXT,

    -- Ingredientes (JSON)
    ingredientes TEXT NOT NULL,  -- JSON: [{"flora_id": 1, "cantidad": 2}, {"flora_id": 5, "cantidad": 1}]

    -- Efectos
    efectos TEXT,  -- JSON: [{"tipo": "curacion", "potencia": 50}, {"tipo": "veneno", "potencia": 30}]
    duracion_efecto_horas INTEGER,

    -- Creación
    dificultad INTEGER DEFAULT 1,  -- 1-100
    tiempo_preparacion_minutos INTEGER,
    herramientas_necesarias TEXT,  -- JSON: ['mortero', 'caldero']

    -- Economía
    valor_venta INTEGER DEFAULT 0,

    -- Descubrimiento
    descubierta_por_id INTEGER,
    año_descubrimiento INTEGER,
    es_secreta BOOLEAN DEFAULT 0,

    FOREIGN KEY (descubierta_por_id) REFERENCES personas(id)
);

-- ================================================================
-- TABLA: Cultivos (agricultura)
-- ================================================================
CREATE TABLE IF NOT EXISTS cultivos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    especie_flora_id INTEGER NOT NULL,
    granjero_id INTEGER NOT NULL,
    zona_id INTEGER NOT NULL,

    -- Ciclo de cultivo
    año_plantado INTEGER NOT NULL,
    año_cosecha_esperada INTEGER,
    año_cosechado INTEGER,

    -- Producción
    cantidad_plantada INTEGER DEFAULT 1,
    cantidad_cosechada INTEGER,
    calidad VARCHAR(20),  -- 'mala', 'regular', 'buena', 'excelente'

    -- Condiciones
    clima_durante_cultivo TEXT,  -- JSON
    plagas BOOLEAN DEFAULT 0,
    bendicion_divina BOOLEAN DEFAULT 0,

    FOREIGN KEY (especie_flora_id) REFERENCES especies_flora(id),
    FOREIGN KEY (granjero_id) REFERENCES personas(id) ON DELETE CASCADE,
    FOREIGN KEY (zona_id) REFERENCES pueblos_ciudades(id)
);

-- ================================================================
-- TABLA: Inventario de flora (lo que NPCs/jugadores tienen)
-- ================================================================
CREATE TABLE IF NOT EXISTS inventario_flora (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    persona_id INTEGER NOT NULL,
    especie_flora_id INTEGER NOT NULL,
    cantidad INTEGER DEFAULT 1,
    calidad VARCHAR(20) DEFAULT 'regular',  -- 'mala', 'regular', 'buena', 'excelente'

    -- Origen
    recolectado_en_zona_id INTEGER,
    año_recoleccion INTEGER,

    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE,
    FOREIGN KEY (especie_flora_id) REFERENCES especies_flora(id),
    FOREIGN KEY (recolectado_en_zona_id) REFERENCES pueblos_ciudades(id)
);

-- ================================================================
-- TABLA: Comercio de flora
-- ================================================================
CREATE TABLE IF NOT EXISTS mercado_flora (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    especie_flora_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL,
    vendedor_id INTEGER,
    comprador_id INTEGER,
    zona_id INTEGER NOT NULL,
    año_venta INTEGER NOT NULL,
    precio_unitario INTEGER NOT NULL,
    calidad VARCHAR(20),

    FOREIGN KEY (especie_flora_id) REFERENCES especies_flora(id),
    FOREIGN KEY (vendedor_id) REFERENCES personas(id),
    FOREIGN KEY (comprador_id) REFERENCES personas(id),
    FOREIGN KEY (zona_id) REFERENCES pueblos_ciudades(id)
);

-- ================================================================
-- ÍNDICES para optimización
-- ================================================================
CREATE INDEX IF NOT EXISTS idx_flora_tipo ON especies_flora(tipo_planta);
CREATE INDEX IF NOT EXISTS idx_flora_alimento ON especies_flora(es_alimento);
CREATE INDEX IF NOT EXISTS idx_flora_veneno ON especies_flora(es_veneno);
CREATE INDEX IF NOT EXISTS idx_flora_curativo ON especies_flora(es_curativo);
CREATE INDEX IF NOT EXISTS idx_flora_alucinogeno ON especies_flora(es_alucinogeno);
CREATE INDEX IF NOT EXISTS idx_flora_adorno ON especies_flora(es_adorno);
CREATE INDEX IF NOT EXISTS idx_flora_recurso ON especies_flora(es_recurso);
CREATE INDEX IF NOT EXISTS idx_flora_rareza ON especies_flora(rareza);
CREATE INDEX IF NOT EXISTS idx_flora_zonas_zona ON flora_zonas(zona_id);
CREATE INDEX IF NOT EXISTS idx_flora_zonas_especie ON flora_zonas(especie_flora_id);
CREATE INDEX IF NOT EXISTS idx_plantas_ind_especie ON plantas_individuales(especie_id);
CREATE INDEX IF NOT EXISTS idx_plantas_ind_zona ON plantas_individuales(zona_actual_id);
CREATE INDEX IF NOT EXISTS idx_plantas_ind_sagrado ON plantas_individuales(es_sagrado);
CREATE INDEX IF NOT EXISTS idx_cultivos_granjero ON cultivos(granjero_id);
CREATE INDEX IF NOT EXISTS idx_cultivos_zona ON cultivos(zona_id);
CREATE INDEX IF NOT EXISTS idx_inventario_persona ON inventario_flora(persona_id);
CREATE INDEX IF NOT EXISTS idx_mercado_flora_año ON mercado_flora(año_venta);

-- ================================================================
-- FIN DEL SCHEMA
-- ================================================================
