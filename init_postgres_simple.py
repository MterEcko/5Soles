#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inicializa PostgreSQL - Versión Simplificada
Solo ejecuta schema_postgres.sql y pobla datos base

Ejecutar con: python run_with_env.py init_postgres_simple.py
"""

import os
import sys
from pathlib import Path
from database_connector import DatabaseConnector


def main():
    """Función principal"""
    print("\n" + "=" * 70)
    print("INICIALIZACIÓN POSTGRESQL - VERSIÓN SIMPLIFICADA")
    print("=" * 70)

    # Verificar tipo de BD
    db_type = os.getenv('DB_TYPE', 'sqlite')
    if db_type != 'postgres':
        print("\n❌ ERROR: DB_TYPE debe ser 'postgres'")
        print("   Verifica tu archivo .env")
        sys.exit(1)

    print(f"\n✅ DB_TYPE: {db_type}")
    print(f"   Host: {os.getenv('PG_HOST')}")
    print(f"   Port: {os.getenv('PG_PORT')}")
    print(f"   Database: {os.getenv('PG_DATABASE')}")
    print(f"   User: {os.getenv('PG_USER')}")

    # Conectar
    db = DatabaseConnector()
    try:
        db.connect()
    except Exception as e:
        print(f"\n❌ Error de conexión: {e}")
        sys.exit(1)

    # Ejecutar schema_postgres.sql
    print("\n📄 Ejecutando schema_postgres.sql...")
    schema_file = Path('schema_postgres.sql')

    if not schema_file.exists():
        print(f"❌ Archivo no encontrado: schema_postgres.sql")
        sys.exit(1)

    try:
        with open(schema_file, 'r', encoding='utf-8') as f:
            sql_content = f.read()

        # Ejecutar todo el contenido (incluye funciones con $$)
        db.cursor.execute(sql_content)
        db.conn.commit()
        print("✅ Schema PostgreSQL ejecutado correctamente")

    except Exception as e:
        print(f"❌ Error ejecutando schema: {e}")
        db.conn.rollback()
        sys.exit(1)

    # Poblar datos base
    print("\n" + "=" * 70)
    print("POBLANDO DATOS BASE")
    print("=" * 70)

    # 1. ERAS
    print("\n📋 Insertando Eras...")
    eras = [
        ('Era Alpha', 'La Primera Era - Llegada por los Portales.', 1500, 1650, False),
        ('Era de la Fundación', 'Establecimiento de las primeras aldeas.', 1651, 1800, False),
        ('Era del Despertar', 'Desarrollo de habilidades únicas.', 1801, 2000, False),
        ('Era de la Expansión', 'Crecimiento de ciudades.', 2001, 2200, False),
        ('Era del Cataclismo', 'Llegada de Humanos II.', 2201, 2400, False),
        ('Era del Conflicto', 'Tensiones entre humanidades.', 2401, 2700, False),
        ('Era de la Síntesis', 'Integración y florecimiento.', 2701, 3000, True),
    ]

    for era in eras:
        db.cursor.execute('''
            INSERT INTO eras (nombre, descripcion, año_inicio, año_fin, es_actual)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (nombre) DO NOTHING
        ''', era)

    db.conn.commit()
    print(f"   ✅ {len(eras)} eras insertadas")

    # 2. DIOSES
    print("\n📋 Insertando Dioses...")
    dioses = [
        ('Quetzalcóatl', 'Sabiduría, Viento', 'Mexica,Maya', 'Positiva', 'Educación', 'Serpiente Emplumada'),
        ('Tezcatlipoca', 'Destino, Noche', 'Mexica', 'Negativa', 'Magia', 'Espejo Humeante'),
        ('Tláloc', 'Lluvia, Agua', 'Mexica', 'Neutral', 'Agricultura', 'Dios de la lluvia'),
        ('Huitzilopochtli', 'Guerra, Sol', 'Mexica', 'Neutral', 'Guerra', 'Colibrí del Sur'),
        ('Chaac', 'Lluvia', 'Maya', 'Positiva', 'Agricultura', 'Dios maya lluvia'),
        ('Kukulkán', 'Viento', 'Maya', 'Positiva', 'Arquitectura', 'Equivalente Quetzalcóatl'),
        ('Itzamná', 'Cielo', 'Maya', 'Positiva', 'Escritura', 'Dios creador maya'),
        ('Xipe Tótec', 'Renovación', 'Mexica,Zapoteca', 'Neutral', 'Agricultura', 'El Desollado'),
    ]

    for dios in dioses:
        db.cursor.execute('''
            INSERT INTO dioses (nombre, dominio_principal, culturas, polaridad, eje_tecnologico, descripcion)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (nombre) DO NOTHING
        ''', dios)

    db.conn.commit()
    print(f"   ✅ {len(dioses)} dioses insertados")

    # 3. ESPECIES
    print("\n📋 Insertando Especies...")
    especies = [
        ('Humanos I', 'Primera oleada 1500', 'humano', 70, 90, 4, 7, None),
        ('Humanos II', 'Segunda oleada 2201', 'humano', 75, 95, 3, 6, None),
    ]

    for especie in especies:
        db.cursor.execute('''
            INSERT INTO especies (nombre, descripcion, tipo, esperanza_vida_min, esperanza_vida_max,
                                 hijos_min, hijos_max, dios_creador_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (nombre) DO NOTHING
        ''', especie)

    db.conn.commit()
    print(f"   ✅ {len(especies)} especies insertadas")

    # 4. CIVILIZACIONES
    print("\n📋 Insertando Civilizaciones...")
    db.cursor.execute("SELECT id FROM dioses WHERE nombre = 'Huitzilopochtli'")
    dios_mexica = db.cursor.fetchone()['id']

    db.cursor.execute("SELECT id FROM dioses WHERE nombre = 'Kukulkán'")
    dios_maya = db.cursor.fetchone()['id']

    civilizaciones = [
        ('Mexica de Obsidiana', 'Mexica de Obsidiana', dios_mexica, 'Guerrera y tecnológica', 1520),
        ('Mayas Celeste', 'Mayas Celeste', dios_maya, 'Astrónomos y arquitectos', 1515),
    ]

    for civ in civilizaciones:
        db.cursor.execute('''
            INSERT INTO civilizaciones (nombre, tipo, dios_patron_id, descripcion, año_fundacion)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (nombre) DO NOTHING
        ''', civ)

    db.conn.commit()
    print(f"   ✅ {len(civilizaciones)} civilizaciones insertadas")

    # 5. PUEBLOS
    print("\n📋 Insertando Ciudades...")
    db.cursor.execute("SELECT id FROM civilizaciones WHERE nombre = 'Mexica de Obsidiana'")
    civ_mexica = db.cursor.fetchone()['id']

    ciudades = [
        ('Tenochtitlán', 'capital', civ_mexica, 50000, 50, 1521, None, 0, 0, 'Capital mexica'),
        ('Chichén Itzá', 'ciudad', civ_mexica, 20000, 40, 1516, None, 100, 50, 'Ciudad maya'),
    ]

    for ciudad in ciudades:
        db.cursor.execute('''
            INSERT INTO pueblos_ciudades
            (nombre, tipo, civilizacion_id, poblacion_aproximada, nivel_zona,
             año_fundacion, año_destruccion, coordenadas_x, coordenadas_y, descripcion)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', ciudad)

    db.conn.commit()
    print(f"   ✅ {len(ciudades)} ciudades insertadas")

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
    print(f"\n✅ Total de tablas creadas: {len(tablas)}")

    # Cerrar
    db.close()

    print("\n✅ INICIALIZACIÓN COMPLETADA")
    print("\nAhora ejecuta:")
    print("  python run_with_env.py simulacion_mundo_completo.py")


if __name__ == '__main__':
    main()
