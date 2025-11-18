-- ========================================
-- PORTALES DEL QUINTO SOL - SISTEMAS COMPLETOS
-- Todos los sistemas adicionales integrados
-- ========================================

-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
-- 1. SISTEMA DE COMBATE Y BATALLAS
-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

-- TABLA: BATALLAS
CREATE TABLE IF NOT EXISTS batallas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(200),
    tipo VARCHAR(50), -- 'duelo', 'escaramuza', 'batalla', 'guerra', 'emboscada'
    año INTEGER NOT NULL,
    lugar_id INTEGER,

    -- Bandos (puede ser persona o facción)
    atacante_persona_id INTEGER,
    atacante_faccion_id INTEGER,
    defensor_persona_id INTEGER,
    defensor_faccion_id INTEGER,

    -- Resultado
    ganador VARCHAR(50), -- 'atacante', 'defensor', 'empate'
    bajas_atacante INTEGER DEFAULT 0,
    bajas_defensor INTEGER DEFAULT 0,

    -- Contexto
    causa TEXT,
    consecuencias TEXT,
    botin_obtenido TEXT, -- JSON con items

    FOREIGN KEY (lugar_id) REFERENCES pueblos_ciudades(id),
    FOREIGN KEY (atacante_persona_id) REFERENCES personas(id),
    FOREIGN KEY (defensor_persona_id) REFERENCES personas(id)
);

-- TABLA: PARTICIPANTES EN BATALLAS
CREATE TABLE IF NOT EXISTS batalla_participantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    batalla_id INTEGER NOT NULL,
    persona_id INTEGER NOT NULL,
    bando VARCHAR(50), -- 'atacante', 'defensor'
    rol VARCHAR(50), -- 'soldado', 'capitan', 'comandante', 'heroe'
    resultado VARCHAR(50), -- 'sobrevivio', 'herido', 'muerto', 'capturado'
    enemigos_eliminados INTEGER DEFAULT 0,
    FOREIGN KEY (batalla_id) REFERENCES batallas(id),
    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE
);

-- TABLA: HERIDAS
CREATE TABLE IF NOT EXISTS heridas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    persona_id INTEGER NOT NULL,
    tipo VARCHAR(50), -- 'leve', 'moderado', 'grave', 'permanente', 'mortal'
    parte_cuerpo VARCHAR(50), -- 'cabeza', 'brazo_izq', 'brazo_der', 'pierna', 'torso'
    causa VARCHAR(100), -- 'espada', 'flecha', 'caida', 'quemadura', 'bestia'
    año_ocurrencia INTEGER NOT NULL,

    -- Recuperación
    dias_recuperacion INTEGER,
    curado_por_id INTEGER, -- Curandero/Alquimista que lo curó

    -- Secuelas
    es_permanente BOOLEAN DEFAULT 0,
    cicatriz_visible BOOLEAN DEFAULT 0,
    penalizacion TEXT, -- JSON: {'combate': -10, 'carisma': -5}

    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE,
    FOREIGN KEY (curado_por_id) REFERENCES personas(id)
);

-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
-- 2. SISTEMA DE REPUTACIÓN Y FACCIONES
-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

-- TABLA: FACCIONES (además de civilizaciones)
CREATE TABLE IF NOT EXISTS facciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    tipo VARCHAR(50), -- 'politica', 'religiosa', 'militar', 'comercial', 'criminal'
    ideologia TEXT,
    lider_id INTEGER,
    civilizacion_base_id INTEGER,
    año_fundacion INTEGER,
    año_disolucion INTEGER,
    sede_id INTEGER, -- Lugar principal

    FOREIGN KEY (lider_id) REFERENCES personas(id),
    FOREIGN KEY (civilizacion_base_id) REFERENCES civilizaciones(id),
    FOREIGN KEY (sede_id) REFERENCES pueblos_ciudades(id)
);

-- TABLA: RELACIONES ENTRE FACCIONES
CREATE TABLE IF NOT EXISTS faccion_relaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    faccion1_id INTEGER NOT NULL,
    faccion2_id INTEGER NOT NULL,
    relacion INTEGER DEFAULT 0, -- -100 (enemigos) a +100 (aliados)
    tipo VARCHAR(50), -- 'alianza', 'guerra', 'tregua', 'comercio', 'neutral'
    año_inicio INTEGER,
    año_fin INTEGER,

    FOREIGN KEY (faccion1_id) REFERENCES facciones(id),
    FOREIGN KEY (faccion2_id) REFERENCES facciones(id),
    CONSTRAINT check_facciones_diferentes CHECK (faccion1_id != faccion2_id)
);

