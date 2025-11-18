-- ========================================
-- EXTENSIÓN: Sistema de Personalidades, Necesidades y IA Conversacional
-- ========================================

-- TABLA: RASGOS DE PERSONALIDAD
CREATE TABLE IF NOT EXISTS rasgos_personalidad (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    categoria VARCHAR(50), -- 'temperamento', 'etica', 'social', 'mental'
    descripcion TEXT,
    opuesto_id INTEGER, -- Rasgo opuesto (ej: generoso <-> avaro)
    FOREIGN KEY (opuesto_id) REFERENCES rasgos_personalidad(id)
);

-- TABLA: PERSONALIDAD DE PERSONA
CREATE TABLE IF NOT EXISTS persona_personalidad (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    persona_id INTEGER NOT NULL,
    rasgo_id INTEGER NOT NULL,
    intensidad INTEGER DEFAULT 5, -- 1-10 (qué tan fuerte es el rasgo)
    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE,
    FOREIGN KEY (rasgo_id) REFERENCES rasgos_personalidad(id),
    UNIQUE(persona_id, rasgo_id)
);

-- TABLA: NECESIDADES (hambre, sed, recursos, etc.)
CREATE TABLE IF NOT EXISTS necesidades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    tipo VARCHAR(50), -- 'basica', 'profesional', 'social'
    descripcion TEXT,
    prioridad INTEGER DEFAULT 5 -- 1-10
);

-- TABLA: NECESIDADES DE PERSONA (estado actual)
CREATE TABLE IF NOT EXISTS persona_necesidades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    persona_id INTEGER NOT NULL,
    necesidad_id INTEGER NOT NULL,
    nivel_actual INTEGER DEFAULT 100, -- 0-100 (100 = satisfecho)
    nivel_minimo INTEGER DEFAULT 20, -- Umbral crítico
    ultima_actualizacion INTEGER, -- Año
    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE,
    FOREIGN KEY (necesidad_id) REFERENCES necesidades(id),
    UNIQUE(persona_id, necesidad_id)
);

-- TABLA: RECURSOS/ITEMS DEL JUEGO
CREATE TABLE IF NOT EXISTS items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    tipo VARCHAR(50), -- 'comida', 'herramienta', 'arma', 'armadura', 'material', etc.
    subtipo VARCHAR(50), -- 'carne', 'pan', 'espada', 'hierro', etc.
    valor_base INTEGER DEFAULT 1, -- Valor en sistema de trueque
    peso REAL DEFAULT 1.0,
    es_perecedero BOOLEAN DEFAULT 0,
    duracion_años INTEGER, -- Para items perecederos
    descripcion TEXT,
    metadata TEXT -- JSON con propiedades adicionales
);

-- TABLA: INVENTARIO DE PERSONA
CREATE TABLE IF NOT EXISTS persona_inventario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    persona_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    cantidad INTEGER DEFAULT 1,
    calidad INTEGER DEFAULT 5, -- 1-10 (afecta valor)
    año_adquisicion INTEGER,
    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES items(id)
);

-- TABLA: TRANSACCIONES/TRUEQUES
CREATE TABLE IF NOT EXISTS transacciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    año INTEGER NOT NULL,
    persona_vendedor_id INTEGER NOT NULL,
    persona_comprador_id INTEGER NOT NULL,
    tipo_transaccion VARCHAR(50), -- 'trueque', 'compra', 'regalo', 'robo'

    -- Items intercambiados
    item_ofrecido_id INTEGER,
    cantidad_ofrecida INTEGER,
    item_recibido_id INTEGER,
    cantidad_recibida INTEGER,

    -- Contexto
    lugar_id INTEGER,
    precio_acordado INTEGER, -- En valor base
    satisfaccion_vendedor INTEGER, -- 1-10
    satisfaccion_comprador INTEGER, -- 1-10
    notas TEXT,

    FOREIGN KEY (persona_vendedor_id) REFERENCES personas(id),
    FOREIGN KEY (persona_comprador_id) REFERENCES personas(id),
    FOREIGN KEY (item_ofrecido_id) REFERENCES items(id),
    FOREIGN KEY (item_recibido_id) REFERENCES items(id),
    FOREIGN KEY (lugar_id) REFERENCES pueblos_ciudades(id)
);

