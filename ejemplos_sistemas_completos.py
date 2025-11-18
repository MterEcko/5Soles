#!/usr/bin/env python3
"""
Ejemplos completos de TODOS los sistemas integrados
Demuestra: Combate, Reputación, Enfermedades, Crafting, Justicia,
          Mutaciones, Organizaciones, Artefactos, Clima
"""

import sqlite3
import random
import json
from datetime import datetime

def ejemplo_batalla_epica(conn):
    """
    Ejemplo: Batalla entre dos guerreros
    - Heridas
    - Cambios de reputación
    - Memoria del evento
    """
    print("\n" + "="*80)
    print("EJEMPLO 1: BATALLA ÉPICA CON CONSECUENCIAS")
    print("="*80 + "\n")

    cursor = conn.cursor()

    # Obtener dos guerreros
    cursor.execute('''
        SELECT p.id, p.nombre_completo
        FROM personas p
        JOIN persona_oficios po ON p.id = po.persona_id
        JOIN oficios o ON po.oficio_id = o.id
        WHERE o.nombre = 'Guerrero' AND p.es_npc = 1
        LIMIT 2
    ''')

    guerreros = cursor.fetchall()

    if len(guerreros) < 2:
        # Crear guerreros
        print("📝 Creando guerreros...")

        cursor.execute("SELECT id FROM especies WHERE nombre = 'Humanos I'")
        especie_id = cursor.fetchone()[0]

        cursor.execute("SELECT id FROM civilizaciones LIMIT 2")
        civs = cursor.fetchall()

        cursor.execute("SELECT id FROM oficios WHERE nombre = 'Guerrero'")
        guerrero_oficio = cursor.fetchone()[0]

        # Guerrero 1
        cursor.execute('''
            INSERT INTO personas
            (nombre, apellido, especie_id, genero, año_nacimiento, civilizacion_id,
             clase_social, es_npc)
            VALUES ('Tlacaelel', 'Jaguar Sangriento', ?, 'masculino', 1490, ?, 'guerrero', 1)
        ''', (especie_id, civs[0][0]))
        g1_id = cursor.lastrowid

        cursor.execute('''
            INSERT INTO persona_oficios (persona_id, oficio_id, año_inicio, nivel_maestria, es_principal)
            VALUES (?, ?, 1510, 9, 1)
        ''', (g1_id, guerrero_oficio))

        # Guerrero 2
        cursor.execute('''
            INSERT INTO personas
            (nombre, apellido, especie_id, genero, año_nacimiento, civilizacion_id,
             clase_social, es_npc)
            VALUES ('Xicoténcatl', 'Águila del Norte', ?, 'masculino', 1492, ?, 'guerrero', 1)
        ''', (especie_id, civs[1][0] if len(civs) > 1 else civs[0][0]))
        g2_id = cursor.lastrowid

        cursor.execute('''
            INSERT INTO persona_oficios (persona_id, oficio_id, año_inicio, nivel_maestria, es_principal)
            VALUES (?, ?, 1512, 8, 1)
        ''', (g2_id, guerrero_oficio))

        guerreros = [(g1_id, 'Tlacaelel Jaguar Sangriento'), (g2_id, 'Xicoténcatl Águila del Norte')]

    g1_id, g1_nombre = guerreros[0]
    g2_id, g2_nombre = guerreros[1]

    print(f"⚔️  Combatientes:")
    print(f"   {g1_nombre} (ID: {g1_id})")
    print(f"   vs")
    print(f"   {g2_nombre} (ID: {g2_id})")

    # Crear batalla
    cursor.execute("SELECT id FROM pueblos_ciudades LIMIT 1")
    lugar_id = cursor.fetchone()[0]

    año_batalla = 1550

    cursor.execute('''
        INSERT INTO batallas
        (nombre, tipo, año, lugar_id, atacante_persona_id, defensor_persona_id,
         ganador, bajas_atacante, bajas_defensor, causa, consecuencias)
        VALUES ('Duelo por el Honor', 'duelo', ?, ?, ?, ?, 'atacante', 0, 0,
                'Disputa por tierras', 'El ganador se lleva la tierra disputada')
    ''', (año_batalla, lugar_id, g1_id, g2_id))
    batalla_id = cursor.lastrowid

    print(f"\n💥 Batalla creada: 'Duelo por el Honor' ({año_batalla})")

    # Registrar participantes
    cursor.execute('''
        INSERT INTO batalla_participantes
        (batalla_id, persona_id, bando, rol, resultado, enemigos_eliminados)
        VALUES (?, ?, 'atacante', 'heroe', 'sobrevivio', 1)
    ''', (batalla_id, g1_id))

    cursor.execute('''
        INSERT INTO batalla_participantes
        (batalla_id, persona_id, bando, rol, resultado, enemigos_eliminados)
        VALUES (?, ?, 'defensor', 'heroe', 'muerto', 0)
    ''', (batalla_id, g2_id))

    print(f"   {g1_nombre}: GANADOR (sobrevivió)")
    print(f"   {g2_nombre}: PERDEDOR (murió)")

    # Crear herida para el ganador
    cursor.execute('''
        INSERT INTO heridas
        (persona_id, tipo, parte_cuerpo, causa, año_ocurrencia,
         dias_recuperacion, es_permanente, cicatriz_visible, penalizacion)
        VALUES (?, 'grave', 'brazo_izq', 'espada', ?, 90, 1, 1, ?)
    ''', (g1_id, año_batalla, json.dumps({'combate': -5, 'fuerza': -3})))

    print(f"\n🩹 {g1_nombre} recibió herida grave en brazo izquierdo")
    print("   └─ Cicatriz permanente visible")
    print("   └─ Penalización: -5 combate, -3 fuerza")

    # Actualizar muerte del perdedor
    cursor.execute('''
        UPDATE personas
        SET año_muerte = ?, causa_muerte = 'combate'
        WHERE id = ?
    ''', (año_batalla, g2_id))

    print(f"\n💀 {g2_nombre} murió en combate")

    # Crear memoria para el ganador
    cursor.execute('''
        INSERT INTO memoria_npc
        (npc_id, tipo_memoria, año, titulo, descripcion, importancia, emocion)
        VALUES (?, 'evento', ?, 'Victoria en Duelo',
                ?, 10, 'orgullo')
    ''', (g1_id, año_batalla, f'Derroté a {g2_nombre} en duelo. Gané honor pero perdí movilidad en mi brazo.'))

    # Actualizar reputación del ganador
    cursor.execute("SELECT id FROM civilizaciones LIMIT 1")
    civ_id = cursor.fetchone()[0]

    cursor.execute('''
        INSERT OR REPLACE INTO persona_reputacion
        (persona_id, civilizacion_id, nivel_reputacion, titulos, modificador_precio)
        VALUES (?, ?, 50, ?, 0.9)
    ''', (g1_id, civ_id, json.dumps(['Vencedor del Duelo por el Honor'])))

    print(f"\n🌟 {g1_nombre} ganó reputación:")
    print("   └─ +50 puntos de reputación")
    print("   └─ Título: 'Vencedor del Duelo por el Honor'")
    print("   └─ 10% descuento en comercio")

    conn.commit()
    print("\n✓ Batalla completa registrada con todas sus consecuencias")

    return g1_id, g2_id, batalla_id


