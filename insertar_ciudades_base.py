#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inserta pueblos y ciudades base para las civilizaciones

Ejecutar con: python run_with_env.py insertar_ciudades_base.py
"""

from database_connector import DatabaseConnector

def main():
    print("\n" + "=" * 70)
    print("INSERTANDO CIUDADES BASE")
    print("=" * 70)

    db = DatabaseConnector()
    db.connect()

    # Obtener IDs de civilizaciones
    db.cursor.execute("SELECT id, nombre FROM civilizaciones")
    civs = {row['nombre']: row['id'] for row in db.cursor.fetchall()}

    print(f"\n📋 Civilizaciones encontradas: {len(civs)}")
    for nombre in civs.keys():
        print(f"   • {nombre}")

    if not civs:
        print("\n❌ No hay civilizaciones en la BD")
        print("   Ejecuta primero: python run_with_env.py extraer_crear_tablas.py")
        return

    # Ciudades base
    ciudades = []

    if 'Mexica de Obsidiana' in civs:
        ciudades.extend([
            ('Tenochtitlán', 'capital', civs['Mexica de Obsidiana'], 50000, 50, 1521, None, 0.0, 0.0, 'Gran capital mexica'),
            ('Tlatelolco', 'ciudad', civs['Mexica de Obsidiana'], 20000, 40, 1520, None, 0.5, 0.5, 'Ciudad comercial'),
            ('Texcoco', 'ciudad', civs['Mexica de Obsidiana'], 15000, 35, 1519, None, 1.0, 0.0, 'Ciudad cultural'),
        ])

    if 'Mayas Celeste' in civs:
        ciudades.extend([
            ('Chichén Itzá', 'ciudad', civs['Mayas Celeste'], 25000, 45, 1516, None, 100.0, 50.0, 'Ciudad maya del conocimiento'),
            ('Uxmal', 'ciudad', civs['Mayas Celeste'], 12000, 35, 1515, None, 95.0, 48.0, 'Ciudad maya'),
            ('Tulum', 'pueblo', civs['Mayas Celeste'], 8000, 30, 1518, None, 105.0, 52.0, 'Pueblo costero'),
        ])

    print(f"\n📄 Insertando {len(ciudades)} ciudades...")

    for ciudad in ciudades:
        try:
            db.cursor.execute('''
                INSERT INTO pueblos_ciudades
                (nombre, tipo, civilizacion_id, poblacion_aproximada, nivel_zona,
                 año_fundacion, año_destruccion, coordenadas_x, coordenadas_y, descripcion)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', ciudad)
            print(f"   ✅ {ciudad[0]} ({ciudad[1]})")
        except Exception as e:
            print(f"   ⚠️  {ciudad[0]}: {str(e)[:80]}")

    db.conn.commit()

    # Verificar
    db.cursor.execute("SELECT COUNT(*) FROM pueblos_ciudades")
    result = db.cursor.fetchone()
    total = result['count'] if isinstance(result, dict) else result[0]

    print(f"\n✅ Total ciudades en BD: {total}")

    db.close()

    print("\n" + "=" * 70)
    print("✅ CIUDADES BASE INSERTADAS")
    print("=" * 70)
    print("\nAhora ejecuta:")
    print("  python run_with_env.py generar_poblacion.py")
    print()


if __name__ == '__main__':
    main()