-- TABLA: PATERNIDAD MÚLTIPLE/INCIERTA
CREATE TABLE IF NOT EXISTS paternidad_posible (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hijo_id INTEGER NOT NULL,
    madre_id INTEGER NOT NULL,
    padre_posible_id INTEGER NOT NULL,
    probabilidad INTEGER, -- 0-100 (% de probabilidad)
    año_concepcion INTEGER,
    confirmado BOOLEAN DEFAULT 0, -- Si se confirmó o no
    metodo_confirmacion VARCHAR(100), -- 'adn_divino', 'confesion', 'rasgos_fisicos', etc.
    FOREIGN KEY (hijo_id) REFERENCES personas(id),
    FOREIGN KEY (madre_id) REFERENCES personas(id),
    FOREIGN KEY (padre_posible_id) REFERENCES personas(id)
);

-- TABLA: RELACIONES ENTRE PERSONAS
CREATE TABLE IF NOT EXISTS relaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    persona1_id INTEGER NOT NULL,
    persona2_id INTEGER NOT NULL,
    tipo_relacion VARCHAR(50), -- 'amigo', 'enemigo', 'rival', 'mentor', 'aprendiz', 'cliente', 'amante'
    intensidad INTEGER DEFAULT 5, -- 1-10
    año_inicio INTEGER,
    año_fin INTEGER,
    es_reciproca BOOLEAN DEFAULT 1,
    notas TEXT,
    FOREIGN KEY (persona1_id) REFERENCES personas(id),
    FOREIGN KEY (persona2_id) REFERENCES personas(id),
    CONSTRAINT check_personas_diferentes CHECK (persona1_id != persona2_id)
);

-- TABLA: MEMORIA DE NPC (para IA conversacional)
CREATE TABLE IF NOT EXISTS memoria_npc (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    npc_id INTEGER NOT NULL,
    jugador_id INTEGER, -- NULL si es memoria general
    tipo_memoria VARCHAR(50), -- 'interaccion', 'transaccion', 'evento', 'herencia'
    año INTEGER NOT NULL,

    -- Contenido de la memoria
    titulo VARCHAR(200),
    descripcion TEXT NOT NULL,
    importancia INTEGER DEFAULT 5, -- 1-10 (afecta si se recuerda o no)
    emocion VARCHAR(50), -- 'alegria', 'tristeza', 'ira', 'miedo', 'neutral'

    -- Referencias
    persona_relacionada_id INTEGER,
    item_relacionado_id INTEGER,
    lugar_relacionado_id INTEGER,
    transaccion_relacionada_id INTEGER,

    -- Metadata para IA
    metadata TEXT, -- JSON con contexto adicional

    FOREIGN KEY (npc_id) REFERENCES personas(id) ON DELETE CASCADE,
    FOREIGN KEY (jugador_id) REFERENCES personas(id),
    FOREIGN KEY (persona_relacionada_id) REFERENCES personas(id),
    FOREIGN KEY (item_relacionado_id) REFERENCES items(id),
    FOREIGN KEY (lugar_relacionado_id) REFERENCES pueblos_ciudades(id),
    FOREIGN KEY (transaccion_relacionada_id) REFERENCES transacciones(id)
);

-- TABLA: DIÁLOGOS GENERADOS (historial de conversaciones)
CREATE TABLE IF NOT EXISTS dialogos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    año INTEGER NOT NULL,
    npc_id INTEGER NOT NULL,
    jugador_id INTEGER,

    -- Contexto
    tipo_dialogo VARCHAR(50), -- 'saludo', 'comercio', 'mision', 'casual', 'despedida'
    lugar_id INTEGER,

    -- Contenido
    linea_npc TEXT NOT NULL,
    linea_jugador TEXT,
    tono VARCHAR(50), -- 'amigable', 'hostil', 'neutral', 'triste', 'alegre'

    -- Metadata para IA
    contexto_previo TEXT, -- JSON con info relevante
    memoria_activada_ids TEXT, -- IDs de memorias que se usaron

    FOREIGN KEY (npc_id) REFERENCES personas(id),
    FOREIGN KEY (jugador_id) REFERENCES personas(id),
    FOREIGN KEY (lugar_id) REFERENCES pueblos_ciudades(id)
);

-- TABLA: SUCESIÓN DE OFICIOS
CREATE TABLE IF NOT EXISTS sucesion_oficios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    oficio_id INTEGER NOT NULL,
    persona_anterior_id INTEGER NOT NULL,
    persona_sucesor_id INTEGER NOT NULL,
    año_sucesion INTEGER NOT NULL,
    tipo_sucesion VARCHAR(50), -- 'herencia', 'aprendizaje', 'compra', 'conquista'
    nivel_maestria_heredado INTEGER, -- Cuánto conocimiento se transfirió
    lugar_id INTEGER,
    notas TEXT,
    FOREIGN KEY (oficio_id) REFERENCES oficios(id),
    FOREIGN KEY (persona_anterior_id) REFERENCES personas(id),
    FOREIGN KEY (persona_sucesor_id) REFERENCES personas(id),
    FOREIGN KEY (lugar_id) REFERENCES pueblos_ciudades(id)
);

