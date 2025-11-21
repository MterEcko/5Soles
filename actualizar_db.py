#!/usr/bin/env python3
"""
Script para actualizar la base de datos con las nuevas tablas e idiomas
"""

import random
import json
from database_connector import DatabaseConnector # Importación clave

# La clase DatabaseConnector ahora maneja la conexión

def actualizar_schema(db: DatabaseConnector):
    """Agrega las nuevas tablas si no existen"""
    print("Actualizando esquema de base de datos...")

    # El cursor ya está disponible a través de db
    
    # 1. Ejecutar solo las partes nuevas del esquema
    nuevas_tablas_sql = """
    -- TABLA: EVENTOS_VITALES - Historial detallado de vida de personas
    CREATE TABLE IF NOT EXISTS eventos_vitales (
        id SERIAL PRIMARY KEY,
        persona_id INTEGER NOT NULL REFERENCES personas(id) ON DELETE CASCADE,
        tipo_evento VARCHAR(50) NOT NULL,
        año INTEGER NOT NULL,
        descripcion TEXT NOT NULL,
        lugar_id INTEGER REFERENCES pueblos_ciudades(id),
        evento_relacionado_id INTEGER REFERENCES eventos(id),
        persona_relacionada_id INTEGER REFERENCES personas(id),
        severidad VARCHAR(20),
        resultado VARCHAR(100),
        metadata JSONB
    );

    CREATE TABLE IF NOT EXISTS idiomas (
        id SERIAL PRIMARY KEY,
        nombre VARCHAR(100) NOT NULL UNIQUE,
        codigo_iso VARCHAR(10),
        tipo VARCHAR(50),
        familia_linguistica VARCHAR(100),
        hablantes_nativos INTEGER,
        descripcion TEXT
    );

    CREATE TABLE IF NOT EXISTS traducciones (
        id SERIAL PRIMARY KEY,
        clave VARCHAR(200) NOT NULL,
        idioma_id INTEGER NOT NULL REFERENCES idiomas(id),
        texto TEXT NOT NULL,
        contexto VARCHAR(100),
        es_formal BOOLEAN DEFAULT FALSE,
        metadata JSONB,
        UNIQUE(clave, idioma_id)
    );

    CREATE TABLE IF NOT EXISTS persona_idiomas (
        id SERIAL PRIMARY KEY,
        persona_id INTEGER NOT NULL REFERENCES personas(id) ON DELETE CASCADE,
        idioma_id INTEGER NOT NULL REFERENCES idiomas(id),
        nivel_dominio INTEGER DEFAULT 1,
        es_nativo BOOLEAN DEFAULT FALSE,
        UNIQUE(persona_id, idioma_id)
    );

    -- Índices
    CREATE INDEX IF NOT EXISTS idx_eventos_vitales_persona ON eventos_vitales(persona_id);
    CREATE INDEX IF NOT EXISTS idx_eventos_vitales_año ON eventos_vitales(año);
    CREATE INDEX IF NOT EXISTS idx_eventos_vitales_tipo ON eventos_vitales(tipo_evento);
    CREATE INDEX IF NOT EXISTS idx_traducciones_clave ON traducciones(clave);
    CREATE INDEX IF NOT EXISTS idx_traducciones_idioma ON traducciones(idioma_id);
    CREATE INDEX IF NOT EXISTS idx_traducciones_contexto ON traducciones(contexto);
    """

    # La función executescript en DatabaseConnector maneja el reemplazo de ? por %s y SERIAL PRIMARY KEY por AUTOINCREMENT
    db.executescript(nuevas_tablas_sql)
    db.commit()

    print("✓ Esquema actualizado correctamente")


