from database_connector import DatabaseConnector

def insertar_especies_sirvientes():
    db = DatabaseConnector()
    db.connect()

    print("🔌 Conexión establecida. Verificando Dioses...")
    # Recuperación de IDs de Dioses (requeridos para la llave foránea)
    db.execute("SELECT id, nombre FROM dioses")
    dioses_map = {row['nombre']: row['id'] for row in db.fetchall()}

    quetza_id = dioses_map.get('Quetzalcóatl')
    tezcat_id = dioses_map.get('Tezcatlipoca')
    ixchel_id = dioses_map.get('Ixchel')
    tlaloc_id = dioses_map.get('Tláloc')
    huitzi_id = dioses_map.get('Huitzilopochtli')
    
    if not quetza_id:
        print("❌ Error Crítico: Los Dioses base (Quetzalcóatl, etc.) no existen.")
        print("   Asegúrate de que 'python run_with_env.py poblar_sistemas_completos.py' se haya ejecutado (y no haya fallado la inserción de Dioses).")
        db.close()
        return

    especies_a_insertar = [
        ('Tlacatl de Luz', 'Sirvientes humanoides de Quetzalcóatl, con piel luminiscente y alas vestigiales', 'sirviente_divino', 200, 300, 2, 4, quetza_id),
        ('Sombra-Coyotes', 'Sirvientes metamórficos de Tezcatlipoca, pueden cambiar de forma', 'sirviente_divino', 150, 250, 3, 6, tezcat_id),
        ('Bio-Constructores', 'Sirvientes de Ixchel, maestros de la bioingeniería viviente', 'sirviente_divino', 180, 280, 2, 5, ixchel_id),
        ('Acuátiles', 'Sirvientes anfibios de Tláloc, pueden respirar bajo el agua', 'sirviente_divino', 120, 200, 4, 8, tlaloc_id),
        ('Guerreros Solares', 'Sirvientes guerreros de Huitzilopochtli, resistencia sobrehumana', 'sirviente_divino', 100, 180, 3, 5, huitzi_id),
    ]

    print(f"📋 Insertando {len(especies_a_insertar)} especies sirvientes faltantes...")
    
    for especie in especies_a_insertar:
        try:
            db.execute('''
                INSERT INTO especies (nombre, descripcion, tipo, esperanza_vida_min, esperanza_vida_max,
                                     hijos_min, hijos_max, dios_creador_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (nombre) DO NOTHING
            ''', especie)
            print(f"   ✅ {especie[0]}")
        except Exception as e:
            print(f"   ⚠️  Fallo al insertar {especie[0]}: {e}")

    db.commit()
    
    # Verificación
    db.execute("SELECT COUNT(*) FROM especies")
    print(f"\n✅ Total de especies en BD: {db.fetchone()['count']}")
    
    db.close()

if __name__ == '__main__':
    insertar_especies_sirvientes()