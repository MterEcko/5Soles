#!/usr/bin/env python3
"""
Pobla TODOS los sistemas completos del juego
"""

import sqlite3
import random
import json
from typing import List, Dict

def ejecutar_esquema_completo(conn):
    """Ejecuta el esquema completo de sistemas"""
    print("\n🔧 Aplicando esquema de sistemas completos...")

    with open('schema_sistemas_completos.sql', 'r', encoding='utf-8') as f:
        schema = f.read()
        conn.executescript(schema)

    conn.commit()
    print("✓ Esquema aplicado")

def verificar_y_completar_dioses(conn):
    """Verifica que los 17 dioses estén completos"""
    print("\n👁️  Verificando dioses...")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM dioses")
    count = cursor.fetchone()[0]

    if count >= 17:
        print(f"✓ {count} dioses ya en la base de datos")
        return

    print(f"⚠️  Solo {count} dioses encontrados. Agregando faltantes...")

    # Los 17 dioses principales (por si acaso)
    dioses_completos = [
        ('Quetzalcóatl', 'Equilibrio, Viento, Sabiduría', 'Mexica, Tolteca, Maya, Olmeca, Mixteca', 'Positiva', 'Energía Fotónica'),
        ('Tezcatlipoca', 'Conflicto, Sombra, Ilusión', 'Mexica, Tolteca, Maya', 'Negativa', 'Realidad Virtual'),
        ('Tláloc', 'Agua, Lluvia, Fertilidad', 'Mexica, Teotihuacano, Tlaxcalteca, Maya, Zapoteca', 'Neutral', 'Ingeniería Hidráulica'),
        ('Huitzilopochtli', 'Voluntad, Guerra, Sol', 'Mexica, Tlaxcalteca, Purépecha', 'Neutral', 'Escudos de Energía'),
        ('Ixchel', 'Luna, Sanación, Biogénesis', 'Maya, Zapoteca, Purépecha', 'Positiva', 'Bioingeniería'),
        ('Mictlantecuhtli', 'Muerte, Inframundo', 'Mexica, Mixteca, Zapoteca', 'Negativa', 'Necrotecnología'),
        ('Xipe Tótec', 'Sacrificio, Renovación', 'Mexica, Zapoteca, Mixteca', 'Negativa', 'Mutación Genética'),
        ('Xochiquétzal', 'Flores, Amor, Artesanía', 'Mexica, Tlaxcalteca, Zapoteca', 'Positiva', 'Diseño Orgánico'),
        ('Chaac', 'Lluvia, Rayo, Trueno', 'Maya, Zapoteca', 'Neutral', 'Energía Eléctrica'),
        ('Cochise', 'Cacería, Vida Silvestre', 'Zapoteca', 'Neutral', 'Integración Fauna'),
        ('Centéotl', 'Maíz, Subsistencia', 'Mexica, Zapoteca', 'Positiva', 'Alimentos Sintéticos'),
        ('Mayahuel', 'Agave, Embriaguez', 'Mexica', 'Neutral', 'Bio-química'),
        ('Zipacná', 'Tierra, Montañas, Terremotos', 'Maya', 'Neutral', 'Ingeniería Tectónica'),
        ('Metztli', 'Luna, Noche, Agua', 'Mexica, Purépecha', 'Positiva', 'Invisibilidad'),
        ('Piltzintecuhtli', 'Sol Joven, Juventud', 'Mexica', 'Positiva', 'Aceleración Biológica'),
        ('Xólotl', 'Fuego, Dualidad, Monstruosidad', 'Mexica, Mixteca', 'Negativa', 'Transmutación'),
        ('Huracán', 'Viento, Tormenta, Fuego', 'Maya', 'Neutral', 'Control Climático'),
    ]

    for dios in dioses_completos:
        cursor.execute('''
            INSERT OR IGNORE INTO dioses (nombre, dominio_principal, culturas, polaridad, eje_tecnologico)
            VALUES (?, ?, ?, ?, ?)
        ''', dios)

    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM dioses")
    print(f"✓ Total: {cursor.fetchone()[0]} dioses")

