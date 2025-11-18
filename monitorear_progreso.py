#!/usr/bin/env python3
"""
Monitor de progreso de la simulación histórica
Muestra estadísticas en tiempo real de la base de datos
"""

import sqlite3
import time
import sys


def mostrar_estadisticas():
    """Muestra estadísticas actuales de la simulación"""
    conn = sqlite3.connect('quinto_sol.db')
    cursor = conn.cursor()

    print("\n" + "=" * 80)
    print("📊 ESTADÍSTICAS DE SIMULACIÓN HISTÓRICA - PORTALES DEL QUINTO SOL")
    print("=" * 80)

    # Personas totales
    cursor.execute("SELECT COUNT(*) FROM personas")
    total_personas = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM personas WHERE es_npc = 1")
    total_npcs = cursor.fetchone()[0]

    print(f"\n👥 POBLACIÓN:")
    print(f"   Total personas: {total_personas:,}")
    print(f"   NPCs: {total_npcs:,}")

    # Por género
    cursor.execute("SELECT genero, COUNT(*) FROM personas GROUP BY genero")
    generos = cursor.fetchall()
    print(f"\n   Por género:")
    for genero, count in generos:
        print(f"      {genero.capitalize()}: {count:,}")

    # Matrimonios
    cursor.execute("SELECT COUNT(*) FROM matrimonios")
    total_matrimonios = cursor.fetchone()[0]
    print(f"\n💑 MATRIMONIOS:")
    print(f"   Total: {total_matrimonios:,}")

    # Genealogía
    cursor.execute("SELECT COUNT(*) FROM personas WHERE padre_id IS NOT NULL")
    con_padre = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM personas WHERE madre_id IS NOT NULL")
    con_madre = cursor.fetchone()[0]

    print(f"\n👨‍👩‍👧‍👦 GENEALOGÍA:")
    print(f"   Personas con padre conocido: {con_padre:,}")
    print(f"   Personas con madre conocida: {con_madre:,}")
    print(f"   Huérfanos/Fundadores: {total_personas - con_padre:,}")

    # Rango de años
    cursor.execute("SELECT MIN(año_nacimiento), MAX(año_nacimiento) FROM personas")
    min_año, max_año = cursor.fetchone()

    if min_año and max_año:
        print(f"\n📅 RANGO TEMPORAL:")
        print(f"   Primer nacimiento: {min_año}")
        print(f"   Último nacimiento: {max_año}")
        print(f"   Años simulados: {max_año - min_año}")
        progreso = ((max_año - 1500) / (3000 - 1500)) * 100
        print(f"   Progreso: {progreso:.1f}% (objetivo: 1500-3000)")

    # Muertes
    cursor.execute("SELECT COUNT(*) FROM personas WHERE año_muerte IS NOT NULL")
    fallecidos = cursor.fetchone()[0]

    print(f"\n💀 MORTALIDAD:")
    print(f"   Fallecidos: {fallecidos:,}")
    print(f"   Vivos: {total_personas - fallecidos:,}")

    if fallecidos > 0:
        cursor.execute("""
            SELECT causa_muerte, COUNT(*)
            FROM personas
            WHERE causa_muerte IS NOT NULL
            GROUP BY causa_muerte
            ORDER BY COUNT(*) DESC
            LIMIT 5
        """)
        causas = cursor.fetchall()
        if causas:
            print(f"\n   Principales causas de muerte:")
            for causa, count in causas:
                print(f"      {causa}: {count:,}")

    # Oficios
    cursor.execute("""
        SELECT o.nombre, COUNT(po.persona_id)
        FROM persona_oficios po
        JOIN oficios o ON po.oficio_id = o.id
        WHERE po.es_principal = 1
        GROUP BY o.nombre
        ORDER BY COUNT(po.persona_id) DESC
        LIMIT 10
    """)
    oficios = cursor.fetchall()

    if oficios:
        print(f"\n🛠️  TOP 10 OFICIOS:")
        for i, (oficio, count) in enumerate(oficios, 1):
            print(f"   {i:2}. {oficio:25} {count:5} personas")

    # Civilizaciones
    cursor.execute("""
        SELECT c.nombre, COUNT(p.id)
        FROM personas p
        JOIN civilizaciones c ON p.civilizacion_id = c.id
        GROUP BY c.nombre
        ORDER BY COUNT(p.id) DESC
    """)
    civs = cursor.fetchall()

    if civs:
        print(f"\n🏛️  POBLACIÓN POR CIVILIZACIÓN:")
        for civ, count in civs:
            print(f"   {civ:30} {count:6,} personas")

    # Sistemas adicionales
    cursor.execute("SELECT COUNT(*) FROM batallas")
    batallas = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM crimenes")
    crimenes = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM memoria_npc")
    memorias = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM paternidad_posible")
    paternidades = cursor.fetchone()[0]

    print(f"\n⚔️  SISTEMAS ADICIONALES:")
    print(f"   Batallas: {batallas}")
    print(f"   Crímenes: {crimenes}")
    print(f"   Memorias de NPCs: {memorias}")
    print(f"   Paternidades inciertas: {paternidades}")

    # Tamaño de base de datos
    import os
    db_size = os.path.getsize('quinto_sol.db') / (1024 * 1024)  # MB
    print(f"\n💾 BASE DE DATOS:")
    print(f"   Tamaño: {db_size:.2f} MB")

    conn.close()

    print("\n" + "=" * 80)
    print(f"Última actualización: {time.strftime('%H:%M:%S')}")
    print("=" * 80)


def monitor_continuo(intervalo=30):
    """Monitorea continuamente cada X segundos"""
    print("🔄 Monitor de progreso iniciado (Ctrl+C para detener)")

    try:
        while True:
            mostrar_estadisticas()
            print(f"\n⏳ Próxima actualización en {intervalo} segundos...")
            time.sleep(intervalo)
    except KeyboardInterrupt:
        print("\n\n✋ Monitor detenido")


def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--continuo':
        intervalo = int(sys.argv[2]) if len(sys.argv) > 2 else 30
        monitor_continuo(intervalo)
    else:
        mostrar_estadisticas()
        print("\n💡 Tip: Usa --continuo para monitoreo en tiempo real")
        print("   Ejemplo: python3 monitorear_progreso.py --continuo 30")


if __name__ == '__main__':
    main()
