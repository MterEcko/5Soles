-- ================================================================
-- SCHEMAS COMBINADOS: Migraciones + Justicia + Clima + Economía
-- Portales del Quinto Sol - MMORPG
-- ================================================================

-- ================================================================
-- MIGRACIONES
-- ================================================================

CREATE TABLE IF NOT EXISTS migraciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    año_inicio INTEGER NOT NULL,
    año_fin INTEGER,

    -- Origen y destino
    lugar_origen_id INTEGER NOT NULL,
    lugar_destino_id INTEGER,  -- NULL si nomadas
    especie_id INTEGER,

    -- Causa
    causa VARCHAR(50),  -- 'guerra', 'desastre', 'recursos', 'persecucion', 'sobrepoblacion', 'exploracion'
    evento_causante_id INTEGER,  -- ID de guerra o desastre

    -- Escala
    num_migrantes INTEGER NOT NULL,
    tipo_migracion VARCHAR(20),  -- 'masiva', 'gradual', 'forzada', 'voluntaria'

    -- Resultado
    exito BOOLEAN,
    llegaron INTEGER,  -- Cuántos llegaron (pueden morir en camino)
    años_viaje INTEGER,

    -- Asentamiento
    fundaron_comunidad BOOLEAN DEFAULT 0,
    nueva_comunidad_id INTEGER,

    FOREIGN KEY (lugar_origen_id) REFERENCES pueblos_ciudades(id),
    FOREIGN KEY (lugar_destino_id) REFERENCES pueblos_ciudades(id),
    FOREIGN KEY (especie_id) REFERENCES especies(id)
);

CREATE TABLE IF NOT EXISTS refugiados (
    persona_id INTEGER PRIMARY KEY,
    migracion_id INTEGER NOT NULL,
    año_desplazamiento INTEGER NOT NULL,
    razon TEXT,
    asentado BOOLEAN DEFAULT 0,
    lugar_actual_id INTEGER,

    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE,
    FOREIGN KEY (migracion_id) REFERENCES migraciones(id),
    FOREIGN KEY (lugar_actual_id) REFERENCES pueblos_ciudades(id)
);

-- ================================================================
-- SISTEMA DE JUSTICIA
-- ================================================================

CREATE TABLE IF NOT EXISTS crimenes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    criminal_id INTEGER NOT NULL,
    año_crimen INTEGER NOT NULL,
    tipo_crimen VARCHAR(50),  -- 'asesinato', 'robo', 'traicion', 'herejia', 'desercion', 'contrabando'
    gravedad VARCHAR(20),  -- 'leve', 'grave', 'capital'

    -- Víctima
    victima_id INTEGER,
    daño_causado INTEGER,  -- monetario o físico

    -- Lugar
    lugar_id INTEGER,
    civilizacion_id INTEGER,

    -- Detección
    descubierto BOOLEAN DEFAULT 0,
    año_descubrimiento INTEGER,
    testigos TEXT,  -- JSON: [persona_id, ...]

    FOREIGN KEY (criminal_id) REFERENCES personas(id) ON DELETE CASCADE,
    FOREIGN KEY (victima_id) REFERENCES personas(id),
    FOREIGN KEY (lugar_id) REFERENCES pueblos_ciudades(id),
    FOREIGN KEY (civilizacion_id) REFERENCES civilizaciones(id)
);

