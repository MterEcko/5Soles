#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Poblar Sistema de Especies Sirvientes y Fauna
Portales del Quinto Sol
"""

import sqlite3
import json

DB_PATH = 'quinto_sol.db'

def aplicar_schema():
    """Aplicar schema de especies y fauna"""
    print("📋 Aplicando schema de especies y fauna...")

    conn = sqlite3.connect(DB_PATH)

    with open('schema_especies_fauna.sql', 'r', encoding='utf-8') as f:
        schema_sql = f.read()

    conn.executescript(schema_sql)
    conn.commit()
    conn.close()

    print("✅ Schema aplicado correctamente")

def poblar_stats_especies():
    """Poblar stats evolutivos de las 6 especies sirvientes"""
    print("\n📊 Poblando stats evolutivos de especies...")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Obtener IDs de especies
    cursor.execute("SELECT id, nombre FROM especies WHERE id > 1")  # Excluir humanos (id=1)
    especies = cursor.fetchall()

    especies_config = {
        'Nahuas': {
            1500: {'int': 150, 'vida': 300, 'fuerza': 80, 'agilidad': 120, 'magia': 180, 'sigilo': 100, 'hijos': (2, 4)},
            3000: {'int': 100, 'vida': 250, 'fuerza': 85, 'agilidad': 115, 'magia': 150, 'sigilo': 100, 'hijos': (3, 5)}
        },
        'Tlaloqueh': {
            1500: {'int': 130, 'vida': 250, 'fuerza': 110, 'agilidad': 130, 'magia': 200, 'sigilo': 90, 'hijos': (2, 4)},
            3000: {'int': 100, 'vida': 220, 'fuerza': 115, 'agilidad': 125, 'magia': 170, 'sigilo': 95, 'hijos': (3, 5)}
        },
        'Tezcatl': {
            1500: {'int': 140, 'vida': 220, 'fuerza': 100, 'agilidad': 150, 'magia': 170, 'sigilo': 200, 'hijos': (2, 3)},
            3000: {'int': 100, 'vida': 180, 'fuerza': 105, 'agilidad': 140, 'magia': 150, 'sigilo': 180, 'hijos': (3, 4)}
        },
        'Xipeh': {
            1500: {'int': 120, 'vida': 200, 'fuerza': 170, 'agilidad': 130, 'magia': 90, 'sigilo': 80, 'hijos': (3, 5)},
            3000: {'int': 100, 'vida': 150, 'fuerza': 150, 'agilidad': 120, 'magia': 95, 'sigilo': 85, 'hijos': (4, 6)}
        },
        'Coatlicueh': {
            1500: {'int': 135, 'vida': 320, 'fuerza': 130, 'agilidad': 90, 'magia': 190, 'sigilo': 70, 'hijos': (2, 3)},
            3000: {'int': 100, 'vida': 280, 'fuerza': 125, 'agilidad': 95, 'magia': 160, 'sigilo': 75, 'hijos': (3, 4)}
        },
        'Mictlanecah': {
            1500: {'int': 145, 'vida': 250, 'fuerza': 90, 'agilidad': 100, 'magia': 220, 'sigilo': 140, 'hijos': (2, 4)},
            3000: {'int': 100, 'vida': 200, 'fuerza': 95, 'agilidad': 105, 'magia': 180, 'sigilo': 130, 'hijos': (3, 5)}
        }
    }

    for especie_id, especie_nombre in especies:
        if especie_nombre in especies_config:
            config = especies_config[especie_nombre]

            # Stats para año 1500
            stats_1500 = config[1500]
            cursor.execute("""
                INSERT INTO especies_stats (
                    especie_id, año, inteligencia_base, esperanza_vida,
                    resistencia_fisica, resistencia_magica,
                    fertilidad_min, fertilidad_max, edad_madurez,
                    fuerza, agilidad, magia, sigilo
                ) VALUES (?, 1500, ?, ?, 150, 200, ?, ?, 25, ?, ?, ?, ?)
            """, (
                especie_id,
                stats_1500['int'],
                stats_1500['vida'],
                stats_1500['hijos'][0],
                stats_1500['hijos'][1],
                stats_1500['fuerza'],
                stats_1500['agilidad'],
                stats_1500['magia'],
                stats_1500['sigilo']
            ))

            # Stats para año 3000
            stats_3000 = config[3000]
            cursor.execute("""
                INSERT INTO especies_stats (
                    especie_id, año, inteligencia_base, esperanza_vida,
                    resistencia_fisica, resistencia_magica,
                    fertilidad_min, fertilidad_max, edad_madurez,
                    fuerza, agilidad, magia, sigilo
                ) VALUES (?, 3000, ?, ?, 120, 130, ?, ?, 20, ?, ?, ?, ?)
            """, (
                especie_id,
                stats_3000['int'],
                stats_3000['vida'],
                stats_3000['hijos'][0],
                stats_3000['hijos'][1],
                stats_3000['fuerza'],
                stats_3000['agilidad'],
                stats_3000['magia'],
                stats_3000['sigilo']
            ))

            print(f"  ✓ {especie_nombre}: Stats 1500-3000 añadidos")

    conn.commit()
    conn.close()
    print(f"✅ Stats de {len(especies)} especies configurados")

def poblar_habilidades_especies():
    """Poblar habilidades especiales de cada especie"""
    print("\n🔮 Poblando habilidades especiales...")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Obtener IDs de especies
    cursor.execute("SELECT id, nombre FROM especies WHERE id > 1")
    especies = {nombre: id for id, nombre in cursor.fetchall()}

    habilidades = [
        # NAHUAS
        (especies.get('Nahuas'), 'Sabiduría Ancestral', 'Acceso a conocimientos antiguos', 'pasiva', 150, 0, 0),
        (especies.get('Nahuas'), 'Lengua de Serpiente', 'Persuasión mejorada +50%', 'pasiva', 150, 0, 0),
        (especies.get('Nahuas'), 'Escamas Protectoras', 'Armadura natural +20', 'pasiva', 120, 0, 0),

        # TLALOQUEH
        (especies.get('Tlaloqueh'), 'Respiración Acuática', 'Respirar bajo el agua indefinidamente', 'pasiva', 200, 0, 0),
        (especies.get('Tlaloqueh'), 'Invocar Lluvia', 'Crear lluvia en un área', 'activa', 150, 50, 3),
        (especies.get('Tlaloqueh'), 'Forma de Agua', 'Convertirse en agua durante 10 minutos', 'activa', 180, 80, 7),

        # TEZCATL
        (especies.get('Tezcatl'), 'Visión Nocturna', 'Ver perfectamente en oscuridad total', 'pasiva', 200, 0, 0),
        (especies.get('Tezcatl'), 'Camuflaje de Sombras', 'Invisibilidad en áreas oscuras', 'activa', 180, 30, 1),
        (especies.get('Tezcatl'), 'Golpe Silencioso', 'Ataque garantizado crítico si no detectado', 'activa', 200, 20, 0),

        # XIPEH
        (especies.get('Xipeh'), 'Regeneración Rápida', 'Recuperar 15% salud cada día', 'pasiva', 150, 0, 0),
        (especies.get('Xipeh'), 'Resistencia al Dolor', 'Ignorar penalizaciones de heridas leves', 'pasiva', 200, 0, 0),
        (especies.get('Xipeh'), 'Furia de Batalla', 'Daño +100% cuando salud < 30%', 'pasiva', 180, 0, 0),

        # COATLICUEH
        (especies.get('Coatlicueh'), 'Comunión con Plantas', 'Comunicarse con vegetación', 'pasiva', 150, 0, 0),
        (especies.get('Coatlicueh'), 'Curación Natural', 'Curar heridas con hierbas (+50% efectividad)', 'activa', 200, 25, 1),
        (especies.get('Coatlicueh'), 'Inmunidad a Venenos', 'Inmunidad total a venenos naturales', 'pasiva', 250, 0, 0),

        # MICTLANECAH
        (especies.get('Mictlanecah'), 'Visión de Muerte', 'Ver si alguien morirá pronto', 'activa', 180, 40, 7),
        (especies.get('Mictlanecah'), 'Hablar con Muertos', 'Comunicarse con espíritus', 'activa', 200, 60, 3),
        (especies.get('Mictlanecah'), 'Resistencia a Enfermedades', 'Inmunidad a 90% de enfermedades', 'pasiva', 300, 0, 0),
    ]

    for hab in habilidades:
        if hab[0] is not None:  # Solo si la especie existe
            cursor.execute("""
                INSERT INTO especies_habilidades (
                    especie_id, nombre, descripcion, tipo, potencia, costo_mana, cooldown_dias
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, hab)

    conn.commit()
    conn.close()
    print(f"✅ {len(habilidades)} habilidades añadidas")

