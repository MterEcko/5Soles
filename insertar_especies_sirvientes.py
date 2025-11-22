from database_connector import DatabaseConnector

def insert_missing_species():
    """Inserta las 5 especies sirvientes faltantes en la BD."""
    db = DatabaseConnector()
    conn = db.connect()
    cursor = db.cursor

    # 1. Cargar IDs de Dioses (asumiendo que se insertaron 8)
    cursor.execute("SELECT id, nombre FROM dioses")
    dioses = {row['nombre']: row['id'] for row in db.fetchall()}

    # 2. Datos de las 5 especies sirvientes (basado en la documentación del proyecto)
    missing_species = [
        # (Nombre, Descripción, Tipo, Vida_min, Vida_max, Hijos_min, Hijos_max, Dios_ID)
        ('Tlacatl de Luz', 'Sirvientes humanoides de Quetzalcóatl, con piel luminiscente y alas vestigiales', 'sirviente_divino', 200, 300, 2, 4, dioses.get('Quetzalcóatl')),
        ('Sombra-Coyotes', 'Sirvientes metamórficos de Tezcatlipoca, pueden cambiar de forma', 'sirviente_divino', 150, 250, 3, 6, dioses.get('Tezcatlipoca')),
        ('Bio-Constructores', 'Sirvientes de Ixchel, maestros de la bioingeniería viviente (Coatlicueh en otras versiones)', 'sirviente_divino', 180, 280, 2, 5, dioses.get('Ixchel')),
        ('Acuátiles', 'Sirvientes anfibios de Tláloc, pueden respirar bajo el agua', 'sirviente_divino', 120, 200, 4, 8, dioses.get('Tláloc')),
        ('Guerreros Solares', 'Sirvientes guerreros de Huitzilopochtli, resistencia sobrehumana', 'sirviente_divino', 100, 180, 3, 5, dioses.get('Huitzilopochtli')),
    ]

    print("Insertando 5 especies sirvientes faltantes...")

    for especie in missing_species:
        cursor.execute("""
            INSERT INTO especies (nombre, descripcion, tipo, esperanza_vida_min, esperanza_vida_max,
                                hijos_min, hijos_max, dios_creador_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (nombre) DO NOTHING
        """, especie)

    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM especies")
    total_count = cursor.fetchone()['count']
    print(f"✅ Total especies en BD: {total_count}")

    db.close()

if __name__ == '__main__':
    insert_missing_species()