def poblar_idiomas(db: DatabaseConnector):
    """Pobla la tabla de idiomas"""
    print("\nPoblando idiomas...")
    
    db.execute("SELECT COUNT(*) FROM idiomas")
    if db.fetchone()['count'] > 0:
        print("✓ Los idiomas ya están poblados")
        return

    idiomas = [
        ('Náhuatl', 'nah', 'indigena', 'Uto-azteca', 1500000, 'Lengua de los mexicas (aztecas)'),
        ('Maya Yucateco', 'yua', 'indigena', 'Maya', 800000, 'Principal lengua maya'),
        ('Zapoteco', 'zap', 'indigena', 'Otomangue', 450000, 'Familia de lenguas habladas en Oaxaca'),
        ('Mixteco', 'mix', 'indigena', 'Otomangue', 500000, 'Lenguas habladas por el pueblo mixteco'),
        ('Purépecha (Tarasco)', 'tsz', 'indigena', 'Lengua aislada', 140000, 'Lengua del pueblo purépecha en Michoacán'),
        ('Otomí', 'oto', 'indigena', 'Otomangue', 280000, 'Lengua otomangue hablada en el centro de México'),
        ('Totonaco', 'top', 'indigena', 'Totonaco-tepehua', 250000, 'Lengua hablada en Veracruz y Puebla'),
        ('Español', 'es', 'moderno', 'Indoeuropeo (Romance)', 500000000, 'Idioma romance derivado del latín'),
        ('Inglés', 'en', 'moderno', 'Indoeuropeo (Germánico)', 1500000000, 'Idioma germánico de origen anglosajón'),
        ('Francés', 'fr', 'moderno', 'Indoeuropeo (Romance)', 280000000, 'Idioma romance hablado principalmente en Francia'),
        ('Ruso', 'ru', 'moderno', 'Indoeuropeo (Eslavo)', 258000000, 'Idioma eslavo oriental'),
        ('Chino Mandarín', 'zh', 'moderno', 'Sino-tibetano', 1100000000, 'Variante estándar del chino'),
        ('Japonés', 'ja', 'moderno', 'Japónico', 125000000, 'Lengua del archipiélago japonés'),
    ]

    for idioma in idiomas:
        db.execute('''
            INSERT INTO idiomas (nombre, codigo_iso, tipo, familia_linguistica, hablantes_nativos, descripcion)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (nombre) DO NOTHING
        ''', idioma)

    db.commit()
    db.execute("SELECT COUNT(*) FROM idiomas")
    print(f"✓ {db.fetchone()['count']} idiomas insertados")


def poblar_traducciones_basicas(db: DatabaseConnector):
    """Pobla traducciones básicas para entrenamiento de IA"""
    print("\nPoblando traducciones básicas...")
    
    db.execute("SELECT COUNT(*) FROM traducciones")
    if db.fetchone()['count'] > 0:
        print("✓ Las traducciones ya están pobladas")
        return

    # Obtener IDs de idiomas
    db.execute("SELECT id, codigo_iso FROM idiomas")
    idiomas_map = {row['codigo_iso']: row['id'] for row in db.fetchall()}

    # Frases comunes
    frases_saludos = {
        'saludo_hola': {'nah': 'Niltze', 'yua': 'Bix a beel', 'es': 'Hola', 'en': 'Hello'},
        'despedida_adios': {'nah': 'Ōmpa timonēxtīz', 'yua': 'Túun túun', 'es': 'Adiós', 'en': 'Goodbye'},
        'gracias': {'nah': 'Tlazohcāmati', 'yua': 'Yuum bo\'otik', 'es': 'Gracias', 'en': 'Thank you'},
        'nombre_como_te_llamas': {'nah': '¿Quen motōcā?', 'yua': '¿Bix a k\'aaba\'?', 'es': '¿Cómo te llamas?', 'en': 'What is your name?'},
    }

    traducciones_lista = []
    for clave, traducciones in frases_saludos.items():
        for codigo_iso, texto in traducciones.items():
            if codigo_iso in idiomas_map:
                traducciones_lista.append((
                    clave,
                    idiomas_map[codigo_iso],
                    texto,
                    'saludo' if 'saludo' in clave or 'despedida' in clave else 'pregunta',
                    False,
                    json.dumps({'pronunciacion': 'varios'})
                ))

    for clave, idioma_id, texto, contexto, formal, metadata in traducciones_lista:
        db.execute('''
            INSERT INTO traducciones (clave, idioma_id, texto, contexto, es_formal, metadata)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (clave, idioma_id) DO NOTHING
        ''', (clave, idioma_id, texto, contexto, formal, metadata))

    db.commit()
    db.execute("SELECT COUNT(*) FROM traducciones")
    print(f"✓ {db.fetchone()['count']} traducciones insertadas")


