#!/usr/bin/env python3
"""
Ejemplos avanzados del sistema:
- Paternidad incierta (prostituta con múltiples padres posibles)
- Sistema de sucesión (hijo hereda taller)
- Memoria heredada ("Mi padre te mencionó")
- Sistema de aprendices
"""

import sqlite3
import random
import json
from modelo_ia_conversacional import NPCConversacional, SistemaConversacionalIA


def ejemplo_paternidad_incierta(conn):
    """
    Ejemplo: Prostituta tiene un hijo, pero no sabe quién es el padre
    Pueden ser: Herrero, Pescador o Guardián
    """
    print("\n" + "="*70)
    print("EJEMPLO 1: PATERNIDAD INCIERTA")
    print("="*70 + "\n")

    cursor = conn.cursor()

    # Crear prostituta
    cursor.execute("SELECT id FROM oficios WHERE nombre = 'Prostituta'")
    prostituta_oficio_id = cursor.fetchone()[0]

    cursor.execute("SELECT id FROM especies WHERE nombre = 'Humanos I'")
    especie_id = cursor.fetchone()[0]

    cursor.execute("SELECT id FROM civilizaciones LIMIT 1")
    civ_id = cursor.fetchone()[0]

    # Crear la prostituta
    cursor.execute('''
        INSERT INTO personas
        (nombre, apellido, especie_id, genero, año_nacimiento, civilizacion_id,
         clase_social, es_npc)
        VALUES ('Isha', 'de la Noche', ?, 'femenino', 1480, ?, 'artesano', 1)
    ''', (especie_id, civ_id))
    prostituta_id = cursor.lastrowid

    cursor.execute('''
        INSERT INTO persona_oficios
        (persona_id, oficio_id, año_inicio, nivel_maestria, es_principal)
        VALUES (?, ?, 1498, 7, 1)
    ''', (prostituta_id, prostituta_oficio_id))

    print(f"✓ Creada: Isha de la Noche (ID: {prostituta_id}) - Prostituta")

    # Crear 3 clientes habituales
    clientes = []
    oficios_clientes = ['Herrero', 'Pescador', 'Guardián']

    for oficio_nombre in oficios_clientes:
        cursor.execute("SELECT id FROM oficios WHERE nombre = ?", (oficio_nombre,))
        oficio_id = cursor.fetchone()[0]

        cursor.execute('''
            INSERT INTO personas
            (nombre, apellido, especie_id, genero, año_nacimiento, civilizacion_id,
             clase_social, es_npc)
            VALUES (?, 'de la Cantina', ?, 'masculino', ?, ?, 'artesano', 1)
        ''', (oficio_nombre, especie_id, random.randint(1475, 1485), civ_id))
        cliente_id = cursor.lastrowid

        cursor.execute('''
            INSERT INTO persona_oficios
            (persona_id, oficio_id, año_inicio, nivel_maestria, es_principal)
            VALUES (?, ?, 1500, ?, 1)
        ''', (cliente_id, oficio_id, random.randint(5, 8)))

        clientes.append(cliente_id)
        print(f"  └─ Cliente: {oficio_nombre} (ID: {cliente_id})")

    # Crear hijo con paternidad desconocida
    cursor.execute('''
        INSERT INTO personas
        (nombre, apellido, especie_id, genero, año_nacimiento, madre_id,
         padre_id, civilizacion_id, clase_social, es_npc)
        VALUES ('Tōnalli', 'de la Noche', ?, 'masculino', 1510, ?, NULL, ?, 'campesino', 1)
    ''', (especie_id, prostituta_id, civ_id))
    hijo_id = cursor.lastrowid

    print(f"\n✓ Nació: Tōnalli de la Noche (ID: {hijo_id})")
    print(f"  Madre: Isha de la Noche")
    print(f"  Padre: DESCONOCIDO")

    # Registrar posibles padres
    probabilidades = [40, 35, 25]  # %
    for cliente_id, prob in zip(clientes, probabilidades):
        cursor.execute('''
            INSERT INTO paternidad_posible
            (hijo_id, madre_id, padre_posible_id, probabilidad, año_concepcion, confirmado)
            VALUES (?, ?, ?, ?, 1509, 0)
        ''', (hijo_id, prostituta_id, cliente_id, prob))

        print(f"    └─ Posible padre: Cliente #{cliente_id} ({prob}% probabilidad)")

    # Crear relaciones
    for cliente_id in clientes:
        cursor.execute('''
            INSERT INTO relaciones
            (persona1_id, persona2_id, tipo_relacion, intensidad, año_inicio)
            VALUES (?, ?, 'cliente', 6, 1505)
        ''', (cliente_id, prostituta_id))

    conn.commit()

    print("\n💡 NOTA: El sistema permite resolver la paternidad más tarde mediante:")
    print("   - Prueba divina (magia de Quetzalcóatl)")
    print("   - Rasgos físicos heredados")
    print("   - Confesión de la madre")

    return hijo_id, clientes, prostituta_id


