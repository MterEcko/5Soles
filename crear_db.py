#!/usr/bin/env python3
"""
Script para crear e inicializar la base de datos de Portales del Quinto Sol
"""

import sqlite3
import random
from datetime import datetime

def crear_base_datos():
    """Crea la base de datos y ejecuta el esquema"""
    print("Creando base de datos...")

    # Conectar a la base de datos (la crea si no existe)
    conn = sqlite3.connect('quinto_sol.db')
    cursor = conn.cursor()

    # Leer y ejecutar el esquema
    with open('schema.sql', 'r', encoding='utf-8') as f:
        schema = f.read()
        cursor.executescript(schema)

    conn.commit()
    print("✓ Base de datos creada exitosamente")
    return conn

def poblar_eras(conn):
    """Inserta las eras históricas"""
    print("\nPoblando Eras...")
    cursor = conn.cursor()

    eras = [
        ('Era Alpha', 'La Primera Era - Llegada por los Portales. Los 40 humanos originales llegan a Aztlán Prime. Muchos murieron cuando el portal colapsó antes de tiempo.', 1500, 1650, 0),
        ('Era de la Fundación', 'Establecimiento de las primeras aldeas y aceptación de los dioses como guías.', 1651, 1800, 0),
        ('Era del Despertar', 'Las primeras generaciones nacidas en Aztlán Prime comienzan a desarrollar habilidades únicas.', 1801, 2000, 0),
        ('Era de la Expansión', 'Crecimiento de ciudades y desarrollo de la tecnología simbólica.', 2001, 2200, 0),
        ('Era del Cataclismo', 'La Tierra colapsa en el siglo XXIII. Los Humanos II llegan a Aztlán Prime.', 2201, 2400, 0),
        ('Era del Conflicto', 'Tensiones entre Humanos I y Humanos II. Guerras por recursos y territorio.', 2401, 2700, 0),
        ('Era de la Síntesis', 'Integración gradual de ambas humanidades y florecimiento cultural.', 2701, 3000, 1),
    ]

    cursor.executemany('''
        INSERT INTO eras (nombre, descripcion, año_inicio, año_fin, es_actual)
        VALUES (?, ?, ?, ?, ?)
    ''', eras)

    conn.commit()
    print(f"✓ {len(eras)} eras insertadas")