-- TABLA: REPUTACIÓN DE PERSONA
CREATE TABLE IF NOT EXISTS persona_reputacion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    persona_id INTEGER NOT NULL,
    faccion_id INTEGER,
    civilizacion_id INTEGER,

    -- Reputación (-100 a +100)
    nivel_reputacion INTEGER DEFAULT 0,

    -- Títulos ganados
    titulos TEXT, -- JSON: ["Héroe de los Mayas", "Matador de Dragones"]

    -- Hazañas
    hazañas_conocidas TEXT, -- JSON con lista de hazañas

    -- Modificadores comerciales
    modificador_precio REAL DEFAULT 1.0, -- 0.8 = 20% descuento, 1.3 = 30% extra

    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE,
    FOREIGN KEY (faccion_id) REFERENCES facciones(id),
    FOREIGN KEY (civilizacion_id) REFERENCES civilizaciones(id),
    CONSTRAINT check_una_entidad CHECK (
        (faccion_id IS NOT NULL AND civilizacion_id IS NULL) OR
        (faccion_id IS NULL AND civilizacion_id IS NOT NULL)
    )
);

-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
-- 3. EVENTOS HISTÓRICOS PROCEDURALES
-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

-- TABLA: BODAS (expandido)
CREATE TABLE IF NOT EXISTS bodas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    matrimonio_id INTEGER NOT NULL,
    año INTEGER NOT NULL,
    lugar_id INTEGER,

    -- Tipo
    tipo VARCHAR(50), -- 'comun', 'noble', 'real', 'divina'
    es_publica BOOLEAN DEFAULT 1,

    -- Asistentes
    asistentes_ids TEXT, -- JSON array de IDs
    numero_asistentes INTEGER,

    -- Importancia
    importancia INTEGER DEFAULT 5, -- 1-10
    une_facciones BOOLEAN DEFAULT 0,
    facciones_unidas TEXT, -- JSON

    descripcion TEXT,

    FOREIGN KEY (matrimonio_id) REFERENCES matrimonios(id),
    FOREIGN KEY (lugar_id) REFERENCES pueblos_ciudades(id)
);

-- TABLA: FESTIVALES Y CELEBRACIONES
CREATE TABLE IF NOT EXISTS festivales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(200) NOT NULL,
    tipo VARCHAR(50), -- 'religioso', 'cosecha', 'militar', 'astronomico'
    frecuencia_años INTEGER, -- Cada cuántos años ocurre
    dios_asociado_id INTEGER,
    civilizacion_id INTEGER,

    descripcion TEXT,
    actividades TEXT, -- JSON

    FOREIGN KEY (dios_asociado_id) REFERENCES dioses(id),
    FOREIGN KEY (civilizacion_id) REFERENCES civilizaciones(id)
);

-- TABLA: OCURRENCIAS DE FESTIVALES
CREATE TABLE IF NOT EXISTS festival_ocurrencias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    festival_id INTEGER NOT NULL,
    año INTEGER NOT NULL,
    lugar_id INTEGER NOT NULL,

    asistentes_aproximados INTEGER,
    eventos_especiales TEXT, -- JSON

    FOREIGN KEY (festival_id) REFERENCES festivales(id),
    FOREIGN KEY (lugar_id) REFERENCES pueblos_ciudades(id)
);

-- TABLA: DESASTRES NATURALES
CREATE TABLE IF NOT EXISTS desastres (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo VARCHAR(50), -- 'erupcion', 'terremoto', 'huracan', 'sequia', 'inundacion', 'epidemia'
    nombre VARCHAR(200),
    año INTEGER NOT NULL,
    duracion_años INTEGER DEFAULT 1,

    -- Ubicación
    lugar_epicentro_id INTEGER,
    radio_afectacion INTEGER, -- km

    -- Impacto
    muertes_aproximadas INTEGER,
    ciudades_destruidas TEXT, -- JSON array de IDs

    -- Consecuencias
    migracion_masiva BOOLEAN DEFAULT 0,
    hambruna_resultante BOOLEAN DEFAULT 0,

    descripcion TEXT,

    FOREIGN KEY (lugar_epicentro_id) REFERENCES pueblos_ciudades(id)
);

