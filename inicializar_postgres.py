#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inicializa PostgreSQL con todos los esquemas y datos base
Portales del Quinto Sol

Ejecutar con: python run_with_env.py inicializar_postgres.py
"""

import os
import sys
from pathlib import Path
from database_connector import DatabaseConnector

def ejecutar_archivo_sql(db, archivo_sql):
    """Ejecuta un archivo SQL completo"""
    print(f"\n📄 Ejecutando: {archivo_sql}")

    if not Path(archivo_sql).exists():
        print(f"   ⚠️  Archivo no encontrado: {archivo_sql}")
        return False

    with open(archivo_sql, 'r', encoding='utf-8') as f:
        sql_content = f.read()

    try:
        # Dividir en statements individuales
        statements = sql_content.split(';')

        for i, statement in enumerate(statements, 1):
            statement = statement.strip()
            if not statement:
                continue

            # Ejecutar statement
            db.cursor.execute(statement)

        db.conn.commit()
        print(f"   ✅ {archivo_sql} ejecutado correctamente")
        return True

    except Exception as e:
        print(f"   ❌ Error en {archivo_sql}: {e}")
        db.conn.rollback()
        return False


def poblar_datos_base(db):
    """Inserta datos base (eras, especies, dioses, civilizaciones)"""
    print("\n" + "=" * 70)
    print("POBLANDO DATOS BASE")
    print("=" * 70)

    # 1. ERAS
    print("\n📋 Insertando Eras...")
    eras = [
        ('Era Alpha', 'La Primera Era - Llegada por los Portales. Los 40 humanos originales llegan a Aztlán Prime. Muchos murieron cuando el portal colapsó antes de tiempo.', 1500, 1650, False),
        ('Era de la Fundación', 'Establecimiento de las primeras aldeas y aceptación de los dioses como guías.', 1651, 1800, False),
        ('Era del Despertar', 'Las primeras generaciones nacidas en Aztlán Prime comienzan a desarrollar habilidades únicas.', 1801, 2000, False),
        ('Era de la Expansión', 'Crecimiento de ciudades y desarrollo de la tecnología simbólica.', 2001, 2200, False),
        ('Era del Cataclismo', 'La Tierra colapsa en el siglo XXIII. Los Humanos II llegan a Aztlán Prime.', 2201, 2400, False),
        ('Era del Conflicto', 'Tensiones entre Humanos I y Humanos II. Guerras por recursos y territorio.', 2401, 2700, False),
        ('Era de la Síntesis', 'Integración gradual de ambas humanidades y florecimiento cultural.', 2701, 3000, True),
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
        ('Quetzalcóatl', 'Sabiduría, Viento, Conocimiento', 'Mexica,Maya,Tolteca', 'Positiva', 'Educación y Astronomía', 'Serpiente Emplumada, dios creador y civilizador'),
        ('Tezcatlipoca', 'Destino, Noche, Hechicería', 'Mexica', 'Negativa', 'Magia y Guerra', 'El Espejo Humeante, señor del cielo y la tierra'),
        ('Tláloc', 'Lluvia, Agua, Fertilidad', 'Mexica,Totonaca', 'Neutral', 'Agricultura y Clima', 'Dios de la lluvia y las tormentas'),
        ('Huitzilopochtli', 'Guerra, Sol, Sacrificio', 'Mexica', 'Neutral', 'Armas y Estrategia', 'Colibrí del Sur, dios solar de los mexicas'),
        ('Chaac', 'Lluvia, Relámpago', 'Maya', 'Positiva', 'Agricultura', 'Dios maya de la lluvia y las tormentas'),
        ('Kukulkán', 'Viento, Conocimiento', 'Maya', 'Positiva', 'Arquitectura', 'Equivalente maya de Quetzalcóatl'),
        ('Itzamná', 'Cielo, Día, Noche', 'Maya', 'Positiva', 'Escritura y Calendario', 'Dios creador maya del conocimiento'),
        ('Xipe Tótec', 'Renovación, Primavera', 'Mexica,Zapoteca', 'Neutral', 'Agricultura', 'Nuestro Señor el Desollado'),
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

    # Obtener IDs de dioses para referencias
    db.cursor.execute("SELECT id, nombre FROM dioses")
    dioses_dict = {row[1]: row[0] for row in db.cursor.fetchall()}

    especies = [
        ('Humanos I', 'Primera oleada de humanos llegados por los portales en 1500', 'humano', 70, 90, 4, 7, None),
        ('Humanos II', 'Segunda oleada llegada tras el colapso de la Tierra (2201)', 'humano', 75, 95, 3, 6, None),
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
    civilizaciones = [
        ('Mexica de Obsidiana', 'Mexica de Obsidiana', dioses_dict.get('Huitzilopochtli'),
         'Civilización guerrera y tecnológica', 1520),
        ('Mayas Celeste', 'Mayas Celeste', dioses_dict.get('Kukulkán'),
         'Civilización de astrónomos y arquitectos', 1515),
        ('Olmeca Primordial', 'Olmeca Primordial', dioses_dict.get('Quetzalcóatl'),
         'La civilización más antigua', 1500),
        ('Zapoteca Montaña', 'Zapoteca Montaña', dioses_dict.get('Xipe Tótec'),
         'Maestros de las montañas', 1530),
    ]

    for civ in civilizaciones:
        db.cursor.execute('''
            INSERT INTO civilizaciones (nombre, tipo, dios_patron_id, descripcion, año_fundacion)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (nombre) DO NOTHING
        ''', civ)

    db.conn.commit()
    print(f"   ✅ {len(civilizaciones)} civilizaciones insertadas")

    # 5. PUEBLOS Y CIUDADES (muestra)
    print("\n📋 Insertando Pueblos y Ciudades...")
    db.cursor.execute("SELECT id, nombre FROM civilizaciones")
    civs_dict = {row[1]: row[0] for row in db.cursor.fetchall()}

    ciudades = [
        ('Tenochtitlán', 'capital', civs_dict.get('Mexica de Obsidiana'), 50000, 50, 1521, None, 0, 0,
         'Gran capital mexica construida sobre el lago'),
        ('Chichén Itzá', 'ciudad', civs_dict.get('Mayas Celeste'), 20000, 40, 1516, None, 100, 50,
         'Gran ciudad maya del conocimiento'),
        ('Monte Albán', 'ciudad', civs_dict.get('Zapoteca Montaña'), 15000, 35, 1531, None, -50, 80,
         'Ciudad en las montañas zapotecas'),
        ('La Venta', 'ciudad', civs_dict.get('Olmeca Primordial'), 8000, 30, 1505, None, -100, -50,
         'Ciudad olmeca primordial'),
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

    print("\n✅ Datos base poblados correctamente")


def main():
    """Función principal"""
    print("\n" + "=" * 70)
    print("INICIALIZACIÓN DE POSTGRESQL - PORTALES DEL QUINTO SOL")
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

    # Lista de archivos SQL a ejecutar
    archivos_sql = [
        'schema_postgres.sql',                               # Schema principal
        'schema_sistemas_completos.sql',                     # Sistemas completos
        'schema_extension_ia.sql',                           # Extensión IA
        'schema_especies_fauna.sql',                         # Fauna
        'schema_flora.sql',                                  # Flora
        'schema_relaciones_especies_civilizaciones.sql',     # Relaciones
        'schema_guerras_especies.sql',                       # Guerras
        'schema_mutaciones.sql',                             # Mutaciones
        'schema_matrimonios_interespecie.sql',               # Matrimonios
        'schema_artefactos_organizaciones_eventos.sql',      # Artefactos
        'schema_migraciones_justicia_clima_economia.sql',   # Migraciones
    ]

    print("\n" + "=" * 70)
    print("EJECUTANDO ARCHIVOS SQL")
    print("=" * 70)

    # Ejecutar cada archivo
    errores = []
    for archivo in archivos_sql:
        if not ejecutar_archivo_sql(db, archivo):
            errores.append(archivo)

    if errores:
        print(f"\n⚠️  {len(errores)} archivos con errores:")
        for err in errores:
            print(f"   - {err}")

    # Poblar datos base
    poblar_datos_base(db)

    # Verificar tablas creadas
    print("\n" + "=" * 70)
    print("VERIFICACIÓN FINAL")
    print("=" * 70)

    db.cursor.execute("""
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public'
        ORDER BY tablename
    """)

    tablas = db.cursor.fetchall()
    print(f"\n✅ Total de tablas creadas: {len(tablas)}")
    print("\nPrimeras 20 tablas:")
    for i, tabla in enumerate(tablas[:20], 1):
        print(f"   {i:2d}. {tabla[0]}")

    if len(tablas) > 20:
        print(f"   ... y {len(tablas) - 20} más")

    # Cerrar conexión
    db.close()

    print("\n" + "=" * 70)
    print("✅ INICIALIZACIÓN COMPLETADA")
    print("=" * 70)
    print("\nAhora puedes ejecutar:")
    print("  python run_with_env.py simulacion_mundo_completo.py")
    print()


if __name__ == '__main__':
    main()