def poblar_dioses(conn):
    """Inserta los 17 dioses principales"""
    print("\nPoblando Dioses...")
    cursor = conn.cursor()

    dioses = [
        ('Quetzalcóatl', 'Equilibrio, Viento, Sabiduría', 'Mexica, Tolteca, Maya, Olmeca, Mixteca', 'Positiva', 'Energía Fotónica, Ciencia de la Estabilidad Dimensional, Geometría Avanzada'),
        ('Tezcatlipoca', 'Conflicto, Sombra, Ilusión', 'Mexica, Tolteca, Maya', 'Negativa', 'Tecnología de la Ilusión, Realidad Aumentada/Virtual (Espejos), Control Mental'),
        ('Tláloc', 'Agua, Lluvia, Fertilidad', 'Mexica, Teotihuacano, Tlaxcalteca, Maya, Zapoteca', 'Neutral', 'Ingeniería Hidráulica Biológica, Manipulación de la Humedad Atmosférica'),
        ('Huitzilopochtli', 'Voluntad, Guerra, Sol del Mediodía', 'Mexica, Tlaxcalteca, Purépecha', 'Neutral', 'Tecnología de Armamento y Escudos de Energía Dura'),
        ('Ixchel', 'Luna, Sanación, Biogénesis', 'Maya, Zapoteca, Purépecha', 'Positiva', 'Bioingeniería Avanzada, Curación Genética, Control de Ciclos Biológicos'),
        ('Mictlantecuhtli', 'Muerte, Inframundo', 'Mexica, Mixteca, Zapoteca', 'Negativa', 'Necrotecnología, Manipulación de la Materia Orgánica Muerta'),
        ('Xipe Tótec', 'Sacrificio, Renovación Forzada', 'Mexica, Zapoteca, Mixteca', 'Negativa', 'Mutación Genética, Revestimiento Orgánico, Armas de Corrosión'),
        ('Xochiquétzal', 'Flores, Amor, Artesanía', 'Mexica, Tlaxcalteca, Zapoteca', 'Positiva', 'Tecnología de Diseño, Fabricación de Componentes Orgánicos Raros'),
        ('Chaac', 'Lluvia, Rayo, Trueno', 'Maya, Zapoteca', 'Neutral', 'Generación y Canalización de Energía Eléctrica y Atmosférica'),
        ('Cochise', 'Cacería, Vida Silvestre', 'Zapoteca', 'Neutral', 'Habilidades de Rastreo Biológico, Integración de Fauna a la Tecnología'),
        ('Centéotl', 'Maíz, Subsistencia, Juvencia', 'Mexica, Zapoteca', 'Positiva', 'Tecnología de Alimentos Sintéticos, Bio-Almacenamiento'),
        ('Mayahuel', 'Agave, Embriaguez, Placer', 'Mexica', 'Neutral', 'Bio-química de la Felicidad, Control de Placer/Dolor'),
        ('Zipacná', 'Tierra, Montañas, Terremotos', 'Maya', 'Neutral', 'Ingeniería Tectónica, Estabilización/Desestabilización Geológica'),
        ('Metztli', 'Luna, Noche, Agua', 'Mexica, Purépecha', 'Positiva', 'Tecnología de Capas de Invisibilidad, Control de Mareas Energéticas'),
        ('Piltzintecuhtli', 'Sol Joven, Juventud', 'Mexica', 'Positiva', 'Aceleración de Procesos Biológicos, Energía Pura'),
        ('Xólotl', 'Fuego, Dualidad, Monstruosidad', 'Mexica, Mixteca', 'Negativa', 'Mutación Biológica Forzada, Transmutación Extrema de Materia'),
        ('Huracán', 'Viento, Tormenta, Fuego', 'Maya', 'Neutral', 'Manipulación Extrema del Clima, Armamento Sónico y de Resonancia'),
    ]

    cursor.executemany('''
        INSERT INTO dioses (nombre, dominio_principal, culturas, polaridad, eje_tecnologico)
        VALUES (?, ?, ?, ?, ?)
    ''', dioses)

    conn.commit()
    print(f"✓ {len(dioses)} dioses insertados")

def poblar_civilizaciones(conn):
    """Inserta las civilizaciones principales"""
    print("\nPoblando Civilizaciones...")
    cursor = conn.cursor()

    # Obtener IDs de dioses
    cursor.execute("SELECT id FROM dioses WHERE nombre = 'Huitzilopochtli'")
    huitzi_id = cursor.fetchone()[0]

    cursor.execute("SELECT id FROM dioses WHERE nombre = 'Ixchel'")
    ixchel_id = cursor.fetchone()[0]

    cursor.execute("SELECT id FROM dioses WHERE nombre = 'Quetzalcóatl'")
    quetza_id = cursor.fetchone()[0]

    cursor.execute("SELECT id FROM dioses WHERE nombre = 'Huracán'")
    huracan_id = cursor.fetchone()[0]

    cursor.execute("SELECT id FROM dioses WHERE nombre = 'Tláloc'")
    tlaloc_id = cursor.fetchone()[0]

    civilizaciones = [
        ('Mexica de Obsidiana', 'Imperio Tecno-Guerrero', huitzi_id, 'Tierras volcánicas, arquitectura negra y roja. Fábricas de armas biomecánicas.', 1520),
        ('Zapotecas del Eco', 'Sanadores y Bio-Ingenieros', ixchel_id, 'Jungla luminosa. Arquitectura de organismos vivos. Maestros de la sanación.', 1515),
        ('Mayas Celeste', 'Sabios del Tiempo y Espacio', quetza_id, 'Ciudades flotantes con energía solar cuántica. Maestros del tiempo.', 1518),
        ('Toltecas del Viento', 'Ingenieros de Resonancia', huracan_id, 'Desiertos rocosos. Ciudades en cañones. Maestros de la resonancia sónica.', 1522),
        ('Purépecha del Fuego', 'Artesanos y Metalúrgicos', tlaloc_id, 'Montañas volcánicas. Maestros de la forja y la metalurgia divina.', 1525),
    ]

    cursor.executemany('''
        INSERT INTO civilizaciones (nombre, tipo, dios_patron_id, descripcion, año_fundacion)
        VALUES (?, ?, ?, ?, ?)
    ''', civilizaciones)

    conn.commit()
    print(f"✓ {len(civilizaciones)} civilizaciones insertadas")