def poblar_facciones(conn):
    """Crea facciones políticas y religiosas"""
    print("\n🏛️  Poblando facciones...")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM facciones")
    if cursor.fetchone()[0] > 0:
        print("✓ Facciones ya pobladas")
        return

    # Obtener civilizaciones y dioses
    cursor.execute("SELECT id, nombre FROM civilizaciones")
    civs = dict(cursor.fetchall())

    cursor.execute("SELECT id, nombre FROM dioses LIMIT 5")
    dioses = dict(cursor.fetchall())

    facciones = [
        ('Orden de Quetzalcóatl', 'religiosa', 'Defensores del equilibrio y la sabiduría', None, list(civs.values())[0], 1505, None, None),
        ('Culto de Tezcatlipoca', 'religiosa', 'Adoradores de la sombra y el conflicto', None, list(civs.values())[0], 1510, None, None),
        ('Gremio de Herreros Unidos', 'comercial', 'Asociación de todos los herreros de Aztlán', None, list(civs.values())[1], 1520, None, None),
        ('Guardia del Sol Negro', 'militar', 'Élite militar de guerreros jaguar', None, list(civs.values())[0], 1515, None, None),
        ('Red de las Sombras', 'criminal', 'Organización clandestina de ladrones y espías', None, list(civs.values())[2], 1530, None, None),
        ('Consejo de Sabios', 'politica', 'Asesores y filósofos de las ciudades', None, list(civs.values())[3], 1525, None, None),
    ]

    for faccion in facciones:
        cursor.execute('''
            INSERT INTO facciones
            (nombre, tipo, ideologia, lider_id, civilizacion_base_id, año_fundacion, año_disolucion, sede_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', faccion)

    conn.commit()
    print(f"✓ {len(facciones)} facciones creadas")

def poblar_enfermedades(conn):
    """Crea enfermedades del mundo"""
    print("\n🦠 Poblando enfermedades...")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM enfermedades")
    if cursor.fetchone()[0] > 0:
        print("✓ Enfermedades ya pobladas")
        return

    enfermedades = [
        # Nombre, tipo, gravedad, contagio, vector, síntomas, duracion_dias, mortalidad, curas
        ('Fiebre del Quinto Sol', 'infecciosa', 7, 60, 'aire',
         json.dumps(['fiebre alta', 'delirios', 'debilidad']), 14, 30,
         json.dumps([{'tipo': 'hierba', 'efectividad': 70}])),

        ('Plaga de Obsidiana', 'infecciosa', 9, 80, 'contacto',
         json.dumps(['piel negra', 'sangrado', 'muerte rápida']), 7, 80,
         json.dumps([{'tipo': 'divino', 'efectividad': 90}])),

        ('Mal del Portal', 'magica', 6, 20, 'maldicion',
         json.dumps(['visiones', 'locura temporal', 'cansancio']), 30, 15,
         json.dumps([{'tipo': 'ritual', 'efectividad': 85}])),

        ('Fiebre del Maíz', 'parasitaria', 4, 30, 'agua',
         json.dumps(['dolor estomacal', 'vómito', 'diarrea']), 10, 5,
         json.dumps([{'tipo': 'hierba', 'efectividad': 90}])),

        ('Lepra Divina', 'cronica', 8, 10, 'contacto',
         json.dumps(['manchas piel', 'pérdida sensibilidad', 'deformación']), 3650, 40,
         json.dumps([{'tipo': 'alquimia', 'efectividad': 60}])),

        ('Peste Roja', 'infecciosa', 10, 90, 'insecto',
         json.dumps(['fiebre extrema', 'erupciones rojas', 'hemorragias']), 5, 95,
         json.dumps([{'tipo': 'divino', 'efectividad': 50}])),
    ]

    for enf in enfermedades:
        cursor.execute('''
            INSERT INTO enfermedades
            (nombre, tipo, gravedad, contagio, vector, sintomas, duracion_dias,
             tasa_mortalidad, curas_posibles)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', enf)

    conn.commit()
    print(f"✓ {len(enfermedades)} enfermedades creadas")

def poblar_mutaciones(conn):
    """Crea mutaciones bio-tecnológicas"""
    print("\n🧬 Poblando mutaciones...")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM mutaciones")
    if cursor.fetchone()[0] > 0:
        print("✓ Mutaciones ya pobladas")
        return

    cursor.execute("SELECT id FROM dioses WHERE nombre = 'Ixchel'")
    ixchel_id = cursor.fetchone()[0]

    cursor.execute("SELECT id FROM dioses WHERE nombre = 'Xólotl'")
    xolotl_id = cursor.fetchone()[0]

    mutaciones = [
        # Positivas
        ('Piel Luminiscente', 'fisica', 'positiva', 'divina', ixchel_id, 1, 75, 1,
         'Piel que brilla suavemente en la oscuridad',
         json.dumps({'carisma': +5, 'vision_nocturna': True}), 8),

        ('Visión de Águila', 'sensorial', 'positiva', 'biotecnologica', None, 1, 50, 0,
         'Vista extremadamente aguda',
         json.dumps({'percepcion': +10, 'alcance_visual': 'x3'}), 7),

        ('Regeneración Acelerada', 'fisica', 'positiva', 'divina', ixchel_id, 1, 30, 1,
         'Cura heridas 5 veces más rápido',
         json.dumps({'recuperacion': 'x5', 'resistencia': +15}), 9),

        # Negativas
        ('Alergia Solar', 'fisica', 'negativa', 'radiacion_portal', None, 1, 60, 1,
         'Piel se quema con luz solar',
         json.dumps({'resistencia_sol': -50, 'daño_dia': True}), -6),

        ('Sed de Sangre', 'mental', 'negativa', 'maldicion', xolotl_id, 1, 40, 1,
         'Necesidad compulsiva de sangre',
         json.dumps({'agresion': +20, 'control': -15}), -8),

        # Neutrales
        ('Alas Vestigiales', 'fisica', 'neutral', 'divina', None, 1, 80, 1,
         'Pequeñas alas no funcionales en la espalda',
         json.dumps({'velocidad': +2, 'salto': +3}), 0),

        ('Ojos Heterocromáticos', 'sensorial', 'neutral', 'natural', None, 1, 90, 0,
         'Ojos de diferentes colores',
         json.dumps({'carisma': +2}), 1),
    ]

    for mut in mutaciones:
        cursor.execute('''
            INSERT INTO mutaciones
            (nombre, tipo, polaridad, origen, dios_creador_id, es_heredable,
             probabilidad_herencia, dominante, descripcion_visual, efectos_mecanicos,
             aceptacion_social)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', mut)

    conn.commit()
    print(f"✓ {len(mutaciones)} mutaciones creadas")

def poblar_organizaciones(conn):
    """Crea organizaciones y gremios"""
    print("\n🏴 Poblando organizaciones...")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM organizaciones")
    if cursor.fetchone()[0] > 0:
        print("✓ Organizaciones ya pobladas")
        return

    cursor.execute("SELECT id FROM oficios WHERE nombre = 'Herrero'")
    herrero_id = cursor.fetchone()[0]

    cursor.execute("SELECT id FROM oficios WHERE nombre = 'Alquimista'")
    alquimista_id = cursor.fetchone()[0]

    cursor.execute("SELECT id FROM dioses WHERE nombre = 'Quetzalcóatl'")
    quetza_id = cursor.fetchone()[0]

    cursor.execute("SELECT id FROM civilizaciones LIMIT 1")
    civ_id = cursor.fetchone()[0]

    organizaciones = [
        ('Gremio de Herreros de Obsidiana', 'gremio', herrero_id, None, civ_id, None, None, 1520, None,
         json.dumps({'nivel_herrero': 5}), 50,
         json.dumps(['Descuento 20% en materiales', 'Acceso a forjas del gremio']),
         json.dumps([])),

        ('Academia de Alquimistas', 'academia', alquimista_id, None, civ_id, None, None, 1525, None,
         json.dumps({'nivel_alquimista': 7}), 100,
         json.dumps(['Acceso a laboratorios', 'Recetas exclusivas']),
         json.dumps([])),

        ('Orden del Sol Naciente', 'orden_militar', None, quetza_id, civ_id, None, None, 1515, None,
         json.dumps({'nivel_combate': 8, 'devocion_quetzalcoatl': 7}), 0,
         json.dumps(['Armadura sagrada', 'Entrenamiento élite']),
         json.dumps([])),

        ('Casa de las Flores', 'gremio', None, None, civ_id, None, None, 1530, None,
         json.dumps({'oficio': 'prostituta'}), 10,
         json.dumps(['Protección legal', 'Casa segura']),
         json.dumps([])),
    ]

    for org in organizaciones:
        cursor.execute('''
            INSERT INTO organizaciones
            (nombre, tipo, oficio_asociado_id, dios_patron_id, civilizacion_id,
             lider_id, sede_id, año_fundacion, año_disolucion,
             requisitos_ingreso, cuota_membresia, beneficios, recetas_exclusivas)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', org)

    conn.commit()
    print(f"✓ {len(organizaciones)} organizaciones creadas")

def poblar_artefactos(conn):
    """Crea artefactos divinos legendarios"""
    print("\n✨ Poblando artefactos divinos...")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM artefactos")
    if cursor.fetchone()[0] > 0:
        print("✓ Artefactos ya poblados")
        return

    cursor.execute("SELECT id FROM dioses WHERE nombre = 'Quetzalcóatl'")
    quetza_id = cursor.fetchone()[0]

    cursor.execute("SELECT id FROM dioses WHERE nombre = 'Tezcatlipoca'")
    tezcat_id = cursor.fetchone()[0]

    cursor.execute("SELECT id FROM dioses WHERE nombre = 'Huitzilopochtli'")
    huitzi_id = cursor.fetchone()[0]

    artefactos = [
        ('Corazón de Quetzalcóatl', 'reliquia', quetza_id, 1000, None, 10,
         json.dumps([
             {'nombre': 'Curación Masiva', 'coste': '1 año de vida del portador'},
             {'nombre': 'Resurrección', 'coste': '10 años de vida'}
         ]),
         0, None, 'unico', None, None, 1,
         'Cristal pulsante que contiene el poder de vida de Quetzalcóatl',
         'Creado por Quetzalcóatl para salvar a la primera generación de humanos'),

        ('Espejo de Tezcatlipoca', 'reliquia', tezcat_id, 500, None, 10,
         json.dumps([
             {'nombre': 'Visión del Futuro', 'coste': '1 día de cordura'},
             {'nombre': 'Portal de Sombras', 'coste': 'Consumir alma de enemigo'}
         ]),
         1,
         json.dumps({'descripcion': 'Ver el futuro causa locura temporal'}),
         'unico', None, None, 1,
         'Espejo de obsidiana que muestra verdades ocultas',
         'Usado por Tezcatlipoca para manipular el destino de mortales'),

        ('Macuahuitl del Sol Guerrero', 'arma', huitzi_id, 1200, None, 9,
         json.dumps([
             {'nombre': 'Filo Solar', 'coste': 'Ninguno'},
             {'nombre': 'Llamarada', 'coste': 'Energía vital'}
         ]),
         0, None, 'legendario', None, None, 0,
         'Espada de obsidiana que brilla con luz solar',
         'Forjada en el corazón del sol para el primer guerrero jaguar'),

        ('Grimorio de los Glifos Perdidos', 'grimorio', quetza_id, 1400, None, 8,
         json.dumps([
             {'nombre': 'Conocimiento Absoluto', 'coste': '10 años de vida'},
             {'nombre': 'Crear Vida', 'coste': 'Sacrificio equivalente'}
         ]),
         1,
         json.dumps({'descripcion': 'El conocimiento causa envejecimiento prematuro'}),
         'unico', None, None, 1,
         'Libro antiguo con todos los glifos de creación',
         'Contiene el conocimiento prohibido de los dioses'),
    ]

    for art in artefactos:
        cursor.execute('''
            INSERT INTO artefactos
            (nombre, tipo, dios_creador_id, año_creacion, creador_mortal_id,
             nivel_poder, poderes, tiene_maldicion, maldicion, rareza,
             poseedor_actual_id, lugar_actual_id, esta_perdido,
             descripcion, historia)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', art)

    conn.commit()
    print(f"✓ {len(artefactos)} artefactos creados")

def poblar_recetas_avanzadas(conn):
    """Crea recetas de crafting"""
    print("\n📜 Poblando recetas de crafting...")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM recetas")
    if cursor.fetchone()[0] > 0:
        print("✓ Recetas ya pobladas")
        return

    cursor.execute("SELECT id FROM oficios WHERE nombre = 'Herrero'")
    herrero_id = cursor.fetchone()[0]

    cursor.execute("SELECT id FROM items WHERE nombre = 'Macuahuitl'")
    macua_id = cursor.fetchone()[0]

    cursor.execute("SELECT id FROM items WHERE nombre = 'Martillo'")
    martillo_id = cursor.fetchone()[0]

    recetas = [
        ('Macuahuitl Superior', macua_id, 1, herrero_id, 7, martillo_id, 5, 7,
         'epico', 0, None,
         'Versión mejorada del Macuahuitl con filo más duradero'),

        ('Macuahuitl Legendario', macua_id, 1, herrero_id, 10, martillo_id, 10, 10,
         'legendario', 1, None,
         'El mejor Macuahuitl posible, solo maestros pueden crearlo'),
    ]

    for rec in recetas:
        cursor.execute('''
            INSERT INTO recetas
            (nombre, item_resultado_id, cantidad_resultado, oficio_requerido_id,
             nivel_maestria_minimo, herramienta_requerida_id, tiempo_creacion_dias,
             dificultad, rareza, es_secreta, linaje_id, descripcion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', rec)

    conn.commit()
    print(f"✓ {len(recetas)} recetas creadas")

def poblar_castigos(conn):
    """Crea tipos de castigos"""
    print("\n⚖️  Poblando castigos...")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM castigos")
    if cursor.fetchone()[0] > 0:
        print("✓ Castigos ya poblados")
        return

    castigos = [
        ('Multa Menor', 'multa', 2, None, 'Pago de 50 en trueque', -10, 0),
        ('Multa Mayor', 'multa', 4, None, 'Pago de 200 en trueque', -25, 0),
        ('Prisión Corta', 'prision', 5, 1, 'Encarcelamiento por 1 año', -30, 0),
        ('Prisión Larga', 'prision', 7, 10, 'Encarcelamiento por 10 años', -50, 0),
        ('Trabajo Forzado', 'trabajo_forzado', 6, 5, 'Trabajos forzados por 5 años', -40, 1),
        ('Exilio', 'exilio', 8, None, 'Expulsión permanente de la civilización', -100, 1),
        ('Ejecución Pública', 'ejecucion', 10, None, 'Muerte por decapitación', -100, 1),
        ('Mutilación', 'mutilacion', 9, None, 'Corte de mano derecha', -70, 1),
    ]

    for cast in castigos:
        cursor.execute('''
            INSERT INTO castigos
            (nombre, tipo, gravedad, duracion_años, descripcion,
             afecta_reputacion, afecta_clase_social)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', cast)

    conn.commit()
    print(f"✓ {len(castigos)} castigos creados")

def poblar_festivales(conn):
    """Crea festivales religiosos"""
    print("\n🎉 Poblando festivales...")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM festivales")
    if cursor.fetchone()[0] > 0:
        print("✓ Festivales ya poblados")
        return

    cursor.execute("SELECT id FROM dioses WHERE nombre = 'Quetzalcóatl'")
    quetza_id = cursor.fetchone()[0]

    cursor.execute("SELECT id FROM civilizaciones LIMIT 1")
    civ_id = cursor.fetchone()[0]

    festivales = [
        ('Festival del Quinto Sol', 'religioso', 52, quetza_id, civ_id,
         'Celebración cada 52 años del ciclo solar',
         json.dumps(['Sacrificios', 'Danzas', 'Fuego Nuevo'])),

        ('Fiesta de la Cosecha', 'cosecha', 1, None, civ_id,
         'Celebración anual de la cosecha',
         json.dumps(['Ofrendas', 'Banquetes', 'Competencias'])),
    ]

    for fest in festivales:
        cursor.execute('''
            INSERT INTO festivales
            (nombre, tipo, frecuencia_años, dios_asociado_id, civilizacion_id,
             descripcion, actividades)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', fest)

    conn.commit()
    print(f"✓ {len(festivales)} festivales creados")

def main():
    print("\n" + "="*80)
    print("POBLANDO TODOS LOS SISTEMAS COMPLETOS")
    print("="*80)

    conn = sqlite3.connect('quinto_sol.db')

    try:
        ejecutar_esquema_completo(conn)
        verificar_y_completar_dioses(conn)
        poblar_facciones(conn)
        poblar_enfermedades(conn)
        poblar_mutaciones(conn)
        poblar_organizaciones(conn)
        poblar_artefactos(conn)
        poblar_recetas_avanzadas(conn)
        poblar_castigos(conn)
        poblar_festivales(conn)

        print("\n" + "="*80)
        print("✓ TODOS LOS SISTEMAS POBLADOS EXITOSAMENTE")
        print("="*80 + "\n")

        # Estadísticas finales
        cursor = conn.cursor()

        estadisticas = [
            ("Dioses", "dioses"),
            ("Facciones", "facciones"),
            ("Enfermedades", "enfermedades"),
            ("Mutaciones", "mutaciones"),
            ("Organizaciones", "organizaciones"),
            ("Artefactos Divinos", "artefactos"),
            ("Recetas de Crafting", "recetas"),
            ("Castigos", "castigos"),
            ("Festivales", "festivales"),
        ]

        print("📊 Estadísticas:")
        for nombre, tabla in estadisticas:
            cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
            count = cursor.fetchone()[0]
            print(f"  • {nombre}: {count}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        conn.close()

if __name__ == '__main__':
    main()
