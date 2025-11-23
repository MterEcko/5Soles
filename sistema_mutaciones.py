#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Mutaciones Genéticas
Portales del Quinto Sol
ADAPTADO A POSTGRESQL (DatabaseConnector)
"""

import random
import json
import re # Para el schema
from typing import List, Tuple, Optional, Dict
from database_connector import DatabaseConnector # Importación clave

# ================================================================
# CATÁLOGO DE MUTACIONES (Mantiene el contenido)
# ================================================================
MUTACIONES_BASE = [
    # FÍSICAS POSITIVAS
    {
        'nombre': 'Fuerza Titánica',
        'tipo': 'fisica',
        'rareza': 'rara',
        'prob': 0.0005,
        'causas': ['divina', 'herencia', 'ritual'],
        'stats': {'fuerza': 25, 'resistencia': 15},
        'habilidades': ['carga_devastadora', 'levitar_peso_masivo'],
        'heredable': True,
        'prob_herencia': 0.3,
        'visual': {'musculatura': 'desarrollada', 'estatura': '+20cm'},
        'descripcion': 'Fuerza sobrehumana capaz de levantar 5 veces el peso normal'
    },
    # ... (Resto del catálogo MUTACIONES_BASE no modificado por longitud) ...
    {
        'nombre': 'Alas de Mariposa',
        'tipo': 'fisica',
        'rareza': 'legendaria',
        'prob': 0.00001,
        'causas': ['divina', 'herencia_mixta'],
        'stats': {'agilidad': 20, 'carisma': 25, 'fuerza': -10},
        'habilidades': ['volar_corto', 'levitar'],
        'heredable': True,
        'prob_herencia': 0.1,
        'visual': {'alas': 'mariposa_espalda', 'piel': 'iridiscente'},
        'descripcion': 'Alas funcionales de mariposa, belleza sobrenatural'
    }
]

# ================================================================
# GENERADOR DE MUTACIONES (ADAPTADO A POSTGRESQL)
# ================================================================

class GeneradorMutaciones:
    # Adaptación de la inicialización
    def __init__(self):
        self.db = DatabaseConnector()
        self.conn = self.db.connect()
        self.cursor = self.db.cursor

    def execute_query(self, query, params=None):
        """Wrapper para adaptar placeholders de SQLite (?) a PostgreSQL (%s)"""
        if self.db.db_type == 'postgres':
            query = query.replace('?', '%s')
            
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def commit(self):
        self.conn.commit()
        
    # Aplicar schema (eliminado de aquí para ser ejecutado desde el script principal)

    def poblar_catalogo(self):
        """Pobla catálogo con mutaciones base"""
        print("\n📚 Poblando catálogo de mutaciones...")

        for mut in MUTACIONES_BASE:
            causas = json.dumps(mut['causas'])
            habilidades = json.dumps(mut.get('habilidades', []))
            debilidades = json.dumps(mut.get('debilidades', []))
            visual = json.dumps(mut.get('visual', {}))

            stats_keys = ['fuerza', 'agilidad', 'inteligencia', 'resistencia', 'carisma', 'longevidad']
            stats = {k: mut.get('stats', {}).get(k, 0) for k in stats_keys}

            # Uso de %s y ON CONFLICT (asumiendo que 'nombre' es UNIQUE)
            self.execute_query('''
                INSERT INTO mutaciones_catalogo (
                    nombre, descripcion, tipo, rareza, probabilidad_natural,
                    causas_posibles, modificador_fuerza, modificador_agilidad,
                    modificador_inteligencia, modificador_resistencia,
                    modificador_carisma, modificador_longevidad,
                    habilidades_especiales, debilidades,
                    es_heredable, probabilidad_herencia, dominante,
                    cambios_fisicos
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (nombre) DO NOTHING
            ''', (
                mut['nombre'], mut['descripcion'], mut['tipo'],
                mut['rareza'], mut['prob'], causas,
                stats['fuerza'], stats['agilidad'], stats['inteligencia'],
                stats['resistencia'], stats['carisma'], stats['longevidad'],
                habilidades, debilidades,
                mut.get('heredable', False),
                mut.get('prob_herencia', 0.5),
                mut.get('dominante', False),
                visual
            ))

        self.commit()
        print(f"✅ {len(MUTACIONES_BASE)} mutaciones añadidas al catálogo")

    def asignar_mutacion_natural(self, persona_id: int, año: int) -> bool:
        """Intenta asignar una mutación natural (muy raro)"""

        if random.random() > 0.001:
            return False

        # Seleccionar mutación al azar según probabilidades
        self.execute_query('''
            SELECT id, nombre, probabilidad_natural
            FROM mutaciones_catalogo
            ORDER BY RANDOM()
            LIMIT 10
        ''')

        mutaciones = self.fetchall()
        if not mutaciones:
            return False

        total_prob = sum(m['probabilidad_natural'] for m in mutaciones)
        r = random.random() * total_prob
        acum = 0

        mutacion_id = None
        for mut in mutaciones:
            acum += mut['probabilidad_natural']
            if r <= acum:
                mutacion_id = mut['id']
                break

        if not mutacion_id:
            return False

        # Asignar mutación (uso de %s y ON CONFLICT DO NOTHING)
        self.execute_query('''
            INSERT INTO personas_mutaciones (
                persona_id, mutacion_id, año_adquisicion,
                causa, evento_origen, nivel_manifestacion
            ) VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (persona_id, mutacion_id) DO NOTHING
        ''', (
            persona_id, mutacion_id, año,
            'nacimiento', 'Mutación espontánea natural',
            random.randint(1, 3)
        ))

        self.actualizar_stats_persona(persona_id)

        self.commit()
        return True

    def asignar_mutacion_divina(self, persona_id: int, año: int,
                                dios_id: Optional[int] = None) -> int:
        """Asigna mutación por intervención divina"""

        self.execute_query('''
            SELECT id FROM mutaciones_catalogo
            WHERE tipo IN (%s, %s)
            AND rareza IN (%s, %s)
            ORDER BY RANDOM()
            LIMIT 1
        ''', ('divina', 'magica', 'epica', 'legendaria'))

        result = self.fetchone()
        if not result:
            return 0

        mutacion_id = result['id']

        self.execute_query('''
            INSERT INTO personas_mutaciones (
                persona_id, mutacion_id, año_adquisicion,
                causa, evento_origen, nivel_manifestacion
            ) VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (persona_id, mutacion_id) DO NOTHING
        ''', (
            persona_id, mutacion_id, año,
            'divina', f'Bendición/Maldición divina (dios_id: {dios_id})',
            random.randint(5, 10)
        ))

        self.actualizar_stats_persona(persona_id)
        self.commit()
        return mutacion_id

    def heredar_mutaciones(self, hijo_id: int, padre_id: int, madre_id: int, año: int):
        """Hereda mutaciones de los padres"""

        self.execute_query('''
            SELECT pm.mutacion_id, pm.persona_id, mc.probabilidad_herencia,
                   mc.dominante, mc.nombre
            FROM personas_mutaciones pm
            JOIN mutaciones_catalogo mc ON pm.mutacion_id = mc.id
            WHERE pm.persona_id IN (%s, %s)
            AND mc.es_heredable = TRUE
        ''', (padre_id, madre_id))

        mutaciones_padres = self.fetchall()

        for mut in mutaciones_padres:
            mut_id = mut['mutacion_id']
            progenitor_id = mut['persona_id']
            prob_her = mut['probabilidad_herencia']
            dominante = mut['dominante']
            nombre = mut['nombre']

            if dominante:
                prob_her *= 1.5

            if random.random() < prob_her:
                # Heredar mutación
                self.execute_query('''
                    INSERT INTO personas_mutaciones (
                        persona_id, mutacion_id, año_adquisicion,
                        causa, evento_origen, heredada_de_id,
                        nivel_manifestacion
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (persona_id, mutacion_id) DO NOTHING
                ''', (
                    hijo_id, mut_id, año,
                    'nacimiento', 'Heredado de progenitor',
                    progenitor_id,
                    random.randint(1, 5)
                ))

                self.verificar_crear_linaje(mut_id, progenitor_id, año)

        self.actualizar_stats_persona(hijo_id)
        self.commit()

    def actualizar_stats_persona(self, persona_id: int):
        """Actualiza stats de persona según sus mutaciones"""

        self.execute_query('''
            SELECT
                SUM(mc.modificador_fuerza) AS mod_fuerza,
                SUM(mc.modificador_agilidad) AS mod_agilidad,
                SUM(mc.modificador_inteligencia) AS mod_inteligencia,
                SUM(mc.modificador_resistencia) AS mod_resistencia,
                SUM(mc.modificador_carisma) AS mod_carisma
            FROM personas_mutaciones pm
            JOIN mutaciones_catalogo mc ON pm.mutacion_id = mc.id
            WHERE pm.persona_id = %s
            AND pm.activa = TRUE
        ''', (persona_id,))

        mods = self.fetchone()

        if mods:
            # PostgreSQL usa COALESCE para manejar el NULL de SUM en SQL si no hay mutaciones
            fuerza = mods.get('mod_fuerza') or 0
            agilidad = mods.get('mod_agilidad') or 0
            inteligencia = mods.get('mod_inteligencia') or 0
            resistencia = mods.get('mod_resistencia') or 0
            carisma = mods.get('mod_carisma') or 0

            # Aplicar modificadores
            self.execute_query('''
                UPDATE personas
                SET
                    fuerza = fuerza + %s,
                    agilidad = agilidad + %s,
                    inteligencia = inteligencia + %s,
                    resistencia = resistencia + %s,
                    carisma = carisma + %s
                WHERE id = %s
            ''', (fuerza, agilidad, inteligencia, resistencia, carisma, persona_id))

        self.commit()

    def verificar_crear_linaje(self, mutacion_id: int, fundador_id: int, año: int):
        """Crea un linaje si no existe"""

        self.execute_query('''
            SELECT id FROM linajes_mutaciones
            WHERE mutacion_id = %s AND fundador_persona_id = %s
        ''', (mutacion_id, fundador_id))

        if self.fetchone():
            return

        # Obtener info del fundador
        self.execute_query('''
            SELECT nombre_completo, civilizacion_id
            FROM personas WHERE id = %s
        ''', (fundador_id,))

        fundador_info = self.fetchone()
        nombre = fundador_info['nombre_completo']
        civ_id = fundador_info['civilizacion_id']

        # Obtener nombre mutación
        self.execute_query('SELECT nombre FROM mutaciones_catalogo WHERE id = %s', (mutacion_id,))
        mut_nombre = self.fetchone()['nombre']

        nombre_linaje = f"Linaje {mut_nombre} de {nombre.split()[0]}"

        self.execute_query('''
            INSERT INTO linajes_mutaciones (
                nombre_linaje, mutacion_id, fundador_persona_id,
                año_origen, civilizacion_origen_id
            ) VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (nombre_linaje) DO NOTHING
        ''', (nombre_linaje, mutacion_id, fundador_id, año, civ_id))

        self.commit()

    def simular_mutaciones_poblacion(self, año_inicio: int = 1500, año_fin: int = 3000):
        """Simula mutaciones para toda la población durante el período"""
        print(f"\n{'='*70}")
        print(f"SIMULANDO MUTACIONES: {año_inicio}-{año_fin}")
        print(f"{'='*70}\n")

        self.execute_query('''
            SELECT id, año_nacimiento
            FROM personas
            WHERE año_nacimiento >= %s AND año_nacimiento <= %s
        ''', (año_inicio, año_fin))

        personas = self.fetchall()
        print(f"📊 Evaluando {len(personas)} personas para mutaciones naturales...")

        mutaciones_asignadas = 0

        for i, persona in enumerate(personas):
            if self.asignar_mutacion_natural(persona['id'], persona['año_nacimiento']):
                mutaciones_asignadas += 1

            if (i + 1) % 1000 == 0:
                print(f"  ✓ {i + 1}/{len(personas)} evaluados... ({mutaciones_asignadas} mutaciones)")

        print(f"\n✅ Mutaciones naturales: {mutaciones_asignadas}")

        # Eventos divinos (raros)
        print(f"\n⚡ Simulando intervenciones divinas...")
        eventos_divinos = int((año_fin - año_inicio) * 0.01)

        for _ in range(eventos_divinos):
            self.execute_query('SELECT id FROM personas ORDER BY RANDOM() LIMIT 1')
            persona_row = self.fetchone()
            if not persona_row: continue # Si la BD está vacía

            persona_id = persona_row['id']
            año = random.randint(año_inicio, año_fin)

            self.execute_query('SELECT id FROM dioses ORDER BY RANDOM() LIMIT 1')
            dios_row = self.fetchone()
            dios_id = dios_row['id'] if dios_row else None
            
            self.asignar_mutacion_divina(persona_id, año, dios_id)

        print(f"✅ {eventos_divinos} intervenciones divinas")

    def generar_reporte(self):
        """Genera reporte de mutaciones"""
        print(f"\n{'='*70}")
        print("REPORTE DE MUTACIONES")
        print(f"{'='*70}\n")

        self.execute_query('SELECT COUNT(*) AS total FROM personas_mutaciones')
        total = self.fetchone()['total']
        
        # Por tipo
        self.execute_query('''
            SELECT mc.tipo, COUNT(*) AS count
            FROM personas_mutaciones pm
            JOIN mutaciones_catalogo mc ON pm.mutacion_id = mc.id
            GROUP BY mc.tipo
            ORDER BY COUNT(*) DESC
        ''')

        print(f"📊 MUTACIONES POR TIPO (Total: {total}):")
        for row in self.fetchall():
            print(f"  {row['tipo']:15s}: {row['count']:5d}")

        # Más comunes
        print(f"\n🔝 MUTACIONES MÁS COMUNES:")
        self.execute_query('''
            SELECT mc.nombre, COUNT(*) AS count, mc.rareza
            FROM personas_mutaciones pm
            JOIN mutaciones_catalogo mc ON pm.mutacion_id = mc.id
            GROUP BY mc.nombre, mc.rareza
            ORDER BY COUNT(*) DESC
            LIMIT 10
        ''')

        for row in self.fetchall():
            print(f"  {row['nombre']:30s}: {row['count']:4d} ({row['rareza']})")

        # Linajes
        self.execute_query('SELECT COUNT(*) AS count FROM linajes_mutaciones')
        linajes = self.fetchone()['count']
        print(f"\n🧬 LINAJES FORMADOS: {linajes}")

def main():
    """Función principal (para ejecución directa del módulo)"""
    print("="*70)
    print("SISTEMA DE MUTACIONES GENÉTICAS (STANDALONE)")
    print("Portales del Quinto Sol")
    print("="*70)

    try:
        generador = GeneradorMutaciones()
        generador.poblar_catalogo() # Aplicar schema se hace en el script integrador
    except Exception as e:
        print(f"❌ Error al inicializar: {e}")
        return

    # Menú
    print("\nOpciones:")
    print("  1. Simular mutaciones en población (1500-3000)")
    print("  2. Ver catálogo de mutaciones")
    print("  3. Generar reporte")

    opcion = input("\nSelecciona opción (1-3): ").strip()

    if opcion == '1':
        confirm = input("\n⚠️  ¿Simular mutaciones en toda la población? (s/n): ").strip().lower()
        if confirm == 's':
            generador.simular_mutaciones_poblacion()
            generador.generar_reporte()
    elif opcion == '2':
        generador.execute_query('SELECT nombre, tipo, rareza, descripcion FROM mutaciones_catalogo')
        print(f"\n{'='*70}")
        print("CATÁLOGO DE MUTACIONES")
        print(f"{'='*70}\n")
        for row in generador.fetchall():
            print(f"🧬 {row['nombre']} ({row['tipo']} - {row['rareza']})")
            print(f"   {row['descripcion']}\n")
    elif opcion == '3':
        generador.generar_reporte()

    generador.conn.close()
    print("\n✅ Proceso completado")

if __name__ == '__main__':
    main()