#!/usr/bin/env python3
"""
Actualiza la base de datos con sistema de personalidades, necesidades y memoria de IA
"""

import sqlite3
import random
import json

def actualizar_schema_ia(db_path='quinto_sol.db'):
    """Aplica el nuevo esquema de IA"""
    print("Actualizando esquema con sistema de IA...")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Ejecutar el esquema de extensión
    with open('schema_extension_ia.sql', 'r', encoding='utf-8') as f:
        schema = f.read()
        cursor.executescript(schema)

    conn.commit()
    print("✓ Esquema de IA actualizado")
    return conn


def agregar_nuevos_oficios(conn):
    """Agrega oficios adicionales para el mundo futurista-natural"""
    print("\nAgregando nuevos oficios...")
    cursor = conn.cursor()

    nuevos_oficios = [
        # Científicos y académicos
        ('Alquimista', 'cientifico', 'Combina química antigua con tecnología simbólica para crear pociones y transmutaciones', 1, 10),
        ('Matemático', 'cientifico', 'Estudia patrones numéricos y geometría sagrada para descifrar glifos', 1, 12),
        ('Filósofo', 'cientifico', 'Contempla la naturaleza de la existencia y el significado de los dioses', 1, 15),
        ('Astrónomo', 'cientifico', 'Estudia los cuerpos celestes y su influencia en el mundo', 1, 10),
        ('Naturalista', 'cientifico', 'Estudia la flora y fauna de Aztlán Prime', 1, 8),
        ('Cartógrafo', 'cientifico', 'Mapea territorios y descubre nuevas tierras', 1, 7),

        # Servicios sociales
        ('Prostituta', 'social', 'Ofrece compañía y placer en tabernas y casas especializadas', 0, 1),
        ('Prostituto', 'social', 'Ofrece compañía y placer en tabernas y casas especializadas', 0, 1),
        ('Cantinero', 'social', 'Administra tabernas, sirve bebidas y escucha historias', 0, 2),
        ('Bardo', 'social', 'Músico y narrador de historias', 1, 5),
        ('Mensajero', 'social', 'Lleva mensajes y paquetes entre ciudades', 0, 2),

        # Tecnólogos (equilibrio naturaleza-tecnología)
        ('Biomecánico', 'tecnologico', 'Fusiona tecnología con organismos vivos', 1, 12),
        ('Sintetizador', 'tecnologico', 'Crea materiales híbridos orgánico-tecnológicos', 1, 10),
        ('Ingeniero de Glifos', 'tecnologico', 'Programa y diseña secuencias de glifos para tecnología simbólica', 1, 15),
        ('Cultivador de Cristales', 'tecnologico', 'Cultiva cristales energéticos bio-tecnológicos', 1, 8),

        # Guardianes y protección
        ('Guardián', 'militar', 'Protege lugares y personas importantes', 1, 6),
        ('Vigilante Nocturno', 'militar', 'Patrulla durante la noche', 1, 4),
        ('Guardaespaldas', 'militar', 'Protección personal de nobles y comerciantes', 1, 8),

        # Oficios oscuros/moralmente ambiguos
        ('Ladrón', 'criminal', 'Roba para vivir o por encargo', 0, 3),
        ('Asesino', 'criminal', 'Elimina objetivos por contrato', 1, 10),
        ('Contrabandista', 'criminal', 'Trafica bienes ilegales entre ciudades', 0, 4),
        ('Espía', 'criminal', 'Recopila información para diferentes facciones', 1, 12),

        # Artesanos especializados
        ('Tatuador', 'artesanal', 'Marca la piel con diseños sagrados y tecnológicos', 1, 6),
        ('Perfumista', 'artesanal', 'Crea fragancias de plantas exóticas', 1, 5),
        ('Vidriero', 'artesanal', 'Trabaja con cristales y vidrios especiales', 1, 7),
    ]

    for oficio in nuevos_oficios:
        cursor.execute('''
            INSERT OR IGNORE INTO oficios
            (nombre, categoria, descripcion, requiere_entrenamiento, años_aprendizaje)
            VALUES (?, ?, ?, ?, ?)
        ''', oficio)

    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM oficios")
    total = cursor.fetchone()[0]
    print(f"✓ Total de oficios en sistema: {total}")