-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
-- 4. SISTEMA DE ENFERMEDADES Y SANACIÓN
-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

-- TABLA: ENFERMEDADES
CREATE TABLE IF NOT EXISTS enfermedades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    tipo VARCHAR(50), -- 'infecciosa', 'cronica', 'parasitaria', 'magica', 'maldicion'
    gravedad INTEGER, -- 1-10

    -- Transmisión
    contagio INTEGER, -- 0-100 (probabilidad de contagio)
    vector VARCHAR(50), -- 'aire', 'agua', 'contacto', 'insecto', 'maldicion'

    -- Síntomas
    sintomas TEXT, -- JSON
    duracion_dias INTEGER,

    -- Mortalidad
    tasa_mortalidad INTEGER, -- 0-100 (%)

    -- Cura
    curas_posibles TEXT, -- JSON: [{"tipo": "hierba", "item_id": 5, "efectividad": 80}]

    descripcion TEXT
);

-- TABLA: PERSONA ENFERMEDADES (estado actual)
CREATE TABLE IF NOT EXISTS persona_enfermedades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    persona_id INTEGER NOT NULL,
    enfermedad_id INTEGER NOT NULL,

    año_contagio INTEGER NOT NULL,
    año_recuperacion INTEGER,

    estado VARCHAR(50), -- 'incubacion', 'sintomatico', 'grave', 'recuperando', 'cronico'
    gravedad_actual INTEGER, -- 1-10

    -- Tratamiento
    esta_siendo_tratado BOOLEAN DEFAULT 0,
    curandero_id INTEGER,
    tratamiento_actual TEXT, -- JSON

    -- Resultado
    resultado VARCHAR(50), -- 'recuperado', 'muerto', 'cronico', 'inmune'

    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE,
    FOREIGN KEY (enfermedad_id) REFERENCES enfermedades(id),
    FOREIGN KEY (curandero_id) REFERENCES personas(id)
);

-- TABLA: EPIDEMIAS
CREATE TABLE IF NOT EXISTS epidemias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(200) NOT NULL,
    enfermedad_id INTEGER NOT NULL,
    año_inicio INTEGER NOT NULL,
    año_fin INTEGER,

    -- Ubicación
    lugar_origen_id INTEGER,
    lugares_afectados TEXT, -- JSON array de IDs

    -- Impacto
    infectados_totales INTEGER,
    muertes_totales INTEGER,

    -- Respuesta
    cuarentena_aplicada BOOLEAN DEFAULT 0,
    cura_encontrada BOOLEAN DEFAULT 0,

    descripcion TEXT,

    FOREIGN KEY (enfermedad_id) REFERENCES enfermedades(id),
    FOREIGN KEY (lugar_origen_id) REFERENCES pueblos_ciudades(id)
);

-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
-- 5. CRAFTING AVANZADO CON RECETAS
-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

-- TABLA: RECETAS
CREATE TABLE IF NOT EXISTS recetas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(200) NOT NULL,
    item_resultado_id INTEGER NOT NULL,
    cantidad_resultado INTEGER DEFAULT 1,

    -- Requisitos
    oficio_requerido_id INTEGER,
    nivel_maestria_minimo INTEGER DEFAULT 1,
    herramienta_requerida_id INTEGER,

    -- Tiempo y dificultad
    tiempo_creacion_dias INTEGER DEFAULT 1,
    dificultad INTEGER, -- 1-10

    -- Rareza
    rareza VARCHAR(50), -- 'comun', 'poco_comun', 'raro', 'epico', 'legendario'
    es_secreta BOOLEAN DEFAULT 0, -- Si es receta secreta de familia
    linaje_id INTEGER, -- Si es exclusiva de un linaje

    descripcion TEXT,

    FOREIGN KEY (item_resultado_id) REFERENCES items(id),
    FOREIGN KEY (oficio_requerido_id) REFERENCES oficios(id),
    FOREIGN KEY (herramienta_requerida_id) REFERENCES items(id),
    FOREIGN KEY (linaje_id) REFERENCES linajes(id)
);

-- TABLA: INGREDIENTES DE RECETA
CREATE TABLE IF NOT EXISTS receta_ingredientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    receta_id INTEGER NOT NULL,
    item_id INTEGER NOT NULL,
    cantidad_requerida INTEGER NOT NULL,
    es_opcional BOOLEAN DEFAULT 0,

    FOREIGN KEY (receta_id) REFERENCES recetas(id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES items(id)
);