def generar_eventos_vitales_iniciales(db: DatabaseConnector):
    """Genera eventos vitales para las personas existentes"""
    print("\nGenerando eventos vitales iniciales...")

    db.execute("SELECT COUNT(*) FROM eventos_vitales")
    if db.fetchone()['count'] > 0:
        print("✓ Los eventos vitales ya existen")
        return

    # Obtener todas las personas
    db.execute('''
        SELECT id, nombre_completo, año_nacimiento, año_muerte,
               lugar_nacimiento_id, causa_muerte
        FROM personas
        LIMIT 100
    ''')

    personas = db.fetchall()
    eventos = []

    for persona in personas:
        pid = persona['id']
        nombre = persona['nombre_completo']
        año_nac = persona['año_nacimiento']
        año_muerte = persona['año_muerte']
        lugar_nac = persona['lugar_nacimiento_id']
        causa = persona['causa_muerte']

        # Evento de nacimiento
        eventos.append((
            pid,
            'nacimiento',
            año_nac,
            f'{nombre} nació en el año {año_nac}',
            lugar_nac,
            None,
            None,
            None,
            None,
            json.dumps({})
        ))

        # Evento de muerte si aplica
        if año_muerte is not None and causa is not None:
            eventos.append((
                pid,
                'muerte',
                año_muerte,
                f'{nombre} murió por {causa} a los {año_muerte - año_nac} años',
                lugar_nac,
                None,
                None,
                'critico',
                'murio',
                json.dumps({'causa': causa, 'edad': año_muerte - año_nac})
            ))

    if eventos:
        for evento in eventos:
            db.execute('''
                INSERT INTO eventos_vitales
                (persona_id, tipo_evento, año, descripcion, lugar_id,
                 evento_relacionado_id, persona_relacionada_id, severidad, resultado, metadata)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', evento)

        db.commit()
        db.execute("SELECT COUNT(*) FROM eventos_vitales")
        print(f"✓ {db.fetchone()['count']} eventos vitales generados")
    else:
        print("⚠ No hay personas para generar eventos")


def main():
    print("="*70)
    print("ACTUALIZACIÓN DE BASE DE DATOS - Portales del Quinto Sol")
    print("="*70 + "\n")

    try:
        # 1. Inicializar DatabaseConnector
        db = DatabaseConnector()
        db.connect()

        # 2. Aplicar cambios
        actualizar_schema(db)
        poblar_idiomas(db)
        poblar_traducciones_basicas(db)
        generar_eventos_vitales_iniciales(db)

        print("\n" + "="*70)
        print("✓ Actualización completada exitosamente")
        print("="*70 + "\n")

        # Mostrar estadísticas
        print("📊 Estadísticas:")
        db.execute("SELECT COUNT(*) FROM idiomas")
        print(f"Idiomas en sistema: {db.fetchone()['count']}")
        db.execute("SELECT COUNT(*) FROM traducciones")
        print(f"Traducciones: {db.fetchone()['count']}")
        db.execute("SELECT COUNT(*) FROM eventos_vitales")
        print(f"Eventos vitales: {db.fetchone()['count']}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        if 'db' in locals():
            db.close()


if __name__ == '__main__':
    main()