def poblar_especies(conn):
    """Inserta las especies del mundo"""
    print("\nPoblando Especies...")
    cursor = conn.cursor()

    # Obtener algunos IDs de dioses para las especies
    cursor.execute("SELECT id FROM dioses WHERE nombre = 'Quetzalcóatl'")
    quetza_id = cursor.fetchone()[0]

    cursor.execute("SELECT id FROM dioses WHERE nombre = 'Tezcatlipoca'")
    tezcat_id = cursor.fetchone()[0]

    cursor.execute("SELECT id FROM dioses WHERE nombre = 'Ixchel'")
    ixchel_id = cursor.fetchone()[0]

    cursor.execute("SELECT id FROM dioses WHERE nombre = 'Tláloc'")
    tlaloc_id = cursor.fetchone()[0]

    cursor.execute("SELECT id FROM dioses WHERE nombre = 'Huitzilopochtli'")
    huitzi_id = cursor.fetchone()[0]

    especies = [
        ('Humanos I', 'Humanos del siglo XV, salvados durante la Conquista Española', 'humano', 80, 150, 4, 7, quetza_id),
        ('Humanos II', 'Humanos del siglo XXIII, sobrevivientes del cataclismo terrestre', 'humano', 70, 120, 2, 5, None),
        ('Tlacatl de Luz', 'Sirvientes humanoides de Quetzalcóatl, con piel luminiscente y alas vestigiales', 'sirviente_divino', 200, 300, 2, 4, quetza_id),
        ('Sombra-Coyotes', 'Sirvientes metamórficos de Tezcatlipoca, pueden cambiar de forma', 'sirviente_divino', 150, 250, 3, 6, tezcat_id),
        ('Bio-Constructores', 'Sirvientes de Ixchel, maestros de la bioingeniería viviente', 'sirviente_divino', 180, 280, 2, 5, ixchel_id),
        ('Acuátiles', 'Sirvientes anfibios de Tláloc, pueden respirar bajo el agua', 'sirviente_divino', 120, 200, 4, 8, tlaloc_id),
        ('Guerreros Solares', 'Sirvientes guerreros de Huitzilopochtli, resistencia sobrehumana', 'sirviente_divino', 100, 180, 3, 5, huitzi_id),
    ]

    cursor.executemany('''
        INSERT INTO especies (nombre, descripcion, tipo, esperanza_vida_min, esperanza_vida_max,
                             hijos_min, hijos_max, dios_creador_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', especies)

    conn.commit()
    print(f"✓ {len(especies)} especies insertadas")

def poblar_oficios(conn):
    """Inserta oficios disponibles"""
    print("\nPoblando Oficios...")
    cursor = conn.cursor()

    oficios = [
        # Artesanales
        ('Herrero', 'artesanal', 'Forja armas, herramientas y armaduras de metal', 1, 7),
        ('Carpintero', 'artesanal', 'Construye estructuras y muebles de madera', 1, 5),
        ('Alfarero', 'artesanal', 'Crea vasijas, platos y objetos de cerámica', 1, 4),
        ('Tejedor', 'artesanal', 'Teje telas y crea vestimentas', 1, 3),
        ('Tallador', 'artesanal', 'Talla piedra y madera con diseños artísticos', 1, 6),
        ('Joyero', 'artesanal', 'Crea joyas y ornamentos preciosos', 1, 8),

        # Religiosos
        ('Sacerdote', 'religioso', 'Líder espiritual y guía de la comunidad', 1, 15),
        ('Sacerdotisa', 'religioso', 'Líder espiritual femenina, sanadora y vidente', 1, 15),
        ('Chamán', 'religioso', 'Sanador espiritual y médico tradicional', 1, 12),
        ('Augur', 'religioso', 'Intérprete de señales divinas y profecías', 1, 10),

        # Militares
        ('Guerrero', 'militar', 'Soldado entrenado en combate cuerpo a cuerpo', 1, 8),
        ('Arquero', 'militar', 'Experto en combate a distancia con arco', 1, 6),
        ('Capitán', 'militar', 'Líder de grupos de guerreros', 1, 10),
        ('Estratega', 'militar', 'Planificador militar y táctico', 1, 12),

        # Agrícolas
        ('Agricultor', 'agricola', 'Cultiva la tierra y cosecha alimentos', 0, 2),
        ('Pastor', 'agricola', 'Cuida y guía rebaños de animales', 0, 2),
        ('Pescador', 'agricola', 'Pesca y recolecta recursos del agua', 0, 2),
        ('Cazador', 'agricola', 'Caza animales para alimento y recursos', 1, 4),

        # Comerciales
        ('Comerciante', 'comercial', 'Compra y vende bienes entre comunidades', 0, 3),
        ('Posadero', 'comercial', 'Administra posadas y tabernas', 0, 2),

        # Servicios
        ('Cocinero', 'servicios', 'Prepara alimentos y bebidas', 0, 2),
        ('Curandero', 'servicios', 'Sana heridas y enfermedades con hierbas', 1, 6),
        ('Escriba', 'servicios', 'Registra información y mantiene archivos', 1, 8),
        ('Arquitecto', 'servicios', 'Diseña y planifica construcciones', 1, 10),
        ('Minero', 'servicios', 'Extrae minerales y piedras preciosas', 0, 3),

        # Especialistas divinos
        ('Tecnomístico', 'especialista', 'Descifra glifos y crea tecnología simbólica', 1, 15),
        ('Geomante', 'especialista', 'Manipula la tierra y las piedras con poder divino', 1, 12),
        ('Bio-Ingeniero', 'especialista', 'Crea y modifica formas de vida orgánicas', 1, 15),
    ]

    cursor.executemany('''
        INSERT INTO oficios (nombre, categoria, descripcion, requiere_entrenamiento, años_aprendizaje)
        VALUES (?, ?, ?, ?, ?)
    ''', oficios)

    conn.commit()
    print(f"✓ {len(oficios)} oficios insertados")

def poblar_habilidades(conn):
    """Inserta habilidades especiales"""
    print("\nPoblando Habilidades...")
    cursor = conn.cursor()

    # Obtener IDs de dioses
    cursor.execute("SELECT id, nombre FROM dioses")
    dioses_map = {nombre: id for id, nombre in cursor.fetchall()}

    habilidades = [
        # Combate
        ('Maestría con Espada', 'combate', 'Experto en combate con espadas', None, 5),
        ('Maestría con Arco', 'combate', 'Experto en tiro con arco', None, 5),
        ('Combate Cuerpo a Cuerpo', 'combate', 'Pelea sin armas con gran destreza', None, 4),
        ('Resistencia de Batalla', 'combate', 'Aguante superior en combate prolongado', dioses_map['Huitzilopochtli'], 6),
        ('Sigilo Mortal', 'combate', 'Movimiento sigiloso y ataques sorpresa', dioses_map['Tezcatlipoca'], 5),

        # Magia/Divina
        ('Curación Divina', 'magia', 'Capacidad de curar heridas con energía divina', dioses_map['Ixchel'], 8),
        ('Invocación de Lluvia', 'magia', 'Puede convocar lluvia en áreas pequeñas', dioses_map['Tláloc'], 7),
        ('Visión de Sombras', 'magia', 'Ve a través de ilusiones y en la oscuridad', dioses_map['Tezcatlipoca'], 6),
        ('Luz Solar', 'magia', 'Emite luz brillante a voluntad', dioses_map['Huitzilopochtli'], 5),
        ('Control de Viento', 'magia', 'Manipula corrientes de aire', dioses_map['Quetzalcóatl'], 7),

        # Artesanales
        ('Forja Maestra', 'artesanal', 'Crea armas y armaduras de calidad superior', None, 7),
        ('Carpintería Avanzada', 'artesanal', 'Construye estructuras complejas', None, 6),
        ('Diseño Artístico', 'artesanal', 'Crea obras de arte excepcionales', dioses_map['Xochiquétzal'], 6),

        # Sociales
        ('Liderazgo Natural', 'social', 'Inspira y guía a otros con facilidad', None, 5),
        ('Negociación Experta', 'social', 'Excelente en tratos comerciales', None, 4),
        ('Oratoria Divina', 'social', 'Discursos que conmueven multitudes', dioses_map['Quetzalcóatl'], 6),
        ('Intimidación', 'social', 'Infunde miedo en los enemigos', dioses_map['Mictlantecuhtli'], 5),

        # Conocimiento
        ('Conocimiento de Hierbas', 'conocimiento', 'Experto en plantas medicinales', dioses_map['Ixchel'], 5),
        ('Lectura de Glifos', 'conocimiento', 'Interpreta símbolos antiguos', dioses_map['Quetzalcóatl'], 8),
        ('Astronomía', 'conocimiento', 'Conocimiento de los astros', dioses_map['Quetzalcóatl'], 6),
        ('Arquitectura Avanzada', 'conocimiento', 'Diseña edificios complejos', dioses_map['Zipacná'], 7),

        # Supervivencia
        ('Rastreo Experto', 'supervivencia', 'Sigue rastros con gran precisión', dioses_map['Cochise'], 6),
        ('Conocimiento de la Naturaleza', 'supervivencia', 'Entiende ecosistemas y animales', dioses_map['Cochise'], 5),
        ('Resistencia al Frío', 'supervivencia', 'Soporta temperaturas extremas bajas', None, 4),
        ('Resistencia al Calor', 'supervivencia', 'Soporta temperaturas extremas altas', dioses_map['Huitzilopochtli'], 4),
    ]

    cursor.executemany('''
        INSERT INTO habilidades (nombre, categoria, descripcion, dios_asociado_id, nivel_poder)
        VALUES (?, ?, ?, ?, ?)
    ''', habilidades)

    conn.commit()
    print(f"✓ {len(habilidades)} habilidades insertadas")

def poblar_pueblos_ciudades(conn):
    """Inserta pueblos y ciudades iniciales"""
    print("\nPoblando Pueblos y Ciudades...")
    cursor = conn.cursor()

    # Obtener IDs de civilizaciones
    cursor.execute("SELECT id, nombre FROM civilizaciones")
    civs_map = {nombre: id for id, nombre in cursor.fetchall()}

    pueblos_ciudades = [
        # Mexica de Obsidiana
        ('Ciudad del Quinto Sol', 'capital', civs_map['Mexica de Obsidiana'], 5000, 50, 1520, None, 0.0, 0.0, 'Capital del imperio Mexica. Centro de poder militar y tecnológico.'),
        ('Fortaleza Negra', 'ciudad', civs_map['Mexica de Obsidiana'], 2000, 45, 1535, None, 10.5, -5.2, 'Ciudad fortificada en las montañas volcánicas.'),
        ('Aldea del Guerrero', 'aldea', civs_map['Mexica de Obsidiana'], 300, 20, 1540, None, 8.3, -3.1, 'Pequeña aldea de entrenamiento militar.'),

        # Zapotecas del Eco
        ('Jardín de Sanación', 'capital', civs_map['Zapotecas del Eco'], 3500, 30, 1515, None, -15.2, 12.8, 'Capital Zapoteca. Centro de bio-ingeniería y curación.'),
        ('Cuenca Espejo de Agua', 'ciudad', civs_map['Zapotecas del Eco'], 1500, 25, 1525, None, -12.0, 15.0, 'Ciudad de sanadores y cultivadores.'),
        ('Aldea de las Flores', 'aldea', civs_map['Zapotecas del Eco'], 250, 15, 1530, None, -14.0, 13.5, 'Aldea agrícola especializada en plantas medicinales.'),

        # Mayas Celeste
        ('Tamoanchan', 'capital', civs_map['Mayas Celeste'], 4000, 70, 1518, None, 20.0, 30.0, 'Ciudad flotante. Centro del conocimiento y la ciencia.'),
        ('Observatorio de las Estrellas', 'ciudad', civs_map['Mayas Celeste'], 1800, 60, 1540, None, 22.5, 28.0, 'Ciudad dedicada al estudio astronómico.'),
        ('Puerto Celeste', 'pueblo', civs_map['Mayas Celeste'], 600, 40, 1545, None, 19.0, 32.0, 'Puerto comercial y de transferencia.'),

        # Toltecas del Viento
        ('Cañón del Eco', 'capital', civs_map['Toltecas del Viento'], 2800, 35, 1522, None, 5.0, -20.0, 'Capital Tolteca en los cañones del desierto.'),
        ('Aldea de la Resonancia', 'aldea', civs_map['Toltecas del Viento'], 400, 25, 1535, None, 7.0, -18.0, 'Aldea de ingenieros y artesanos del sonido.'),

        # Purépecha del Fuego
        ('Monte Ígneo', 'capital', civs_map['Purépecha del Fuego'], 2500, 40, 1525, None, -5.0, -10.0, 'Capital en las montañas volcánicas. Centro de metalurgia.'),
        ('Forjas del Amanecer', 'ciudad', civs_map['Purépecha del Fuego'], 1200, 35, 1540, None, -3.0, -12.0, 'Ciudad de herreros y artesanos del metal.'),
    ]

    cursor.executemany('''
        INSERT INTO pueblos_ciudades (nombre, tipo, civilizacion_id, poblacion_aproximada, nivel_zona,
                                      año_fundacion, año_destruccion, coordenadas_x, coordenadas_y, descripcion)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', pueblos_ciudades)

    conn.commit()
    print(f"✓ {len(pueblos_ciudades)} pueblos y ciudades insertados")

if __name__ == '__main__':
    print("=" * 60)
    print("PORTALES DEL QUINTO SOL - Inicialización de Base de Datos")
    print("=" * 60)

    conn = crear_base_datos()

    try:
        poblar_eras(conn)
        poblar_dioses(conn)
        poblar_civilizaciones(conn)
        poblar_especies(conn)
        poblar_oficios(conn)
        poblar_habilidades(conn)
        poblar_pueblos_ciudades(conn)

        print("\n" + "=" * 60)
        print("✓ Base de datos inicializada exitosamente")
        print("=" * 60)

        # Mostrar estadísticas
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM dioses")
        print(f"\nEstadísticas:")
        print(f"  • Dioses: {cursor.fetchone()[0]}")

        cursor.execute("SELECT COUNT(*) FROM civilizaciones")
        print(f"  • Civilizaciones: {cursor.fetchone()[0]}")

        cursor.execute("SELECT COUNT(*) FROM especies")
        print(f"  • Especies: {cursor.fetchone()[0]}")

        cursor.execute("SELECT COUNT(*) FROM oficios")
        print(f"  • Oficios: {cursor.fetchone()[0]}")

        cursor.execute("SELECT COUNT(*) FROM habilidades")
        print(f"  • Habilidades: {cursor.fetchone()[0]}")

        cursor.execute("SELECT COUNT(*) FROM pueblos_ciudades")
        print(f"  • Pueblos y Ciudades: {cursor.fetchone()[0]}")

        cursor.execute("SELECT COUNT(*) FROM eras")
        print(f"  • Eras: {cursor.fetchone()[0]}")

    finally:
        conn.close()