-- TABLA: PERSONA RECETAS CONOCIDAS
CREATE TABLE IF NOT EXISTS persona_recetas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    persona_id INTEGER NOT NULL,
    receta_id INTEGER NOT NULL,

    año_aprendizaje INTEGER,
    aprendido_de_id INTEGER, -- Maestro que le enseñó

    -- Maestría
    veces_creada INTEGER DEFAULT 0,
    tasa_exito INTEGER DEFAULT 50, -- 0-100

    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE,
    FOREIGN KEY (receta_id) REFERENCES recetas(id),
    FOREIGN KEY (aprendido_de_id) REFERENCES personas(id),
    UNIQUE(persona_id, receta_id)
);

-- TABLA: HISTORIAL DE CRAFTING
CREATE TABLE IF NOT EXISTS crafting_historial (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    persona_id INTEGER NOT NULL,
    receta_id INTEGER NOT NULL,
    año INTEGER NOT NULL,

    exitoso BOOLEAN NOT NULL,
    calidad_resultado INTEGER, -- 1-10 (si fue exitoso)
    item_creado_id INTEGER, -- Referencia al item en inventario

    FOREIGN KEY (persona_id) REFERENCES personas(id),
    FOREIGN KEY (receta_id) REFERENCES recetas(id)
);

-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
-- 6. SISTEMA DE CRÍMENES Y JUSTICIA
-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

-- TABLA: CRÍMENES
CREATE TABLE IF NOT EXISTS crimenes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo VARCHAR(50), -- 'robo', 'asesinato', 'asalto', 'traicion', 'herejia', 'desercion'
    gravedad INTEGER, -- 1-10

    año INTEGER NOT NULL,
    lugar_id INTEGER,

    -- Involucrados
    perpetrador_id INTEGER NOT NULL,
    victima_id INTEGER,
    complices_ids TEXT, -- JSON array
    testigos_ids TEXT, -- JSON array

    -- Evidencia
    atrapado BOOLEAN DEFAULT 0,
    evidencia TEXT, -- JSON

    descripcion TEXT,

    FOREIGN KEY (lugar_id) REFERENCES pueblos_ciudades(id),
    FOREIGN KEY (perpetrador_id) REFERENCES personas(id),
    FOREIGN KEY (victima_id) REFERENCES personas(id)
);

-- TABLA: JUICIOS
CREATE TABLE IF NOT EXISTS juicios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    crimen_id INTEGER NOT NULL,
    año INTEGER NOT NULL,
    lugar_id INTEGER NOT NULL,

    -- Autoridades
    juez_id INTEGER NOT NULL, -- Sacerdote, noble o dios
    tipo_juez VARCHAR(50), -- 'sacerdote', 'noble', 'consejo', 'divino'

    -- Proceso
    acusado_id INTEGER NOT NULL,
    defensores_ids TEXT, -- JSON
    acusadores_ids TEXT, -- JSON
    testimonios TEXT, -- JSON

    -- Veredicto
    veredicto VARCHAR(50), -- 'culpable', 'inocente', 'parcial'
    castigo_id INTEGER,

    -- Apelación
    apelado BOOLEAN DEFAULT 0,

    FOREIGN KEY (crimen_id) REFERENCES crimenes(id),
    FOREIGN KEY (lugar_id) REFERENCES pueblos_ciudades(id),
    FOREIGN KEY (juez_id) REFERENCES personas(id),
    FOREIGN KEY (acusado_id) REFERENCES personas(id)
);

-- TABLA: CASTIGOS
CREATE TABLE IF NOT EXISTS castigos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100),
    tipo VARCHAR(50), -- 'multa', 'prision', 'trabajo_forzado', 'exilio', 'ejecucion', 'mutilacion'
    gravedad INTEGER, -- 1-10

    -- Detalles
    duracion_años INTEGER,
    descripcion TEXT,

    -- Efecto en persona
    afecta_reputacion INTEGER, -- Penalización
    afecta_clase_social BOOLEAN DEFAULT 0
);

