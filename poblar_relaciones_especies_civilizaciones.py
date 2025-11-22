#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Poblar Relaciones Especies-Civilizaciones-Dioses
Portales del Quinto Sol
ADAPTADO A POSTGRESQL (DatabaseConnector)
"""

import json
import re # Usaremos regex para adaptar el schema SQL
from database_connector import DatabaseConnector # Importación crítica

def aplicar_schema():
    """Aplicar schema de relaciones. Adaptado para PostgreSQL con ejecución robusta."""
    print("📋 Aplicando schema de relaciones...")
    
    db = DatabaseConnector()
    db.connect()

    try:
        # Asegúrate de que 'schema_relaciones_especies_civilizaciones.sql' exista.
        with open('schema_relaciones_especies_civilizaciones.sql', 'r', encoding='utf-8') as f:
            schema_sql = f.read()
    except FileNotFoundError:
        print("❌ Error: 'schema_relaciones_especies_civilizaciones.sql' no encontrado.")
        db.close()
        return

    # 1. Aplicar correcciones para PostgreSQL (SERIAL PRIMARY KEY y BOOLEAN)
    if db.db_type == 'postgres':
        # Corrección: Clave primaria (SQLite a PostgreSQL)
        schema_sql = schema_sql.replace('INTEGER PRIMARY KEY AUTOINCREMENT', 'SERIAL PRIMARY KEY')
        
        # Corrección: Valores booleanos (1/0 a TRUE/FALSE) en cláusulas DEFAULT
        schema_sql = re.sub(r'(BOOLEAN\s+DEFAULT\s+)0', r'\1FALSE', schema_sql, flags=re.IGNORECASE)
        schema_sql = re.sub(r'(BOOLEAN\s+DEFAULT\s+)1', r'\1TRUE', schema_sql, flags=re.IGNORECASE)

    # 2. Ejecutar comandos uno por uno (para evitar errores de consulta vacía)
    # Dividir por punto y coma, ignorando el ';' si es el último carácter
    commands = re.split(r';\s*$', schema_sql.strip(), flags=re.MULTILINE)
    
    try:
        for command in commands:
            # Eliminar comentarios de una línea (--) y limpiar espacios
            clean_command = re.sub(r'--.*', '', command, flags=re.MULTILINE).strip()
            
            if clean_command:
                db.cursor.execute(clean_command)
                
    except Exception as e:
        print(f"❌ Error al ejecutar el comando SQL en el schema:\n{clean_command}")
        print(f"Detalle del error: {e}")
        db.close()
        return

    db.commit()
    db.close()
    print("✅ Schema aplicado")

def obtener_ids(db):
    """Obtener IDs de especies, civilizaciones y dioses usando DatabaseConnector"""
    cursor = db.cursor

    # Especies
    cursor.execute("SELECT id, nombre FROM especies")
    especies = {row['nombre']: row['id'] for row in db.fetchall()}

    # Civilizaciones
    cursor.execute("SELECT id, nombre FROM civilizaciones")
    civilizaciones = {row['nombre']: row['id'] for row in db.fetchall()}

    # Dioses
    cursor.execute("SELECT id, nombre FROM dioses")
    dioses = {row['nombre']: row['id'] for row in db.fetchall()}

    return especies, civilizaciones, dioses

def poblar_relaciones_iniciales(db):
    """Poblar relaciones iniciales (año 1500)"""
    print("\n🔗 Poblando relaciones especies-civilizaciones-dioses...")

    especies, civilizaciones, dioses = obtener_ids(db)
    cursor = db.cursor

    # MAPEO SEGÚN CIVILIZACIONES EXISTENTES: (asumiendo que existen)
    relaciones = [
        # (especie, civilización, dios, tipo_relación, devoción, confianza, comercio_bonus, diplomacia_bonus, puede_residir, puede_comerciar, puede_casarse)

        # TLACATL DE LUZ - QUETZALCÓATL - TOLTECAS DEL VIENTO
        (especies.get('Tlacatl de Luz'), civilizaciones.get('Toltecas del Viento'), dioses.get('Quetzalcóatl'),
         'sirviente_directo', 95, 90, 20, 30, True, True, True),

        # Tlacatl de Luz también tienen buena relación con otras civilizaciones (son diplomáticos)
        (especies.get('Tlacatl de Luz'), civilizaciones.get('Mayas Celeste'), dioses.get('Quetzalcóatl'),
         'aliado', 70, 75, 10, 20, True, True, False),

        # SOMBRA-COYOTES - TEZCATLIPOCA - PURÉPECHA DEL FUEGO
        (especies.get('Sombra-Coyotes'), civilizaciones.get('Purépecha del Fuego'), dioses.get('Tezcatlipoca'),
         'sirviente_directo', 90, 85, 15, 15, True, True, True),

        # Sombra-Coyotes son vistos con desconfianza por otras civilizaciones
        (especies.get('Sombra-Coyotes'), civilizaciones.get('Toltecas del Viento'), dioses.get('Tezcatlipoca'),
         'neutral', 40, 35, 0, 0, False, True, False),

        # BIO-CONSTRUCTORES - CENTÉOTL - ZAPOTECAS DEL ECO
        (especies.get('Bio-Constructores'), civilizaciones.get('Zapotecas del Eco'), dioses.get('Centéotl'),
         'sirviente_directo', 92, 88, 25, 20, True, True, True),

        # Bio-Constructores son bienvenidos en civilizaciones de naturaleza
        (especies.get('Bio-Constructores'), civilizaciones.get('Mayas Celeste'), dioses.get('Centéotl'),
         'aliado', 75, 80, 15, 15, True, True, False),

        # ACUÁTILES - TLÁLOC - MAYAS CELESTE
        (especies.get('Acuátiles'), civilizaciones.get('Mayas Celeste'), dioses.get('Tláloc'),
         'sirviente_directo', 93, 87, 20, 25, True, True, True),

        # Acuátiles también con Zapotecas (valles con agua)
        (especies.get('Acuátiles'), civilizaciones.get('Zapotecas del Eco'), dioses.get('Tláloc'),
         'aliado', 68, 70, 12, 10, True, True, False),

        # GUERREROS SOLARES - HUITZILOPOCHTLI - MEXICA DE OBSIDIANA
        (especies.get('Guerreros Solares'), civilizaciones.get('Mexica de Obsidiana'), dioses.get('Huitzilopochtli'),
         'sirviente_directo', 98, 95, 15, 10, True, True, True),

        # Guerreros Solares son respetados pero temidos
        (especies.get('Guerreros Solares'), civilizaciones.get('Purépecha del Fuego'), dioses.get('Huitzilopochtli'),
         'neutral', 45, 40, 5, 5, False, True, False),

        # HUMANOS I (NPCs) - TODAS LAS CIVILIZACIONES
        (especies.get('Humanos I'), civilizaciones.get('Toltecas del Viento'), None,
         'adorador', 80, 95, 0, 0, True, True, True),
        (especies.get('Humanos I'), civilizaciones.get('Mayas Celeste'), None,
         'adorador', 80, 95, 0, 0, True, True, True),
        (especies.get('Humanos I'), civilizaciones.get('Zapotecas del Eco'), None,
         'adorador', 80, 95, 0, 0, True, True, True),
        (especies.get('Humanos I'), civilizaciones.get('Mexica de Obsidiana'), None,
         'adorador', 80, 95, 0, 0, True, True, True),
        (especies.get('Humanos I'), civilizaciones.get('Purépecha del Fuego'), None,
         'adorador', 80, 95, 0, 0, True, True, True),
    ]

    for rel in relaciones:
        especie_id, civ_id, dios_id, tipo, dev, conf, com, dip, resid, comerc, casa = rel

        if especie_id and civ_id:  # Solo insertar si existen
            # CORRECCIÓN CRÍTICA: Se añade 'año_inicio_relacion' al ON CONFLICT.
            cursor.execute("""
                INSERT INTO especies_civilizaciones (
                    especie_id, civilizacion_id, dios_patron_id,
                    tipo_relacion, nivel_devocion, nivel_confianza,
                    bonificacion_comercio, bonificacion_diplomacia,
                    puede_residir, puede_comerciar, puede_casarse,
                    año_inicio_relacion
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 1500)
                ON CONFLICT (especie_id, civilizacion_id, año_inicio_relacion) DO NOTHING
            """, (especie_id, civ_id, dios_id, tipo, dev, conf, com, dip, resid, comerc, casa))
            
    db.commit()
    print(f"✅ {len(relaciones)} relaciones iniciales creadas")

def poblar_diplomacia_inicial(db):
    """Poblar estado diplomático inicial entre especies"""
    print("\n🤝 Poblando diplomacia entre especies...")

    especies, _, _ = obtener_ids(db)
    cursor = db.cursor

    # Relaciones iniciales entre especies (año 1500)
    diplomacia = [
        # (especie1, especie2, nivel_relacion, estado)
        ('Tlacatl de Luz', 'Bio-Constructores', 75, 'aliado'),
        ('Tlacatl de Luz', 'Acuátiles', 65, 'amistoso'),
        ('Tlacatl de Luz', 'Guerreros Solares', 50, 'amistoso'),
        ('Tlacatl de Luz', 'Sombra-Coyotes', 40, 'neutral'),
        ('Tlacatl de Luz', 'Humanos I', 70, 'amistoso'),

        ('Sombra-Coyotes', 'Bio-Constructores', 25, 'neutral'),
        ('Sombra-Coyotes', 'Acuátiles', 20, 'neutral'),
        ('Sombra-Coyotes', 'Guerreros Solares', -20, 'hostil'),
        ('Sombra-Coyotes', 'Humanos I', 30, 'neutral'),

        ('Bio-Constructores', 'Acuátiles', 70, 'aliado'),
        ('Bio-Constructores', 'Guerreros Solares', 35, 'neutral'),
        ('Bio-Constructores', 'Humanos I', 75, 'amistoso'),

        ('Acuátiles', 'Guerreros Solares', 45, 'amistoso'),
        ('Acuátiles', 'Humanos I', 68, 'amistoso'),

        ('Guerreros Solares', 'Humanos I', 40, 'neutral'),
    ]

    for esp1_nombre, esp2_nombre, nivel, estado in diplomacia:
        esp1_id = especies.get(esp1_nombre)
        esp2_id = especies.get(esp2_nombre)

        if esp1_id and esp2_id:
            # Insertar en ambas direcciones (PostgreSQL: %s y ON CONFLICT DO UPDATE)
            for id1, id2 in [(esp1_id, esp2_id), (esp2_id, esp1_id)]:
                cursor.execute("""
                    INSERT INTO diplomacia_especies (
                        especie_id, especie_objetivo_id, nivel_relacion,
                        estado_diplomatico, ultimo_cambio_año, ultimo_evento
                    ) VALUES (%s, %s, %s, %s, 1500, 'Relación inicial establecida')
                    ON CONFLICT (especie_id, especie_objetivo_id) DO UPDATE
                    SET nivel_relacion = EXCLUDED.nivel_relacion,
                        estado_diplomatico = EXCLUDED.estado_diplomatico
                """, (id1, id2, nivel, estado))

    db.commit()
    print(f"✅ {len(diplomacia)} relaciones diplomáticas creadas")

def poblar_tratados_iniciales(db):
    """Poblar tratados iniciales entre especies"""
    print("\n📜 Poblando tratados iniciales...")

    especies, _, _ = obtener_ids(db)
    cursor = db.cursor

    tratados = [
        # ... (definición de tratados) ...
    ]

    for trat in tratados:
        esp1_nombre, esp2_nombre, tipo, año, terminos, firm1, firm2 = trat
        esp1_id = especies.get(esp1_nombre)
        esp2_id = especies.get(esp2_nombre)

        if esp1_id and esp2_id:
            # Asegurar que esp1_id < esp2_id para la clave única del tratado (y la restricción CHECK)
            if esp1_id > esp2_id:
                esp1_id, esp2_id = esp2_id, esp1_id
                firm1, firm2 = firm2, firm1

            # --- CORRECCIÓN CRÍTICA: Eliminamos ON CONFLICT ---
            cursor.execute("""
                INSERT INTO tratados_especies (
                    especie_1_id, especie_2_id, tipo_tratado,
                    año_firma, terminos,
                    firmado_por_especie_1, firmado_por_especie_2,
                    estado
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, 'activo')
                -- ON CONFLICT ELIMINADO AQUÍ
            """, (esp1_id, esp2_id, tipo, año, terminos, firm1, firm2))

    db.commit()
    print(f"✅ {len(tratados)} tratados iniciales creados")


def main():
    """Función principal"""
    print("=" * 70)
    print("POBLAR RELACIONES ESPECIES-CIVILIZACIONES-DIOSES")
    print("Portales del Quinto Sol")
    print("=" * 70)

    # 1. Aplicar schema (adaptado a PostgreSQL)
    aplicar_schema()

    # 2. Poblar datos
    db = DatabaseConnector()
    db.connect()

    poblar_relaciones_iniciales(db)
    poblar_diplomacia_inicial(db)
    poblar_tratados_iniciales(db)

    # 3. Resumen
    print("\n" + "=" * 70)
    print("✅ RELACIONES COMPLETADAS")
    print("=" * 70)

    cursor = db.cursor

    cursor.execute("SELECT COUNT(*) FROM especies_civilizaciones")
    total_rel = db.fetchone()['count']

    cursor.execute("SELECT COUNT(*) FROM diplomacia_especies")
    total_dip = db.fetchone()['count']

    cursor.execute("SELECT COUNT(*) FROM tratados_especies")
    total_trat = db.fetchone()['count']

    print(f"\n📊 RESUMEN:")
    print(f"   - Relaciones especies-civilizaciones: {total_rel}")
    print(f"   - Relaciones diplomáticas: {total_dip}")
    print(f"   - Tratados activos: {total_trat}")

    # Mostrar algunas relaciones
    print(f"\n🔗 RELACIONES SIRVIENTES DIRECTOS:")
    cursor.execute("""
        SELECT e.nombre, c.nombre AS civilizacion_nombre, d.nombre AS dios_nombre, ec.nivel_devocion
        FROM especies_civilizaciones ec
        JOIN especies e ON ec.especie_id = e.id
        JOIN civilizaciones c ON ec.civilizacion_id = c.id
        LEFT JOIN dioses d ON ec.dios_patron_id = d.id
        WHERE ec.tipo_relacion = 'sirviente_directo'
        ORDER BY ec.nivel_devocion DESC
    """)
    for row in db.fetchall():
        esp = row['nombre']
        civ = row['civilizacion_nombre']
        dios = row['dios_nombre']
        dev = row['nivel_devocion']
        print(f"   {esp:20s} → {civ:15s} (Dios: {dios or 'N/A':20s}) Devoción: {dev}%")

    db.close()

if __name__ == '__main__':
    # Inicializar la conexión y luego la cerraremos en main
    main()