def ejemplo_epidemia_y_curacion(conn):
    """
    Ejemplo: Epidemia azota una ciudad
    - Alquimista cura enfermos
    - Gana reputación
    - Algunos mueren
    """
    print("\n" + "="*80)
    print("EJEMPLO 2: EPIDEMIA Y EL ALQUIMISTA SALVADOR")
    print("="*80 + "\n")

    cursor = conn.cursor()

    # Obtener enfermedad
    cursor.execute("SELECT id, nombre FROM enfermedades WHERE nombre = 'Fiebre del Quinto Sol'")
    enfermedad_id, enf_nombre = cursor.fetchone()

    print(f"🦠 Epidemia: {enf_nombre}")

    # Crear epidemia
    cursor.execute("SELECT id, nombre FROM pueblos_ciudades LIMIT 1")
    lugar_id, lugar_nombre = cursor.fetchone()

    año_epidemia = 1560

    cursor.execute('''
        INSERT INTO epidemias
        (nombre, enfermedad_id, año_inicio, año_fin, lugar_origen_id,
         infectados_totales, muertes_totales, cuarentena_aplicada, cura_encontrada)
        VALUES ('La Gran Fiebre del 1560', ?, ?, ?, ?, 200, 50, 1, 1)
    ''', (enfermedad_id, año_epidemia, año_epidemia + 1, lugar_id))
    epidemia_id = cursor.lastrowid

    print(f"   Lugar: {lugar_nombre}")
    print(f"   Año: {año_epidemia}")
    print(f"   Infectados: 200")
    print(f"   Muertes: 50")

    # Buscar o crear alquimista
    cursor.execute('''
        SELECT p.id, p.nombre_completo
        FROM personas p
        JOIN persona_oficios po ON p.id = po.persona_id
        JOIN oficios o ON po.oficio_id = o.id
        WHERE o.nombre = 'Alquimista' AND p.año_muerte IS NULL
        LIMIT 1
    ''')

    alquimista = cursor.fetchone()

    if not alquimista:
        # Crear alquimista heroico
        cursor.execute("SELECT id FROM especies WHERE nombre = 'Humanos I'")
        especie_id = cursor.fetchone()[0]

        cursor.execute("SELECT id FROM civilizaciones LIMIT 1")
        civ_id = cursor.fetchone()[0]

        cursor.execute("SELECT id FROM oficios WHERE nombre = 'Alquimista'")
        alq_oficio = cursor.fetchone()[0]

        cursor.execute('''
            INSERT INTO personas
            (nombre, apellido, especie_id, genero, año_nacimiento, civilizacion_id,
             clase_social, es_npc)
            VALUES ('Nezahualcóyotl', 'el Sabio', ?, 'masculino', 1500, ?, 'sacerdote', 1)
        ''', (especie_id, civ_id))
        alq_id = cursor.lastrowid

        cursor.execute('''
            INSERT INTO persona_oficios (persona_id, oficio_id, año_inicio, nivel_maestria, es_principal)
            VALUES (?, ?, 1520, 10, 1)
        ''', (alq_id, alq_oficio))

        alquimista = (alq_id, 'Nezahualcóyotl el Sabio')

    alq_id, alq_nombre = alquimista

    print(f"\n🧪 Alquimista: {alq_nombre}")

    # Infectar a 5 NPCs
    cursor.execute("SELECT id, nombre_completo FROM personas WHERE es_npc = 1 AND año_muerte IS NULL LIMIT 5")
    enfermos = cursor.fetchall()

    curados = 0
    muertos = 0

    for enfermo_id, enfermo_nombre in enfermos:
        # 70% de probabilidad de curación
        se_cura = random.random() < 0.7

        cursor.execute('''
            INSERT INTO persona_enfermedades
            (persona_id, enfermedad_id, año_contagio, año_recuperacion,
             estado, curandero_id, resultado)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (enfermo_id, enfermedad_id, año_epidemia,
              año_epidemia + 1 if se_cura else None,
              'recuperado' if se_cura else 'muerto',
              alq_id,
              'recuperado' if se_cura else 'muerto'))

        if se_cura:
            curados += 1
            print(f"   ✓ {enfermo_nombre}: CURADO")
        else:
            muertos += 1
            cursor.execute('''
                UPDATE personas
                SET año_muerte = ?, causa_muerte = 'enfermedad'
                WHERE id = ?
            ''', (año_epidemia, enfermo_id))
            print(f"   ✗ {enfermo_nombre}: MURIÓ")

    print(f"\n📊 Resultado:")
    print(f"   Curados: {curados}/5")
    print(f"   Muertos: {muertos}/5")

    # Reputación heroica para el alquimista
    cursor.execute("SELECT id FROM civilizaciones LIMIT 1")
    civ_id = cursor.fetchone()[0]

    cursor.execute('''
        INSERT OR REPLACE INTO persona_reputacion
        (persona_id, civilizacion_id, nivel_reputacion, titulos, hazañas_conocidas, modificador_precio)
        VALUES (?, ?, 80, ?, ?, 0.7)
    ''', (alq_id, civ_id,
          json.dumps(['Salvador de la Gran Fiebre', 'Maestro Alquimista']),
          json.dumps([f'Curó a {curados} personas durante la epidemia del {año_epidemia}'])))

    print(f"\n🌟 {alq_nombre} ahora es un HÉROE:")
    print("   └─ +80 puntos de reputación")
    print("   └─ Título: 'Salvador de la Gran Fiebre'")
    print("   └─ 30% descuento en todos los comercios")

    conn.commit()
    print("\n✓ Epidemia completa con curaciones y muertes registradas")

    return alq_id, epidemia_id


def ejemplo_crimen_y_justicia(conn):
    """
    Ejemplo: Ladrón roba, es atrapado, juzgado y castigado
    """
    print("\n" + "="*80)
    print("EJEMPLO 3: CRIMEN, JUICIO Y CASTIGO")
    print("="*80 + "\n")

    cursor = conn.cursor()

    # Crear ladrón
    cursor.execute("SELECT id FROM especies WHERE nombre = 'Humanos I'")
    especie_id = cursor.fetchone()[0]

    cursor.execute("SELECT id FROM civilizaciones LIMIT 1")
    civ_id = cursor.fetchone()[0]

    cursor.execute("SELECT id FROM oficios WHERE nombre = 'Ladrón'")
    ladron_oficio = cursor.fetchone()[0]

    cursor.execute('''
        INSERT INTO personas
        (nombre, apellido, especie_id, genero, año_nacimiento, civilizacion_id,
         clase_social, es_npc)
        VALUES ('Yaotl', 'Sombra Rápida', ?, 'masculino', 1520, ?, 'campesino', 1)
    ''', (especie_id, civ_id))
    ladron_id = cursor.lastrowid

    cursor.execute('''
        INSERT INTO persona_oficios (persona_id, oficio_id, año_inicio, nivel_maestria, es_principal)
        VALUES (?, ?, 1540, 6, 1)
    ''', (ladron_id, ladron_oficio))

    print(f"🦹 Criminal: Yaotl Sombra Rápida (ID: {ladron_id})")

    # Víctima (un comerciante rico)
    cursor.execute("SELECT id, nombre_completo FROM personas WHERE es_npc = 1 AND clase_social = 'noble' LIMIT 1")
    victima = cursor.fetchone()

    if not victima:
        cursor.execute("SELECT id, nombre_completo FROM personas WHERE es_npc = 1 LIMIT 1")
        victima = cursor.fetchone()

    victima_id, victima_nombre = victima

    print(f"👤 Víctima: {victima_nombre}")

    # Registrar crimen
    año_crimen = 1565
    cursor.execute("SELECT id FROM pueblos_ciudades LIMIT 1")
    lugar_id = cursor.fetchone()[0]

    cursor.execute('''
        INSERT INTO crimenes
        (tipo, gravedad, año, lugar_id, perpetrador_id, victima_id, atrapado, descripcion)
        VALUES ('robo', 6, ?, ?, ?, ?, 1,
                'Robo de 500 en joyas y obsidiana del hogar de la víctima')
    ''', (año_crimen, lugar_id, ladron_id, victima_id))
    crimen_id = cursor.lastrowid

    print(f"\n🚨 Crimen: Robo de 500 en joyas ({año_crimen})")
    print("   └─ Gravedad: 6/10")
    print("   └─ Estado: ATRAPADO")

    # Crear juicio
    cursor.execute('''
        SELECT p.id FROM personas p
        JOIN persona_oficios po ON p.id = po.persona_id
        JOIN oficios o ON po.oficio_id = o.id
        WHERE o.nombre = 'Sacerdote' LIMIT 1
    ''')
    juez = cursor.fetchone()

    if juez:
        juez_id = juez[0]
    else:
        juez_id = victima_id  # La víctima actúa como juez temporalmente

    cursor.execute("SELECT id FROM castigos WHERE nombre = 'Prisión Larga'")
    castigo_id = cursor.fetchone()[0]

    cursor.execute('''
        INSERT INTO juicios
        (crimen_id, año, lugar_id, juez_id, tipo_juez, acusado_id, veredicto, castigo_id)
        VALUES (?, ?, ?, ?, 'sacerdote', ?, 'culpable', ?)
    ''', (crimen_id, año_crimen, lugar_id, juez_id, ladron_id, castigo_id))
    juicio_id = cursor.lastrowid

    print(f"\n⚖️  Juicio realizado:")
    print("   └─ Veredicto: CULPABLE")
    print("   └─ Castigo: Prisión Larga (10 años)")

    # Aplicar castigo
    cursor.execute('''
        INSERT INTO persona_castigos
        (persona_id, castigo_id, juicio_id, año_inicio, año_fin, completado)
        VALUES (?, ?, ?, ?, ?, 0)
    ''', (ladron_id, castigo_id, juicio_id, año_crimen, año_crimen + 10))

    print(f"   └─ Encarcelado desde {año_crimen} hasta {año_crimen + 10}")

    # Destruir reputación
    cursor.execute('''
        INSERT OR REPLACE INTO persona_reputacion
        (persona_id, civilizacion_id, nivel_reputacion, modificador_precio)
        VALUES (?, ?, -80, 2.0)
    ''', (ladron_id, civ_id))

    print(f"\n💔 Reputación destruida:")
    print("   └─ -80 puntos")
    print("   └─ +100% sobreprecio en comercio")

    conn.commit()
    print("\n✓ Sistema de justicia aplicado completamente")

    return ladron_id, crimen_id, juicio_id


def ejemplo_artefacto_legendario(conn):
    """
    Ejemplo: Búsqueda y uso de artefacto divino
    """
    print("\n" + "="*80)
    print("EJEMPLO 4: ARTEFACTO DIVINO - EL CORAZÓN DE QUETZALCÓATL")
    print("="*80 + "\n")

    cursor = conn.cursor()

    # Obtener artefacto
    cursor.execute('''
        SELECT id, nombre, nivel_poder, poderes, maldicion
        FROM artefactos
        WHERE nombre = 'Corazón de Quetzalcóatl'
    ''')
    art_id, art_nombre, poder, poderes_json, maldicion = cursor.fetchone()

    poderes = json.loads(poderes_json)

    print(f"✨ Artefacto: {art_nombre}")
    print(f"   Nivel de Poder: {poder}/10")
    print(f"\n   Poderes:")
    for poder_data in poderes:
        print(f"      • {poder_data['nombre']} (Coste: {poder_data['coste']})")

    # Crear héroe que lo encuentra
    cursor.execute("SELECT id FROM especies WHERE nombre = 'Humanos I'")
    especie_id = cursor.fetchone()[0]

    cursor.execute("SELECT id FROM civilizaciones LIMIT 1")
    civ_id = cursor.fetchone()[0]

    cursor.execute('''
        INSERT INTO personas
        (nombre, apellido, especie_id, genero, año_nacimiento, civilizacion_id,
         clase_social, es_npc)
        VALUES ('Cuauhtémoc', 'Buscador de Reliquias', ?, 'masculino', 1530, ?, 'noble', 1)
    ''', (especie_id, civ_id))
    heroe_id = cursor.lastrowid

    print(f"\n🦸 Héroe: Cuauhtémoc Buscador de Reliquias (ID: {heroe_id})")

    año_hallazgo = 1570

    # Registrar en historia del artefacto
    cursor.execute('''
        INSERT INTO artefacto_historia
        (artefacto_id, año, evento, poseedor_nuevo_id, descripcion)
        VALUES (?, ?, 'transferencia', ?,
                'Encontrado en las ruinas del Templo Antiguo tras 50 años perdido')
    ''', (art_id, año_hallazgo, heroe_id))

    # Actualizar poseedor actual
    cursor.execute('''
        UPDATE artefactos
        SET poseedor_actual_id = ?, esta_perdido = 0
        WHERE id = ?
    ''', (heroe_id, art_id))

    print(f"   └─ Encontró el {art_nombre} en {año_hallazgo}")
    print("   └─ Ubicación: Ruinas del Templo Antiguo")

    # Usar poder de curación masiva
    print(f"\n💫 {heroe_id} usa 'Curación Masiva':")
    print("   └─ Cura a 20 personas de una plaga")
    print("   └─ Coste: Perdió 1 año de vida")

    # Ajustar esperanza de vida
    cursor.execute('''
        UPDATE personas
        SET año_muerte = (SELECT año_muerte FROM personas WHERE id = ?) - 1
        WHERE id = ?
    ''', (heroe_id, heroe_id))

    print(f"   └─ Nueva esperanza de vida: Reducida en 1 año")

    # Reputación divina
    cursor.execute('''
        INSERT OR REPLACE INTO persona_reputacion
        (persona_id, civilizacion_id, nivel_reputacion, titulos, hazañas_conocidas)
        VALUES (?, ?, 100, ?, ?)
    ''', (heroe_id, civ_id,
          json.dumps(['Portador del Corazón Divino', 'Salvador del Pueblo']),
          json.dumps(['Usó el Corazón de Quetzalcóatl para salvar 20 vidas'])))

    print(f"\n🌟 Reputación: LEGENDARIA")
    print("   └─ 100 puntos (máximo)")
    print("   └─ Venerado como semi-dios")

    conn.commit()
    print("\n✓ Artefacto encontrado y usado con consecuencias")

    return heroe_id, art_id


def ejemplo_mutacion_heredable(conn):
    """
    Ejemplo: Linaje con mutación heredable
    """
    print("\n" + "="*80)
    print("EJEMPLO 5: LINAJE DE MUTANTES - PIEL LUMINISCENTE")
    print("="*80 + "\n")

    cursor = conn.cursor()

    # Obtener mutación
    cursor.execute('''
        SELECT id, nombre, es_heredable, probabilidad_herencia, efectos_mecanicos
        FROM mutaciones
        WHERE nombre = 'Piel Luminiscente'
    ''')
    mut_id, mut_nombre, heredable, prob, efectos_json = cursor.fetchone()

    efectos = json.loads(efectos_json)

    print(f"🧬 Mutación: {mut_nombre}")
    print(f"   Heredable: {'Sí' if heredable else 'No'}")
    print(f"   Probabilidad de herencia: {prob}%")
    print(f"   Efectos:")
    for key, value in efectos.items():
        print(f"      • {key}: {value}")

    # Crear fundador del linaje
    cursor.execute("SELECT id FROM especies WHERE nombre = 'Humanos I'")
    especie_id = cursor.fetchone()[0]

    cursor.execute("SELECT id FROM civilizaciones LIMIT 1")
    civ_id = cursor.fetchone()[0]

    cursor.execute('''
        INSERT INTO personas
        (nombre, apellido, especie_id, genero, año_nacimiento, civilizacion_id,
         clase_social, es_npc)
        VALUES ('Citlali', 'de la Luz', ?, 'femenino', 1540, ?, 'noble', 1)
    ''', (especie_id, civ_id))
    fundador_id = cursor.lastrowid

    print(f"\n👤 Fundador: Citlali de la Luz (ID: {fundador_id})")

    # Dar mutación al fundador
    cursor.execute('''
        INSERT INTO persona_mutaciones
        (persona_id, mutacion_id, año_adquisicion, forma_adquisicion, nivel_control)
        VALUES (?, ?, 1540, 'bendicion', 7)
    ''', (fundador_id, mut_id))

    print(f"   └─ Recibió bendición divina: {mut_nombre}")
    print("   └─ Nivel de control: 7/10")

    # Crear linaje
    cursor.execute('''
        INSERT INTO linajes
        (nombre, fundador_id, civilizacion_id, año_fundacion, descripcion)
        VALUES ('Linaje de la Luz Eterna', ?, ?, 1540,
                'Familia bendecida por Ixchel con piel que brilla en la oscuridad')
    ''', (fundador_id, civ_id))
    linaje_id = cursor.lastrowid

    print(f"\n🏛️  Linaje fundado: 'Linaje de la Luz Eterna'")

    # Crear hijos con herencia de mutación
    cursor.execute('''
        INSERT INTO personas
        (nombre, apellido, especie_id, genero, año_nacimiento, madre_id,
         civilizacion_id, clase_social, es_npc)
        VALUES ('Tonalli', 'de la Luz', ?, 'masculino', 1565, ?, ?, 'noble', 1)
    ''', (especie_id, fundador_id, civ_id))
    hijo1_id = cursor.lastrowid

    # 75% de probabilidad de heredar
    heredo = random.random() < 0.75

    if heredo:
        cursor.execute('''
            INSERT INTO persona_mutaciones
            (persona_id, mutacion_id, año_adquisicion, forma_adquisicion,
             heredada_de_id, nivel_control)
            VALUES (?, ?, 1565, 'nacimiento', ?, 5)
        ''', (hijo1_id, mut_id, fundador_id))

        print(f"\n👶 Hijo: Tonalli de la Luz")
        print(f"   └─ HEREDÓ la mutación {mut_nombre}")
        print("   └─ Nivel de control inicial: 5/10")
    else:
        print(f"\n👶 Hijo: Tonalli de la Luz")
        print(f"   └─ NO heredó la mutación (25% probabilidad)")

    conn.commit()
    print("\n✓ Linaje mutante establecido con herencia genética")

    return fundador_id, linaje_id


def main():
    print("\n" + "="*80)
    print("DEMOSTRACIÓN COMPLETA DE TODOS LOS SISTEMAS INTEGRADOS")
    print("="*80)

    conn = sqlite3.connect('quinto_sol.db')

    try:
        # Ejecutar todos los ejemplos
        g1_id, g2_id, batalla_id = ejemplo_batalla_epica(conn)
        alq_id, epidemia_id = ejemplo_epidemia_y_curacion(conn)
        ladron_id, crimen_id, juicio_id = ejemplo_crimen_y_justicia(conn)
        heroe_id, art_id = ejemplo_artefacto_legendario(conn)
        fundador_id, linaje_id = ejemplo_mutacion_heredable(conn)

        print("\n" + "="*80)
        print("✓ TODOS LOS EJEMPLOS COMPLETADOS EXITOSAMENTE")
        print("="*80)

        print("\n📊 IDs Generados:")
        print(f"   Batalla: {batalla_id}")
        print(f"   Epidemia: {epidemia_id}")
        print(f"   Crimen/Juicio: {crimen_id}/{juicio_id}")
        print(f"   Artefacto usado por: {heroe_id}")
        print(f"   Linaje Mutante: {linaje_id}")

        print("\n💡 Ahora puedes:")
        print("   • Consultar historiales: python3 consultas.py")
        print("   • Simular más eventos con estos personajes")
        print("   • Ver cómo sus historias se entrelazan")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        conn.close()


if __name__ == '__main__':
    main()
