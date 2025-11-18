#!/usr/bin/env python3
"""
Genera guerras históricas con bajas masivas
Reduce población drásticamente en períodos clave
"""

import sqlite3
import random


def generar_guerra_masiva(conn, nombre, año, civ_atacante_id, civ_defensora_id,
                          porcentaje_bajas_atacante=0.15, porcentaje_bajas_defensor=0.25):
    """
    Genera una guerra con bajas masivas

    Args:
        porcentaje_bajas_atacante: % de población que muere del atacante (default 15%)
        porcentaje_bajas_defensor: % de población que muere del defensor (default 25%)
    """
    cursor = conn.cursor()

    print(f"\n{'='*70}")
    print(f"⚔️  GUERRA: {nombre} ({año})")
    print(f"{'='*70}")

    # Obtener nombres de civilizaciones
    cursor.execute("SELECT nombre FROM civilizaciones WHERE id = ?", (civ_atacante_id,))
    nombre_atacante = cursor.fetchone()[0]

    cursor.execute("SELECT nombre FROM civilizaciones WHERE id = ?", (civ_defensora_id,))
    nombre_defensor = cursor.fetchone()[0]

    print(f"\n🗡️  Atacante: {nombre_atacante}")
    print(f"🛡️  Defensor: {nombre_defensor}")

    # Contar población viva de cada civilización en ese año
    cursor.execute("""
        SELECT COUNT(*) FROM personas
        WHERE civilizacion_id = ?
        AND año_nacimiento <= ?
        AND (año_muerte IS NULL OR año_muerte > ?)
        AND genero = 'masculino'
        AND (? - año_nacimiento) >= 16  -- Edad mínima para combatir
        AND (? - año_nacimiento) <= 60  -- Edad máxima
    """, (civ_atacante_id, año, año, año, año))
    guerreros_atacante = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM personas
        WHERE civilizacion_id = ?
        AND año_nacimiento <= ?
        AND (año_muerte IS NULL OR año_muerte > ?)
        AND genero = 'masculino'
        AND (? - año_nacimiento) >= 16
        AND (? - año_nacimiento) <= 60
    """, (civ_defensora_id, año, año, año, año))
    guerreros_defensor = cursor.fetchone()[0]

    if guerreros_atacante == 0 or guerreros_defensor == 0:
        print(f"\n⚠️  No hay suficientes guerreros disponibles")
        return

    print(f"\n👥 Guerreros disponibles:")
    print(f"   Atacante: {guerreros_atacante:,}")
    print(f"   Defensor: {guerreros_defensor:,}")

    # Calcular bajas
    bajas_atacante = int(guerreros_atacante * porcentaje_bajas_atacante)
    bajas_defensor = int(guerreros_defensor * porcentaje_bajas_defensor)

    print(f"\n💀 Bajas calculadas:")
    print(f"   Atacante: {bajas_atacante:,} ({porcentaje_bajas_atacante*100:.0f}%)")
    print(f"   Defensor: {bajas_defensor:,} ({porcentaje_bajas_defensor*100:.0f}%)")

    # Determinar ganador (más sobrevivientes)
    sobrevivientes_atacante = guerreros_atacante - bajas_atacante
    sobrevivientes_defensor = guerreros_defensor - bajas_defensor

    if sobrevivientes_atacante > sobrevivientes_defensor:
        ganador = 'atacante'
        print(f"\n🏆 VICTORIA: {nombre_atacante}")
    else:
        ganador = 'defensor'
        print(f"\n🏆 VICTORIA: {nombre_defensor}")

    # Crear registro de batalla
    cursor.execute("""
        INSERT INTO batallas
        (nombre, tipo, año, ganador, bajas_atacante, bajas_defensor)
        VALUES (?, 'guerra', ?, ?, ?, ?)
    """, (nombre, año, ganador, bajas_atacante, bajas_defensor))
    batalla_id = cursor.lastrowid

    # Matar guerreros del atacante
    print(f"\n⚰️  Registrando bajas del atacante...")
    cursor.execute("""
        SELECT id FROM personas
        WHERE civilizacion_id = ?
        AND año_nacimiento <= ?
        AND (año_muerte IS NULL OR año_muerte > ?)
        AND genero = 'masculino'
        AND (? - año_nacimiento) >= 16
        AND (? - año_nacimiento) <= 60
        ORDER BY RANDOM()
        LIMIT ?
    """, (civ_atacante_id, año, año, año, año, bajas_atacante))

    muertos_atacante = cursor.fetchall()
    for (persona_id,) in muertos_atacante:
        cursor.execute("""
            UPDATE personas
            SET año_muerte = ?, causa_muerte = 'combate'
            WHERE id = ?
        """, (año, persona_id))

        # Registrar participación
        cursor.execute("""
            INSERT INTO batalla_participantes
            (batalla_id, persona_id, faccion, murio)
            VALUES (?, ?, 'atacante', 1)
        """, (batalla_id, persona_id))

    # Matar guerreros del defensor
    print(f"⚰️  Registrando bajas del defensor...")
    cursor.execute("""
        SELECT id FROM personas
        WHERE civilizacion_id = ?
        AND año_nacimiento <= ?
        AND (año_muerte IS NULL OR año_muerte > ?)
        AND genero = 'masculino'
        AND (? - año_nacimiento) >= 16
        AND (? - año_nacimiento) <= 60
        ORDER BY RANDOM()
        LIMIT ?
    """, (civ_defensora_id, año, año, año, año, bajas_defensor))

    muertos_defensor = cursor.fetchall()
    for (persona_id,) in muertos_defensor:
        cursor.execute("""
            UPDATE personas
            SET año_muerte = ?, causa_muerte = 'combate'
            WHERE id = ?
        """, (año, persona_id))

        # Registrar participación
        cursor.execute("""
            INSERT INTO batalla_participantes
            (batalla_id, persona_id, faccion, murio)
            VALUES (?, ?, 'defensor', 1)
        """, (batalla_id, persona_id))

    conn.commit()

    print(f"\n✅ Guerra completada:")
    print(f"   Total muertos: {bajas_atacante + bajas_defensor:,}")
    print(f"   Batalla ID: {batalla_id}")


def generar_todas_guerras(conn):
    """Genera las guerras históricas principales"""

    cursor = conn.cursor()

    print("\n" + "="*70)
    print("🗡️  GENERACIÓN DE GUERRAS HISTÓRICAS")
    print("="*70)

    # Obtener IDs de civilizaciones
    cursor.execute("SELECT id, nombre FROM civilizaciones")
    civs = {nombre: civ_id for civ_id, nombre in cursor.fetchall()}

    print(f"\n📋 Civilizaciones disponibles:")
    for nombre, civ_id in civs.items():
        print(f"   {civ_id}. {nombre}")

    # Guerra 1: Guerra de las Dos Lunas (1820)
    # Mexica vs Toltecas
    if 'Mexica de Obsidiana' in civs and 'Toltecas del Viento' in civs:
        generar_guerra_masiva(
            conn,
            nombre="Guerra de las Dos Lunas",
            año=1820,
            civ_atacante_id=civs['Mexica de Obsidiana'],
            civ_defensora_id=civs['Toltecas del Viento'],
            porcentaje_bajas_atacante=0.12,  # 12% bajas atacante
            porcentaje_bajas_defensor=0.30   # 30% bajas defensor (derrota aplastante)
        )

    # Guerra 2: Rebelión Zapoteca (1950)
    # Zapotecas vs Mexica
    if 'Zapotecas del Eco' in civs and 'Mexica de Obsidiana' in civs:
        generar_guerra_masiva(
            conn,
            nombre="Rebelión Zapoteca",
            año=1950,
            civ_atacante_id=civs['Zapotecas del Eco'],
            civ_defensora_id=civs['Mexica de Obsidiana'],
            porcentaje_bajas_atacante=0.25,  # 25% - rebelión costosa
            porcentaje_bajas_defensor=0.15   # 15% - defendieron bien
        )

    # Guerra 3: Primera Guerra de Unificación (2250)
    # Mexica vs Purépecha (después del Cataclismo)
    if 'Mexica de Obsidiana' in civs and 'Purépecha del Fuego' in civs:
        generar_guerra_masiva(
            conn,
            nombre="Primera Guerra de Unificación",
            año=2250,
            civ_atacante_id=civs['Mexica de Obsidiana'],
            civ_defensora_id=civs['Purépecha del Fuego'],
            porcentaje_bajas_atacante=0.20,  # 20%
            porcentaje_bajas_defensor=0.35   # 35% - derrota
        )

    # Guerra 4: Guerra Civil Mexica (2500)
    # Mexica del Norte vs Mexica del Sur (guerra civil)
    if 'Mexica de Obsidiana' in civs:
        generar_guerra_masiva(
            conn,
            nombre="Guerra Civil Mexica",
            año=2500,
            civ_atacante_id=civs['Mexica de Obsidiana'],
            civ_defensora_id=civs['Mexica de Obsidiana'],  # Misma civilización
            porcentaje_bajas_atacante=0.18,  # 18%
            porcentaje_bajas_defensor=0.22   # 22%
        )

    # Guerra 5: La Gran Conquista (2750)
    # Mexica vs Todos los demás
    if 'Mexica de Obsidiana' in civs and 'Toltecas del Viento' in civs:
        generar_guerra_masiva(
            conn,
            nombre="La Gran Conquista",
            año=2750,
            civ_atacante_id=civs['Mexica de Obsidiana'],
            civ_defensora_id=civs['Toltecas del Viento'],
            porcentaje_bajas_atacante=0.10,  # 10% - victoria aplastante
            porcentaje_bajas_defensor=0.40   # 40% - casi aniquilados
        )

    print("\n" + "="*70)
    print("✅ TODAS LAS GUERRAS GENERADAS")
    print("="*70)


def main():
    print("\n" + "="*70)
    print("⚔️  GENERADOR DE GUERRAS HISTÓRICAS - PORTALES DEL QUINTO SOL")
    print("="*70)
    print("\nEste script generará guerras con bajas masivas en períodos clave")
    print("ADVERTENCIA: Esto modificará la base de datos y matará muchos NPCs")

    respuesta = input("\n¿Deseas continuar? (s/n): ")

    if respuesta.lower() != 's':
        print("Operación cancelada.")
        return

    conn = sqlite3.connect('quinto_sol.db')

    try:
        generar_todas_guerras(conn)

        # Mostrar estadísticas finales
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM batallas WHERE tipo = 'guerra'")
        num_guerras = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM personas WHERE causa_muerte = 'combate'")
        total_muertos = cursor.fetchone()[0]

        print(f"\n📊 ESTADÍSTICAS FINALES:")
        print(f"   Guerras generadas: {num_guerras}")
        print(f"   Total muertos en combate: {total_muertos:,}")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()
    finally:
        conn.close()


if __name__ == '__main__':
    main()