def ejemplo_sucesion_taller(conn, año_inicial=1520):
    """
    Ejemplo: Herrero muere, su hijo hereda el taller
    El hijo recuerda a clientes de su padre
    """
    print("\n" + "="*70)
    print("EJEMPLO 2: SUCESIÓN DE TALLER")
    print("="*70 + "\n")

    cursor = conn.cursor()

    # Buscar un herrero existente
    cursor.execute('''
        SELECT p.id, p.nombre_completo
        FROM personas p
        JOIN persona_oficios po ON p.id = po.persona_id
        JOIN oficios o ON po.oficio_id = o.id
        WHERE o.nombre = 'Herrero' AND p.es_npc = 1
        LIMIT 1
    ''')

    herrero_padre = cursor.fetchone()

    if not herrero_padre:
        print("⚠️  No hay herreros disponibles")
        return None, None

    padre_id, padre_nombre = herrero_padre
    print(f"✓ Herrero maestro: {padre_nombre} (ID: {padre_id})")

    # Crear jugador ficticio que fue cliente
    jugador_id = 9999
    cursor.execute('''
        INSERT OR IGNORE INTO personas
        (id, nombre, apellido, especie_id, genero, año_nacimiento, es_npc, es_jugador)
        VALUES (?, 'Jugador', 'Viajero', 1, 'masculino', 1490, 0, 1)
    ''', (jugador_id,))

    # Crear memoria de transacción con el padre
    cursor.execute('''
        INSERT INTO memoria_npc
        (npc_id, jugador_id, tipo_memoria, año, titulo, descripcion,
         importancia, emocion)
        VALUES (?, ?, 'transaccion', ?, 'Excelente cliente',
                'Un viajero que siempre paga bien y trata con respeto. Cliente de confianza.',
                9, 'alegria')
    ''', (padre_id, jugador_id, año_inicial))

    print(f"  └─ Memoria creada: El padre conoció al jugador (ID: {jugador_id})")

    # "Matar" al padre (actualizar año de muerte)
    año_muerte = año_inicial + 30
    cursor.execute('''
        UPDATE personas
        SET año_muerte = ?, causa_muerte = 'edad_avanzada'
        WHERE id = ?
    ''', (año_muerte, padre_id))

    print(f"\n💀 {padre_nombre} falleció en {año_muerte} por edad avanzada")

    # Crear hijo
    cursor.execute("SELECT especie_id, civilizacion_id FROM personas WHERE id = ?", (padre_id,))
    especie_id, civ_id = cursor.fetchone()

    cursor.execute('''
        INSERT INTO personas
        (nombre, apellido, especie_id, genero, año_nacimiento, padre_id,
         civilizacion_id, clase_social, es_npc)
        VALUES ('Cuauhtémoc', (SELECT apellido FROM personas WHERE id = ?),
                ?, 'masculino', ?, ?, ?, 'artesano', 1)
    ''', (padre_id, especie_id, año_inicial - 20, padre_id, civ_id))
    hijo_id = cursor.lastrowid

    print(f"✓ Hijo: Cuauhtémoc (ID: {hijo_id}), nacido en {año_inicial - 20}")

    # Registrar aprendizaje
    cursor.execute("SELECT id FROM oficios WHERE nombre = 'Herrero'")
    herrero_oficio_id = cursor.fetchone()[0]

    cursor.execute('''
        INSERT INTO aprendices
        (maestro_id, aprendiz_id, oficio_id, año_inicio, año_finalizacion,
         nivel_progreso, es_exitoso)
        VALUES (?, ?, ?, ?, ?, 100, 1)
    ''', (padre_id, hijo_id, herrero_oficio_id, año_inicial, año_muerte - 5))

    print(f"  └─ Aprendió de su padre desde {año_inicial} hasta {año_muerte - 5}")

    # Asignar oficio al hijo
    cursor.execute('''
        INSERT INTO persona_oficios
        (persona_id, oficio_id, año_inicio, nivel_maestria, es_principal)
        VALUES (?, ?, ?, 7, 1)
    ''', (hijo_id, herrero_oficio_id, año_muerte - 5))

    # Registrar sucesión
    cursor.execute('''
        INSERT INTO sucesion_oficios
        (oficio_id, persona_anterior_id, persona_sucesor_id, año_sucesion,
         tipo_sucesion, nivel_maestria_heredado)
        VALUES (?, ?, ?, ?, 'herencia', 8)
    ''', (herrero_oficio_id, padre_id, hijo_id, año_muerte))

    print(f"✓ Sucesión registrada: Cuauhtémoc heredó el taller en {año_muerte}")

    conn.commit()

    # Ahora simular conversación con el hijo
    print("\n" + "-"*70)
    print(f"CONVERSACIÓN CON EL HIJO ({año_muerte + 1})")
    print("-"*70 + "\n")

    sistema = SistemaConversacionalIA()
    npc_hijo = sistema.obtener_npc(hijo_id)

    # Generar saludo con memoria heredada
    saludo = npc_hijo.generar_saludo(jugador_id, año_muerte + 1)
    print(f"💬 {npc_hijo.nombre}: {saludo}")

    # Agregar diálogo de sucesión
    dialogo_sucesion = npc_hijo.generar_dialogo_sucesion(padre_id)
    print(f"\n💬 {npc_hijo.nombre}: {dialogo_sucesion}")

    return hijo_id, padre_id