-- TABLA: CASTIGOS APLICADOS
CREATE TABLE IF NOT EXISTS persona_castigos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    persona_id INTEGER NOT NULL,
    castigo_id INTEGER NOT NULL,
    juicio_id INTEGER,

    año_inicio INTEGER NOT NULL,
    año_fin INTEGER,

    completado BOOLEAN DEFAULT 0,
    escapo BOOLEAN DEFAULT 0,

    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE,
    FOREIGN KEY (castigo_id) REFERENCES castigos(id),
    FOREIGN KEY (juicio_id) REFERENCES juicios(id)
);

-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
-- 7. MUTACIONES Y BIO-TECNOLOGÍA
-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

-- TABLA: MUTACIONES
CREATE TABLE IF NOT EXISTS mutaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(100) NOT NULL UNIQUE,
    tipo VARCHAR(50), -- 'fisica', 'mental', 'sensorial', 'magica'
    polaridad VARCHAR(50), -- 'positiva', 'negativa', 'neutral'

    -- Origen
    origen VARCHAR(50), -- 'divina', 'biotecnologica', 'radiacion_portal', 'natural'
    dios_creador_id INTEGER,

    -- Genética
    es_heredable BOOLEAN DEFAULT 0,
    probabilidad_herencia INTEGER, -- 0-100 (%)
    dominante BOOLEAN DEFAULT 0, -- Si es dominante sobre mutaciones normales

    -- Efectos
    descripcion_visual TEXT,
    efectos_mecanicos TEXT, -- JSON: {"fuerza": +10, "velocidad": +5}

    -- Social
    aceptacion_social INTEGER, -- -10 a +10 (rechazado a venerado)

    FOREIGN KEY (dios_creador_id) REFERENCES dioses(id)
);

-- TABLA: PERSONA MUTACIONES
CREATE TABLE IF NOT EXISTS persona_mutaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    persona_id INTEGER NOT NULL,
    mutacion_id INTEGER NOT NULL,

    año_adquisicion INTEGER NOT NULL,
    forma_adquisicion VARCHAR(50), -- 'nacimiento', 'bendicion', 'experimento', 'accidente'

    -- Control
    nivel_control INTEGER DEFAULT 1, -- 1-10
    efectos_secundarios TEXT, -- JSON

    -- Heredada
    heredada_de_id INTEGER, -- Si fue heredada, de quién

    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE,
    FOREIGN KEY (mutacion_id) REFERENCES mutaciones(id),
    FOREIGN KEY (heredada_de_id) REFERENCES personas(id),
    UNIQUE(persona_id, mutacion_id)
);

-- TABLA: EXPERIMENTOS BIO-TECNOLÓGICOS
CREATE TABLE IF NOT EXISTS experimentos_biotech (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(200),
    tipo VARCHAR(50), -- 'mutacion', 'mejora', 'curacion', 'arma_biologica'

    año INTEGER NOT NULL,
    cientifico_id INTEGER NOT NULL, -- Biomecánico, Alquimista, etc.
    lugar_id INTEGER,

    -- Sujetos
    sujetos_ids TEXT, -- JSON array

    -- Resultado
    exitoso BOOLEAN,
    mutacion_resultante_id INTEGER,
    efectos_colaterales TEXT, -- JSON

    notas TEXT,

    FOREIGN KEY (cientifico_id) REFERENCES personas(id),
    FOREIGN KEY (lugar_id) REFERENCES pueblos_ciudades(id),
    FOREIGN KEY (mutacion_resultante_id) REFERENCES mutaciones(id)
);

-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
-- 8. ORGANIZACIONES Y GREMIOS
-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

-- TABLA: ORGANIZACIONES
CREATE TABLE IF NOT EXISTS organizaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(200) NOT NULL UNIQUE,
    tipo VARCHAR(50), -- 'gremio', 'culto', 'orden_militar', 'sociedad_secreta', 'academia'

    -- Afiliación
    oficio_asociado_id INTEGER,
    dios_patron_id INTEGER,
    civilizacion_id INTEGER,

    -- Estructura
    lider_id INTEGER,
    sede_id INTEGER,
    año_fundacion INTEGER,
    año_disolucion INTEGER,

    -- Requisitos
    requisitos_ingreso TEXT, -- JSON
    cuota_membresia INTEGER, -- Costo en trueque

    -- Beneficios
    beneficios TEXT, -- JSON
    recetas_exclusivas TEXT, -- JSON array de receta_ids

    descripcion TEXT,

    FOREIGN KEY (oficio_asociado_id) REFERENCES oficios(id),
    FOREIGN KEY (dios_patron_id) REFERENCES dioses(id),
    FOREIGN KEY (civilizacion_id) REFERENCES civilizaciones(id),
    FOREIGN KEY (lider_id) REFERENCES personas(id),
    FOREIGN KEY (sede_id) REFERENCES pueblos_ciudades(id)
);

