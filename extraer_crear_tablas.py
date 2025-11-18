#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrae y ejecuta SOLO las definiciones CREATE TABLE de todos los schemas
Ignora índices, vistas y constraints que fallen

Ejecutar con: python run_with_env.py extraer_crear_tablas.py
"""

import os
import sys
import re
from pathlib import Path
from database_connector import DatabaseConnector


def extraer_create_tables(sql_content):
    """Extrae solo los CREATE TABLE statements de un archivo SQL"""
    tables = []
    lines = sql_content.split('\n')
    current_table = []
    in_table = False
    paren_count = 0

    for line in lines:
        # Detectar inicio de CREATE TABLE
        if re.search(r'CREATE\s+TABLE\s+IF\s+NOT\s+EXISTS', line, re.IGNORECASE):
            in_table = True
            current_table = [line]
            paren_count = line.count('(') - line.count(')')
            continue

        if in_table:
            current_table.append(line)
            paren_count += line.count('(') - line.count(')')

            # Cuando cerramos todos los paréntesis, terminó la tabla
            if paren_count == 0 and ';' in line:
                table_sql = '\n'.join(current_table)
                tables.append(table_sql)
                current_table = []
                in_table = False

    return tables


def convertir_create_table_postgres(table_sql):
    """Convierte una definición de tabla de SQLite a PostgreSQL"""
    # AUTOINCREMENT → SERIAL
    table_sql = table_sql.replace('INTEGER PRIMARY KEY AUTOINCREMENT', 'SERIAL PRIMARY KEY')
    table_sql = re.sub(r'\sAUTOINCREMENT\b', '', table_sql, flags=re.IGNORECASE)

    # BOOLEAN DEFAULT 0/1 → FALSE/TRUE
    table_sql = re.sub(r'\bBOOLEAN\s+DEFAULT\s+0\b', 'BOOLEAN DEFAULT FALSE', table_sql, flags=re.IGNORECASE)
    table_sql = re.sub(r'\bBOOLEAN\s+DEFAULT\s+1\b', 'BOOLEAN DEFAULT TRUE', table_sql, flags=re.IGNORECASE)

    # DATETIME → TIMESTAMP
    table_sql = table_sql.replace('DATETIME DEFAULT CURRENT_TIMESTAMP', 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
    table_sql = table_sql.replace('DATETIME', 'TIMESTAMP')

    # TEXT → TEXT (ya compatible)
    # VARCHAR → VARCHAR (ya compatible)

    return table_sql


def main():
    print("\n" + "=" * 70)
    print("EXTRACCIÓN Y CREACIÓN DE TODAS LAS TABLAS")
    print("=" * 70)

    # Verificar conexión
    db_type = os.getenv('DB_TYPE', 'sqlite')
    if db_type != 'postgres':
        print("\n❌ ERROR: DB_TYPE debe ser 'postgres'")
        sys.exit(1)

    print(f"\n✅ PostgreSQL: {os.getenv('PG_HOST')}:{os.getenv('PG_PORT')}/{os.getenv('PG_DATABASE')}")

    # Conectar
    db = DatabaseConnector()
    try:
        db.connect()
    except Exception as e:
        print(f"\n❌ Error de conexión: {e}")
        sys.exit(1)

    # Archivos SQL a procesar (en orden de dependencias)
    archivos_sql = [
        'schema_postgres.sql',                               # 1. Tablas base
        'schema_relaciones_especies_civilizaciones.sql',     # 2. Relaciones
        'schema_guerras_especies.sql',                       # 3. Guerras
        'schema_mutaciones.sql',                             # 4. Mutaciones
        'schema_matrimonios_interespecie.sql',               # 5. Matrimonios
        'schema_artefactos_organizaciones_eventos.sql',      # 6. Artefactos
        'schema_migraciones_justicia_clima_economia.sql',   # 7. Migraciones/Economía
        'schema_especies_fauna.sql',                         # 8. Fauna
        'schema_flora.sql',                                  # 9. Flora
        'schema_sistemas_completos.sql',                     # 10. Sistemas
        'schema_extension_ia.sql',                           # 11. IA
    ]

    print("\n" + "=" * 70)
    print("EXTRAYENDO CREATE TABLE DE CADA ARCHIVO")
    print("=" * 70)

    todas_las_tablas = []

    for archivo in archivos_sql:
        if not Path(archivo).exists():
            print(f"⚠️  {archivo} no encontrado")
            continue

        print(f"\n📄 Procesando: {archivo}")

        with open(archivo, 'r', encoding='utf-8') as f:
            sql_content = f.read()

        # Extraer CREATE TABLE
        if 'postgres' in archivo.lower():
            # schema_postgres.sql ya está en formato PostgreSQL
            # Ejecutar completo (tiene funciones, triggers, etc.)
            print(f"   ✅ Ejecutando archivo completo (PostgreSQL nativo)")
            try:
                db.cursor.execute(sql_content)
                db.conn.commit()
                print(f"   ✅ Ejecutado correctamente")
            except Exception as e:
                print(f"   ⚠️  Error: {str(e)[:150]}")
                db.conn.rollback()
        else:
            # Otros archivos: extraer solo CREATE TABLE
            tables = extraer_create_tables(sql_content)
            print(f"   📋 {len(tables)} tablas encontradas")

            for table_sql in tables:
                # Convertir a PostgreSQL
                table_sql_pg = convertir_create_table_postgres(table_sql)

                # Extraer nombre de tabla para logging
                match = re.search(r'CREATE\s+TABLE\s+IF\s+NOT\s+EXISTS\s+(\w+)', table_sql_pg, re.IGNORECASE)
                table_name = match.group(1) if match else "unknown"

                # Ejecutar
                try:
                    db.cursor.execute(table_sql_pg)
                    db.conn.commit()
                    print(f"      ✅ {table_name}")
                except Exception as e:
                    db.conn.rollback()
                    error_msg = str(e).lower()
                    # Ignorar errores de "ya existe"
                    if "ya existe" not in error_msg and "already exists" not in error_msg:
                        print(f"      ❌ {table_name}: {str(e)[:100]}")

    # Poblar datos base
    print("\n" + "=" * 70)
    print("POBLANDO DATOS BASE")
    print("=" * 70)

    # Eras
    print("\n📋 Eras...")
    eras = [
        ('Era Alpha', 'Llegada por los Portales', 1500, 1650, False),
        ('Era de la Fundación', 'Primeras aldeas', 1651, 1800, False),
        ('Era del Despertar', 'Habilidades únicas', 1801, 2000, False),
        ('Era de la Expansión', 'Crecimiento', 2001, 2200, False),
        ('Era del Cataclismo', 'Humanos II', 2201, 2400, False),
        ('Era del Conflicto', 'Tensiones', 2401, 2700, False),
        ('Era de la Síntesis', 'Integración', 2701, 3000, True),
    ]

    for era in eras:
        db.cursor.execute('''
            INSERT INTO eras (nombre, descripcion, año_inicio, año_fin, es_actual)
            VALUES (%s, %s, %s, %s, %s) ON CONFLICT (nombre) DO NOTHING
        ''', era)
    db.conn.commit()
    print(f"   ✅ {len(eras)} eras")

    # Dioses
    print("\n📋 Dioses...")
    dioses = [
        ('Quetzalcóatl', 'Sabiduría', 'Mexica,Maya', 'Positiva', 'Educación', 'Serpiente Emplumada'),
        ('Tezcatlipoca', 'Destino', 'Mexica', 'Negativa', 'Magia', 'Espejo Humeante'),
        ('Tláloc', 'Lluvia', 'Mexica', 'Neutral', 'Agricultura', 'Lluvia'),
        ('Huitzilopochtli', 'Guerra', 'Mexica', 'Neutral', 'Guerra', 'Sol'),
        ('Chaac', 'Lluvia', 'Maya', 'Positiva', 'Agricultura', 'Lluvia maya'),
        ('Kukulkán', 'Viento', 'Maya', 'Positiva', 'Arquitectura', 'Serpiente'),
        ('Itzamná', 'Cielo', 'Maya', 'Positiva', 'Escritura', 'Creador'),
        ('Xipe Tótec', 'Renovación', 'Mexica,Zapoteca', 'Neutral', 'Agricultura', 'Desollado'),
    ]

    for dios in dioses:
        db.cursor.execute('''
            INSERT INTO dioses (nombre, dominio_principal, culturas, polaridad, eje_tecnologico, descripcion)
            VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (nombre) DO NOTHING
        ''', dios)
    db.conn.commit()
    print(f"   ✅ {len(dioses)} dioses")

    # Especies
    print("\n📋 Especies...")
    especies = [
        ('Humanos I', 'Primera oleada 1500', 'humano', 70, 90, 4, 7, None),
        ('Humanos II', 'Segunda oleada 2201', 'humano', 75, 95, 3, 6, None),
    ]

    for especie in especies:
        db.cursor.execute('''
            INSERT INTO especies (nombre, descripcion, tipo, esperanza_vida_min, esperanza_vida_max,
                                 hijos_min, hijos_max, dios_creador_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (nombre) DO NOTHING
        ''', especie)
    db.conn.commit()
    print(f"   ✅ {len(especies)} especies")

    # Civilizaciones
    print("\n📋 Civilizaciones...")
    db.cursor.execute("SELECT id FROM dioses WHERE nombre = 'Huitzilopochtli'")
    result = db.cursor.fetchone()
    dios_mexica = result['id'] if result else None

    if dios_mexica:
        civilizaciones = [
            ('Mexica de Obsidiana', 'Mexica', dios_mexica, 'Guerrera', 1520),
            ('Mayas Celeste', 'Maya', dios_mexica, 'Astrónomos', 1515),
        ]

        for civ in civilizaciones:
            db.cursor.execute('''
                INSERT INTO civilizaciones (nombre, tipo, dios_patron_id, descripcion, año_fundacion)
                VALUES (%s, %s, %s, %s, %s) ON CONFLICT (nombre) DO NOTHING
            ''', civ)
        db.conn.commit()
        print(f"   ✅ {len(civilizaciones)} civilizaciones")

    # Verificar tablas
    print("\n" + "=" * 70)
    print("VERIFICACIÓN FINAL")
    print("=" * 70)

    db.cursor.execute("""
        SELECT tablename FROM pg_tables
        WHERE schemaname = 'public'
        ORDER BY tablename
    """)

    tablas = db.cursor.fetchall()
    print(f"\n✅ TOTAL TABLAS CREADAS: {len(tablas)}\n")

    # Mostrar todas las tablas en columnas
    for i, tabla in enumerate(tablas, 1):
        nombre = tabla['tablename'] if isinstance(tabla, dict) else tabla[0]
        print(f"   {i:2d}. {nombre}")

    db.close()

    print("\n" + "=" * 70)
    print("✅ TODAS LAS TABLAS LISTAS")
    print("=" * 70)
    print("\n🚀 Ahora ejecuta:")
    print("  python run_with_env.py simulacion_mundo_completo.py\n")


if __name__ == '__main__':
    main()
