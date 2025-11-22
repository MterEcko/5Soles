from database_connector import DatabaseConnector

def insertar_ciudades():
    db = DatabaseConnector()
    db.connect()

    # Obtener IDs de civilizaciones
    db.cursor.execute("SELECT id, nombre FROM civilizaciones")
    civs = {row['nombre']: row['id'] for row in db.fetchall()}

    if not civs:
        print("\n❌ No hay civilizaciones en la BD. Asegúrate de correr crear_db.py primero.")
        return

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

    # Insertar el resto de ciudades para las otras 3 civilizaciones:
    if 'Zapotecas del Eco' in civs:
         ciudades.extend([
            ('Jardín de Sanación', 'capital', civs['Zapotecas del Eco'], 3500, 30, 1515, None, -15.2, 12.8, 'Capital Zapoteca. Centro de bio-ingeniería y curación.'),
            ('Cuenca Espejo de Agua', 'ciudad', civs['Zapotecas del Eco'], 1500, 25, 1525, None, -12.0, 15.0, 'Ciudad de sanadores y cultivadores.'),
        ])
    
    if 'Toltecas del Viento' in civs:
         ciudades.extend([
            ('Cañón del Eco', 'capital', civs['Toltecas del Viento'], 2800, 35, 1522, None, 5.0, -20.0, 'Capital Tolteca en los cañones del desierto.'),
            ('Aldea de la Resonancia', 'aldea', civs['Toltecas del Viento'], 400, 25, 1535, None, 7.0, -18.0, 'Aldea de ingenieros y artesanos del sonido.'),
        ])
        
    if 'Purépecha del Fuego' in civs:
         ciudades.extend([
            ('Monte Ígneo', 'capital', civs['Purépecha del Fuego'], 2500, 40, 1525, None, -5.0, -10.0, 'Capital en las montañas volcánicas. Centro de metalurgia.'),
            ('Forjas del Amanecer', 'ciudad', civs['Purépecha del Fuego'], 1200, 35, 1540, None, -3.0, -12.0, 'Ciudad de herreros y artesanos del metal.'),
        ])


    for ciudad in ciudades:
        try:
            db.cursor.execute('''
                INSERT INTO pueblos_ciudades
                (nombre, tipo, civilizacion_id, poblacion_aproximada, nivel_zona,
                 año_fundacion, año_destruccion, coordenadas_x, coordenadas_y, descripcion)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', ciudad)
        except Exception as e:
            # Ignorar si ya existe
            pass

    db.conn.commit()
    db.close()
    print(f"✅ {len(ciudades)} ciudades base insertadas.")

if __name__ == '__main__':
    insertar_ciudades()