-- TABLA: MIEMBROS DE ORGANIZACIONES
CREATE TABLE IF NOT EXISTS organizacion_miembros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    organizacion_id INTEGER NOT NULL,
    persona_id INTEGER NOT NULL,

    año_ingreso INTEGER NOT NULL,
    año_salida INTEGER,

    -- Rango
    rango VARCHAR(50), -- 'iniciado', 'miembro', 'veterano', 'maestro', 'lider'
    nivel_rango INTEGER DEFAULT 1, -- 1-10

    -- Contribuciones
    contribuciones_totales INTEGER DEFAULT 0,
    reputacion_interna INTEGER DEFAULT 50, -- 0-100

    -- Estado
    activo BOOLEAN DEFAULT 1,
    razon_salida VARCHAR(100),

    FOREIGN KEY (organizacion_id) REFERENCES organizaciones(id),
    FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE,
    UNIQUE(organizacion_id, persona_id)
);

-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
-- 9. RELIQUIAS Y ARTEFACTOS DIVINOS
-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

-- TABLA: ARTEFACTOS
CREATE TABLE IF NOT EXISTS artefactos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre VARCHAR(200) NOT NULL UNIQUE,
    tipo VARCHAR(50), -- 'arma', 'armadura', 'joya', 'reliquia', 'grimorio'

    -- Origen
    dios_creador_id INTEGER,
    año_creacion INTEGER,
    creador_mortal_id INTEGER, -- Si fue creado por un mortal

    -- Poder
    nivel_poder INTEGER, -- 1-10
    poderes TEXT, -- JSON: [{"nombre": "Visión del futuro", "coste": "1 año de vida"}]

    -- Maldición
    tiene_maldicion BOOLEAN DEFAULT 0,
    maldicion TEXT, -- JSON

    -- Rareza
    rareza VARCHAR(50), -- 'unico', 'legendario', 'epico'

    -- Ubicación actual
    poseedor_actual_id INTEGER,
    lugar_actual_id INTEGER,
    esta_perdido BOOLEAN DEFAULT 0,

    -- Herencia
    linaje_protector_id INTEGER, -- Familia que lo protege

    descripcion TEXT,
    historia TEXT,

    FOREIGN KEY (dios_creador_id) REFERENCES dioses(id),
    FOREIGN KEY (creador_mortal_id) REFERENCES personas(id),
    FOREIGN KEY (poseedor_actual_id) REFERENCES personas(id),
    FOREIGN KEY (lugar_actual_id) REFERENCES pueblos_ciudades(id),
    FOREIGN KEY (linaje_protector_id) REFERENCES linajes(id)
);

-- TABLA: HISTORIA DE ARTEFACTOS
CREATE TABLE IF NOT EXISTS artefacto_historia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    artefacto_id INTEGER NOT NULL,
    año INTEGER NOT NULL,

    evento VARCHAR(50), -- 'creacion', 'transferencia', 'robo', 'perdida', 'batalla'
    poseedor_previo_id INTEGER,
    poseedor_nuevo_id INTEGER,

    lugar_id INTEGER,

    descripcion TEXT,

    FOREIGN KEY (artefacto_id) REFERENCES artefactos(id),
    FOREIGN KEY (poseedor_previo_id) REFERENCES personas(id),
    FOREIGN KEY (poseedor_nuevo_id) REFERENCES personas(id),
    FOREIGN KEY (lugar_id) REFERENCES pueblos_ciudades(id)
);

-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
-- 10. SISTEMA DE CLIMA Y ESTACIONES
-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

-- TABLA: CICLOS CLIMÁTICOS
CREATE TABLE IF NOT EXISTS ciclos_climaticos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    año INTEGER NOT NULL,
    estacion VARCHAR(50), -- 'seca', 'lluvias', 'frio', 'calor_extremo'
    region_id INTEGER, -- Puede afectar solo una región

    -- Duración (en meses del calendario del juego)
    mes_inicio INTEGER,
    mes_fin INTEGER,

    -- Intensidad
    intensidad INTEGER, -- 1-10

    -- Efectos
    afecta_cosechas BOOLEAN DEFAULT 1,
    modificador_cosecha REAL DEFAULT 1.0, -- 0.5 = mitad, 2.0 = doble

    afecta_pesca BOOLEAN DEFAULT 0,
    afecta_comercio BOOLEAN DEFAULT 0,

    -- Eventos extremos
    es_extremo BOOLEAN DEFAULT 0, -- Sequía, tormenta severa, etc.

    FOREIGN KEY (region_id) REFERENCES civilizaciones(id)
);

