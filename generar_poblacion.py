#!/usr/bin/env python3
"""
Sistema de generación de población y genealogía para Portales del Quinto Sol
"""

import random
from typing import List, Tuple, Optional
from database_connector import DatabaseConnector

# Listas de nombres mesoamericanos
NOMBRES_MASCULINOS = [
    'Dron', 'Bell', 'Drasus', 'Tlaloc', 'Citlali', 'Tonatiuh', 'Cuauhtémoc', 'Moctezuma',
    'Itzcoatl', 'Nezahualcóyotl', 'Xicoténcatl', 'Cualli', 'Izel', 'Yaotl', 'Cipactli',
    'Ehecatl', 'Xipil', 'Tecpatl', 'Chimalli', 'Itotia', 'Yolotl', 'Mazatl', 'Tezcatl',
    'Yaretzi', 'Atl', 'Tochtli', 'Ollin', 'Cozamalotl', 'Ichtaca', 'Nochehuatl',
    'Tezcatlipoca', 'Acatl', 'Zuma', 'Tlanextli', 'Xochipilli', 'Zyanya', 'Nahuel',
    'Tlacaelel', 'Chicahua'
]

NOMBRES_FEMENINOS = [
    'Isha', 'Ikara', 'Xochitl', 'Citlalli', 'Ixchel', 'Nenetl', 'Xoco', 'Tlalli',
    'Itzel', 'Necahual', 'Yaretzi', 'Zyanya', 'Sacnité', 'Citlalic', 'Miyaoaxochitl',
    'Cuicatl', 'Eloxochitl', 'Amoxtli', 'Chalchiuitl', 'Tecuani', 'Teyacapan',
    'Quetzalli', 'Tlazohtlaloni', 'Meztli', 'Tonaltzin', 'Xiloxoch', 'Nayeli',
    'Ixtli', 'Centehua', 'Tlaco', 'Patli', 'Ixcatzin', 'Moyolehuani', 'Tlazohtzin',
    'Xochiquetzal', 'Temicxoch', 'Ahuic', 'Mahuizoh', 'Tlaneci'
]

APELLIDOS = [
    'del Sol', 'de la Luna', 'del Viento', 'de la Lluvia', 'del Jaguar', 'de la Serpiente',
    'del Águila', 'de la Obsidiana', 'del Jade', 'de la Montaña', 'del Río', 'del Fuego',
    'de las Estrellas', 'del Trueno', 'de la Sombra', 'de la Luz', 'del Crepúsculo',
    'del Amanecer', 'de la Tormenta', 'del Maíz', 'de la Flor', 'del Espejo',
    'de la Pluma', 'del Escudo', 'de la Lanza', 'del Cuchillo', 'del Templo',
    'de la Plaza', 'del Mercado', 'de la Cueva'
]