def poblar_rasgos_personalidad(conn):
    """Pobla rasgos de personalidad"""
    print("\nPoblando rasgos de personalidad...")
    cursor = conn.cursor()

    # Verificar si ya existen
    cursor.execute("SELECT COUNT(*) FROM rasgos_personalidad")
    if cursor.fetchone()[0] > 0:
        print("✓ Rasgos ya poblados")
        return

    rasgos = [
        # Temperamento
        ('Valiente', 'temperamento', 'Enfrenta peligros sin miedo'),
        ('Cobarde', 'temperamento', 'Evita el peligro y los riesgos'),
        ('Paciente', 'temperamento', 'Mantiene la calma en situaciones difíciles'),
        ('Impulsivo', 'temperamento', 'Actúa sin pensar en las consecuencias'),
        ('Optimista', 'temperamento', 'Ve el lado positivo de las cosas'),
        ('Pesimista', 'temperamento', 'Espera lo peor de las situaciones'),

        # Ética y moral
        ('Honesto', 'etica', 'Siempre dice la verdad'),
        ('Mentiroso', 'etica', 'Miente con frecuencia para beneficio propio'),
        ('Generoso', 'etica', 'Comparte recursos sin esperar nada'),
        ('Avaro', 'etica', 'Acumula riquezas y no comparte'),
        ('Leal', 'etica', 'Fiel a sus amigos y aliados'),
        ('Traicionero', 'etica', 'Cambia de bando por conveniencia'),
        ('Compasivo', 'etica', 'Se preocupa por el sufrimiento ajeno'),
        ('Cruel', 'etica', 'Disfruta causar dolor a otros'),

        # Social
        ('Carismático', 'social', 'Atrae y convence a los demás fácilmente'),
        ('Introvertido', 'social', 'Prefiere la soledad a la compañía'),
        ('Amigable', 'social', 'Hace amigos con facilidad'),
        ('Hostil', 'social', 'Desconfía y rechaza a los demás'),
        ('Seductor', 'social', 'Atrae románticamente con facilidad'),
        ('Tímido', 'social', 'Le cuesta relacionarse con otros'),

        # Mental
        ('Inteligente', 'mental', 'Aprende y razona rápidamente'),
        ('Simple', 'mental', 'Le cuesta entender conceptos complejos'),
        ('Creativo', 'mental', 'Genera ideas originales'),
        ('Pragmático', 'mental', 'Se enfoca en soluciones prácticas'),
        ('Curioso', 'mental', 'Siempre busca aprender cosas nuevas'),
        ('Conformista', 'mental', 'Acepta las cosas como son'),

        # Trabajo
        ('Trabajador', 'laboral', 'Dedicado y esforzado en su oficio'),
        ('Holgazán', 'laboral', 'Evita el trabajo duro'),
        ('Perfeccionista', 'laboral', 'Busca la excelencia en todo'),
        ('Descuidado', 'laboral', 'No presta atención a los detalles'),

        # Espiritual
        ('Devoto', 'espiritual', 'Profundamente religioso'),
        ('Escéptico', 'espiritual', 'Duda de los dioses y la religión'),
        ('Místico', 'espiritual', 'Conectado con lo sobrenatural'),
        ('Materialista', 'espiritual', 'Solo cree en lo tangible'),
    ]

    for rasgo in rasgos:
        cursor.execute('''
            INSERT INTO rasgos_personalidad (nombre, categoria, descripcion)
            VALUES (?, ?, ?)
        ''', rasgo)

    # Establecer opuestos
    opuestos = [
        ('Valiente', 'Cobarde'),
        ('Paciente', 'Impulsivo'),
        ('Optimista', 'Pesimista'),
        ('Honesto', 'Mentiroso'),
        ('Generoso', 'Avaro'),
        ('Leal', 'Traicionero'),
        ('Compasivo', 'Cruel'),
        ('Carismático', 'Introvertido'),
        ('Amigable', 'Hostil'),
        ('Seductor', 'Tímido'),
        ('Inteligente', 'Simple'),
        ('Creativo', 'Pragmático'),
        ('Curioso', 'Conformista'),
        ('Trabajador', 'Holgazán'),
        ('Perfeccionista', 'Descuidado'),
        ('Devoto', 'Escéptico'),
        ('Místico', 'Materialista'),
    ]

    for rasgo1, rasgo2 in opuestos:
        cursor.execute('''
            UPDATE rasgos_personalidad
            SET opuesto_id = (SELECT id FROM rasgos_personalidad WHERE nombre = ?)
            WHERE nombre = ?
        ''', (rasgo2, rasgo1))
        cursor.execute('''
            UPDATE rasgos_personalidad
            SET opuesto_id = (SELECT id FROM rasgos_personalidad WHERE nombre = ?)
            WHERE nombre = ?
        ''', (rasgo1, rasgo2))

    conn.commit()
    print(f"✓ {len(rasgos)} rasgos de personalidad insertados")