CREATE TABLE IF NOT EXISTS juicios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    crimen_id INTEGER NOT NULL,
    acusado_id INTEGER NOT NULL,
    año_juicio INTEGER NOT NULL,

    -- Corte
    juez_id INTEGER,
    lugar_juicio_id INTEGER,
    tipo_juicio VARCHAR(50),  -- 'civil', 'militar', 'religioso', 'tribal'

    -- Veredicto
    veredicto VARCHAR(20),  -- 'culpable', 'inocente', 'absuelto'
    evidencias TEXT,  -- JSON

    -- Castigo
    castigo VARCHAR(100),
    años_prision INTEGER,
    multa INTEGER,
    exilio BOOLEAN DEFAULT 0,
    ejecucion BOOLEAN DEFAULT 0,
    año_ejecucion INTEGER,

    -- Consecuencias
    cumplido BOOLEAN DEFAULT 0,

    FOREIGN KEY (crimen_id) REFERENCES crimenes(id) ON DELETE CASCADE,
    FOREIGN KEY (acusado_id) REFERENCES personas(id),
    FOREIGN KEY (juez_id) REFERENCES personas(id),
    FOREIGN KEY (lugar_juicio_id) REFERENCES pueblos_ciudades(id)
);

CREATE TABLE IF NOT EXISTS prisioneros (
    persona_id INTEGER PRIMARY KEY,
    juicio_id INTEGER NOT NULL,
    año_encarcelamiento INTEGER NOT NULL,
    año_liberacion INTEGER,
    lugar_prision_id INTEGER,

    -- Estado
    vivo BOOLEAN DEFAULT 1,
    escapo BOOLEAN DEFAULT 0,
    año_escape INTEGER,

    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE,
    FOREIGN KEY (juicio_id) REFERENCES juicios(id),
    FOREIGN KEY (lugar_prision_id) REFERENCES pueblos_ciudades(id)
);

-- ================================================================
-- CLIMA Y ESTACIONES
-- ================================================================

CREATE TABLE IF NOT EXISTS ciclos_climaticos (
    año INTEGER PRIMARY KEY,
    estacion_dominante VARCHAR(20),  -- 'primavera', 'verano', 'otoño', 'invierno', 'lluvias', 'secas'

    -- Condiciones globales
    temperatura_promedio INTEGER,  -- °C
    precipitacion VARCHAR(20),  -- 'muy_baja', 'baja', 'normal', 'alta', 'muy_alta'

    -- Eventos climáticos
    sequia BOOLEAN DEFAULT 0,
    inundaciones BOOLEAN DEFAULT 0,
    tormenta_severa BOOLEAN DEFAULT 0,
    huracan BOOLEAN DEFAULT 0,

    -- Impacto en agricultura (NO afecta directamente, solo bonus/penalty)
    bonus_agricultura INTEGER DEFAULT 0,  -- -50 a +50
    bonus_caza INTEGER DEFAULT 0,

    -- Impacto en guerras
    guerras_canceladas INTEGER DEFAULT 0,  -- Guerras que no pueden ocurrir por clima
    batallas_afectadas INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS eventos_climaticos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    año INTEGER NOT NULL,
    tipo VARCHAR(50),  -- 'sequia', 'huracan', 'nevada', 'granizo', 'eclipse', 'cometa'
    gravedad VARCHAR(20),  -- 'leve', 'moderado', 'severo', 'catastrofico'

    -- Área afectada
    lugares_afectados TEXT,  -- JSON: [lugar_id, ...]
    civilizaciones_afectadas TEXT,  -- JSON

    -- Impacto
    muertos INTEGER DEFAULT 0,
    cosechas_perdidas INTEGER DEFAULT 0,  -- %
    edificios_dañados INTEGER DEFAULT 0,

    -- Duración
    duracion_dias INTEGER DEFAULT 1,

    -- Divino
    causado_por_dios_id INTEGER,

    FOREIGN KEY (causado_por_dios_id) REFERENCES dioses(id)
);

-- ================================================================
-- ECONOMÍA DUAL (Dinero Normal + Criptomonedas)
-- ================================================================