class GeneradorGenealogico:
    def __init__(self):
        self.db = DatabaseConnector()
        self.conn = self.db.connect()
        self.cursor = self.db.cursor

        # Cargar datos de referencia
        self.cargar_datos_referencia()

    def execute(self, query, params=None):
        """Wrapper para convertir placeholders ? a %s automáticamente"""
        if '?' in query:
            query = query.replace('?', '%s')
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)
        return self.cursor

    def cargar_datos_referencia(self):
        """Carga datos necesarios de la BD"""
        # Especies
        self.execute("SELECT id, nombre FROM especies WHERE nombre = 'Humanos I'")
        result = self.cursor.fetchone()
        self.humanos1_id = result['id'] if result else None

        # Civilizaciones
        self.execute("SELECT id, nombre FROM civilizaciones")
        self.civilizaciones = {row['nombre']: row['id'] for row in self.cursor.fetchall()}

        # Dioses
        self.execute("SELECT id, nombre FROM dioses")
        self.dioses = {row['nombre']: row['id'] for row in self.cursor.fetchall()}

        # Pueblos/Ciudades
        self.execute("SELECT id, nombre, civilizacion_id FROM pueblos_ciudades")
        self.lugares = [(row['id'], row['nombre'], row['civilizacion_id']) for row in self.cursor.fetchall()]

        # Oficios
        self.execute("SELECT id, nombre, categoria FROM oficios")
        self.oficios = [(row['id'], row['nombre'], row['categoria']) for row in self.cursor.fetchall()]

        # Habilidades
        self.execute("SELECT id, nombre, categoria FROM habilidades")
        self.habilidades = [(row['id'], row['nombre'], row['categoria']) for row in self.cursor.fetchall()]

    def calcular_esperanza_vida(self, clase_social: str) -> int:
        """Calcula esperanza de vida según clase social"""
        esperanzas = {
            'sacerdote': random.randint(120, 300),
            'sacerdotisa': random.randint(120, 300),
            'noble': random.randint(100, 200),
            'guerrero': random.randint(80, 120),
            'artesano': random.randint(90, 150),
            'campesino': random.randint(80, 130),
        }
        return esperanzas.get(clase_social, random.randint(80, 150))

    def seleccionar_clase_social(self) -> str:
        """Selecciona clase social con distribución realista"""
        clases = [
            ('sacerdote', 5),
            ('sacerdotisa', 5),
            ('noble', 10),
            ('guerrero', 20),
            ('artesano', 30),
            ('campesino', 30),
        ]
        total = sum(peso for _, peso in clases)
        r = random.randint(1, total)

        acumulado = 0
        for clase, peso in clases:
            acumulado += peso
            if r <= acumulado:
                return clase
        return 'campesino'

    def seleccionar_oficios(self, clase_social: str, genero: str) -> List[int]:
        """Selecciona 1-2 oficios según clase social"""
        oficios_por_clase = {
            'sacerdote': ['Sacerdote', 'Augur', 'Chamán', 'Escriba'],
            'sacerdotisa': ['Sacerdotisa', 'Curandero', 'Chamán'],
            'noble': ['Estratega', 'Arquitecto', 'Escriba', 'Comerciante'],
            'guerrero': ['Guerrero', 'Capitán', 'Arquero'],
            'artesano': ['Herrero', 'Carpintero', 'Alfarero', 'Tejedor', 'Tallador', 'Joyero'],
            'campesino': ['Agricultor', 'Pastor', 'Pescador', 'Cazador', 'Cocinero'],
        }

        nombres_disponibles = oficios_por_clase.get(clase_social, ['Agricultor'])
        oficios_ids = []

        # Seleccionar 1-2 oficios
        num_oficios = random.choice([1, 1, 2])  # Mayor probabilidad de 1
        nombres_seleccionados = random.sample(
            nombres_disponibles,
            min(num_oficios, len(nombres_disponibles))
        )

        for nombre_oficio in nombres_seleccionados:
            for of_id, of_nombre, _ in self.oficios:
                if of_nombre == nombre_oficio:
                    oficios_ids.append(of_id)
                    break

        return oficios_ids

    def seleccionar_habilidades(self, clase_social: str, num_habilidades: int = None) -> List[int]:
        """Selecciona 0-3 habilidades según clase social"""
        if num_habilidades is None:
            num_habilidades = random.randint(0, 3)

        habilidades_por_clase = {
            'sacerdote': ['magia', 'conocimiento', 'social'],
            'sacerdotisa': ['magia', 'conocimiento'],
            'noble': ['social', 'conocimiento'],
            'guerrero': ['combate'],
            'artesano': ['artesanal', 'conocimiento'],
            'campesino': ['supervivencia'],
        }

        categorias = habilidades_por_clase.get(clase_social, ['supervivencia'])
        habs_disponibles = [
            (h_id, h_nombre) for h_id, h_nombre, h_cat in self.habilidades
            if h_cat in categorias
        ]

        if not habs_disponibles:
            return []

        seleccionadas = random.sample(
            habs_disponibles,
            min(num_habilidades, len(habs_disponibles))
        )

        return [h_id for h_id, _ in seleccionadas]

    def crear_persona(self, nombre: str, genero: str, año_nacimiento: int,
                     padre_id: Optional[int] = None, madre_id: Optional[int] = None,
                     civilizacion_id: Optional[int] = None, lugar_id: Optional[int] = None) -> int:
        """Crea una nueva persona en la base de datos"""

        # Seleccionar apellido (heredado del padre si existe, sino aleatorio)
        if padre_id:
            self.execute("SELECT apellido FROM personas WHERE id = ?", (padre_id,))
            result = self.cursor.fetchone()
            apellido = result['apellido'] if result else random.choice(APELLIDOS)
        else:
            apellido = random.choice(APELLIDOS)

        # Clase social
        clase_social = self.seleccionar_clase_social()

        # Esperanza de vida
        esperanza_vida = self.calcular_esperanza_vida(clase_social)
        año_muerte = año_nacimiento + esperanza_vida

        # Seleccionar civilización y lugar si no se proporcionan
        if not civilizacion_id:
            civilizacion_id = random.choice(list(self.civilizaciones.values()))

        if not lugar_id:
            # Buscar lugares de la misma civilización
            lugares_civ = [l_id for l_id, l_nombre, l_civ_id in self.lugares if l_civ_id == civilizacion_id]
            lugar_id = random.choice(lugares_civ) if lugares_civ else self.lugares[0][0]

        # Seleccionar dios patrón
        dios_patron_id = random.choice(list(self.dioses.values()))
        nivel_devoto = random.randint(1, 5)  # Inicial bajo

        # Insertar persona
        self.execute('''
            INSERT INTO personas (
                nombre, apellido, especie_id, padre_id, madre_id, genero,
                año_nacimiento, año_muerte, lugar_nacimiento_id, lugar_residencia_id,
                civilizacion_id, clase_social, dios_patron_id, nivel_devoto,
                es_npc, es_jugador, nivel
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            RETURNING id
        ''', (
            nombre, apellido, self.humanos1_id, padre_id, madre_id, genero,
            año_nacimiento, año_muerte, lugar_id, lugar_id,
            civilizacion_id, clase_social, dios_patron_id, nivel_devoto,
            True, False, 1  # es_npc=True, es_jugador=False, nivel=1
        ))

        result = self.cursor.fetchone()
        persona_id = result['id'] if isinstance(result, dict) else result[0]

        # Asignar oficios
        oficios_ids = self.seleccionar_oficios(clase_social, genero)
        for i, oficio_id in enumerate(oficios_ids):
            es_principal = (i == 0)
            nivel_maestria = random.randint(1, 3)  # Inicial
            self.execute('''
                INSERT INTO persona_oficios (persona_id, oficio_id, año_inicio, nivel_maestria, es_principal)
                VALUES (?, ?, ?, ?, ?)
            ''', (persona_id, oficio_id, año_nacimiento + 15, nivel_maestria, es_principal))

        # Asignar habilidades
        habilidades_ids = self.seleccionar_habilidades(clase_social)
        for hab_id in habilidades_ids:
            nivel_dominio = random.randint(1, 3)  # Inicial
            self.execute('''
                INSERT INTO persona_habilidades (persona_id, habilidad_id, año_adquisicion, nivel_dominio)
                VALUES (?, ?, ?, ?)
            ''', (persona_id, hab_id, año_nacimiento + random.randint(10, 20), nivel_dominio))

        self.conn.commit()
        return persona_id

    def crear_poblacion_inicial(self, num_personas: int = 40, año_inicio: int = 1500):
        """Crea la población inicial de 40 humanos en la Era Alpha"""
        print(f"\n{'='*60}")
        print(f"Generando {num_personas} humanos iniciales (Era Alpha - {año_inicio})")
        print(f"{'='*60}\n")

        personas_creadas = []

        # Distribuir entre las civilizaciones
        civs_lista = list(self.civilizaciones.values())
        personas_por_civ = num_personas // len(civs_lista)
        resto = num_personas % len(civs_lista)

        contador = 0
        for i, civ_id in enumerate(civs_lista):
            num_en_civ = personas_por_civ + (1 if i < resto else 0)

            # Nombre de la civilización
            civ_nombre = [k for k, v in self.civilizaciones.items() if v == civ_id][0]
            print(f"Creando {num_en_civ} personas en {civ_nombre}...")

            for _ in range(num_en_civ):
                # Mitad hombres, mitad mujeres (aproximadamente)
                genero = 'masculino' if contador % 2 == 0 else 'femenino'
                nombres_lista = NOMBRES_MASCULINOS if genero == 'masculino' else NOMBRES_FEMENINOS
                nombre = random.choice(nombres_lista)

                # Edad al llegar (20-40 años)
                edad_llegada = random.randint(20, 40)
                año_nacimiento = año_inicio - edad_llegada

                persona_id = self.crear_persona(
                    nombre=nombre,
                    genero=genero,
                    año_nacimiento=año_nacimiento,
                    civilizacion_id=civ_id
                )

                personas_creadas.append(persona_id)
                contador += 1

                # Mostrar información
                self.execute('''
                    SELECT nombre_completo, clase_social
                    FROM personas WHERE id = ?
                ''', (persona_id,))
                nombre_completo, clase = self.cursor.fetchone()
                print(f"  ✓ {nombre_completo} - {clase}")

        print(f"\n✓ {len(personas_creadas)} personas creadas exitosamente")
        return personas_creadas

    def crear_matrimonio(self, persona1_id: int, persona2_id: int, año_union: int,
                        lugar_id: Optional[int] = None) -> int:
        """Crea un matrimonio entre dos personas"""

        if not lugar_id:
            # Usar el lugar de residencia de persona1
            self.execute(
                "SELECT lugar_residencia_id FROM personas WHERE id = ?",
                (persona1_id,)
            )
            result = self.cursor.fetchone()
            lugar_id = result['lugar_residencia_id'] if result else None

        self.execute('''
            INSERT INTO matrimonios (persona1_id, persona2_id, año_union, lugar_union_id)
            VALUES (?, ?, ?, ?)
            RETURNING id
        ''', (persona1_id, persona2_id, año_union, lugar_id))

        result = self.cursor.fetchone()
        matrimonio_id = result['id'] if isinstance(result, dict) else result[0]

        self.conn.commit()
        return matrimonio_id

    def generar_hijos(self, padre_id: int, madre_id: int, año_matrimonio: int,
                     num_hijos: Optional[int] = None) -> List[int]:
        """Genera hijos para una pareja"""

        if num_hijos is None:
            num_hijos = random.randint(4, 7)

        hijos_ids = []

        # Obtener información de los padres
        self.execute('''
            SELECT civilizacion_id, lugar_residencia_id, año_muerte
            FROM personas WHERE id = ?
        ''', (madre_id,))
        madre_info = self.cursor.fetchone()
        civ_id, lugar_id, año_muerte_madre = madre_info

        # Los hijos nacen en intervalos de 2-4 años
        año_actual = año_matrimonio + 1

        for i in range(num_hijos):
            # Verificar que la madre esté viva
            if año_actual > año_muerte_madre:
                break

            genero = random.choice(['masculino', 'femenino'])
            nombres_lista = NOMBRES_MASCULINOS if genero == 'masculino' else NOMBRES_FEMENINOS
            nombre = random.choice(nombres_lista)

            hijo_id = self.crear_persona(
                nombre=nombre,
                genero=genero,
                año_nacimiento=año_actual,
                padre_id=padre_id,
                madre_id=madre_id,
                civilizacion_id=civ_id,
                lugar_id=lugar_id
            )

            hijos_ids.append(hijo_id)

            # Siguiente hijo en 2-4 años
            año_actual += random.randint(2, 4)

        # Actualizar contador de hijos en matrimonio
        self.execute('''
            UPDATE matrimonios
            SET hijos_totales = ?
            WHERE (persona1_id = ? AND persona2_id = ?)
               OR (persona1_id = ? AND persona2_id = ?)
        ''', (len(hijos_ids), padre_id, madre_id, madre_id, padre_id))

        self.conn.commit()
        return hijos_ids

    def generar_generacion(self, año_inicio: int, año_fin: int):
        """Genera matrimonios e hijos para un período de tiempo"""
        print(f"\n{'='*60}")
        print(f"Generando nueva generación ({año_inicio} - {año_fin})")
        print(f"{'='*60}\n")

        # Buscar personas solteras en edad de casarse (18-35 años)
        self.execute('''
            SELECT p.id, p.genero, p.año_nacimiento, p.civilizacion_id, p.nombre_completo
            FROM personas p
            WHERE p.id NOT IN (
                SELECT persona1_id FROM matrimonios
                UNION
                SELECT persona2_id FROM matrimonios
            )
            AND p.año_nacimiento >= ? AND p.año_nacimiento <= ?
            AND p.año_muerte >= ?
            ORDER BY p.civilizacion_id, p.genero
        ''', (año_inicio - 35, año_inicio - 18, año_inicio))

        solteros = self.cursor.fetchall()

        # Separar por género
        hombres = [s for s in solteros if s[1] == 'masculino']
        mujeres = [s for s in solteros if s[1] == 'femenino']

        print(f"Personas disponibles: {len(hombres)} hombres, {len(mujeres)} mujeres")

        matrimonios_creados = 0
        hijos_totales = 0

        # Emparejar (preferir misma civilización, pero permitir mezcla)
        random.shuffle(hombres)
        random.shuffle(mujeres)

        for hombre in hombres:
            if not mujeres:
                break

            hombre_id, _, h_año_nac, h_civ_id, h_nombre = hombre

            # Buscar mujer de la misma civilización
            mujer_misma_civ = [m for m in mujeres if m[3] == h_civ_id]

            if mujer_misma_civ:
                mujer = random.choice(mujer_misma_civ)
            elif mujeres:
                # Si no hay de la misma civ, tomar cualquiera (10% probabilidad)
                if random.random() < 0.1:
                    mujer = random.choice(mujeres)
                else:
                    continue
            else:
                break

            mujer_id, _, m_año_nac, m_civ_id, m_nombre = mujer
            mujeres.remove(mujer)

            # Edad de matrimonio
            edad_h = año_inicio - h_año_nac
            edad_m = año_inicio - m_año_nac

            # Solo casar si ambos tienen entre 18 y 40
            if 18 <= edad_h <= 40 and 18 <= edad_m <= 40:
                año_matrimonio = año_inicio + random.randint(0, 5)

                mat_id = self.crear_matrimonio(hombre_id, mujer_id, año_matrimonio)
                matrimonios_creados += 1

                print(f"  💑 Matrimonio #{matrimonios_creados}: {h_nombre} y {m_nombre} ({año_matrimonio})")

                # Generar hijos
                hijos = self.generar_hijos(hombre_id, mujer_id, año_matrimonio)
                hijos_totales += len(hijos)

                print(f"     └─ {len(hijos)} hijos")

        print(f"\n✓ {matrimonios_creados} matrimonios creados")
        print(f"✓ {hijos_totales} hijos nacidos")

        return matrimonios_creados, hijos_totales

    def simular_historia(self, año_inicio: int = 1500, año_fin: int = 3000,
                        intervalo_generacion: int = 25):
        """Simula toda la historia generando generaciones"""
        print(f"\n{'='*70}")
        print(f"SIMULACIÓN HISTÓRICA COMPLETA")
        print(f"Desde {año_inicio} hasta {año_fin}")
        print(f"{'='*70}\n")

        estadisticas = {
            'matrimonios_totales': 0,
            'hijos_totales': 0,
            'generaciones': 0
        }

        año_actual = año_inicio
        while año_actual < año_fin:
            año_fin_generacion = min(año_actual + intervalo_generacion, año_fin)

            mat, hijos = self.generar_generacion(año_actual, año_fin_generacion)

            estadisticas['matrimonios_totales'] += mat
            estadisticas['hijos_totales'] += hijos
            estadisticas['generaciones'] += 1

            año_actual = año_fin_generacion

        # Estadísticas finales
        self.execute("SELECT COUNT(*) FROM personas")
        result = self.cursor.fetchone()
        total_personas = result['count'] if isinstance(result, dict) else result[0]

        print(f"\n{'='*70}")
        print(f"ESTADÍSTICAS FINALES")
        print(f"{'='*70}")
        print(f"  • Total de personas creadas: {total_personas}")
        print(f"  • Matrimonios totales: {estadisticas['matrimonios_totales']}")
        print(f"  • Hijos totales: {estadisticas['hijos_totales']}")
        print(f"  • Generaciones simuladas: {estadisticas['generaciones']}")
        print(f"{'='*70}\n")

        return estadisticas

    def cerrar(self):
        """Cierra la conexión a la base de datos"""
        self.conn.close()


def main():
    print("\n" + "="*70)
    print("PORTALES DEL QUINTO SOL - Generador de Población y Genealogía")
    print("="*70)

    gen = GeneradorGenealogico()

    try:
        # Crear población inicial
        gen.crear_poblacion_inicial(num_personas=40, año_inicio=1500)

        # Simular historia (puedes descomentar para generar toda la historia)
        # print("\n¿Deseas simular toda la historia hasta el año 3000? (s/n)")
        # respuesta = input("> ")
        # if respuesta.lower() == 's':
        #     gen.simular_historia(año_inicio=1500, año_fin=3000, intervalo_generacion=25)

        print("\n" + "="*70)
        print("✓ Generación completada exitosamente")
        print("="*70 + "\n")

    finally:
        gen.cerrar()


if __name__ == '__main__':
    main()
