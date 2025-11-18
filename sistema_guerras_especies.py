#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Guerras Inter-Especies
Portales del Quinto Sol

Simula conflictos entre especies sirvientes y humanos:
- Guerras menos frecuentes que guerras humanas
- Impacto en poblaciones y diplomacia
- Causas variadas (territorio, religión, recursos)
- Intervención divina posible
"""

import sqlite3
import random
import json
from typing import List, Tuple, Optional, Dict

# ================================================================
# CONFIGURACIÓN DE GUERRA
# ================================================================

# Probabilidad de guerra por año (muy baja)
PROBABILIDAD_GUERRA_ANUAL = 0.003  # 0.3% por año = ~4.5 guerras en 1500 años entre todas las especies

# Probabilidad de escaramuza (más común)
PROBABILIDAD_ESCARAMUZA_ANUAL = 0.015  # 1.5% por año

# Causas de guerra y sus probabilidades
CAUSAS_GUERRA = {
    'territorial': {
        'prob': 0.35,
        'desc': 'Disputa por territorios y fronteras',
        'intensidad_media': 'guerra'
    },
    'recursos': {
        'prob': 0.25,
        'desc': 'Conflicto por recursos naturales (agua, minerales, flora)',
        'intensidad_media': 'guerra'
    },
    'religiosa': {
        'prob': 0.15,
        'desc': 'Guerra santa o profanación de lugares sagrados',
        'intensidad_media': 'guerra_total'
    },
    'venganza': {
        'prob': 0.12,
        'desc': 'Venganza por agravios previos',
        'intensidad_media': 'batalla'
    },
    'expansion': {
        'prob': 0.08,
        'desc': 'Expansión imperialista de una especie',
        'intensidad_media': 'guerra'
    },
    'defensa': {
        'prob': 0.05,
        'desc': 'Defensa preventiva ante amenaza percibida',
        'intensidad_media': 'batalla'
    }
}

# Intensidades de guerra
INTENSIDADES = {
    'escaramuza': {
        'bajas_atacante': (5, 50),
        'bajas_defensora': (5, 50),
        'duracion': (1, 30),  # días
        'num_batallas': (1, 3)
    },
    'batalla': {
        'bajas_atacante': (50, 300),
        'bajas_defensora': (50, 300),
        'duracion': (30, 180),  # ~1-6 meses
        'num_batallas': (2, 8)
    },
    'guerra': {
        'bajas_atacante': (200, 1500),
        'bajas_defensora': (200, 1500),
        'duracion': (180, 1095),  # 0.5-3 años
        'num_batallas': (5, 20)
    },
    'guerra_total': {
        'bajas_atacante': (1000, 8000),
        'bajas_defensora': (1000, 8000),
        'duracion': (1095, 3650),  # 3-10 años
        'num_batallas': (15, 50)
    }
}

# Tipos de batalla
TIPOS_BATALLA = [
    'campo_abierto', 'asedio', 'emboscada', 'naval',
    'aerea', 'nocturna', 'defensiva', 'incursion'
]

# ================================================================
# GENERADOR DE GUERRAS
# ================================================================

class GeneradorGuerras:
    def __init__(self, db_path='quinto_sol.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cargar_datos()

    def cargar_datos(self):
        """Carga datos de referencia"""
        # Especies
        self.cursor.execute("SELECT id, nombre FROM especies WHERE nombre != 'Humanos II'")
        self.especies = {nombre: id for id, nombre in self.cursor.fetchall()}

        # Civilizaciones
        self.cursor.execute("SELECT id, nombre FROM civilizaciones")
        self.civilizaciones = {nombre: id for id, nombre in self.cursor.fetchall()}

        # Dioses
        self.cursor.execute("SELECT id, nombre FROM dioses")
        self.dioses = {nombre: id for id, nombre in self.cursor.fetchall()}

        # Lugares
        self.cursor.execute("SELECT id, nombre, civilizacion_id FROM pueblos_ciudades")
        self.lugares = [(id, nombre, civ_id) for id, nombre, civ_id in self.cursor.fetchall()]

        print(f"✅ Datos cargados:")
        print(f"   - {len(self.especies)} especies")
        print(f"   - {len(self.civilizaciones)} civilizaciones")
        print(f"   - {len(self.lugares)} lugares")

    def aplicar_schema(self):
        """Aplica schema de guerras"""
        print("\n📋 Aplicando schema de guerras...")

        with open('schema_guerras_especies.sql', 'r', encoding='utf-8') as f:
            schema_sql = f.read()

        self.conn.executescript(schema_sql)
        self.conn.commit()
        print("✅ Schema aplicado")

    def obtener_relacion_diplomatica(self, especie1_id: int, especie2_id: int) -> int:
        """Obtiene nivel de relación entre dos especies"""
        self.cursor.execute('''
            SELECT nivel_relacion
            FROM diplomacia_especies
            WHERE especie_id = ? AND especie_objetivo_id = ?
        ''', (especie1_id, especie2_id))

        result = self.cursor.fetchone()
        return result[0] if result else 0

    def actualizar_relacion_diplomatica(self, especie1_id: int, especie2_id: int,
                                       cambio: int, evento: str, año: int):
        """Actualiza relación diplomática entre dos especies"""
        # Actualizar en ambas direcciones
        for esp1, esp2 in [(especie1_id, especie2_id), (especie2_id, especie1_id)]:
            self.cursor.execute('''
                UPDATE diplomacia_especies
                SET nivel_relacion = nivel_relacion + ?,
                    ultimo_cambio_año = ?,
                    ultimo_evento = ?
                WHERE especie_id = ? AND especie_objetivo_id = ?
            ''', (cambio, año, evento, esp1, esp2))

            # Si es guerra, incrementar contador
            if 'guerra' in evento.lower():
                self.cursor.execute('''
                    UPDATE diplomacia_especies
                    SET guerras_totales = guerras_totales + 1
                    WHERE especie_id = ? AND especie_objetivo_id = ?
                ''', (esp1, esp2))

            # Actualizar estado diplomático según nivel
            self.cursor.execute('''
                SELECT nivel_relacion FROM diplomacia_especies
                WHERE especie_id = ? AND especie_objetivo_id = ?
            ''', (esp1, esp2))

            nivel = self.cursor.fetchone()[0]

            if nivel < -50:
                nuevo_estado = 'guerra'
            elif nivel < -20:
                nuevo_estado = 'hostil'
            elif nivel < 20:
                nuevo_estado = 'neutral'
            elif nivel < 50:
                nuevo_estado = 'amistoso'
            else:
                nuevo_estado = 'aliado'

            self.cursor.execute('''
                UPDATE diplomacia_especies
                SET estado_diplomatico = ?
                WHERE especie_id = ? AND especie_objetivo_id = ?
            ''', (nuevo_estado, esp1, esp2))

        self.conn.commit()

    def seleccionar_causa_guerra(self) -> Tuple[str, str, str]:
        """Selecciona causa de guerra aleatoria"""
        r = random.random()
        acumulado = 0

        for causa, info in CAUSAS_GUERRA.items():
            acumulado += info['prob']
            if r <= acumulado:
                return causa, info['desc'], info['intensidad_media']

        return 'territorial', 'Disputa territorial', 'guerra'

    def calcular_bajas(self, intensidad: str, modificador: float = 1.0) -> Tuple[int, int, int]:
        """Calcula bajas de una guerra"""
        config = INTENSIDADES[intensidad]

        bajas_atacante = int(random.randint(*config['bajas_atacante']) * modificador)
        bajas_defensora = int(random.randint(*config['bajas_defensora']) * modificador)

        # Civiles (10-30% del total de bajas militares)
        civiles = int((bajas_atacante + bajas_defensora) * random.uniform(0.1, 0.3))

        return bajas_atacante, bajas_defensora, civiles

    def determinar_vencedor(self, especie_atacante_id: int, especie_defensora_id: int,
                           bajas_atacante: int, bajas_defensora: int) -> Tuple[Optional[int], str]:
        """Determina vencedor de la guerra"""

        # Ratio de bajas
        ratio = bajas_defensora / bajas_atacante if bajas_atacante > 0 else 2.0

        # Factores adicionales
        # TODO: Incorporar stats de especies (fuerza, tecnología, etc)

        if ratio > 1.5:
            # Atacante causó más bajas
            return especie_atacante_id, random.choice(['rendicion', 'tratado', 'aniquilacion'])
        elif ratio < 0.67:
            # Defensor resistió mejor
            return especie_defensora_id, random.choice(['retirada', 'tratado', 'defensa_exitosa'])
        else:
            # Empate o tratado
            return None, random.choice(['empate', 'tratado', 'paz_negociada'])

    def crear_guerra(self, especie_atacante: str, especie_defensora: str,
                    año_inicio: int, duracion_años: int = None) -> int:
        """Crea una guerra entre dos especies"""

        especie_atacante_id = self.especies[especie_atacante]
        especie_defensora_id = self.especies[especie_defensora]

        # Verificar relación actual
        relacion = self.obtener_relacion_diplomatica(especie_atacante_id, especie_defensora_id)

        # Seleccionar causa
        causa, descripcion, intensidad_base = self.seleccionar_causa_guerra()

        # Ajustar intensidad según relación
        if relacion < -50:
            intensidad = 'guerra_total'
        elif relacion < -20:
            intensidad = 'guerra'
        else:
            intensidad = intensidad_base

        # Duración
        if not duracion_años:
            duracion_dias_min, duracion_dias_max = INTENSIDADES[intensidad]['duracion']
            duracion_dias = random.randint(duracion_dias_min, duracion_dias_max)
            duracion_años = max(1, duracion_dias // 365)

        año_fin = año_inicio + duracion_años

        # Calcular bajas
        bajas_atacante, bajas_defensora, civiles = self.calcular_bajas(intensidad)

        # Determinar vencedor
        vencedor_id, tipo_victoria = self.determinar_vencedor(
            especie_atacante_id, especie_defensora_id,
            bajas_atacante, bajas_defensora
        )

        # Seleccionar lugar
        lugar = random.choice(self.lugares)
        territorio_disputa = lugar[1]
        civ_afectada_id = lugar[2]

        # Intervención divina (20% de probabilidad)
        dios_favorecio_id = None
        intervencion = None

        if random.random() < 0.20:
            dios_favorecio_id = random.choice(list(self.dioses.values()))
            intervencion = json.dumps({
                'tipo': random.choice(['bendicion', 'maldicion', 'clima', 'terremoto', 'sequia']),
                'descripcion': 'El dios intervino en el conflicto',
                'impacto': random.choice(['decisivo', 'moderado', 'menor'])
            })

        # Insertar guerra
        self.cursor.execute('''
            INSERT INTO guerras_especies (
                especie_atacante_id, especie_defensora_id,
                año_inicio, año_fin, duracion_años,
                causa, descripcion, intensidad,
                territorio_disputa, civilizacion_afectada_id,
                vencedor_especie_id, tipo_victoria,
                bajas_atacante, bajas_defensora, civiles_muertos,
                dios_favorecio_id, intervencion_divina
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            especie_atacante_id, especie_defensora_id,
            año_inicio, año_fin, duracion_años,
            causa, descripcion, intensidad,
            territorio_disputa, civ_afectada_id,
            vencedor_id, tipo_victoria,
            bajas_atacante, bajas_defensora, civiles,
            dios_favorecio_id, intervencion
        ))

        guerra_id = self.cursor.lastrowid

        # Generar batallas
        num_batallas_min, num_batallas_max = INTENSIDADES[intensidad]['num_batallas']
        num_batallas = random.randint(num_batallas_min, num_batallas_max)

        self.generar_batallas(guerra_id, año_inicio, año_fin, num_batallas)

        # Actualizar relación diplomática
        cambio_relacion = -30 if intensidad == 'guerra_total' else -20
        self.actualizar_relacion_diplomatica(
            especie_atacante_id, especie_defensora_id,
            cambio_relacion, f"Guerra: {causa}", año_fin
        )

        self.conn.commit()

        print(f"  ⚔️  Guerra creada: {especie_atacante} vs {especie_defensora}")
        print(f"      Años: {año_inicio}-{año_fin} | Intensidad: {intensidad}")
        print(f"      Bajas: {bajas_atacante + bajas_defensora + civiles}")

        return guerra_id

    def generar_batallas(self, guerra_id: int, año_inicio: int, año_fin: int, num_batallas: int):
        """Genera batallas individuales de una guerra"""

        for i in range(num_batallas):
            # Año de la batalla (distribuido a lo largo de la guerra)
            año_batalla = año_inicio + int((año_fin - año_inicio) * (i / num_batallas))

            # Tipo de batalla
            tipo_batalla = random.choice(TIPOS_BATALLA)

            # Lugar
            lugar = random.choice(self.lugares)
            lugar_id = lugar[0]

            # Fuerzas
            fuerzas_atacante = random.randint(100, 2000)
            fuerzas_defensora = random.randint(100, 2000)

            # Bajas (proporcionales a las fuerzas)
            bajas_atacante = int(fuerzas_atacante * random.uniform(0.05, 0.35))
            bajas_defensora = int(fuerzas_defensora * random.uniform(0.05, 0.35))

            # Vencedor
            if bajas_defensora > bajas_atacante * 1.2:
                vencedor = 'atacante'
            elif bajas_atacante > bajas_defensora * 1.2:
                vencedor = 'defensor'
            else:
                vencedor = 'empate'

            self.cursor.execute('''
                INSERT INTO batallas_guerras (
                    guerra_id, año_batalla, duracion_dias,
                    lugar_nombre, lugar_id,
                    fuerzas_atacante, fuerzas_defensora,
                    vencedor, bajas_atacante, bajas_defensora,
                    tipo_batalla
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                guerra_id, año_batalla, random.randint(1, 30),
                lugar[1], lugar_id,
                fuerzas_atacante, fuerzas_defensora,
                vencedor, bajas_atacante, bajas_defensora,
                tipo_batalla
            ))

        self.conn.commit()

    def generar_escaramuza(self, especie1: str, especie2: str, año: int) -> int:
        """Genera una escaramuza menor entre especies"""

        especie1_id = self.especies[especie1]
        especie2_id = self.especies[especie2]

        tipos_escaramuza = ['fronterizo', 'comercial', 'honor', 'robo', 'asesinato']
        tipo = random.choice(tipos_escaramuza)

        gravedad = random.choice(['menor', 'menor', 'media', 'grave'])

        muertos = random.randint(0, 15) if gravedad == 'menor' else random.randint(5, 50)
        heridos = random.randint(muertos, muertos * 3)

        lugar = random.choice(self.lugares)

        self.cursor.execute('''
            INSERT INTO escaramuzas_especies (
                especie_1_id, especie_2_id, año_incidente, lugar_id,
                tipo, gravedad, muertos, heridos
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (especie1_id, especie2_id, año, lugar[0], tipo, gravedad, muertos, heridos))

        escaramuza_id = self.cursor.lastrowid

        # Pequeño impacto en relación
        cambio = -5 if gravedad == 'grave' else -2
        self.actualizar_relacion_diplomatica(
            especie1_id, especie2_id, cambio,
            f"Escaramuza: {tipo}", año
        )

        self.conn.commit()
        return escaramuza_id

    def simular_guerras_periodo(self, año_inicio: int, año_fin: int):
        """Simula guerras durante un período"""
        print(f"\n{'='*70}")
        print(f"SIMULANDO GUERRAS: {año_inicio}-{año_fin}")
        print(f"{'='*70}\n")

        especies_lista = list(self.especies.keys())
        guerras_creadas = 0
        escaramuzas_creadas = 0

        for año in range(año_inicio, año_fin + 1):
            # Verificar si hay guerra este año
            if random.random() < PROBABILIDAD_GUERRA_ANUAL:
                # Seleccionar dos especies al azar
                especie1, especie2 = random.sample(especies_lista, 2)

                # Verificar que no estén en alianza fuerte
                relacion = self.obtener_relacion_diplomatica(
                    self.especies[especie1],
                    self.especies[especie2]
                )

                if relacion < 70:  # No atacar aliados fuertes
                    duracion = random.randint(1, 8)
                    self.crear_guerra(especie1, especie2, año, duracion)
                    guerras_creadas += 1

            # Escaramuzas (más frecuentes)
            elif random.random() < PROBABILIDAD_ESCARAMUZA_ANUAL:
                especie1, especie2 = random.sample(especies_lista, 2)
                self.generar_escaramuza(especie1, especie2, año)
                escaramuzas_creadas += 1

            if (año - año_inicio + 1) % 100 == 0:
                print(f"  ✓ Año {año} simulado...")

        print(f"\n{'='*70}")
        print("RESUMEN DEL PERÍODO")
        print(f"{'='*70}")
        print(f"  ⚔️  Guerras: {guerras_creadas}")
        print(f"  🗡️  Escaramuzas: {escaramuzas_creadas}")

    def generar_reporte_guerras(self):
        """Genera reporte de todas las guerras"""
        print(f"\n{'='*70}")
        print("REPORTE DE GUERRAS INTER-ESPECIES")
        print(f"{'='*70}\n")

        self.cursor.execute('''
            SELECT
                e1.nombre as atacante,
                e2.nombre as defensor,
                g.año_inicio,
                g.año_fin,
                g.duracion_años,
                g.intensidad,
                g.causa,
                g.bajas_atacante + g.bajas_defensora + g.civiles_muertos as bajas_totales,
                e3.nombre as vencedor
            FROM guerras_especies g
            JOIN especies e1 ON g.especie_atacante_id = e1.id
            JOIN especies e2 ON g.especie_defensora_id = e2.id
            LEFT JOIN especies e3 ON g.vencedor_especie_id = e3.id
            ORDER BY g.año_inicio
        ''')

        print(f"{'Años':<12} {'Atacante':<20} {'Defensor':<20} {'Causa':<15} {'Bajas':>8} {'Vencedor':<20}")
        print("-" * 110)

        for row in self.cursor.fetchall():
            atacante, defensor, año_i, año_f, dur, inten, causa, bajas, vencedor = row
            años = f"{año_i}-{año_f}"
            vencedor = vencedor or "Empate"
            print(f"{años:<12} {atacante:<20} {defensor:<20} {causa:<15} {bajas:8d} {vencedor:<20}")

        # Estadísticas
        self.cursor.execute('''
            SELECT COUNT(*), SUM(bajas_atacante + bajas_defensora + civiles_muertos)
            FROM guerras_especies
        ''')
        total_guerras, total_bajas = self.cursor.fetchone()

        print(f"\n{'='*70}")
        print("ESTADÍSTICAS")
        print(f"{'='*70}")
        print(f"  Total guerras: {total_guerras}")
        print(f"  Bajas totales: {total_bajas}")
        if total_guerras:
            print(f"  Promedio bajas por guerra: {total_bajas / total_guerras:.0f}")

def main():
    """Función principal"""
    print("="*70)
    print("SISTEMA DE GUERRAS INTER-ESPECIES")
    print("Portales del Quinto Sol")
    print("="*70)

    generador = GeneradorGuerras()

    # Aplicar schema
    generador.aplicar_schema()

    # Menú
    print("\nOpciones:")
    print("  1. Simular guerras 1500-3000")
    print("  2. Crear guerra manual")
    print("  3. Ver reporte de guerras")

    opcion = input("\nSelecciona opción (1-3): ").strip()

    if opcion == '1':
        confirm = input("\n⚠️  ¿Simular 1500 años de guerras? (s/n): ").strip().lower()
        if confirm == 's':
            generador.simular_guerras_periodo(1500, 3000)
            generador.generar_reporte_guerras()
    elif opcion == '2':
        especies = list(generador.especies.keys())
        print(f"\nEspecies disponibles: {', '.join(especies)}")
        esp1 = input("Especie atacante: ").strip()
        esp2 = input("Especie defensora: ").strip()
        año = int(input("Año de inicio: "))
        duracion = int(input("Duración (años): "))

        if esp1 in especies and esp2 in especies:
            generador.crear_guerra(esp1, esp2, año, duracion)
            print("✅ Guerra creada")
    elif opcion == '3':
        generador.generar_reporte_guerras()

    generador.conn.close()
    print("\n✅ Proceso completado")

if __name__ == '__main__':
    main()
