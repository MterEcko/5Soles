#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Poblar Relaciones Especies-Civilizaciones-Dioses
Portales del Quinto Sol
"""

import sqlite3
import json

DB_PATH = 'quinto_sol.db'

def aplicar_schema():
    """Aplicar schema de relaciones"""
    print("📋 Aplicando schema de relaciones...")
    conn = sqlite3.connect(DB_PATH)

    with open('schema_relaciones_especies_civilizaciones.sql', 'r', encoding='utf-8') as f:
        schema_sql = f.read()

    conn.executescript(schema_sql)
    conn.commit()
    conn.close()
    print("✅ Schema aplicado")

def obtener_ids(conn):
    """Obtener IDs de especies, civilizaciones y dioses"""
    cursor = conn.cursor()

    # Especies
    cursor.execute("SELECT id, nombre FROM especies")
    especies = {nombre: id for id, nombre in cursor.fetchall()}

    # Civilizaciones
    cursor.execute("SELECT id, nombre FROM civilizaciones")
    civilizaciones = {nombre: id for id, nombre in cursor.fetchall()}

    # Dioses
    cursor.execute("SELECT id, nombre FROM dioses")
    dioses = {nombre: id for id, nombre in cursor.fetchall()}

    return especies, civilizaciones, dioses

def poblar_relaciones_iniciales(conn):
    """Poblar relaciones iniciales (año 1500)"""
    print("\n🔗 Poblando relaciones especies-civilizaciones-dioses...")

    especies, civilizaciones, dioses = obtener_ids(conn)
    cursor = conn.cursor()

    # MAPEO SEGÚN CIVILIZACIONES EXISTENTES:
    # Tlacatl de Luz → Quetzalcóatl → Toltecas del Viento
    # Sombra-Coyotes → Tezcatlipoca → Purépecha del Fuego (sombras nocturnas)
    # Bio-Constructores → Centéotl (agricultura) → Zapotecas del Eco (bio-ingenieros)
    # Acuátiles → Tláloc → Mayas Celeste (costas, cenotes)
    # Guerreros Solares → Huitzilopochtli → Mexica de Obsidiana

    relaciones = [
        # (especie, civilización, dios, tipo_relación, devoción, confianza, comercio_bonus, diplomacia_bonus, puede_residir, puede_comerciar, puede_casarse)

        # TLACATL DE LUZ - QUETZALCÓATL - TOLTECAS DEL VIENTO
        (especies.get('Tlacatl de Luz'), civilizaciones.get('Toltecas del Viento'), dioses.get('Quetzalcóatl'),
         'sirviente_directo', 95, 90, 20, 30, 1, 1, 1),

        # Tlacatl de Luz también tienen buena relación con otras civilizaciones (son diplomáticos)
        (especies.get('Tlacatl de Luz'), civilizaciones.get('Mayas Celeste'), dioses.get('Quetzalcóatl'),
         'aliado', 70, 75, 10, 20, 1, 1, 0),

        # SOMBRA-COYOTES - TEZCATLIPOCA - PURÉPECHA DEL FUEGO
        (especies.get('Sombra-Coyotes'), civilizaciones.get('Purépecha del Fuego'), dioses.get('Tezcatlipoca'),
         'sirviente_directo', 90, 85, 15, 15, 1, 1, 1),

        # Sombra-Coyotes son vistos con desconfianza por otras civilizaciones
        (especies.get('Sombra-Coyotes'), civilizaciones.get('Toltecas del Viento'), dioses.get('Tezcatlipoca'),
         'neutral', 40, 35, 0, 0, 0, 1, 0),

        # BIO-CONSTRUCTORES - CENTÉOTL - ZAPOTECAS DEL ECO
        (especies.get('Bio-Constructores'), civilizaciones.get('Zapotecas del Eco'), dioses.get('Centéotl'),
         'sirviente_directo', 92, 88, 25, 20, 1, 1, 1),

        # Bio-Constructores son bienvenidos en civilizaciones de naturaleza
        (especies.get('Bio-Constructores'), civilizaciones.get('Mayas Celeste'), dioses.get('Centéotl'),
         'aliado', 75, 80, 15, 15, 1, 1, 0),

        # ACUÁTILES - TLÁLOC - MAYAS CELESTE
        (especies.get('Acuátiles'), civilizaciones.get('Mayas Celeste'), dioses.get('Tláloc'),
         'sirviente_directo', 93, 87, 20, 25, 1, 1, 1),

        # Acuátiles también con Zapotecas (valles con agua)
        (especies.get('Acuátiles'), civilizaciones.get('Zapotecas del Eco'), dioses.get('Tláloc'),
         'aliado', 68, 70, 12, 10, 1, 1, 0),

        # GUERREROS SOLARES - HUITZILOPOCHTLI - MEXICA DE OBSIDIANA
        (especies.get('Guerreros Solares'), civilizaciones.get('Mexica de Obsidiana'), dioses.get('Huitzilopochtli'),
         'sirviente_directo', 98, 95, 15, 10, 1, 1, 1),

        # Guerreros Solares son respetados pero temidos
        (especies.get('Guerreros Solares'), civilizaciones.get('Purépecha del Fuego'), dioses.get('Huitzilopochtli'),
         'neutral', 45, 40, 5, 5, 0, 1, 0),

        # HUMANOS I (NPCs) - TODAS LAS CIVILIZACIONES
        (especies.get('Humanos I'), civilizaciones.get('Toltecas del Viento'), None,
         'adorador', 80, 95, 0, 0, 1, 1, 1),
        (especies.get('Humanos I'), civilizaciones.get('Mayas Celeste'), None,
         'adorador', 80, 95, 0, 0, 1, 1, 1),
        (especies.get('Humanos I'), civilizaciones.get('Zapotecas del Eco'), None,
         'adorador', 80, 95, 0, 0, 1, 1, 1),
        (especies.get('Humanos I'), civilizaciones.get('Mexica de Obsidiana'), None,
         'adorador', 80, 95, 0, 0, 1, 1, 1),
        (especies.get('Humanos I'), civilizaciones.get('Purépecha del Fuego'), None,
         'adorador', 80, 95, 0, 0, 1, 1, 1),
    ]

    for rel in relaciones:
        especie_id, civ_id, dios_id, tipo, dev, conf, com, dip, resid, comerc, casa = rel

        if especie_id and civ_id:  # Solo insertar si existen
            cursor.execute("""
                INSERT INTO especies_civilizaciones (
                    especie_id, civilizacion_id, dios_patron_id,
                    tipo_relacion, nivel_devocion, nivel_confianza,
                    bonificacion_comercio, bonificacion_diplomacia,
                    puede_residir, puede_comerciar, puede_casarse,
                    año_inicio_relacion
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1500)
            """, (especie_id, civ_id, dios_id, tipo, dev, conf, com, dip, resid, comerc, casa))

    conn.commit()
    print(f"✅ {len(relaciones)} relaciones iniciales creadas")

def poblar_diplomacia_inicial(conn):
    """Poblar estado diplomático inicial entre especies"""
    print("\n🤝 Poblando diplomacia entre especies...")

    especies, _, _ = obtener_ids(conn)
    cursor = conn.cursor()

    # Relaciones iniciales entre especies (año 1500)
    # nivel: -100 (guerra total) a +100 (aliados perfectos)
    diplomacia = [
        # (especie1, especie2, nivel_relacion, estado)

        # Tlacatl de Luz (diplomáticos) - Buenas relaciones con todos
        ('Tlacatl de Luz', 'Bio-Constructores', 75, 'aliado'),
        ('Tlacatl de Luz', 'Acuátiles', 65, 'amistoso'),
        ('Tlacatl de Luz', 'Guerreros Solares', 50, 'amistoso'),
        ('Tlacatl de Luz', 'Sombra-Coyotes', 40, 'neutral'),
        ('Tlacatl de Luz', 'Humanos I', 70, 'amistoso'),

        # Sombra-Coyotes (solitarios) - Relaciones tensas
        ('Sombra-Coyotes', 'Bio-Constructores', 25, 'neutral'),
        ('Sombra-Coyotes', 'Acuátiles', 20, 'neutral'),
        ('Sombra-Coyotes', 'Guerreros Solares', -20, 'hostil'),
        ('Sombra-Coyotes', 'Humanos I', 30, 'neutral'),

        # Bio-Constructores (pacíficos) - Buenas relaciones
        ('Bio-Constructores', 'Acuátiles', 70, 'aliado'),
        ('Bio-Constructores', 'Guerreros Solares', 35, 'neutral'),
        ('Bio-Constructores', 'Humanos I', 75, 'amistoso'),

        # Acuátiles (comerciantes) - Relaciones comerciales
        ('Acuátiles', 'Guerreros Solares', 45, 'amistoso'),
        ('Acuátiles', 'Humanos I', 68, 'amistoso'),

        # Guerreros Solares (belicosos) - Relaciones competitivas
        ('Guerreros Solares', 'Humanos I', 40, 'neutral'),
    ]

    for esp1_nombre, esp2_nombre, nivel, estado in diplomacia:
        esp1_id = especies.get(esp1_nombre)
        esp2_id = especies.get(esp2_nombre)

        if esp1_id and esp2_id:
            # Insertar en ambas direcciones
            cursor.execute("""
                INSERT OR REPLACE INTO diplomacia_especies (
                    especie_id, especie_objetivo_id, nivel_relacion,
                    estado_diplomatico, ultimo_cambio_año, ultimo_evento
                ) VALUES (?, ?, ?, ?, 1500, 'Relación inicial establecida')
            """, (esp1_id, esp2_id, nivel, estado))

            cursor.execute("""
                INSERT OR REPLACE INTO diplomacia_especies (
                    especie_id, especie_objetivo_id, nivel_relacion,
                    estado_diplomatico, ultimo_cambio_año, ultimo_evento
                ) VALUES (?, ?, ?, ?, 1500, 'Relación inicial establecida')
            """, (esp2_id, esp1_id, nivel, estado))

    conn.commit()
    print(f"✅ {len(diplomacia)} relaciones diplomáticas creadas")

def poblar_tratados_iniciales(conn):
    """Poblar tratados iniciales entre especies"""
    print("\n📜 Poblando tratados iniciales...")

    especies, _, _ = obtener_ids(conn)
    cursor = conn.cursor()

    tratados = [
        # (especie1, especie2, tipo, año, términos, firmante1, firmante2)

        ('Tlacatl de Luz', 'Bio-Constructores', 'alianza', 1480,
         json.dumps({
             'proposito': 'Alianza de Sabiduría y Naturaleza',
             'terminos': [
                 'Intercambio libre de conocimientos',
                 'Ayuda mutua en agricultura y educación',
                 'Defensa conjunta si alguno es atacado'
             ],
             'duracion': 'indefinida'
         }),
         'Sabio Coatl', 'Guardián Yaaxil'),

        ('Bio-Constructores', 'Acuátiles', 'comercio', 1485,
         json.dumps({
             'proposito': 'Tratado Comercial Agua-Tierra',
             'terminos': [
                 'Intercambio de productos agrícolas por pescado',
                 'Construcción conjunta de canales de riego',
                 'Aranceles reducidos 20%'
             ],
             'duracion': '50 años'
         }),
         'Guardián Chimal', 'Navegante Atl'),

        ('Tlacatl de Luz', 'Acuátiles', 'no_agresion', 1475,
         json.dumps({
             'proposito': 'Pacto de No Agresión',
             'terminos': [
                 'No atacar territorios del otro',
                 'Libre tránsito de embajadores',
                 'Resolución pacífica de conflictos'
             ],
             'duracion': 'indefinida'
         }),
         'Sabio Quetzal', 'Guardián de las Aguas'),
    ]

    for trat in tratados:
        esp1_nombre, esp2_nombre, tipo, año, terminos, firm1, firm2 = trat
        esp1_id = especies.get(esp1_nombre)
        esp2_id = especies.get(esp2_nombre)

        if esp1_id and esp2_id:
            # Asegurar que esp1_id < esp2_id
            if esp1_id > esp2_id:
                esp1_id, esp2_id = esp2_id, esp1_id
                firm1, firm2 = firm2, firm1

            cursor.execute("""
                INSERT INTO tratados_especies (
                    especie_1_id, especie_2_id, tipo_tratado,
                    año_firma, terminos,
                    firmado_por_especie_1, firmado_por_especie_2,
                    estado
                ) VALUES (?, ?, ?, ?, ?, ?, ?, 'activo')
            """, (esp1_id, esp2_id, tipo, año, terminos, firm1, firm2))

    conn.commit()
    print(f"✅ {len(tratados)} tratados iniciales creados")

def main():
    """Función principal"""
    print("=" * 70)
    print("POBLAR RELACIONES ESPECIES-CIVILIZACIONES-DIOSES")
    print("Portales del Quinto Sol")
    print("=" * 70)

    # Aplicar schema
    aplicar_schema()

    # Poblar datos
    conn = sqlite3.connect(DB_PATH)

    poblar_relaciones_iniciales(conn)
    poblar_diplomacia_inicial(conn)
    poblar_tratados_iniciales(conn)

    # Resumen
    print("\n" + "=" * 70)
    print("✅ RELACIONES COMPLETADAS")
    print("=" * 70)

    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM especies_civilizaciones")
    total_rel = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM diplomacia_especies")
    total_dip = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tratados_especies")
    total_trat = cursor.fetchone()[0]

    print(f"\n📊 RESUMEN:")
    print(f"   - Relaciones especies-civilizaciones: {total_rel}")
    print(f"   - Relaciones diplomáticas: {total_dip}")
    print(f"   - Tratados activos: {total_trat}")

    # Mostrar algunas relaciones
    print(f"\n🔗 RELACIONES SIRVIENTES DIRECTOS:")
    cursor.execute("""
        SELECT e.nombre, c.nombre, d.nombre, ec.nivel_devocion
        FROM especies_civilizaciones ec
        JOIN especies e ON ec.especie_id = e.id
        JOIN civilizaciones c ON ec.civilizacion_id = c.id
        LEFT JOIN dioses d ON ec.dios_patron_id = d.id
        WHERE ec.tipo_relacion = 'sirviente_directo'
        ORDER BY ec.nivel_devocion DESC
    """)
    for esp, civ, dios, dev in cursor.fetchall():
        print(f"   {esp:20s} → {civ:15s} (Dios: {dios or 'N/A':20s}) Devoción: {dev}%")

    conn.close()

if __name__ == '__main__':
    main()
