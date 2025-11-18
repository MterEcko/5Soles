#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generador de Genealogías para Especies Sirvientes
Portales del Quinto Sol - 5 especies con 300 años de longevidad
Simulación: 1500-3000 (1500 años, ~5 generaciones)
"""

import sqlite3
import random
import json
from typing import List, Tuple, Optional, Dict

# ================================================================
# NOMBRES POR ESPECIE (basados en características)
# ================================================================

NOMBRES_TLACATL_LUZ = {
    'masculino': ['Quetzal', 'Coatl', 'Tlahuiz', 'Tlanex', 'Xipil', 'Yolotl', 'Citlal', 'Tonatiuh',
                  'Ehecatl', 'Mixcoatl', 'Cozamal', 'Yaotl', 'Cualli', 'Tochtli', 'Chimalli'],
    'femenino': ['Xochitl', 'Citlalli', 'Quetzalli', 'Tlaneci', 'Yolotli', 'Mixcoatli', 'Sacnité',
                 'Zyanya', 'Nenetl', 'Xoco', 'Ixtli', 'Meztli', 'Cuicatl', 'Tlalli', 'Chalchi']
}

NOMBRES_SOMBRA_COYOTES = {
    'masculino': ['Yohualli', 'Tezcatl', 'Yaotl', 'Coyotl', 'Itzpapalotl', 'Mictlan', 'Xibalba',
                  'Tecpatl', 'Ichtaca', 'Noche', 'Sombra', 'Calli', 'Tliltic', 'Atl', 'Ocelotl'],
    'femenino': ['Yohuatzin', 'Tezcatli', 'Metztli', 'Coyolxauh', 'Tlazolteotl', 'Itzpapal',
                 'Xochitl', 'Cihuatl', 'Nenetl', 'Tlillan', 'Nochehua', 'Mayahuel', 'Tlaco']
}

NOMBRES_BIO_CONSTRUCTORES = {
    'masculino': ['Yaaxil', 'Chimal', 'Coatl', 'Cuauhtli', 'Itotia', 'Xochipilli', 'Centeotl',
                  'Ameyali', 'Cipactli', 'Tonatiuh', 'Mazatl', 'Ollin', 'Cualli', 'Tlaloc'],
    'femenino': ['Xochitl', 'Citlali', 'Yaaxila', 'Ixchel', 'Sacnité', 'Nenetl', 'Mayahuel',
                 'Amoxtli', 'Eloxochitl', 'Chalchiuitl', 'Tlazohtzin', 'Tlalli', 'Quetzalli']
}

NOMBRES_ACUATILES = {
    'masculino': ['Atl', 'Tlaloc', 'Acatl', 'Cipactli', 'Ehecatl', 'Chalchi', 'Coatl', 'Mizton',
                  'Tezcatlipoca', 'Xiuhtotl', 'Tonatiuh', 'Cualli', 'Yaotl', 'Tecpatl'],
    'femenino': ['Atlacoya', 'Chalchiuitl', 'Cihuatl', 'Xochitl', 'Atlitzin', 'Tezcatli',
                 'Mizton', 'Citlalli', 'Ixchel', 'Mayahuel', 'Nenetl', 'Tlazohtzin', 'Sacnité']
}

NOMBRES_GUERREROS_SOLARES = {
    'masculino': ['Tonatiuh', 'Huitzilopochtli', 'Cuauhtémoc', 'Yaotl', 'Chimalli', 'Tecpatl',
                  'Xicoténcatl', 'Itzcoatl', 'Nezahual', 'Tlaloc', 'Citlali', 'Xipil', 'Ehecatl'],
    'femenino': ['Tonaltzin', 'Xochitl', 'Citlalli', 'Quetzalli', 'Yaretzi', 'Zyanya', 'Cihuatl',
                 'Ixchel', 'Meztli', 'Tecuani', 'Nenetl', 'Chalchiuitl', 'Tlazohtzin']
}

# Apellidos por especie
APELLIDOS_POR_ESPECIE = {
    'Tlacatl de Luz': ['del Alba', 'de la Pluma', 'del Vuelo', 'de la Sabiduría', 'del Cielo',
                       'de la Luz Dorada', 'del Amanecer', 'de las Estrellas', 'del Cristal'],
    'Sombra-Coyotes': ['de la Noche', 'de la Sombra', 'del Crepúsculo', 'del Espejo Oscuro',
                       'de la Luna Nueva', 'del Obsidiano', 'de las Tinieblas', 'del Silencio'],
    'Bio-Constructores': ['del Bosque', 'de la Raíz', 'de la Flor', 'del Jardín', 'de la Semilla',
                          'del Árbol Sagrado', 'de la Tierra Fértil', 'del Verdor', 'de la Hoja'],
    'Acuátiles': ['del Río', 'del Mar', 'de la Lluvia', 'del Lago', 'de las Aguas',
                  'de la Corriente', 'del Cenote', 'de las Olas', 'de la Profundidad'],
    'Guerreros Solares': ['del Sol', 'del Fuego', 'de la Guerra', 'del Escudo Dorado',
                          'de la Lanza Solar', 'del Rayo', 'de la Victoria', 'del Guerrero']
}

# ================================================================
# CONFIGURACIÓN POR ESPECIE
# ================================================================

ESPECIES_CONFIG = {
    'Tlacatl de Luz': {
        'longevidad_base': (250, 320),  # años
        'edad_matrimonio': (35, 55),
        'edad_fertilidad_max': 180,  # pueden tener hijos hasta los 180 años
        'hijos_por_pareja': (3, 6),  # menos hijos que humanos, más longevos
        'esterilidad': 0.10,  # 10%
        'mortalidad_infantil': 0.05,  # 5% (más resistentes)
        'inteligencia_1500': 150,
        'resistencia_base': 85,
        'civilizacion_patron': 'Toltecas del Viento',
        'dios_patron': 'Quetzalcóatl'
    },
    'Sombra-Coyotes': {
        'longevidad_base': (200, 280),
        'edad_matrimonio': (30, 50),
        'edad_fertilidad_max': 160,
        'hijos_por_pareja': (2, 5),  # más solitarios, menos hijos
        'esterilidad': 0.15,  # 15%
        'mortalidad_infantil': 0.08,  # 8%
        'inteligencia_1500': 150,
        'resistencia_base': 90,  # muy resistentes (sombra)
        'civilizacion_patron': 'Purépecha del Fuego',
        'dios_patron': 'Tezcatlipoca'
    },
    'Bio-Constructores': {
        'longevidad_base': (280, 350),  # los más longevos
        'edad_matrimonio': (40, 60),
        'edad_fertilidad_max': 200,
        'hijos_por_pareja': (4, 7),  # naturaleza fértil
        'esterilidad': 0.08,  # 8%
        'mortalidad_infantil': 0.04,  # 4% (máxima resistencia)
        'inteligencia_1500': 150,
        'resistencia_base': 95,  # regeneración natural
        'civilizacion_patron': 'Zapotecas del Eco',
        'dios_patron': 'Centéotl'
    },
    'Acuátiles': {
        'longevidad_base': (230, 300),
        'edad_matrimonio': (32, 52),
        'edad_fertilidad_max': 170,
        'hijos_por_pareja': (3, 6),
        'esterilidad': 0.12,  # 12%
        'mortalidad_infantil': 0.06,  # 6%
        'inteligencia_1500': 150,
        'resistencia_base': 88,
        'civilizacion_patron': 'Mayas Celeste',
        'dios_patron': 'Tláloc'
    },
    'Guerreros Solares': {
        'longevidad_base': (180, 250),  # guerreros, vida más peligrosa
        'edad_matrimonio': (28, 45),
        'edad_fertilidad_max': 150,
        'hijos_por_pareja': (4, 8),  # muchos hijos (cultura guerrera)
        'esterilidad': 0.09,  # 9%
        'mortalidad_infantil': 0.10,  # 10% (combates)
        'inteligencia_1500': 150,
        'resistencia_base': 92,  # física excepcional
        'civilizacion_patron': 'Mexica de Obsidiana',
        'dios_patron': 'Huitzilopochtli'
    }
}

# ================================================================
# GENERADOR DE GENEALOGÍAS
# ================================================================

class GeneradorEspecies:
    def __init__(self, db_path='quinto_sol.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.año_actual = 1500
        self.cargar_datos_referencia()

    def cargar_datos_referencia(self):
        """Carga datos necesarios de la BD"""
        # Especies
        self.cursor.execute("SELECT id, nombre FROM especies WHERE nombre != 'Humanos I' AND nombre != 'Humanos II'")
        self.especies = {nombre: id for id, nombre in self.cursor.fetchall()}

        # Civilizaciones
        self.cursor.execute("SELECT id, nombre FROM civilizaciones")
        self.civilizaciones = {nombre: id for id, nombre in self.cursor.fetchall()}

        # Dioses
        self.cursor.execute("SELECT id, nombre FROM dioses")
        self.dioses = {nombre: id for id, nombre in self.cursor.fetchall()}

        # Lugares por civilización
        self.cursor.execute("SELECT id, nombre, civilizacion_id FROM pueblos_ciudades")
        self.lugares = {}
        for lugar_id, nombre, civ_id in self.cursor.fetchall():
            if civ_id not in self.lugares:
                self.lugares[civ_id] = []
            self.lugares[civ_id].append((lugar_id, nombre))

        # Oficios
        self.cursor.execute("SELECT id, nombre, categoria FROM oficios")
        self.oficios = [(id, nombre, cat) for id, nombre, cat in self.cursor.fetchall()]

        print(f"✅ Referencias cargadas:")
        print(f"   - {len(self.especies)} especies")
        print(f"   - {len(self.civilizaciones)} civilizaciones")
        print(f"   - {len(self.dioses)} dioses")

    def calcular_inteligencia(self, especie_nombre: str, año_nacimiento: int) -> int:
        """Calcula inteligencia que degrada de 150 (1500) a 100 (3000)"""
        config = ESPECIES_CONFIG[especie_nombre]
        intel_inicio = config['inteligencia_1500']

        # Degradación lineal: 150 → 100 en 1500 años
        # Tasa: -50 / 1500 = -0.0333 por año
        años_desde_inicio = año_nacimiento - 1500
        degradacion = (50 / 1500) * años_desde_inicio
        inteligencia = intel_inicio - degradacion

        return max(100, min(150, int(inteligencia)))

    def calcular_esperanza_vida(self, especie_nombre: str, clase_social: str) -> int:
        """Calcula esperanza de vida según especie y clase"""
        config = ESPECIES_CONFIG[especie_nombre]
        base_min, base_max = config['longevidad_base']

        # Modificadores por clase social
        modificadores = {
            'sacerdote': 1.2,
            'sacerdotisa': 1.2,
            'noble': 1.1,
            'guerrero': 0.85,  # vida peligrosa
            'artesano': 1.0,
            'campesino': 0.95,
            'explorador': 0.9,
        }

        mod = modificadores.get(clase_social, 1.0)
        esperanza = random.randint(base_min, base_max) * mod

        return int(esperanza)

    def seleccionar_clase_social(self, especie_nombre: str) -> str:
        """Selecciona clase social según especie"""
        # Distribuciones por especie
        distribuciones = {
            'Tlacatl de Luz': [  # Sabios y diplomáticos
                ('sacerdote', 15),
                ('sacerdotisa', 15),
                ('noble', 20),
                ('artesano', 25),
                ('explorador', 15),
                ('campesino', 10),
            ],
            'Sombra-Coyotes': [  # Sigilo y nocturnos
                ('explorador', 30),
                ('artesano', 20),
                ('guerrero', 20),
                ('sacerdote', 10),
                ('noble', 10),
                ('campesino', 10),
            ],
            'Bio-Constructores': [  # Naturaleza y agricultura
                ('campesino', 35),
                ('artesano', 25),
                ('sacerdotisa', 15),
                ('sacerdote', 10),
                ('noble', 10),
                ('explorador', 5),
            ],
            'Acuátiles': [  # Comercio y exploración
                ('explorador', 25),
                ('campesino', 20),  # pescadores
                ('artesano', 20),
                ('noble', 15),
                ('sacerdote', 10),
                ('guerrero', 10),
            ],
            'Guerreros Solares': [  # Combate y honor
                ('guerrero', 45),
                ('noble', 20),
                ('sacerdote', 15),
                ('artesano', 10),
                ('explorador', 5),
                ('campesino', 5),
            ],
        }

        clases = distribuciones.get(especie_nombre, distribuciones['Tlacatl de Luz'])
        total = sum(peso for _, peso in clases)
        r = random.randint(1, total)

        acumulado = 0
        for clase, peso in clases:
            acumulado += peso
            if r <= acumulado:
                return clase
        return 'artesano'

    def crear_persona_especie(self, especie_nombre: str, nombre: str, genero: str,
                             año_nacimiento: int, padre_id: Optional[int] = None,
                             madre_id: Optional[int] = None) -> int:
        """Crea una persona de especie sirviente"""

        config = ESPECIES_CONFIG[especie_nombre]
        especie_id = self.especies[especie_nombre]

        # Civilización y lugar
        civ_nombre = config['civilizacion_patron']
        civ_id = self.civilizaciones.get(civ_nombre)
        lugares_civ = self.lugares.get(civ_id, [])
        lugar_id = random.choice(lugares_civ)[0] if lugares_civ else None

        # Apellido
        if padre_id:
            self.cursor.execute("SELECT apellido FROM personas WHERE id = ?", (padre_id,))
            result = self.cursor.fetchone()
            apellido = result[0] if result and result[0] else random.choice(APELLIDOS_POR_ESPECIE[especie_nombre])
        else:
            apellido = random.choice(APELLIDOS_POR_ESPECIE[especie_nombre])

        # Clase social y vida
        clase_social = self.seleccionar_clase_social(especie_nombre)
        esperanza_vida = self.calcular_esperanza_vida(especie_nombre, clase_social)
        año_muerte = año_nacimiento + esperanza_vida

        # Inteligencia (degrada con el tiempo)
        inteligencia = self.calcular_inteligencia(especie_nombre, año_nacimiento)

        # Resistencia
        resistencia = config['resistencia_base'] + random.randint(-5, 5)

        # Dios patrón
        dios_patron_nombre = config['dios_patron']
        dios_patron_id = self.dioses.get(dios_patron_nombre)
        nivel_devoto = random.randint(3, 5)  # Sirvientes devotos

        # Insertar persona
        self.cursor.execute('''
            INSERT INTO personas (
                nombre, apellido, genero, especie_id,
                año_nacimiento, año_muerte,
                padre_id, madre_id,
                civilizacion_id, lugar_residencia_id,
                clase_social,
                inteligencia, fuerza, agilidad, resistencia, carisma,
                dios_patron_id, nivel_devoto
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            nombre, apellido, genero, especie_id,
            año_nacimiento, año_muerte,
            padre_id, madre_id,
            civ_id, lugar_id,
            clase_social,
            inteligencia,
            random.randint(70, 95),  # fuerza
            random.randint(70, 95),  # agilidad
            resistencia,
            random.randint(60, 90),  # carisma
            dios_patron_id, nivel_devoto
        ))

        persona_id = self.cursor.lastrowid

        # Actualizar nombre completo
        nombre_completo = f"{nombre} {apellido}"
        self.cursor.execute('''
            UPDATE personas SET nombre_completo = ?
            WHERE id = ?
        ''', (nombre_completo, persona_id))

        self.conn.commit()
        return persona_id

    def generar_poblacion_inicial(self, especie_nombre: str, cantidad: int) -> List[int]:
        """Genera población inicial para una especie (año 1500)"""
        print(f"\n{'='*70}")
        print(f"Generando población inicial: {especie_nombre}")
        print(f"Cantidad: {cantidad} individuos")
        print(f"{'='*70}\n")

        config = ESPECIES_CONFIG[especie_nombre]
        personas_creadas = []

        # Nombres según especie
        if especie_nombre == 'Tlacatl de Luz':
            nombres = NOMBRES_TLACATL_LUZ
        elif especie_nombre == 'Sombra-Coyotes':
            nombres = NOMBRES_SOMBRA_COYOTES
        elif especie_nombre == 'Bio-Constructores':
            nombres = NOMBRES_BIO_CONSTRUCTORES
        elif especie_nombre == 'Acuátiles':
            nombres = NOMBRES_ACUATILES
        else:  # Guerreros Solares
            nombres = NOMBRES_GUERREROS_SOLARES

        for i in range(cantidad):
            # Alternar género
            genero = 'masculino' if i % 2 == 0 else 'femenino'
            nombre = random.choice(nombres[genero])

            # Edad al inicio (20-80 años para tener varias generaciones)
            edad_inicio = random.randint(20, 80)
            año_nacimiento = 1500 - edad_inicio

            persona_id = self.crear_persona_especie(
                especie_nombre=especie_nombre,
                nombre=nombre,
                genero=genero,
                año_nacimiento=año_nacimiento
            )

            personas_creadas.append(persona_id)

            if (i + 1) % 50 == 0:
                print(f"  ✓ {i + 1}/{cantidad} creados...")

        print(f"\n✅ {len(personas_creadas)} individuos de {especie_nombre} creados")
        return personas_creadas

    def crear_matrimonio(self, persona1_id: int, persona2_id: int, año_union: int) -> int:
        """Crea matrimonio entre dos personas"""
        self.cursor.execute("SELECT lugar_residencia_id FROM personas WHERE id = ?", (persona1_id,))
        lugar_id = self.cursor.fetchone()[0]

        self.cursor.execute('''
            INSERT INTO matrimonios (persona1_id, persona2_id, año_union, lugar_union_id)
            VALUES (?, ?, ?, ?)
        ''', (persona1_id, persona2_id, año_union, lugar_id))

        self.conn.commit()
        return self.cursor.lastrowid

    def generar_hijos(self, especie_nombre: str, padre_id: int, madre_id: int,
                     año_matrimonio: int) -> List[int]:
        """Genera hijos para una pareja de especie"""
        config = ESPECIES_CONFIG[especie_nombre]

        # Verificar esterilidad
        if random.random() < config['esterilidad']:
            return []  # Pareja estéril

        # Número de hijos
        min_hijos, max_hijos = config['hijos_por_pareja']
        num_hijos = random.randint(min_hijos, max_hijos)

        # Información de la madre
        self.cursor.execute('''
            SELECT año_nacimiento, año_muerte, especie_id
            FROM personas WHERE id = ?
        ''', (madre_id,))
        año_nac_madre, año_muerte_madre, especie_id = self.cursor.fetchone()

        hijos_ids = []

        # Nombres según especie
        if especie_nombre == 'Tlacatl de Luz':
            nombres = NOMBRES_TLACATL_LUZ
        elif especie_nombre == 'Sombra-Coyotes':
            nombres = NOMBRES_SOMBRA_COYOTES
        elif especie_nombre == 'Bio-Constructores':
            nombres = NOMBRES_BIO_CONSTRUCTORES
        elif especie_nombre == 'Acuátiles':
            nombres = NOMBRES_ACUATILES
        else:
            nombres = NOMBRES_GUERREROS_SOLARES

        # Los hijos nacen en intervalos de 3-7 años (más espaciados que humanos)
        año_actual = año_matrimonio + random.randint(1, 3)

        for i in range(num_hijos):
            # Verificar fertilidad de la madre
            edad_madre = año_actual - año_nac_madre
            if edad_madre > config['edad_fertilidad_max'] or año_actual > año_muerte_madre:
                break

            # Mortalidad infantil
            if random.random() < config['mortalidad_infantil']:
                año_actual += random.randint(3, 7)
                continue

            genero = random.choice(['masculino', 'femenino'])
            nombre = random.choice(nombres[genero])

            hijo_id = self.crear_persona_especie(
                especie_nombre=especie_nombre,
                nombre=nombre,
                genero=genero,
                año_nacimiento=año_actual,
                padre_id=padre_id,
                madre_id=madre_id
            )

            hijos_ids.append(hijo_id)

            # Intervalo hasta el siguiente hijo
            año_actual += random.randint(3, 7)

        return hijos_ids

    def simular_generacion(self, especie_nombre: str, poblacion_actual: List[int],
                          año_inicio: int, año_fin: int) -> List[int]:
        """Simula una generación de matrimonios y reprodución"""
        print(f"\n🔄 Simulando generación {año_inicio}-{año_fin} para {especie_nombre}")
        print(f"   Población inicial: {len(poblacion_actual)}")

        config = ESPECIES_CONFIG[especie_nombre]
        nuevos_individuos = []

        # Obtener solteros en edad de matrimonio
        edad_min, edad_max = config['edad_matrimonio']

        self.cursor.execute(f'''
            SELECT id, genero, año_nacimiento
            FROM personas
            WHERE especie_id = ?
            AND id IN ({','.join('?' * len(poblacion_actual))})
            AND año_nacimiento <= ?
            AND año_nacimiento >= ?
            AND año_muerte >= ?
            AND id NOT IN (
                SELECT persona1_id FROM matrimonios WHERE año_union <= ?
                UNION
                SELECT persona2_id FROM matrimonios WHERE año_union <= ?
            )
        ''', [self.especies[especie_nombre]] + poblacion_actual +
             [año_inicio - edad_min, año_inicio - edad_max, año_inicio, año_inicio, año_inicio])

        solteros = self.cursor.fetchall()

        # Separar por género
        hombres = [id for id, gen, _ in solteros if gen == 'masculino']
        mujeres = [id for id, gen, _ in solteros if gen == 'femenino']

        print(f"   Solteros: {len(hombres)} hombres, {len(mujeres)} mujeres")

        # Crear matrimonios (no todos se casan)
        num_matrimonios = min(len(hombres), len(mujeres))
        num_matrimonios = int(num_matrimonios * 0.75)  # 75% se casa

        random.shuffle(hombres)
        random.shuffle(mujeres)

        matrimonios_creados = 0

        for i in range(num_matrimonios):
            esposo_id = hombres[i]
            esposa_id = mujeres[i]

            año_union = año_inicio + random.randint(0, 10)

            # Crear matrimonio
            self.crear_matrimonio(esposo_id, esposa_id, año_union)

            # Generar hijos
            hijos = self.generar_hijos(especie_nombre, esposo_id, esposa_id, año_union)
            nuevos_individuos.extend(hijos)
            matrimonios_creados += 1

            if matrimonios_creados % 20 == 0:
                print(f"      {matrimonios_creados} matrimonios, {len(nuevos_individuos)} hijos...")

        print(f"   ✅ {matrimonios_creados} matrimonios, {len(nuevos_individuos)} nuevos individuos")

        return poblacion_actual + nuevos_individuos

    def simular_especie_completa(self, especie_nombre: str, poblacion_inicial: int):
        """Simula toda la historia de una especie (1500-3000)"""
        print(f"\n{'='*70}")
        print(f"SIMULACIÓN COMPLETA: {especie_nombre}")
        print(f"{'='*70}")

        # Generar población inicial
        poblacion = self.generar_poblacion_inicial(especie_nombre, poblacion_inicial)

        # Simular por generaciones (cada 80 años aprox)
        config = ESPECIES_CONFIG[especie_nombre]
        edad_min, _ = config['edad_matrimonio']
        intervalo_generacion = edad_min + 20  # ~50-60 años por generación

        año_actual = 1500
        generacion = 1

        while año_actual < 3000:
            año_fin = min(año_actual + intervalo_generacion, 3000)
            poblacion = self.simular_generacion(
                especie_nombre, poblacion, año_actual, año_fin
            )
            año_actual = año_fin
            generacion += 1

        # Resumen final
        print(f"\n{'='*70}")
        print(f"✅ SIMULACIÓN COMPLETADA: {especie_nombre}")
        print(f"{'='*70}")
        print(f"   Población inicial: {poblacion_inicial}")
        print(f"   Población final: {len(poblacion)}")
        print(f"   Crecimiento: {len(poblacion) - poblacion_inicial}")
        print(f"   Generaciones: {generacion}")

def main():
    """Función principal"""
    print("="*70)
    print("GENERADOR DE GENEALOGÍAS - ESPECIES SIRVIENTES")
    print("Portales del Quinto Sol")
    print("Simulación: 1500-3000 (1500 años)")
    print("="*70)

    generador = GeneradorEspecies()

    # Poblaciones iniciales por especie
    poblaciones = {
        'Tlacatl de Luz': 150,        # Sabios, diplomáticos
        'Sombra-Coyotes': 100,        # Solitarios, menos población
        'Bio-Constructores': 180,     # Naturaleza, agrícolas
        'Acuátiles': 140,             # Comercio, exploración
        'Guerreros Solares': 200,     # Guerreros, más población
    }

    print(f"\nPoblaciones iniciales (año 1500):")
    for especie, cantidad in poblaciones.items():
        print(f"  - {especie:25s}: {cantidad:4d} individuos")

    input("\n⏸️  Presiona ENTER para comenzar la simulación...")

    # Simular cada especie
    for especie_nombre, poblacion_inicial in poblaciones.items():
        generador.simular_especie_completa(especie_nombre, poblacion_inicial)
        print("\n")

    # Resumen global
    print("\n" + "="*70)
    print("RESUMEN GLOBAL")
    print("="*70)

    for especie_nombre in poblaciones.keys():
        especie_id = generador.especies[especie_nombre]
        generador.cursor.execute('''
            SELECT COUNT(*) FROM personas WHERE especie_id = ?
        ''', (especie_id,))
        total = generador.cursor.fetchone()[0]
        print(f"  {especie_nombre:25s}: {total:6d} individuos totales")

    generador.conn.close()
    print("\n✅ Simulación completada")

if __name__ == '__main__':
    main()