def poblar_necesidades(conn):
    """Pobla necesidades básicas y profesionales"""
    print("\nPoblando necesidades...")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM necesidades")
    if cursor.fetchone()[0] > 0:
        print("✓ Necesidades ya pobladas")
        return

    necesidades = [
        # Básicas
        ('Comida', 'basica', 'Necesidad de alimentarse', 10),
        ('Agua', 'basica', 'Necesidad de beber', 10),
        ('Descanso', 'basica', 'Necesidad de dormir', 9),
        ('Refugio', 'basica', 'Necesidad de un lugar seguro', 8),
        ('Seguridad', 'basica', 'Protección contra peligros', 8),

        # Sociales
        ('Companía', 'social', 'Interacción con otros', 6),
        ('Reconocimiento', 'social', 'Ser valorado por los demás', 5),
        ('Amor', 'social', 'Afecto romántico o familiar', 5),
        ('Diversión', 'social', 'Entretenimiento y ocio', 4),

        # Profesionales (específicas por oficio)
        ('Materiales de Trabajo', 'profesional', 'Recursos para ejercer el oficio', 7),
        ('Herramientas', 'profesional', 'Instrumentos de trabajo', 7),
        ('Clientes', 'profesional', 'Personas que solicitan servicios', 6),
        ('Aprendizaje', 'profesional', 'Mejorar habilidades', 5),

        # Espirituales
        ('Fe', 'espiritual', 'Conexión con lo divino', 6),
        ('Propósito', 'espiritual', 'Sentido de existencia', 5),
    ]

    cursor.executemany('''
        INSERT INTO necesidades (nombre, tipo, descripcion, prioridad)
        VALUES (?, ?, ?, ?)
    ''', necesidades)

    conn.commit()
    print(f"✓ {len(necesidades)} necesidades insertadas")