def poblar_especies_animales():
    """Poblar especies de animales (NO genealógicos)"""
    print("\n🐾 Poblando especies animales...")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # ANIMALES DOMÉSTICOS
    animales_domesticos = [
        ('Xoloitzcuintle', 'Itzcuintli', 'domestico', 'baja', 50,
         'Perro sagrado azteca sin pelo', 'mediano', 'omnivoro', 120,
         json.dumps([{'nombre': 'Guía Espiritual', 'desc': 'Guía almas al Mictlán'}]),
         json.dumps(['ciudad', 'pueblo', 'campo']), 0.6, 1, 1, 1),

        ('Pavo', 'Huexolotl', 'domestico', 'ninguna', 20,
         'Ave de corral para alimento y plumas', 'mediano', 'omnivoro', 80,
         json.dumps([]),
         json.dumps(['ciudad', 'pueblo', 'campo']), 0.3, 1, 1, 1),

        ('Guajolote', 'Totolin', 'domestico', 'ninguna', 15,
         'Ave similar al pavo, común en granjas', 'mediano', 'omnivoro', 70,
         json.dumps([]),
         json.dumps(['pueblo', 'campo']), 0.35, 1, 1, 1),

        ('Conejo', 'Tochtli', 'domestico', 'ninguna', 10,
         'Conejo para alimento y piel', 'pequeño', 'herbivoro', 150,
         json.dumps([]),
         json.dumps(['campo', 'bosque']), 0.4, 1, 1, 1),
    ]

    # ANIMALES SALVAJES COMUNES
    animales_salvajes = [
        ('Venado', 'Mazatl', 'salvaje', 'baja', 80,
         'Venado de cola blanca', 'grande', 'herbivoro', 180,
         json.dumps([]),
         json.dumps(['bosque', 'montaña', 'campo']), 0.3, 1, 1, 5),

        ('Coyote', 'Coyotl', 'salvaje', 'media', 60,
         'Coyote cazador nocturno', 'mediano', 'carnivoro', 160,
         json.dumps([{'nombre': 'Visión Nocturna', 'desc': 'Ve en la oscuridad'}]),
         json.dumps(['bosque', 'montaña', 'desierto']), 0.25, 1, 1, 8),

        ('Jaguar', 'Ocelotl', 'salvaje', 'alta', 500,
         'Jaguar, depredador supremo', 'grande', 'carnivoro', 170,
         json.dumps([{'nombre': 'Mordida Aplastante', 'desc': 'Daño masivo'}]),
         json.dumps(['bosque', 'selva']), 0.05, 1, 1, 20),

        ('Puma', 'Miztli', 'salvaje', 'alta', 400,
         'Puma, cazador sigiloso', 'grande', 'carnivoro', 190,
         json.dumps([{'nombre': 'Sigilo', 'desc': 'Movimiento silencioso'}]),
         json.dumps(['montaña', 'bosque']), 0.1, 1, 1, 18),

        ('Serpiente', 'Coatl', 'salvaje', 'media', 30,
         'Serpiente venenosa', 'pequeño', 'carnivoro', 90,
         json.dumps([{'nombre': 'Veneno', 'desc': 'Mordida venenosa'}]),
         json.dumps(['bosque', 'selva', 'desierto']), 0.35, 1, 1, 5),

        ('Águila Real', 'Cuauhtli', 'salvaje', 'baja', 200,
         'Águila majestuosa', 'mediano', 'carnivoro', 220,
         json.dumps([{'nombre': 'Vista de Águila', 'desc': 'Visión lejana'}]),
         json.dumps(['montaña', 'bosque']), 0.08, 1, 1, 15),

        ('Armadillo', 'Ayotochtli', 'salvaje', 'ninguna', 25,
         'Armadillo con caparazón', 'pequeño', 'omnivoro', 70,
         json.dumps([{'nombre': 'Armadura Natural', 'desc': 'Defensa +20'}]),
         json.dumps(['bosque', 'campo']), 0.2, 1, 1, 3),

        ('Jabalí', 'Pitzotl', 'salvaje', 'media', 100,
         'Jabalí agresivo', 'grande', 'omnivoro', 140,
         json.dumps([{'nombre': 'Carga', 'desc': 'Ataque de embestida'}]),
         json.dumps(['bosque', 'montaña']), 0.15, 1, 1, 10),
    ]

    # ANIMALES ACUÁTICOS
    animales_acuaticos = [
        ('Ajolote', 'Axolotl', 'salvaje', 'ninguna', 150,
         'Salamandra acuática regenerativa', 'pequeño', 'carnivoro', 50,
         json.dumps([{'nombre': 'Regeneración', 'desc': 'Regenera extremidades'}]),
         json.dumps(['agua', 'lago']), 0.15, 1, 1, 12),

        ('Pez', 'Michin', 'salvaje', 'ninguna', 5,
         'Pez común de río', 'pequeño', 'omnivoro', 100,
         json.dumps([]),
         json.dumps(['agua', 'rio', 'lago']), 0.7, 1, 1, 1),

        ('Tortuga', 'Ayotl', 'salvaje', 'ninguna', 40,
         'Tortuga de río', 'mediano', 'omnivoro', 40,
         json.dumps([{'nombre': 'Caparazón', 'desc': 'Defensa +30'}]),
         json.dumps(['rio', 'lago']), 0.25, 1, 1, 5),

        ('Cocodrilo', 'Acuetzpalin', 'salvaje', 'extrema', 800,
         'Cocodrilo gigante', 'gigante', 'carnivoro', 90,
         json.dumps([{'nombre': 'Mandíbulas Letales', 'desc': 'Daño crítico'}]),
         json.dumps(['pantano', 'rio']), 0.05, 1, 1, 25),
    ]

    # ANIMALES MITOLÓGICOS
    animales_mitologicos = [
        ('Ahuízotl', 'Ahuízotl', 'mitologico', 'extrema', 10000,
         'Criatura acuática con mano en la cola que ahoga víctimas', 'grande', 'carnivoro', 130,
         json.dumps([
             {'nombre': 'Mano de Cola', 'desc': 'Agarra y ahoga víctimas'},
             {'nombre': 'Robar Esencia', 'desc': 'Roba uñas y ojos de muertos'}
         ]),
         json.dumps(['lago', 'agua']), 0.0005, 1, 1, 50),

        ('Cipactli', 'Cipactli', 'mitologico', 'legendaria', 50000,
         'Cocodrilo primordial de la creación del mundo', 'gigante', 'carnivoro', 60,
         json.dumps([
             {'nombre': 'Terremoto', 'desc': 'Causa terremotos al moverse'},
             {'nombre': 'Hambre Infinita', 'desc': 'Devora todo a su paso'}
         ]),
         json.dumps(['mar', 'cenote']), 0.0001, 0, 0, 100),

        ('Nagual (Jaguar)', 'Nagual-Ocelotl', 'mitologico', 'media', 0,
         'Animal espiritual forma jaguar', 'grande', 'carnivoro', 200,
         json.dumps([
             {'nombre': 'Vínculo Psíquico', 'desc': 'Conexión mental con dueño'},
             {'nombre': 'Transformación', 'desc': 'Compartir forma con dueño'}
         ]),
         json.dumps(['bosque', 'selva']), 0.001, 0, 0, 40),

        ('Nagual (Águila)', 'Nagual-Cuauhtli', 'mitologico', 'baja', 0,
         'Animal espiritual forma águila', 'mediano', 'carnivoro', 250,
         json.dumps([
             {'nombre': 'Vínculo Psíquico', 'desc': 'Conexión mental con dueño'},
             {'nombre': 'Visión Compartida', 'desc': 'Dueño ve lo que ve el águila'}
         ]),
         json.dumps(['montaña', 'bosque']), 0.001, 0, 0, 40),

        ('Nagual (Serpiente)', 'Nagual-Coatl', 'mitologico', 'alta', 0,
         'Animal espiritual forma serpiente', 'mediano', 'carnivoro', 140,
         json.dumps([
             {'nombre': 'Vínculo Psíquico', 'desc': 'Conexión mental con dueño'},
             {'nombre': 'Veneno Espiritual', 'desc': 'Veneno afecta magia'}
         ]),
         json.dumps(['selva', 'bosque']), 0.001, 0, 0, 40),

        ('Nagual (Coyote)', 'Nagual-Coyotl', 'mitologico', 'media', 0,
         'Animal espiritual forma coyote', 'mediano', 'carnivoro', 180,
         json.dumps([
             {'nombre': 'Vínculo Psíquico', 'desc': 'Conexión mental con dueño'},
             {'nombre': 'Astucia Compartida', 'desc': '+30 Inteligencia a dueño'}
         ]),
         json.dumps(['desierto', 'montaña']), 0.001, 0, 0, 40),

        ('Quetzal', 'Quetzal', 'mitologico', 'ninguna', 5000,
         'Ave sagrada de Quetzalcóatl con plumas iridiscentes', 'pequeño', 'omnivoro', 200,
         json.dumps([
             {'nombre': 'Bendición', 'desc': '+10% Sabiduría temporal'},
             {'nombre': 'Plumas Divinas', 'desc': 'Plumas valen 100 oro cada una'}
         ]),
         json.dumps(['selva', 'bosque']), 0.005, 0, 1, 30),

        ('Tecolotl Gigante', 'Tecolotl', 'mitologico', 'media', 3000,
         'Búho gigante de 3 metros, mensajero de muerte', 'grande', 'carnivoro', 110,
         json.dumps([
             {'nombre': 'Presagio de Muerte', 'desc': 'Revela muerte cercana'},
             {'nombre': 'Vuelo Silencioso', 'desc': 'Movimiento totalmente silencioso'}
         ]),
         json.dumps(['ruina', 'cementerio', 'bosque']), 0.002, 1, 1, 35),

        ('Lagarto de Fuego', 'Cuetzpalin', 'mitologico', 'alta', 7000,
         'Lagarto que escupe fuego volcánico', 'grande', 'carnivoro', 100,
         json.dumps([
             {'nombre': 'Aliento de Fuego', 'desc': 'Daño de fuego masivo'},
             {'nombre': 'Inmunidad al Fuego', 'desc': 'Inmune al fuego'}
         ]),
         json.dumps(['volcan', 'desierto']), 0.0008, 1, 1, 45),

        ('Jaguar Blanco', 'Ocelopilli', 'mitologico', 'alta', 15000,
         'Jaguar albino criatura lunar extremadamente raro', 'grande', 'carnivoro', 190,
         json.dumps([
             {'nombre': 'Invisibilidad Nocturna', 'desc': 'Invisible en la noche'},
             {'nombre': 'Cacería Perfecta', 'desc': 'Ataque crítico garantizado'}
         ]),
         json.dumps(['selva']), 0.0003, 1, 1, 50),

        ('Xoloitzcuintle Sagrado', 'Itzcuintli Tlamacazqui', 'mitologico', 'ninguna', 8000,
         'Xoloitzcuintle con marcas divinas, guía al Mictlán', 'mediano', 'omnivoro', 130,
         json.dumps([
             {'nombre': 'Guía al Mictlán', 'desc': 'Puede resucitar a dueño 1 vez'},
             {'nombre': 'Protección Espiritual', 'desc': '+50% resistencia magia oscura'}
         ]),
         json.dumps(['templo', 'ciudad']), 0.003, 1, 1, 25),
    ]

    todos_animales = animales_domesticos + animales_salvajes + animales_acuaticos + animales_mitologicos

    for animal in todos_animales:
        cursor.execute("""
            INSERT INTO especies_animales (
                nombre_comun, nombre_nahuatl, categoria, peligrosidad, valor_mercado,
                descripcion, tamaño, dieta, velocidad,
                habilidades_especiales, biomas_preferidos,
                rareza, es_vendible, es_capturable, nivel_min_captura
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, animal)

    conn.commit()
    conn.close()
    print(f"✅ {len(todos_animales)} especies animales añadidas")
    print(f"   - Domésticos: {len(animales_domesticos)}")
    print(f"   - Salvajes: {len(animales_salvajes)}")
    print(f"   - Acuáticos: {len(animales_acuaticos)}")
    print(f"   - Mitológicos: {len(animales_mitologicos)}")

def main():
    """Función principal"""
    print("=" * 70)
    print("POBLAR SISTEMA DE ESPECIES Y FAUNA")
    print("Portales del Quinto Sol")
    print("=" * 70)

    # Aplicar schema
    aplicar_schema()

    # Poblar datos
    poblar_stats_especies()
    poblar_habilidades_especies()
    poblar_especies_animales()

    print("\n" + "=" * 70)
    print("✅ SISTEMA DE ESPECIES Y FAUNA COMPLETADO")
    print("=" * 70)

    # Resumen
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM especies_stats")
    total_stats = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM especies_habilidades")
    total_habilidades = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM especies_animales")
    total_especies_animales = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM especies_animales WHERE categoria = 'mitologico'")
    total_mitologicos = cursor.fetchone()[0]

    print(f"\n📊 RESUMEN:")
    print(f"   - Stats evolutivos: {total_stats} registros")
    print(f"   - Habilidades especiales: {total_habilidades} habilidades")
    print(f"   - Especies animales: {total_especies_animales} especies")
    print(f"   - Animales mitológicos: {total_mitologicos} especies")

    conn.close()

if __name__ == '__main__':
    main()