def ejemplo_aprendiz_no_heredero(conn):
    """
    Ejemplo: Aprendiz que NO es hijo del maestro
    Aprende el oficio pero sin relación familiar
    """
    print("\n" + "="*70)
    print("EJEMPLO 3: APRENDIZ NO FAMILIAR")
    print("="*70 + "\n")

    cursor = conn.cursor()

    # Buscar un alquimista o crear uno
    cursor.execute("SELECT id FROM oficios WHERE nombre = 'Alquimista'")
    alquimista_oficio_id = cursor.fetchone()[0]

    cursor.execute('''
        SELECT id FROM especies WHERE nombre = 'Humanos I'
    ''')
    especie_id = cursor.fetchone()[0]

    cursor.execute("SELECT id FROM civilizaciones LIMIT 1")
    civ_id = cursor.fetchone()[0]

    # Crear maestro alquimista
    cursor.execute('''
        INSERT INTO personas
        (nombre, apellido, especie_id, genero, año_nacimiento, civilizacion_id,
         clase_social, es_npc)
        VALUES ('Xólotl', 'el Sabio', ?, 'masculino', 1470, ?, 'sacerdote', 1)
    ''', (especie_id, civ_id))
    maestro_id = cursor.lastrowid

    cursor.execute('''
        INSERT INTO persona_oficios
        (persona_id, oficio_id, año_inicio, nivel_maestria, es_principal)
        VALUES (?, ?, 1490, 10, 1)
    ''', (maestro_id, alquimista_oficio_id))

    print(f"✓ Maestro: Xólotl el Sabio (ID: {maestro_id}) - Alquimista Maestro")

    # Crear aprendiz (sin relación familiar)
    cursor.execute('''
        INSERT INTO personas
        (nombre, apellido, especie_id, genero, año_nacimiento, civilizacion_id,
         clase_social, es_npc)
        VALUES ('Itzel', 'de las Flores', ?, 'femenino', 1500, ?, 'campesino', 1)
    ''', (especie_id, civ_id))
    aprendiz_id = cursor.lastrowid

    print(f"✓ Aprendiz: Itzel de las Flores (ID: {aprendiz_id})")
    print("  └─ Sin relación familiar con el maestro")

    # Registrar aprendizaje
    cursor.execute('''
        INSERT INTO aprendices
        (maestro_id, aprendiz_id, oficio_id, año_inicio, año_finalizacion,
         nivel_progreso, es_exitoso)
        VALUES (?, ?, ?, 1518, NULL, 65, NULL)
    ''', (maestro_id, aprendiz_id, alquimista_oficio_id))

    print(f"  └─ Comenzó aprendizaje en 1518 (en progreso: 65%)")

    # Crear relación maestro-aprendiz
    cursor.execute('''
        INSERT INTO relaciones
        (persona1_id, persona2_id, tipo_relacion, intensidad, año_inicio)
        VALUES (?, ?, 'mentor', 8, 1518)
    ''', (maestro_id, aprendiz_id))

    cursor.execute('''
        INSERT INTO relaciones
        (persona1_id, persona2_id, tipo_relacion, intensidad, año_inicio)
        VALUES (?, ?, 'aprendiz', 8, 1518)
    ''', (aprendiz_id, maestro_id))

    conn.commit()

    print("\n💡 NOTA: Itzel puede completar su aprendizaje y eventualmente")
    print("   convertirse en Alquimista independiente o incluso superar a su maestro")

    return aprendiz_id, maestro_id


