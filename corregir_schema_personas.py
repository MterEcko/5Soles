from database_connector import DatabaseConnector

def corregir_schema_personas():
    """Añade las 5 columnas de estadísticas faltantes a la tabla 'personas'."""
    db = DatabaseConnector()
    db.connect()
    
    # Lista de columnas a añadir (si no existen)
    alter_statements = [
        "ALTER TABLE personas ADD COLUMN fuerza INTEGER DEFAULT 100;",
        "ALTER TABLE personas ADD COLUMN agilidad INTEGER DEFAULT 100;",
        "ALTER TABLE personas ADD COLUMN resistencia INTEGER DEFAULT 100;",
        "ALTER TABLE personas ADD COLUMN carisma INTEGER DEFAULT 100;",
        "ALTER TABLE personas ADD COLUMN inteligencia INTEGER DEFAULT 100;"
    ]
    
    print("\n🔧 Verificando y añadiendo columnas de stats faltantes a la tabla 'personas'...")
    
    corregido = False
    for stmt in alter_statements:
        try:
            # Intentar ejecutar ALTER TABLE (si la columna no existe, se añade)
            db.execute(stmt)
            print(f"  ✓ Columna añadida: {stmt.split()[4]}")
            corregido = True
        except Exception as e:
            # Si el error indica que la columna ya existe, se ignora
            if 'already exists' in str(e) or 'ya existe' in str(e):
                print(f"  ℹ️  Columna {stmt.split()[4]} ya existe. Saltando.")
            else:
                # Otros errores son críticos
                print(f"  ❌ Error añadiendo columna {stmt.split()[4]}: {e}")
                db.conn.rollback()
                db.close()
                return False
    
    if corregido:
        db.conn.commit()
        print("✅ Esquema de la tabla 'personas' corregido.")
    
    db.close()
    return True

if __name__ == '__main__':
    corregir_schema_personas()