def poblar_items_recursos(conn):
    """Pobla items y recursos del juego"""
    print("\nPoblando items y recursos...")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM items")
    if cursor.fetchone()[0] > 0:
        print("✓ Items ya poblados")
        return

    items = [
        # Comida
        ('Pan de Maíz', 'comida', 'pan', 2, 0.5, 1, 1, 'Pan básico hecho de maíz'),
        ('Carne Seca', 'comida', 'carne', 5, 1.0, 1, 10, 'Carne curada para conservación'),
        ('Pescado Fresco', 'comida', 'pescado', 3, 0.8, 1, 1, 'Pescado recién capturado'),
        ('Tortillas', 'comida', 'pan', 1, 0.3, 1, 2, 'Tortillas de maíz tradicionales'),
        ('Tamales', 'comida', 'preparado', 4, 0.6, 1, 3, 'Tamales rellenos'),

        # Bebidas
        ('Pulque', 'bebida', 'alcohol', 3, 1.0, 1, 5, 'Bebida fermentada de agave'),
        ('Agua Purificada', 'bebida', 'agua', 1, 1.0, 0, None, 'Agua limpia'),
        ('Chocolate Divino', 'bebida', 'especial', 10, 0.5, 1, 30, 'Chocolate ceremonial de los dioses'),

        # Materiales
        ('Hierro', 'material', 'metal', 8, 5.0, 0, None, 'Metal básico para forja'),
        ('Obsidiana', 'material', 'piedra', 15, 3.0, 0, None, 'Vidrio volcánico sagrado'),
        ('Jade', 'material', 'gema', 50, 0.5, 0, None, 'Piedra preciosa verde'),
        ('Madera', 'material', 'organico', 3, 2.0, 0, None, 'Madera de árbol común'),
        ('Cuero', 'material', 'organico', 6, 1.5, 0, None, 'Cuero curtido de animal'),
        ('Plumas de Quetzal', 'material', 'especial', 100, 0.1, 0, None, 'Plumas sagradas muy valiosas'),

        # Herramientas
        ('Martillo', 'herramienta', 'forja', 20, 3.0, 0, None, 'Martillo de herrero'),
        ('Hacha', 'herramienta', 'corte', 15, 2.5, 0, None, 'Hacha para talar'),
        ('Pico', 'herramienta', 'mineria', 18, 3.5, 0, None, 'Pico de minero'),
        ('Anzuelo', 'herramienta', 'pesca', 5, 0.2, 0, None, 'Anzuelo de pesca'),

        # Armas
        ('Macuahuitl', 'arma', 'cuerpo_a_cuerpo', 40, 3.0, 0, None, 'Espada de obsidiana mexica'),
        ('Arco Corto', 'arma', 'distancia', 30, 2.0, 0, None, 'Arco para caza y combate'),
        ('Lanza', 'arma', 'cuerpo_a_cuerpo', 25, 2.5, 0, None, 'Lanza de madera y punta de piedra'),
        ('Cuchillo de Obsidiana', 'arma', 'cuerpo_a_cuerpo', 15, 0.5, 0, None, 'Cuchillo de obsidiana afilada'),

        # Armadura
        ('Escudo de Madera', 'armadura', 'escudo', 20, 3.0, 0, None, 'Escudo básico'),
        ('Peto de Cuero', 'armadura', 'pecho', 35, 4.0, 0, None, 'Protección de pecho de cuero'),
        ('Yelmo de Jaguar', 'armadura', 'cabeza', 80, 2.5, 0, None, 'Casco ceremonial de guerrero jaguar'),

        # Especiales/Tecnológicos
        ('Cristal Energético', 'tecnologico', 'energia', 200, 0.5, 0, None, 'Cristal bio-tecnológico que almacena energía'),
        ('Glifo Programado', 'tecnologico', 'software', 150, 0.1, 0, None, 'Glifo con secuencia simbólica programada'),
        ('Semilla Biomod', 'tecnologico', 'organico', 100, 0.2, 1, 100, 'Semilla modificada genéticamente'),
    ]

    for item in items:
        cursor.execute('''
            INSERT INTO items
            (nombre, tipo, subtipo, valor_base, peso, es_perecedero, duracion_años, descripcion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', item)

    conn.commit()
    print(f"✓ {len(items)} items insertados")


def asignar_personalidades_npcs(conn):
    """Asigna personalidades aleatorias a NPCs existentes"""
    print("\nAsignando personalidades a NPCs...")
    cursor = conn.cursor()

    # Obtener todos los NPCs
    cursor.execute("SELECT id FROM personas WHERE es_npc = 1 LIMIT 100")
    npcs = cursor.fetchall()

    # Obtener todos los rasgos
    cursor.execute("SELECT id, opuesto_id FROM rasgos_personalidad")
    rasgos = cursor.fetchall()

    contador = 0
    for npc_id, in npcs:
        # Asignar 3-6 rasgos aleatorios
        num_rasgos = random.randint(3, 6)
        rasgos_seleccionados = random.sample(rasgos, num_rasgos)

        for rasgo_id, opuesto_id in rasgos_seleccionados:
            # No asignar rasgos opuestos al mismo NPC
            cursor.execute('''
                SELECT COUNT(*) FROM persona_personalidad
                WHERE persona_id = ? AND rasgo_id = ?
            ''', (npc_id, opuesto_id if opuesto_id else -1))

            if cursor.fetchone()[0] == 0:
                intensidad = random.randint(3, 9)  # 3-9 de intensidad
                cursor.execute('''
                    INSERT OR IGNORE INTO persona_personalidad
                    (persona_id, rasgo_id, intensidad)
                    VALUES (?, ?, ?)
                ''', (npc_id, rasgo_id, intensidad))
                contador += 1

    conn.commit()
    print(f"✓ {contador} rasgos de personalidad asignados a {len(npcs)} NPCs")


def asignar_necesidades_npcs(conn):
    """Asigna necesidades a NPCs"""
    print("\nAsignando necesidades a NPCs...")
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM personas WHERE es_npc = 1 LIMIT 100")
    npcs = cursor.fetchall()

    cursor.execute("SELECT id, prioridad FROM necesidades")
    necesidades = cursor.fetchall()

    contador = 0
    for npc_id, in npcs:
        for nec_id, prioridad in necesidades:
            # Nivel inicial aleatorio
            nivel_actual = random.randint(40, 100)
            nivel_minimo = 100 - (prioridad * 10)  # Mayor prioridad = menor mínimo aceptable

            cursor.execute('''
                INSERT OR IGNORE INTO persona_necesidades
                (persona_id, necesidad_id, nivel_actual, nivel_minimo, ultima_actualizacion)
                VALUES (?, ?, ?, ?, 1500)
            ''', (npc_id, nec_id, nivel_actual, nivel_minimo))
            contador += 1

    conn.commit()
    print(f"✓ {contador} necesidades asignadas")


def main():
    print("="*70)
    print("ACTUALIZACIÓN: Sistema de IA, Personalidades y Economía")
    print("="*70 + "\n")

    try:
        conn = actualizar_schema_ia()
        agregar_nuevos_oficios(conn)
        poblar_rasgos_personalidad(conn)
        poblar_necesidades(conn)
        poblar_items_recursos(conn)
        asignar_personalidades_npcs(conn)
        asignar_necesidades_npcs(conn)

        print("\n" + "="*70)
        print("✓ Actualización completada exitosamente")
        print("="*70 + "\n")

        # Estadísticas
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM oficios")
        print(f"Oficios totales: {cursor.fetchone()[0]}")

        cursor.execute("SELECT COUNT(*) FROM rasgos_personalidad")
        print(f"Rasgos de personalidad: {cursor.fetchone()[0]}")

        cursor.execute("SELECT COUNT(*) FROM necesidades")
        print(f"Necesidades: {cursor.fetchone()[0]}")

        cursor.execute("SELECT COUNT(*) FROM items")
        print(f"Items/Recursos: {cursor.fetchone()[0]}")

        cursor.execute("SELECT COUNT(*) FROM persona_personalidad")
        print(f"Rasgos asignados a NPCs: {cursor.fetchone()[0]}")

        conn.close()

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