def main():
    """Ejecuta todos los ejemplos"""

    print("\n" + "="*70)
    print("EJEMPLOS AVANZADOS - Sistema de Genealogía e IA")
    print("="*70)

    conn = sqlite3.connect('quinto_sol.db')

    try:
        # Ejemplo 1: Paternidad incierta
        hijo_id, clientes, prostituta_id = ejemplo_paternidad_incierta(conn)

        # Ejemplo 2: Sucesión de taller
        heredero_id, padre_herrero_id = ejemplo_sucesion_taller(conn, 1520)

        # Ejemplo 3: Aprendiz no familiar
        aprendiz_id, maestro_id = ejemplo_aprendiz_no_heredero(conn)

        print("\n" + "="*70)
        print("✓ TODOS LOS EJEMPLOS COMPLETADOS")
        print("="*70)

        print("\n📊 IDs creados:")
        print(f"  Prostituta: {prostituta_id}")
        print(f"  Hijo (paternidad incierta): {hijo_id}")
        print(f"  Posibles padres: {clientes}")
        if heredero_id and padre_herrero_id:
            print(f"  Herrero padre: {padre_herrero_id}")
            print(f"  Herrero hijo (heredero): {heredero_id}")
        print(f"  Maestro Alquimista: {maestro_id}")
        print(f"  Aprendiz: {aprendiz_id}")

        print("\n💾 Consultas útiles:")
        print("  python3 consultas.py  # Ver árboles genealógicos")
        print("  python3 modelo_ia_conversacional.py  # Probar conversaciones")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

    finally:
        conn.close()


if __name__ == '__main__':
    main()
