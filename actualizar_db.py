#!/usr/bin/env python3
"""
Script para actualizar la base de datos con las nuevas tablas e idiomas
"""

import sqlite3
import json

def actualizar_schema(db_path='quinto_sol.db'):
    """Agrega las nuevas tablas si no existen"""
    print("Actualizando esquema de base de datos...")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Verificar si las tablas nuevas ya existen
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name IN ('eventos_vitales', 'idiomas', 'traducciones', 'persona_idiomas')
    """)
    tablas_existentes = [row[0] for row in cursor.fetchall()]

    if len(tablas_existentes) == 4:
        print("✓ Las tablas ya están actualizadas")
        return conn

    # Leer y ejecutar solo las partes nuevas del esquema
    nuevas_tablas_sql = """
    -- TABLA: EVENTOS_VITALES - Historial detallado de vida de personas
    CREATE TABLE IF NOT EXISTS eventos_vitales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        persona_id INTEGER NOT NULL,
        tipo_evento VARCHAR(50) NOT NULL,
        año INTEGER NOT NULL,
        descripcion TEXT NOT NULL,
        lugar_id INTEGER,
        evento_relacionado_id INTEGER,
        persona_relacionada_id INTEGER,
        severidad VARCHAR(20),
        resultado VARCHAR(100),
        metadata TEXT,
        FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE,
        FOREIGN KEY (lugar_id) REFERENCES pueblos_ciudades(id),
        FOREIGN KEY (evento_relacionado_id) REFERENCES eventos(id),
        FOREIGN KEY (persona_relacionada_id) REFERENCES personas(id)
    );

    CREATE TABLE IF NOT EXISTS idiomas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre VARCHAR(100) NOT NULL UNIQUE,
        codigo_iso VARCHAR(10),
        tipo VARCHAR(50),
        familia_linguistica VARCHAR(100),
        hablantes_nativos INTEGER,
        descripcion TEXT
    );

    CREATE TABLE IF NOT EXISTS traducciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        clave VARCHAR(200) NOT NULL,
        idioma_id INTEGER NOT NULL,
        texto TEXT NOT NULL,
        contexto VARCHAR(100),
        es_formal BOOLEAN DEFAULT 0,
        metadata TEXT,
        FOREIGN KEY (idioma_id) REFERENCES idiomas(id),
        UNIQUE(clave, idioma_id)
    );

    CREATE TABLE IF NOT EXISTS persona_idiomas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        persona_id INTEGER NOT NULL,
        idioma_id INTEGER NOT NULL,
        nivel_dominio INTEGER DEFAULT 1,
        es_nativo BOOLEAN DEFAULT 0,
        FOREIGN KEY (persona_id) REFERENCES personas(id) ON DELETE CASCADE,
        FOREIGN KEY (idioma_id) REFERENCES idiomas(id),
        UNIQUE(persona_id, idioma_id)
    );

    CREATE INDEX IF NOT EXISTS idx_eventos_vitales_persona ON eventos_vitales(persona_id);
    CREATE INDEX IF NOT EXISTS idx_eventos_vitales_año ON eventos_vitales(año);
    CREATE INDEX IF NOT EXISTS idx_eventos_vitales_tipo ON eventos_vitales(tipo_evento);
    CREATE INDEX IF NOT EXISTS idx_traducciones_clave ON traducciones(clave);
    CREATE INDEX IF NOT EXISTS idx_traducciones_idioma ON traducciones(idioma_id);
    CREATE INDEX IF NOT EXISTS idx_traducciones_contexto ON traducciones(contexto);
    """

    cursor.executescript(nuevas_tablas_sql)
    conn.commit()

    print("✓ Esquema actualizado correctamente")
    return conn


def poblar_idiomas(conn):
    """Pobla la tabla de idiomas"""
    print("\nPoblando idiomas...")
    cursor = conn.cursor()

    # Verificar si ya hay idiomas
    cursor.execute("SELECT COUNT(*) FROM idiomas")
    if cursor.fetchone()[0] > 0:
        print("✓ Los idiomas ya están poblados")
        return

    idiomas = [
        # Idiomas indígenas mesoamericanos
        ('Náhuatl', 'nah', 'indigena', 'Uto-azteca', 1500000,
         'Lengua de los mexicas (aztecas), hablada en el centro de México'),

        ('Maya Yucateco', 'yua', 'indigena', 'Maya', 800000,
         'Principal lengua maya, hablada en la península de Yucatán'),

        ('Zapoteco', 'zap', 'indigena', 'Otomangue', 450000,
         'Familia de lenguas habladas en Oaxaca'),

        ('Mixteco', 'mix', 'indigena', 'Otomangue', 500000,
         'Lenguas habladas por el pueblo mixteco en Oaxaca, Guerrero y Puebla'),

        ('Purépecha (Tarasco)', 'tsz', 'indigena', 'Lengua aislada', 140000,
         'Lengua del pueblo purépecha en Michoacán'),

        ('Otomí', 'oto', 'indigena', 'Otomangue', 280000,
         'Lengua otomangue hablada en el centro de México'),

        ('Totonaco', 'top', 'indigena', 'Totonaco-tepehua', 250000,
         'Lengua hablada en Veracruz y Puebla'),

        # Idiomas modernos
        ('Español', 'es', 'moderno', 'Indoeuropeo (Romance)', 500000000,
         'Idioma romance derivado del latín'),

        ('Inglés', 'en', 'moderno', 'Indoeuropeo (Germánico)', 1500000000,
         'Idioma germánico de origen anglosajón'),

        ('Francés', 'fr', 'moderno', 'Indoeuropeo (Romance)', 280000000,
         'Idioma romance hablado principalmente en Francia'),

        ('Ruso', 'ru', 'moderno', 'Indoeuropeo (Eslavo)', 258000000,
         'Idioma eslavo oriental, lengua oficial de Rusia'),

        ('Chino Mandarín', 'zh', 'moderno', 'Sino-tibetano', 1100000000,
         'Variante estándar del chino, lengua más hablada del mundo'),

        ('Japonés', 'ja', 'moderno', 'Japónico', 125000000,
         'Lengua del archipiélago japonés'),
    ]

    cursor.executemany('''
        INSERT INTO idiomas (nombre, codigo_iso, tipo, familia_linguistica, hablantes_nativos, descripcion)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', idiomas)

    conn.commit()
    print(f"✓ {len(idiomas)} idiomas insertados")


def poblar_traducciones_basicas(conn):
    """Pobla traducciones básicas para entrenamiento de IA"""
    print("\nPoblando traducciones básicas...")
    cursor = conn.cursor()

    # Verificar si ya hay traducciones
    cursor.execute("SELECT COUNT(*) FROM traducciones")
    if cursor.fetchone()[0] > 0:
        print("✓ Las traducciones ya están pobladas")
        return

    # Obtener IDs de idiomas
    cursor.execute("SELECT id, codigo_iso FROM idiomas")
    idiomas_map = {codigo: id_idioma for id_idioma, codigo in cursor.fetchall()}

    # Frases comunes en todos los idiomas
    frases_saludos = {
        'saludo_hola': {
            'nah': ('Niltze', 'saludo', False, '{"pronunciacion": "NEEL-tzeh"}'),
            'yua': ('Bix a beel', 'saludo', False, '{"pronunciacion": "beesh ah beh-EHL"}'),
            'zap': ('Naa', 'saludo', False, '{"pronunciacion": "NAH"}'),
            'mix': ('Sáꞌá', 'saludo', False, '{"pronunciacion": "SAH-ah"}'),
            'tsz': ('Narhí', 'saludo', False, '{"pronunciacion": "nah-REE"}'),
            'oto': ('Jamadi', 'saludo', False, '{"pronunciacion": "hah-MAH-dee"}'),
            'top': ('Takgalhtsin', 'saludo', False, '{"pronunciacion": "tahk-gahl-TSEEN"}'),
            'es': ('Hola', 'saludo', False, '{"pronunciacion": "OH-lah"}'),
            'en': ('Hello', 'saludo', False, '{"pronunciacion": "heh-LOH"}'),
            'fr': ('Bonjour', 'saludo', False, '{"pronunciacion": "bon-ZHOOR"}'),
            'ru': ('Здравствуйте', 'saludo', True, '{"pronunciacion": "ZDRAH-stvuy-tye"}'),
            'zh': ('你好', 'saludo', False, '{"pronunciacion": "nǐ hǎo"}'),
            'ja': ('こんにちは', 'saludo', False, '{"pronunciacion": "kon-ni-chi-wa"}'),
        },
        'despedida_adios': {
            'nah': ('Ōmpa timonēxtīz', 'despedida', False, '{"pronunciacion": "OHM-pah tee-moh-NEHKS-tees"}'),
            'yua': ('Túun túun', 'despedida', False, '{"pronunciacion": "TOON toon"}'),
            'zap': ('Gasti cani', 'despedida', False, '{"pronunciacion": "GAHS-tee KAH-nee"}'),
            'mix': ('Kuu yu', 'despedida', False, '{"pronunciacion": "KOO yoo"}'),
            'tsz': ('Jimbó', 'despedida', False, '{"pronunciacion": "heem-BOH"}'),
            'oto': ('Dí nuä', 'despedida', False, '{"pronunciacion": "dee NWAH"}'),
            'top': ('Lakachixku', 'despedida', False, '{"pronunciacion": "lah-kah-CHEESH-koo"}'),
            'es': ('Adiós', 'despedida', False, '{}'),
            'en': ('Goodbye', 'despedida', False, '{}'),
            'fr': ('Au revoir', 'despedida', False, '{"pronunciacion": "oh reh-VWAHR"}'),
            'ru': ('До свидания', 'despedida', True, '{"pronunciacion": "dah svee-DAH-nee-yah"}'),
            'zh': ('再见', 'despedida', False, '{"pronunciacion": "zài jiàn"}'),
            'ja': ('さようなら', 'despedida', False, '{"pronunciacion": "sa-yo-na-ra"}'),
        },
        'gracias': {
            'nah': ('Tlazohcāmati', 'agradecimiento', False, '{"pronunciacion": "tlah-soh-KAH-mah-tee"}'),
            'yua': ('Yuum bo\'otik', 'agradecimiento', False, '{"pronunciacion": "yoom boh-oh-TEEK"}'),
            'zap': ('Dios bo chelu', 'agradecimiento', False, '{"pronunciacion": "dee-OHS boh CHEH-loo"}'),
            'mix': ('Táꞌá tsi\'í', 'agradecimiento', False, '{}'),
            'tsz': ('Dios bo paye', 'agradecimiento', False, '{}'),
            'oto': ('Jamadi ma ra t\'eni', 'agradecimiento', False, '{}'),
            'top': ('Kujnijkatsin', 'agradecimiento', False, '{}'),
            'es': ('Gracias', 'agradecimiento', False, '{}'),
            'en': ('Thank you', 'agradecimiento', False, '{}'),
            'fr': ('Merci', 'agradecimiento', False, '{}'),
            'ru': ('Спасибо', 'agradecimiento', False, '{"pronunciacion": "spah-SEE-bah"}'),
            'zh': ('谢谢', 'agradecimiento', False, '{"pronunciacion": "xiè xie"}'),
            'ja': ('ありがとう', 'agradecimiento', False, '{"pronunciacion": "ah-ree-gah-toh"}'),
        },
        'nombre_como_te_llamas': {
            'nah': ('¿Quen motōcā?', 'pregunta', False, '{"significado": "¿Cuál es tu nombre?"}'),
            'yua': ('¿Bix a k\'aaba\'?', 'pregunta', False, '{}'),
            'zap': ('¿Ti laa ruaa?', 'pregunta', False, '{}'),
            'mix': ('¿Naa sáꞌá ro?', 'pregunta', False, '{}'),
            'tsz': ('¿Ambé tsengueri?', 'pregunta', False, '{}'),
            'oto': ('¿Nu gui xtí?', 'pregunta', False, '{}'),
            'top': ('¿Tasna tlakgalhtsin?', 'pregunta', False, '{}'),
            'es': ('¿Cómo te llamas?', 'pregunta', False, '{}'),
            'en': ('What is your name?', 'pregunta', False, '{}'),
            'fr': ('Comment vous appelez-vous?', 'pregunta', True, '{}'),
            'ru': ('Как вас зовут?', 'pregunta', True, '{"pronunciacion": "kahk vahs zah-VOOT"}'),
            'zh': ('你叫什么名字？', 'pregunta', False, '{"pronunciacion": "nǐ jiào shén me míng zi"}'),
            'ja': ('お名前は何ですか？', 'pregunta', True, '{"pronunciacion": "o-na-ma-e wa nan des ka"}'),
        },
    }

    traducciones_lista = []
    for clave, traducciones in frases_saludos.items():
        for codigo_iso, (texto, contexto, formal, metadata) in traducciones.items():
            if codigo_iso in idiomas_map:
                traducciones_lista.append((
                    clave,
                    idiomas_map[codigo_iso],
                    texto,
                    contexto,
                    1 if formal else 0,
                    metadata
                ))

    cursor.executemany('''
        INSERT INTO traducciones (clave, idioma_id, texto, contexto, es_formal, metadata)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', traducciones_lista)

    conn.commit()
    print(f"✓ {len(traducciones_lista)} traducciones insertadas")


def generar_eventos_vitales_iniciales(conn):
    """Genera eventos vitales para las personas existentes"""
    print("\nGenerando eventos vitales iniciales...")
    cursor = conn.cursor()

    # Verificar si ya hay eventos vitales
    cursor.execute("SELECT COUNT(*) FROM eventos_vitales")
    if cursor.fetchone()[0] > 0:
        print("✓ Los eventos vitales ya existen")
        return

    # Obtener todas las personas
    cursor.execute('''
        SELECT id, nombre_completo, año_nacimiento, año_muerte,
               lugar_nacimiento_id, causa_muerte
        FROM personas
        LIMIT 100
    ''')

    personas = cursor.fetchall()
    eventos = []

    for persona in personas:
        pid, nombre, año_nac, año_muerte, lugar_nac, causa = persona

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
            '{}'
        ))

        # Evento de muerte si aplica
        if año_muerte and causa:
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
        cursor.executemany('''
            INSERT INTO eventos_vitales
            (persona_id, tipo_evento, año, descripcion, lugar_id,
             evento_relacionado_id, persona_relacionada_id, severidad, resultado, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', eventos)

        conn.commit()
        print(f"✓ {len(eventos)} eventos vitales generados")
    else:
        print("⚠ No hay personas para generar eventos")


def main():
    print("="*70)
    print("ACTUALIZACIÓN DE BASE DE DATOS - Portales del Quinto Sol")
    print("="*70 + "\n")

    try:
        conn = actualizar_schema()
        poblar_idiomas(conn)
        poblar_traducciones_basicas(conn)
        generar_eventos_vitales_iniciales(conn)

        print("\n" + "="*70)
        print("✓ Actualización completada exitosamente")
        print("="*70 + "\n")

        # Mostrar estadísticas
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM idiomas")
        print(f"Idiomas en sistema: {cursor.fetchone()[0]}")

        cursor.execute("SELECT COUNT(*) FROM traducciones")
        print(f"Traducciones: {cursor.fetchone()[0]}")

        cursor.execute("SELECT COUNT(*) FROM eventos_vitales")
        print(f"Eventos vitales: {cursor.fetchone()[0]}")

        conn.close()

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