-- TABLA: EVENTOS CLIMÁTICOS
CREATE TABLE IF NOT EXISTS eventos_climaticos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo VARCHAR(50), -- 'huracan', 'sequia', 'inundacion', 'nevada', 'tormenta_electrica'
    nombre VARCHAR(200),

    año INTEGER NOT NULL,
    duracion_dias INTEGER,

    lugar_afectado_id INTEGER,
    radio_impacto INTEGER, -- km

    -- Impacto
    daños_materiales INTEGER, -- Valor en trueque
    cultivos_destruidos BOOLEAN DEFAULT 0,
    casas_destruidas INTEGER DEFAULT 0,

    -- Víctimas
    muertos INTEGER DEFAULT 0,
    heridos INTEGER DEFAULT 0,

    descripcion TEXT,

    FOREIGN KEY (lugar_afectado_id) REFERENCES pueblos_ciudades(id)
);

-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
-- ÍNDICES PARA MEJORAR RENDIMIENTO
-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CREATE INDEX IF NOT EXISTS idx_batallas_año ON batallas(año);
CREATE INDEX IF NOT EXISTS idx_batallas_lugar ON batallas(lugar_id);
CREATE INDEX IF NOT EXISTS idx_heridas_persona ON heridas(persona_id);
CREATE INDEX IF NOT EXISTS idx_persona_reputacion_persona ON persona_reputacion(persona_id);
CREATE INDEX IF NOT EXISTS idx_crimenes_perpetrador ON crimenes(perpetrador_id);
CREATE INDEX IF NOT EXISTS idx_crimenes_año ON crimenes(año);
CREATE INDEX IF NOT EXISTS idx_persona_mutaciones_persona ON persona_mutaciones(persona_id);
CREATE INDEX IF NOT EXISTS idx_organizacion_miembros_org ON organizacion_miembros(organizacion_id);
CREATE INDEX IF NOT EXISTS idx_organizacion_miembros_persona ON organizacion_miembros(persona_id);
CREATE INDEX IF NOT EXISTS idx_artefactos_poseedor ON artefactos(poseedor_actual_id);
CREATE INDEX IF NOT EXISTS idx_recetas_oficio ON recetas(oficio_requerido_id);
CREATE INDEX IF NOT EXISTS idx_persona_recetas_persona ON persona_recetas(persona_id);

-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
-- VISTAS ÚTILES
-- ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

-- Vista: Historial de combate de una persona
CREATE VIEW IF NOT EXISTS historial_combate AS
SELECT
    p.id as persona_id,
    p.nombre_completo,
    b.nombre as batalla,
    b.año,
    bp.bando,
    bp.resultado,
    bp.enemigos_eliminados
FROM personas p
JOIN batalla_participantes bp ON p.id = bp.persona_id
JOIN batallas b ON bp.batalla_id = b.id
ORDER BY p.id, b.año;

-- Vista: Criminales y sus crímenes
CREATE VIEW IF NOT EXISTS registro_criminal AS
SELECT
    p.nombre_completo as criminal,
    c.tipo as crimen,
    c.año,
    c.gravedad,
    c.atrapado,
    j.veredicto,
    ca.nombre as castigo
FROM personas p
JOIN crimenes c ON p.id = c.perpetrador_id
LEFT JOIN juicios j ON c.id = j.crimen_id
LEFT JOIN castigos ca ON j.castigo_id = ca.id
ORDER BY c.año;

-- Vista: Artefactos y sus poseedores
CREATE VIEW IF NOT EXISTS artefactos_poseedores AS
SELECT
    a.nombre as artefacto,
    a.tipo,
    a.nivel_poder,
    p.nombre_completo as poseedor_actual,
    a.esta_perdido,
    d.nombre as creador_divino
FROM artefactos a
LEFT JOIN personas p ON a.poseedor_actual_id = p.id
LEFT JOIN dioses d ON a.dios_creador_id = d.id;
