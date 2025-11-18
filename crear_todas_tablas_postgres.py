#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Crea TODAS las tablas PostgreSQL con conversión mejorada SQLite→PostgreSQL

Ejecutar con: python run_with_env.py crear_todas_tablas_postgres.py
"""

import os
import sys
import re
from pathlib import Path
from database_connector import DatabaseConnector


def convertir_sqlite_a_postgres_avanzado(sql_content):
    """Conversión completa y robusta de SQLite a PostgreSQL"""

    # 1. AUTOINCREMENT → SERIAL
    sql_content = sql_content.replace('INTEGER PRIMARY KEY AUTOINCREMENT', 'SERIAL PRIMARY KEY')
    sql_content = re.sub(r'\sAUTOINCREMENT\b', '', sql_content, flags=re.IGNORECASE)

    # 2. Boolean: DEFAULT 0/1 → FALSE/TRUE (solo para columnas BOOLEAN)
    sql_content = re.sub(r'\bBOOLEAN\s+DEFAULT\s+0\b', 'BOOLEAN DEFAULT FALSE', sql_content, flags=re.IGNORECASE)
    sql_content = re.sub(r'\bBOOLEAN\s+DEFAULT\s+1\b', 'BOOLEAN DEFAULT TRUE', sql_content, flags=re.IGNORECASE)

    # 3. DATETIME → TIMESTAMP
    sql_content = sql_content.replace('DATETIME DEFAULT CURRENT_TIMESTAMP', 'TIMESTAMP DEFAULT CURRENT_TIMESTAMP')
    sql_content = sql_content.replace('DATETIME', 'TIMESTAMP')

    # 4. Índices con condiciones boolean: WHERE columna = 1 → WHERE columna = TRUE
    # Buscar patrones como: WHERE es_heredable = 1, WHERE activa = 1, etc.
    sql_content = re.sub(
        r'WHERE\s+(\w+)\s*=\s*1(?=\s|;|\)|$)',
        r'WHERE \1 = TRUE',
        sql_content,
        flags=re.IGNORECASE
    )
    sql_content = re.sub(
        r'WHERE\s+(\w+)\s*=\s*0(?=\s|;|\)|$)',
        r'WHERE \1 = FALSE',
        sql_content,
        flags=re.IGNORECASE
    )

    # 5. CREATE VIEW IF NOT EXISTS → CREATE OR REPLACE VIEW
    sql_content = re.sub(
        r'CREATE\s+VIEW\s+IF\s+NOT\s+EXISTS\s+',
        'CREATE OR REPLACE VIEW ',
        sql_content,
        flags=re.IGNORECASE
    )

    # 6. Eliminar comentarios que pueden causar problemas
    # (Mantener solo comentarios de línea simples)

    return sql_content


def limpiar_base_datos_completo(db):
    """Limpieza completa: extensiones, funciones, tablas"""
    print("\n🧹 Limpiando base de datos completamente...")

    try:
        # 1. Eliminar todas las tablas en cascada
        print("   🗑️  Eliminando tablas...")
        db.cursor.execute("""
            DO $$ DECLARE
                r RECORD;
            BEGIN
                FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                    EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
                END LOOP;
            END $$;
        """)

        # 2. Eliminar todas las vistas
        print("   🗑️  Eliminando vistas...")
        db.cursor.execute("""
            DO $$ DECLARE
                r RECORD;
            BEGIN
                FOR r IN (SELECT table_name FROM information_schema.views WHERE table_schema = 'public') LOOP
                    EXECUTE 'DROP VIEW IF EXISTS ' || quote_ident(r.table_name) || ' CASCADE';
                END LOOP;
            END $$;
        """)

        # 3. Eliminar funciones (excepto las de extensiones)
        print("   🗑️  Eliminando funciones personalizadas...")
        db.cursor.execute("""
            DO $$ DECLARE
                r RECORD;
            BEGIN
                FOR r IN (
                    SELECT p.proname, pg_get_function_identity_arguments(p.oid) as args
                    FROM pg_proc p
                    INNER JOIN pg_namespace n ON p.pronamespace = n.oid
                    LEFT JOIN pg_depend d ON d.objid = p.oid AND d.deptype = 'e'
                    WHERE n.nspname = 'public' AND d.objid IS NULL
                ) LOOP
                    EXECUTE 'DROP FUNCTION IF EXISTS ' || quote_ident(r.proname) || '(' || r.args || ') CASCADE';
                END LOOP;
            END $$;
        """)

        # 4. Eliminar triggers
        print("   🗑️  Eliminando triggers...")
        db.cursor.execute("""
            DO $$ DECLARE
                r RECORD;
            BEGIN
                FOR r IN (
                    SELECT trigger_name, event_object_table
                    FROM information_schema.triggers
                    WHERE trigger_schema = 'public'
                ) LOOP
                    EXECUTE 'DROP TRIGGER IF EXISTS ' || quote_ident(r.trigger_name) ||
                            ' ON ' || quote_ident(r.event_object_table) || ' CASCADE';
                END LOOP;
            END $$;
        """)

        db.conn.commit()
        print("   ✅ Base de datos limpiada completamente")
        return True

    except Exception as e:
        print(f"   ⚠️  Error limpiando: {e}")
        db.conn.rollback()
        return False


def ejecutar_sql_mejorado(db, archivo_sql):
    """Ejecuta SQL con manejo robusto de statements"""
    print(f"\n📄 Procesando: {archivo_sql}")

    if not Path(archivo_sql).exists():
        print(f"   ⚠️  Archivo no encontrado")
        return False

    with open(archivo_sql, 'r', encoding='utf-8') as f:
        sql_content = f.read()

    # Convertir SQLite → PostgreSQL
    if 'postgres' not in archivo_sql.lower():
        sql_content = convertir_sqlite_a_postgres_avanzado(sql_content)

    try:
        # Para schema_postgres.sql, ejecutar completo (tiene funciones con $$)
        if 'postgres' in archivo_sql.lower():
            db.cursor.execute(sql_content)
            db.conn.commit()
            print(f"   ✅ Ejecutado correctamente")
            return True

        # Para otros archivos: dividir por ; y filtrar vacíos
        statements = []
        current_statement = []
        in_function = False

        for line in sql_content.split('\n'):
            line_stripped = line.strip()

            # Detectar inicio/fin de funciones ($$)
            if '$$' in line:
                in_function = not in_function

            current_statement.append(line)

            # Si encontramos ; y no estamos en función, es fin de statement
            if ';' in line and not in_function:
                stmt = '\n'.join(current_statement).strip()
                if stmt and len(stmt) > 5:  # Filtrar statements vacíos o muy cortos
                    statements.append(stmt)
                current_statement = []

        # Ejecutar cada statement
        executed = 0
        for stmt in statements:
            # Saltar comentarios puros
            if stmt.startswith('--') or stmt.startswith('/*'):
                continue

            try:
                db.cursor.execute(stmt)
                executed += 1
            except Exception as e:
                # Solo mostrar errores que no sean "can't execute empty query"
                if "empty query" not in str(e).lower():
                    print(f"   ⚠️  Error en statement: {str(e)[:100]}")

        db.conn.commit()

        if executed > 0:
            print(f"   ✅ {executed} statements ejecutados")
            return True
        else:
            print(f"   ⚠️  0 statements ejecutados")
            return False

    except Exception as e:
        print(f"   ❌ Error: {e}")
        db.conn.rollback()
        return False


def main():
    """Función principal"""
    print("\n" + "=" * 70)
    print("CREACIÓN COMPLETA DE TABLAS POSTGRESQL")
    print("=" * 70)

    # Verificar tipo de BD
    db_type = os.getenv('DB_TYPE', 'sqlite')
    if db_type != 'postgres':
        print("\n❌ ERROR: DB_TYPE debe ser 'postgres'")
        sys.exit(1)

    print(f"\n✅ Configuración PostgreSQL")
    print(f"   Host: {os.getenv('PG_HOST')}")
    print(f"   Port: {os.getenv('PG_PORT')}")
    print(f"   Database: {os.getenv('PG_DATABASE')}")

    # Conectar
    db = DatabaseConnector()
    try:
        db.connect()
    except Exception as e:
        print(f"\n❌ Error de conexión: {e}")
        sys.exit(1)

    # Limpiar base de datos
    limpiar_base_datos_completo(db)

    # Lista completa de archivos SQL
    archivos_sql = [
        'schema_postgres.sql',                               # 1. Schema principal (17 tablas base)
        'schema_relaciones_especies_civilizaciones.sql',     # 2. Relaciones especies-civilizaciones
        'schema_guerras_especies.sql',                       # 3. Guerras inter-especies
        'schema_mutaciones.sql',                             # 4. Mutaciones
        'schema_matrimonios_interespecie.sql',               # 5. Matrimonios inter-especies
        'schema_artefactos_organizaciones_eventos.sql',      # 6. Artefactos y organizaciones
        'schema_migraciones_justicia_clima_economia.sql',   # 7. Sistemas adicionales
        'schema_especies_fauna.sql',                         # 8. Fauna
        'schema_flora.sql',                                  # 9. Flora
        'schema_sistemas_completos.sql',                     # 10. Sistemas completos
        'schema_extension_ia.sql',                           # 11. Extensión IA
    ]

    print("\n" + "=" * 70)
    print("EJECUTANDO SCHEMAS SQL")
    print("=" * 70)

    exitosos = 0
    fallidos = 0

    for archivo in archivos_sql:
        if ejecutar_sql_mejorado(db, archivo):
            exitosos += 1
        else:
            fallidos += 1

    print(f"\n📊 Resumen: {exitosos} exitosos, {fallidos} con errores")

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
        ('Era de la Expansión', 'Crecimiento ciudades', 2001, 2200, False),
        ('Era del Cataclismo', 'Llegada Humanos II', 2201, 2400, False),
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
        ('Tláloc', 'Lluvia', 'Mexica', 'Neutral', 'Agricultura', 'Dios lluvia'),
        ('Huitzilopochtli', 'Guerra', 'Mexica', 'Neutral', 'Guerra', 'Colibrí del Sur'),
        ('Chaac', 'Lluvia', 'Maya', 'Positiva', 'Agricultura', 'Dios maya lluvia'),
        ('Kukulkán', 'Viento', 'Maya', 'Positiva', 'Arquitectura', 'Serpiente emplumada maya'),
        ('Itzamná', 'Cielo', 'Maya', 'Positiva', 'Escritura', 'Dios creador'),
        ('Xipe Tótec', 'Renovación', 'Mexica,Zapoteca', 'Neutral', 'Agricultura', 'El Desollado'),
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
    dios_mexica = db.cursor.fetchone()['id']

    civilizaciones = [
        ('Mexica de Obsidiana', 'Mexica de Obsidiana', dios_mexica, 'Guerrera', 1520),
        ('Mayas Celeste', 'Mayas Celeste', dios_mexica, 'Astrónomos', 1515),
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
    print(f"\n✅ Total tablas creadas: {len(tablas)}")

    for i, tabla in enumerate(tablas, 1):
        nombre = tabla['tablename'] if isinstance(tabla, dict) else tabla[0]
        print(f"   {i:2d}. {nombre}")

    db.close()

    print("\n" + "=" * 70)
    print("✅ TODAS LAS TABLAS CREADAS")
    print("=" * 70)
    print("\nAhora ejecuta:")
    print("  python run_with_env.py simulacion_mundo_completo.py")
    print()


if __name__ == '__main__':
    main()