-- TABLA: APRENDICES
CREATE TABLE IF NOT EXISTS aprendices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    maestro_id INTEGER NOT NULL,
    aprendiz_id INTEGER NOT NULL,
    oficio_id INTEGER NOT NULL,
    año_inicio INTEGER NOT NULL,
    año_finalizacion INTEGER,
    nivel_progreso INTEGER DEFAULT 0, -- 0-100
    es_exitoso BOOLEAN, -- Si completó el aprendizaje
    lugar_id INTEGER,
    FOREIGN KEY (maestro_id) REFERENCES personas(id),
    FOREIGN KEY (aprendiz_id) REFERENCES personas(id),
    FOREIGN KEY (oficio_id) REFERENCES oficios(id),
    FOREIGN KEY (lugar_id) REFERENCES pueblos_ciudades(id)
);

-- ÍNDICES
CREATE INDEX IF NOT EXISTS idx_memoria_npc ON memoria_npc(npc_id);
CREATE INDEX IF NOT EXISTS idx_memoria_jugador ON memoria_npc(jugador_id);
CREATE INDEX IF NOT EXISTS idx_memoria_año ON memoria_npc(año);
CREATE INDEX IF NOT EXISTS idx_memoria_importancia ON memoria_npc(importancia);
CREATE INDEX IF NOT EXISTS idx_transacciones_vendedor ON transacciones(persona_vendedor_id);
CREATE INDEX IF NOT EXISTS idx_transacciones_comprador ON transacciones(persona_comprador_id);
CREATE INDEX IF NOT EXISTS idx_transacciones_año ON transacciones(año);
CREATE INDEX IF NOT EXISTS idx_dialogos_npc ON dialogos(npc_id);
CREATE INDEX IF NOT EXISTS idx_dialogos_jugador ON dialogos(jugador_id);
CREATE INDEX IF NOT EXISTS idx_paternidad_hijo ON paternidad_posible(hijo_id);
CREATE INDEX IF NOT EXISTS idx_relaciones_persona1 ON relaciones(persona1_id);
CREATE INDEX IF NOT EXISTS idx_relaciones_persona2 ON relaciones(persona2_id);

-- VISTAS ÚTILES

-- Vista: NPCs con su personalidad completa
CREATE VIEW IF NOT EXISTS npc_personalidades AS
SELECT
    p.id,
    p.nombre_completo,
    GROUP_CONCAT(rp.nombre || ':' || pp.intensidad) as rasgos,
    p.clase_social,
    p.civilizacion_id
FROM personas p
LEFT JOIN persona_personalidad pp ON p.id = pp.persona_id
LEFT JOIN rasgos_personalidad rp ON pp.rasgo_id = rp.id
GROUP BY p.id, p.nombre_completo, p.clase_social, p.civilizacion_id;

-- Vista: Historial de transacciones de una persona
CREATE VIEW IF NOT EXISTS historial_comercial AS
SELECT
    t.id,
    t.año,
    v.nombre_completo as vendedor,
    c.nombre_completo as comprador,
    io.nombre as item_ofrecido,
    t.cantidad_ofrecida,
    ir.nombre as item_recibido,
    t.cantidad_recibida,
    t.tipo_transaccion,
    t.satisfaccion_vendedor,
    t.satisfaccion_comprador
FROM transacciones t
JOIN personas v ON t.persona_vendedor_id = v.id
JOIN personas c ON t.persona_comprador_id = c.id
LEFT JOIN items io ON t.item_ofrecido_id = io.id
LEFT JOIN items ir ON t.item_recibido_id = ir.id;

-- Vista: Líneas de sucesión de oficios
CREATE VIEW IF NOT EXISTS lineas_sucesion AS
SELECT
    o.nombre as oficio,
    pa.nombre_completo as antecesor,
    ps.nombre_completo as sucesor,
    so.año_sucesion,
    so.tipo_sucesion,
    so.nivel_maestria_heredado
FROM sucesion_oficios so
JOIN oficios o ON so.oficio_id = o.id
JOIN personas pa ON so.persona_anterior_id = pa.id
JOIN personas ps ON so.persona_sucesor_id = ps.id
ORDER BY o.nombre, so.año_sucesion;