CREATE TABLE IF NOT EXISTS monedas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL,
    simbolo VARCHAR(10),
    tipo VARCHAR(20),  -- 'fisica', 'cripto', 'divina'

    -- Uso
    usada_por VARCHAR(20),  -- 'npcs', 'jugadores', 'comercio', 'especial'
    civilizacion_emisora_id INTEGER,

    -- Valor
    valor_relativo FLOAT DEFAULT 1.0,  -- Relativo al oro estándar
    inflacion_anual FLOAT DEFAULT 0.0,

    -- Criptomoneda (solo si tipo = 'cripto')
    es_cripto BOOLEAN DEFAULT 0,
    wallet_jugador VARCHAR(200),  -- Dirección blockchain

    FOREIGN KEY (civilizacion_emisora_id) REFERENCES civilizaciones(id)
);

CREATE TABLE IF NOT EXISTS wallets (
    persona_id INTEGER PRIMARY KEY,
    moneda_id INTEGER NOT NULL,

    -- Saldo
    saldo FLOAT DEFAULT 0.0,

    -- Transacciones
    total_ganado FLOAT DEFAULT 0.0,
    total_gastado FLOAT DEFAULT 0.0,

    -- Cripto (si aplica)
    direccion_wallet VARCHAR(200),

    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE,
    FOREIGN KEY (moneda_id) REFERENCES monedas(id)
);

CREATE TABLE IF NOT EXISTS transacciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    año INTEGER NOT NULL,
    moneda_id INTEGER NOT NULL,

    -- Partes
    pagador_id INTEGER NOT NULL,
    receptor_id INTEGER NOT NULL,

    -- Monto
    cantidad FLOAT NOT NULL,
    tipo VARCHAR(50),  -- 'compra', 'venta', 'salario', 'impuesto', 'don', 'robo', 'recompensa'

    -- Contexto
    concepto TEXT,
    lugar_id INTEGER,

    FOREIGN KEY (moneda_id) REFERENCES monedas(id),
    FOREIGN KEY (pagador_id) REFERENCES personas(id),
    FOREIGN KEY (receptor_id) REFERENCES personas(id),
    FOREIGN KEY (lugar_id) REFERENCES pueblos_ciudades(id)
);

CREATE TABLE IF NOT EXISTS mercado_precios (
    año INTEGER NOT NULL,
    item_tipo VARCHAR(50) NOT NULL,  -- 'comida', 'arma', 'armadura', 'flora', 'fauna', 'artefacto'
    item_id INTEGER,  -- ID del item específico (opcional)

    precio_base FLOAT NOT NULL,
    moneda_id INTEGER NOT NULL,

    -- Variación
    oferta INTEGER DEFAULT 100,  -- %
    demanda INTEGER DEFAULT 100,  -- %
    precio_ajustado FLOAT,

    PRIMARY KEY (año, item_tipo, item_id),
    FOREIGN KEY (moneda_id) REFERENCES monedas(id)
);

-- ================================================================
-- ÍNDICES
-- ================================================================
CREATE INDEX IF NOT EXISTS idx_migraciones_año ON migraciones(año_inicio);
CREATE INDEX IF NOT EXISTS idx_migraciones_causa ON migraciones(causa);
CREATE INDEX IF NOT EXISTS idx_refugiados_persona ON refugiados(persona_id);
CREATE INDEX IF NOT EXISTS idx_crimenes_año ON crimenes(año_crimen);
CREATE INDEX IF NOT EXISTS idx_crimenes_tipo ON crimenes(tipo_crimen);
CREATE INDEX IF NOT EXISTS idx_juicios_año ON juicios(año_juicio);
CREATE INDEX IF NOT EXISTS idx_prisioneros_persona ON prisioneros(persona_id);
CREATE INDEX IF NOT EXISTS idx_clima_año ON ciclos_climaticos(año);
CREATE INDEX IF NOT EXISTS idx_eventos_clima_año ON eventos_climaticos(año);
CREATE INDEX IF NOT EXISTS idx_wallets_persona ON wallets(persona_id);
CREATE INDEX IF NOT EXISTS idx_transacciones_año ON transacciones(año);
CREATE INDEX IF NOT EXISTS idx_mercado_año ON mercado_precios(año);

-- ================================================================
-- FIN DEL SCHEMA
-- ================================================================
