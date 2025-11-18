#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Mutaciones Genéticas
Portales del Quinto Sol

Mutaciones raras que afectan stats y apariencia:
- Mutaciones naturales (muy raras: 0.1%)
- Mutaciones divinas (bendiciones/maldiciones)
- Mutaciones heredables (pueden formar linajes)
- Efectos en stats y habilidades especiales
"""

import sqlite3
import random
import json
from typing import List, Tuple, Optional, Dict

# ================================================================
# CATÁLOGO DE MUTACIONES
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
    {
        'nombre': 'Velocidad Sobrenatural',
        'tipo': 'fisica',
        'rareza': 'rara',
        'prob': 0.0005,
        'causas': ['divina', 'herencia'],
        'stats': {'agilidad': 30, 'fuerza': -5},
        'habilidades': ['dash_rapido', 'reflejos_felinos'],
        'heredable': True,
        'prob_herencia': 0.4,
        'visual': {'musculatura': 'fibrosa', 'ojos': 'reflejos_dorados'},
        'descripcion': 'Velocidad de movimiento 3x superior al promedio'
    },
    {
        'nombre': 'Piel de Obsidiana',
        'tipo': 'fisica',
        'rareza': 'epica',
        'prob': 0.0002,
        'causas': ['divina', 'radiacion'],
        'stats': {'resistencia': 40, 'carisma': -10},
        'habilidades': ['absorber_golpes', 'inmunidad_cortes'],
        'heredable': True,
        'prob_herencia': 0.5,
        'dominante': True,
        'visual': {'piel': 'negra_brillante', 'textura': 'cristalina'},
        'descripcion': 'Piel dura como obsidiana, casi impenetrable'
    },
    {
        'nombre': 'Regeneración Acelerada',
        'tipo': 'fisica',
        'rareza': 'epica',
        'prob': 0.0003,
        'causas': ['divina', 'herencia', 'ritual'],
        'stats': {'resistencia': 30, 'longevidad': 50},
        'habilidades': ['curar_heridas_rapido', 'regenerar_miembros'],
        'debilidades': ['fuego', 'veneno_mistico'],
        'heredable': True,
        'prob_herencia': 0.25,
        'visual': {'cicatrices': 'desaparecen'},
        'descripcion': 'Heridas curan 10x más rápido, puede regenerar dedos'
    },

    # MENTALES
    {
        'nombre': 'Mente Prodigio',
        'tipo': 'mental',
        'rareza': 'rara',
        'prob': 0.0008,
        'causas': ['herencia', 'divina', 'estudio_extremo'],
        'stats': {'inteligencia': 35, 'carisma': 10},
        'habilidades': ['memoria_fotografica', 'aprendizaje_acelerado', 'calculo_mental'],
        'heredable': True,
        'prob_herencia': 0.6,
        'visual': {'frente': 'ligeramente_mas_grande'},
        'descripcion': 'Inteligencia excepcional, aprende 5x más rápido'
    },
    {
        'nombre': 'Telepatía Menor',
        'tipo': 'magica',
        'rareza': 'epica',
        'prob': 0.0001,
        'causas': ['divina', 'ritual'],
        'stats': {'inteligencia': 20, 'carisma': 15},
        'habilidades': ['leer_emociones', 'enviar_pensamientos_simples'],
        'debilidades': ['ruido_mental', 'agotamiento'],
        'heredable': False,
        'visual': {'ojos': 'brillo_violeta'},
        'descripcion': 'Puede leer emociones superficiales y enviar pensamientos simples'
    },
    {
        'nombre': 'Visión del Águila',
        'tipo': 'fisica',
        'rareza': 'rara',
        'prob': 0.0006,
        'causas': ['herencia', 'divina'],
        'stats': {'agilidad': 10, 'inteligencia': 5},
        'habilidades': ['vision_telescopica', 'detectar_movimiento'],
        'heredable': True,
        'prob_herencia': 0.5,
        'visual': {'ojos': 'dorados_grandes', 'pupilas': 'aguilinas'},
        'descripcion': 'Vista 10x más aguda, ve detalles a kilómetros'
    },

    # MÁGICAS/DIVINAS
    {
        'nombre': 'Sangre de Fuego',
        'tipo': 'magica',
        'rareza': 'legendaria',
        'prob': 0.00005,
        'causas': ['divina', 'ritual'],
        'stats': {'fuerza': 20, 'resistencia': 25, 'carisma': 15},
        'habilidades': ['inmunidad_fuego', 'emanar_calor', 'quemar_contacto'],
        'debilidades': ['agua_helada', 'frio_extremo'],
        'heredable': True,
        'prob_herencia': 0.2,
        'dominante': True,
        'visual': {'venas': 'brillan_rojo', 'temperatura': 'siempre_caliente'},
        'descripcion': 'Sangre ardiente que otorga inmunidad al fuego y poder piroquinético'
    },
    {
        'nombre': 'Aura Divina',
        'tipo': 'divina',
        'rareza': 'legendaria',
        'prob': 0.00003,
        'causas': ['divina'],
        'stats': {'carisma': 40, 'inteligencia': 20, 'resistencia': 15},
        'habilidades': ['inspirar_aliados', 'aterrar_enemigos', 'curar_tocando'],
        'heredable': False,
        'visual': {'aura': 'luz_dorada_visible'},
        'descripcion': 'Aura visible que inspira o aterra, bendición directa de un dios'
    },
    {
        'nombre': 'Comunión con la Naturaleza',
        'tipo': 'magica',
        'rareza': 'epica',
        'prob': 0.0002,
        'causas': ['herencia', 'divina'],
        'stats': {'inteligencia': 15, 'carisma': 20, 'longevidad': 30},
        'habilidades': ['hablar_animales', 'acelerar_plantas', 'sentir_tierra'],
        'heredable': True,
        'prob_herencia': 0.35,
        'visual': {'piel': 'tono_verdoso', 'cabello': 'con_hojas'},
        'descripcion': 'Conexión con plantas y animales, puede comunicarse con ellos'
    },

    # MALDICIONES
    {
        'nombre': 'Sed de Sangre',
        'tipo': 'maldicion',
        'rareza': 'rara',
        'prob': 0.0003,
        'causas': ['maldicion', 'ritual_fallido'],
        'stats': {'fuerza': 25, 'agilidad': 15, 'carisma': -25, 'longevidad': -20},
        'habilidades': ['fuerza_en_combate', 'olfato_sangre'],
        'debilidades': ['luz_solar', 'sed_constante'],
        'heredable': True,
        'prob_herencia': 0.7,
        'dominante': True,
        'visual': {'ojos': 'rojos', 'colmillos': 'pronunciados'},
        'descripcion': 'Necesidad de beber sangre, fuerte en combate pero socialmente rechazado'
    },
    {
        'nombre': 'Marca del Desterrado',
        'tipo': 'maldicion',
        'rareza': 'rara',
        'prob': 0.0002,
        'causas': ['maldicion', 'castigo_divino'],
        'stats': {'carisma': -30, 'resistencia': 10},
        'habilidades': ['invisibilidad_social', 'resistir_dolor'],
        'debilidades': ['rechazo_universal', 'no_entrar_templos'],
        'heredable': True,
        'prob_herencia': 0.5,
        'visual': {'marca': 'simbolo_frente', 'aura': 'sombria'},
        'descripcion': 'Marca visible de castigo divino, rechazado por la sociedad'
    },

    # HÍBRIDAS (RARAS)
    {
        'nombre': 'Metamorfo Nocturno',
        'tipo': 'magica',
        'rareza': 'legendaria',
        'prob': 0.00008,
        'causas': ['ritual', 'herencia_mixta'],
        'stats': {'agilidad': 30, 'inteligencia': 15, 'carisma': -15},
        'habilidades': ['transformacion_animal', 'vision_nocturna', 'sigilo_absoluto'],
        'debilidades': ['luz_solar_directa', 'plata'],
        'heredable': True,
        'prob_herencia': 0.15,
        'visual': {'ojos': 'brillan_noche', 'rasgos': 'animales'},
        'descripcion': 'Puede transformarse en animal nocturno, muy raro'
    },
    {
        'nombre': 'Toque Venenoso',
        'tipo': 'fisica',
        'rareza': 'epica',
        'prob': 0.00015,
        'causas': ['maldicion', 'exposicion_toxica'],
        'stats': {'agilidad': 15, 'carisma': -20},
        'habilidades': ['secretar_veneno', 'inmunidad_venenos'],
        'debilidades': ['aislamiento_social', 'contacto_accidental'],
        'heredable': True,
        'prob_herencia': 0.4,
        'visual': {'piel': 'tono_verdoso', 'uñas': 'negras'},
        'descripcion': 'Secreta veneno por la piel, letal al tacto'
    },
    {
        'nombre': 'Ojos del Futuro',
        'tipo': 'divina',
        'rareza': 'legendaria',
        'prob': 0.00002,
        'causas': ['divina'],
        'stats': {'inteligencia': 25, 'carisma': 20},
        'habilidades': ['visiones_futuro', 'intuicion_sobrenatural'],
        'debilidades': ['locura_progresiva', 'visiones_incontrolables'],
        'heredable': False,
        'visual': {'ojos': 'blancos_brillantes', 'mirada': 'distante'},
        'descripcion': 'Visiones espontáneas del futuro, don divino peligroso'
    },

    # ÚNICAS/COSMÉTICA
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
# GENERADOR DE MUTACIONES
# ================================================================

class GeneradorMutaciones:
    def __init__(self, db_path='quinto_sol.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def aplicar_schema(self):
        """Aplica schema de mutaciones"""
        print("\n📋 Aplicando schema de mutaciones...")

        with open('schema_mutaciones.sql', 'r', encoding='utf-8') as f:
            schema_sql = f.read()

        self.conn.executescript(schema_sql)
        self.conn.commit()
        print("✅ Schema aplicado")

    def poblar_catalogo(self):
        """Pobla catálogo con mutaciones base"""
        print("\n📚 Poblando catálogo de mutaciones...")

        for mut in MUTACIONES_BASE:
            # Preparar JSON
            causas = json.dumps(mut['causas'])
            habilidades = json.dumps(mut.get('habilidades', []))
            debilidades = json.dumps(mut.get('debilidades', []))
            visual = json.dumps(mut.get('visual', {}))

            # Stats
            stats_keys = ['fuerza', 'agilidad', 'inteligencia', 'resistencia', 'carisma', 'longevidad']
            stats = {k: mut.get('stats', {}).get(k, 0) for k in stats_keys}

            self.cursor.execute('''
                INSERT OR IGNORE INTO mutaciones_catalogo (
                    nombre, descripcion, tipo, rareza, probabilidad_natural,
                    causas_posibles, modificador_fuerza, modificador_agilidad,
                    modificador_inteligencia, modificador_resistencia,
                    modificador_carisma, modificador_longevidad,
                    habilidades_especiales, debilidades,
                    es_heredable, probabilidad_herencia, dominante,
                    cambios_fisicos
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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

        self.conn.commit()
        print(f"✅ {len(MUTACIONES_BASE)} mutaciones añadidas al catálogo")

    def asignar_mutacion_natural(self, persona_id: int, año: int) -> bool:
        """Intenta asignar una mutación natural (muy raro)"""

        # Solo 0.1% de probabilidad
        if random.random() > 0.001:
            return False

        # Seleccionar mutación al azar según probabilidades
        self.cursor.execute('''
            SELECT id, nombre, probabilidad_natural
            FROM mutaciones_catalogo
            ORDER BY RANDOM()
            LIMIT 10
        ''')

        mutaciones = self.cursor.fetchall()
        if not mutaciones:
            return False

        # Selección ponderada
        total_prob = sum(m[2] for m in mutaciones)
        r = random.random() * total_prob
        acum = 0

        mutacion_id = None
        for m_id, nombre, prob in mutaciones:
            acum += prob
            if r <= acum:
                mutacion_id = m_id
                break

        if not mutacion_id:
            return False

        # Asignar mutación
        self.cursor.execute('''
            INSERT INTO personas_mutaciones (
                persona_id, mutacion_id, año_adquisicion,
                causa, evento_origen, nivel_manifestacion
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            persona_id, mutacion_id, año,
            'nacimiento', 'Mutación espontánea natural',
            random.randint(1, 3)  # Baja manifestación al inicio
        ))

        # Actualizar stats de la persona
        self.actualizar_stats_persona(persona_id)

        self.conn.commit()
        return True

    def asignar_mutacion_divina(self, persona_id: int, año: int,
                                dios_id: Optional[int] = None) -> int:
        """Asigna mutación por intervención divina"""

        # Seleccionar mutación divina o mágica
        self.cursor.execute('''
            SELECT id FROM mutaciones_catalogo
            WHERE tipo IN ('divina', 'magica')
            AND rareza IN ('epica', 'legendaria')
            ORDER BY RANDOM()
            LIMIT 1
        ''')

        result = self.cursor.fetchone()
        if not result:
            return 0

        mutacion_id = result[0]

        self.cursor.execute('''
            INSERT INTO personas_mutaciones (
                persona_id, mutacion_id, año_adquisicion,
                causa, evento_origen, nivel_manifestacion
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            persona_id, mutacion_id, año,
            'divina', f'Bendición/Maldición divina (dios_id: {dios_id})',
            random.randint(5, 10)  # Alta manifestación
        ))

        self.actualizar_stats_persona(persona_id)
        self.conn.commit()
        return mutacion_id

    def heredar_mutaciones(self, hijo_id: int, padre_id: int, madre_id: int, año: int):
        """Hereda mutaciones de los padres"""

        # Obtener mutaciones heredables de los padres
        self.cursor.execute('''
            SELECT pm.mutacion_id, pm.persona_id, mc.probabilidad_herencia,
                   mc.dominante, mc.nombre
            FROM personas_mutaciones pm
            JOIN mutaciones_catalogo mc ON pm.mutacion_id = mc.id
            WHERE pm.persona_id IN (?, ?)
            AND mc.es_heredable = 1
        ''', (padre_id, madre_id))

        mutaciones_padres = self.cursor.fetchall()

        for mut_id, progenitor_id, prob_her, dominante, nombre in mutaciones_padres:
            # Probabilidad de herencia
            if dominante:
                prob_her *= 1.5  # Más probabilidad si es dominante

            if random.random() < prob_her:
                # Heredar mutación
                self.cursor.execute('''
                    INSERT OR IGNORE INTO personas_mutaciones (
                        persona_id, mutacion_id, año_adquisicion,
                        causa, evento_origen, heredada_de_id,
                        nivel_manifestacion
                    ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    hijo_id, mut_id, año,
                    'nacimiento', f'Heredado de progenitor',
                    progenitor_id,
                    random.randint(1, 5)
                ))

                # Verificar si es fundador de linaje
                self.verificar_crear_linaje(mut_id, progenitor_id, año)

        self.actualizar_stats_persona(hijo_id)
        self.conn.commit()

    def actualizar_stats_persona(self, persona_id: int):
        """Actualiza stats de persona según sus mutaciones"""

        self.cursor.execute('''
            SELECT
                SUM(mc.modificador_fuerza),
                SUM(mc.modificador_agilidad),
                SUM(mc.modificador_inteligencia),
                SUM(mc.modificador_resistencia),
                SUM(mc.modificador_carisma)
            FROM personas_mutaciones pm
            JOIN mutaciones_catalogo mc ON pm.mutacion_id = mc.id
            WHERE pm.persona_id = ?
            AND pm.activa = 1
        ''', (persona_id,))

        mods = self.cursor.fetchone()

        if mods and any(m for m in mods if m):
            # Aplicar modificadores
            self.cursor.execute('''
                UPDATE personas
                SET
                    fuerza = fuerza + ?,
                    agilidad = agilidad + ?,
                    inteligencia = inteligencia + ?,
                    resistencia = resistencia + ?,
                    carisma = carisma + ?
                WHERE id = ?
            ''', (*[m or 0 for m in mods], persona_id))

        self.conn.commit()

    def verificar_crear_linaje(self, mutacion_id: int, fundador_id: int, año: int):
        """Crea un linaje si no existe"""

        self.cursor.execute('''
            SELECT id FROM linajes_mutaciones
            WHERE mutacion_id = ? AND fundador_persona_id = ?
        ''', (mutacion_id, fundador_id))

        if self.cursor.fetchone():
            return  # Ya existe

        # Obtener info del fundador
        self.cursor.execute('''
            SELECT nombre_completo, civilizacion_id
            FROM personas WHERE id = ?
        ''', (fundador_id,))

        nombre, civ_id = self.cursor.fetchone()

        # Obtener nombre mutación
        self.cursor.execute('SELECT nombre FROM mutaciones_catalogo WHERE id = ?', (mutacion_id,))
        mut_nombre = self.cursor.fetchone()[0]

        nombre_linaje = f"Linaje {mut_nombre} de {nombre.split()[0]}"

        self.cursor.execute('''
            INSERT INTO linajes_mutaciones (
                nombre_linaje, mutacion_id, fundador_persona_id,
                año_origen, civilizacion_origen_id
            ) VALUES (?, ?, ?, ?, ?)
        ''', (nombre_linaje, mutacion_id, fundador_id, año, civ_id))

        self.conn.commit()

    def simular_mutaciones_poblacion(self, año_inicio: int = 1500, año_fin: int = 3000):
        """Simula mutaciones para toda la población durante el período"""
        print(f"\n{'='*70}")
        print(f"SIMULANDO MUTACIONES: {año_inicio}-{año_fin}")
        print(f"{'='*70}\n")

        # Mutaciones naturales al nacer
        self.cursor.execute('''
            SELECT id, año_nacimiento
            FROM personas
            WHERE año_nacimiento >= ? AND año_nacimiento <= ?
        ''', (año_inicio, año_fin))

        personas = self.cursor.fetchall()
        print(f"📊 Evaluando {len(personas)} personas para mutaciones naturales...")

        mutaciones_asignadas = 0

        for i, (persona_id, año_nac) in enumerate(personas):
            if self.asignar_mutacion_natural(persona_id, año_nac):
                mutaciones_asignadas += 1

            if (i + 1) % 1000 == 0:
                print(f"  ✓ {i + 1}/{len(personas)} evaluados... ({mutaciones_asignadas} mutaciones)")

        print(f"\n✅ Mutaciones naturales: {mutaciones_asignadas}")

        # Eventos divinos (raros)
        print(f"\n⚡ Simulando intervenciones divinas...")
        eventos_divinos = int((año_fin - año_inicio) * 0.01)  # ~15 eventos en 1500 años

        for _ in range(eventos_divinos):
            # Persona al azar
            self.cursor.execute('SELECT id FROM personas ORDER BY RANDOM() LIMIT 1')
            persona_id = self.cursor.fetchone()[0]
            año = random.randint(año_inicio, año_fin)

            self.asignar_mutacion_divina(persona_id, año)

        print(f"✅ {eventos_divinos} intervenciones divinas")

    def generar_reporte(self):
        """Genera reporte de mutaciones"""
        print(f"\n{'='*70}")
        print("REPORTE DE MUTACIONES")
        print(f"{'='*70}\n")

        # Total mutaciones
        self.cursor.execute('SELECT COUNT(*) FROM personas_mutaciones')
        total = self.cursor.fetchone()[0]

        # Por tipo
        self.cursor.execute('''
            SELECT mc.tipo, COUNT(*)
            FROM personas_mutaciones pm
            JOIN mutaciones_catalogo mc ON pm.mutacion_id = mc.id
            GROUP BY mc.tipo
            ORDER BY COUNT(*) DESC
        ''')

        print(f"📊 MUTACIONES POR TIPO:")
        for tipo, count in self.cursor.fetchall():
            print(f"  {tipo:15s}: {count:5d}")

        # Más comunes
        print(f"\n🔝 MUTACIONES MÁS COMUNES:")
        self.cursor.execute('''
            SELECT mc.nombre, COUNT(*), mc.rareza
            FROM personas_mutaciones pm
            JOIN mutaciones_catalogo mc ON pm.mutacion_id = mc.id
            GROUP BY mc.nombre
            ORDER BY COUNT(*) DESC
            LIMIT 10
        ''')

        for nombre, count, rareza in self.cursor.fetchall():
            print(f"  {nombre:30s}: {count:4d} ({rareza})")

        # Linajes
        self.cursor.execute('SELECT COUNT(*) FROM linajes_mutaciones')
        linajes = self.cursor.fetchone()[0]
        print(f"\n🧬 LINAJES FORMADOS: {linajes}")

def main():
    """Función principal"""
    print("="*70)
    print("SISTEMA DE MUTACIONES GENÉTICAS")
    print("Portales del Quinto Sol")
    print("="*70)

    generador = GeneradorMutaciones()

    # Aplicar schema
    generador.aplicar_schema()

    # Poblar catálogo
    generador.poblar_catalogo()

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
        generador.cursor.execute('SELECT nombre, tipo, rareza, descripcion FROM mutaciones_catalogo')
        print(f"\n{'='*70}")
        print("CATÁLOGO DE MUTACIONES")
        print(f"{'='*70}\n")
        for nombre, tipo, rareza, desc in generador.cursor.fetchall():
            print(f"🧬 {nombre} ({tipo} - {rareza})")
            print(f"   {desc}\n")
    elif opcion == '3':
        generador.generar_reporte()

    generador.conn.close()
    print("\n✅ Proceso completado")

if __name__ == '__main__':
    main()
