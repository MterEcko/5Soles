#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Longevidad por Oficio y Hábitos
Portales del Quinto Sol

Humanos pueden vivir hasta 200 años dependiendo de:
- Oficio (peligrosidad, estrés, beneficios)
- Hábitos de vida (alimentación, ejercicio, descanso)
- Clase social (acceso a recursos)
- Eventos de vida (enfermedades, accidentes, bendiciones)
"""

# Se eliminan las importaciones sqlite3 y se usa DatabaseConnector
import random
import json
from database_connector import DatabaseConnector # Importación clave

# ================================================================
# LONGEVIDAD BASE POR OFICIO (Mantiene el mismo contenido)
# ================================================================
LONGEVIDAD_OFICIOS = {
    # RELIGIOSOS - Muy alta (140-200 años)
    'Sacerdote': (140, 200),
    'Sacerdotisa': (145, 200),
    'Augur': (130, 180),
    'Chamán': (125, 175),
    # CIENTÍFICOS - Alta (130-190 años)
    'Filósofo': (135, 195),
    'Astrónomo': (130, 190),
    'Matemático': (135, 195),
    'Naturalista': (125, 180),
    'Alquimista': (120, 175),
    'Cartógrafo': (115, 165),
    # TECNOLÓGICOS - Alta (120-180 años)
    'Bio-Ingeniero': (125, 185),
    'Tecnomístico': (130, 185),
    'Geomante': (125, 180),
    'Biomecánico': (120, 175),
    'Ingeniero de Glifos': (125, 180),
    'Sintetizador': (120, 175),
    'Cultivador de Cristales': (120, 170),
    # SERVICIOS ESPECIALIZADOS - Media-Alta (110-160 años)
    'Arquitecto': (115, 165),
    'Escriba': (120, 170),
    'Curandero': (115, 165),
    # ARTESANALES - Media-Alta (100-150 años)
    'Herrero': (95, 145),
    'Carpintero': (100, 150),
    'Alfarero': (105, 155),
    'Tejedor': (110, 160),
    'Tallador': (100, 150),
    'Joyero': (110, 160),
    'Vidriero': (100, 150),
    'Perfumista': (110, 160),
    'Tatuador': (105, 155),
    # COMERCIALES - Media (100-145 años)
    'Comerciante': (105, 150),
    'Posadero': (95, 140),
    # AGRÍCOLAS - Media (90-140 años)
    'Agricultor': (90, 140),
    'Pastor': (95, 145),
    'Pescador': (85, 135),
    'Cazador': (80, 130),
    # SERVICIOS - Media (90-135 años)
    'Cocinero': (95, 140),
    'Minero': (75, 120),
    'Cantinero': (90, 135),
    'Mensajero': (85, 130),
    # SOCIALES - Media-Baja (80-130 años)
    'Bardo': (90, 140),
    'Prostituta': (70, 115),
    'Prostituto': (70, 115),
    # MILITARES - Baja (70-120 años)
    'Guerrero': (65, 115),
    'Arquero': (70, 120),
    'Capitán': (75, 125),
    'Estratega': (85, 135),
    'Guardián': (75, 125),
    'Guardaespaldas': (70, 120),
    'Vigilante Nocturno': (75, 125),
    # CRIMINALES - Muy Baja (50-100 años)
    'Ladrón': (60, 105),
    'Asesino': (50, 95),
    'Contrabandista': (55, 100),
    'Espía': (55, 100),
}

# ================================================================
# MODIFICADORES DE HÁBITOS Y CLASE SOCIAL (Mantiene el mismo contenido)
# ================================================================

HABITOS_VIDA = {
    'excelente': {
        'nombre': 'Vida Ejemplar',
        'descripcion': 'Alimentación balanceada, ejercicio regular, meditación, descanso adecuado',
        'modificador': 1.25,
        'probabilidad': 0.10
    },
    'bueno': {
        'nombre': 'Buenos Hábitos',
        'descripcion': 'Alimentación saludable, actividad física moderada, buen descanso',
        'modificador': 1.15,
        'probabilidad': 0.25
    },
    'promedio': {
        'nombre': 'Hábitos Normales',
        'descripcion': 'Alimentación común, actividad moderada',
        'modificador': 1.0,
        'probabilidad': 0.45
    },
    'malo': {
        'nombre': 'Malos Hábitos',
        'descripcion': 'Alimentación pobre, sedentarismo, poco descanso',
        'modificador': 0.85,
        'probabilidad': 0.15
    },
    'pesimo': {
        'nombre': 'Vida Destructiva',
        'descripcion': 'Alcoholismo, drogas, violencia, desnutrición',
        'modificador': 0.65,
        'probabilidad': 0.05
    }
}

MODIFICADOR_CLASE_SOCIAL = {
    'sacerdote': 1.20,
    'sacerdotisa': 1.20,
    'noble': 1.15,
    'artesano': 1.05,
    'campesino': 0.95,
    'guerrero': 0.90,
    'esclavo': 0.70,
}

# ================================================================
# CALCULADOR DE LONGEVIDAD (ADAPTADO A POSTGRESQL)
# ================================================================

class CalculadorLongevidad:
    # Se elimina db_path y se usa DatabaseConnector
    def __init__(self):
        self.db = DatabaseConnector()
        self.conn = self.db.connect()
        self.cursor = self.db.cursor
        self.cargar_oficios()

    def execute_query(self, query, params=None):
        """Wrapper para adaptar placeholders de SQLite (?) a PostgreSQL (%s)"""
        # Hacemos el reemplazo solo si estamos en postgres Y vemos '?'
        if self.db.db_type == 'postgres' and '?' in query:
            query = query.replace('?', '%s')
            
        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

    def fetchone(self):
        """Retorna un único resultado (diccionario en PostgreSQL)"""
        return self.cursor.fetchone()

    def fetchall(self):
        """Retorna todos los resultados (lista de diccionarios en PostgreSQL)"""
        return self.cursor.fetchall()

    def commit(self):
        """Realiza commit"""
        self.conn.commit()

    def close(self):
        """Cierra la conexión"""
        self.db.close()

    def cargar_oficios(self):
        """Carga oficios de la BD"""
        self.execute_query("SELECT id, nombre FROM oficios")
        # Acceso por clave de diccionario para PostgreSQL
        self.oficios = {row['id']: row['nombre'] for row in self.fetchall()}
        print(f"✅ {len(self.oficios)} oficios cargados")

    def seleccionar_habito_vida(self) -> str:
        """Selecciona hábito de vida según probabilidades"""
        r = random.random()
        acumulado = 0

        for habito, info in HABITOS_VIDA.items():
            acumulado += info['probabilidad']
            if r <= acumulado:
                return habito

        return 'promedio'

    def calcular_longevidad(self, persona_id: int) -> dict:
        """Calcula longevidad para una persona específica"""

        # Obtener datos de la persona
        self.execute_query('''
            SELECT p.clase_social, p.año_nacimiento,
                   po.oficio_id
            FROM personas p
            LEFT JOIN persona_oficios po ON p.id = po.persona_id
            WHERE p.id = %s
        ''', (persona_id,))

        result = self.fetchone()
        if not result:
            return None

        # Acceso por clave de diccionario
        clase_social = result.get('clase_social')
        año_nacimiento = result.get('año_nacimiento')
        oficio_id = result.get('oficio_id')

        # Obtener nombre del oficio
        if oficio_id:
            oficio_nombre = self.oficios.get(oficio_id, 'Agricultor')
        else:
            oficio_nombre = 'Agricultor'  # default

        # Longevidad base por oficio
        if oficio_nombre in LONGEVIDAD_OFICIOS:
            min_años, max_años = LONGEVIDAD_OFICIOS[oficio_nombre]
        else:
            min_años, max_años = (90, 140)  # default

        longevidad_base = random.randint(min_años, max_años)

        # Modificador por hábitos
        habito = self.seleccionar_habito_vida()
        mod_habito = HABITOS_VIDA[habito]['modificador']

        # Modificador por clase social
        mod_clase = MODIFICADOR_CLASE_SOCIAL.get(clase_social, 1.0)

        # Eventos especiales (bendiciones, maldiciones, accidentes)
        mod_eventos = random.uniform(0.90, 1.10)

        # Cálculo final
        longevidad_final = longevidad_base * mod_habito * mod_clase * mod_eventos

        # Cap a 200 años para humanos
        longevidad_final = min(200, max(50, int(longevidad_final)))

        return {
            'persona_id': persona_id,
            'oficio': oficio_nombre,
            'clase_social': clase_social,
            'longevidad_base': longevidad_base,
            'habito_vida': habito,
            'habito_nombre': HABITOS_VIDA[habito]['nombre'],
            'modificador_habito': mod_habito,
            'modificador_clase': mod_clase,
            'modificador_eventos': mod_eventos,
            'longevidad_final': longevidad_final,
            'año_muerte_calculado': año_nacimiento + longevidad_final
        }

    def actualizar_longevidad_persona(self, persona_id: int) -> bool:
        """Actualiza la longevidad de una persona en la BD"""
        resultado = self.calcular_longevidad(persona_id)

        if not resultado:
            return False

        # Actualizar año de muerte
        self.execute_query('''
            UPDATE personas
            SET año_muerte = %s
            WHERE id = %s
        ''', (resultado['año_muerte_calculado'], persona_id))

        # Guardar información de longevidad en JSON
        info_longevidad = {
            'oficio': resultado['oficio'],
            'habito_vida': resultado['habito_nombre'],
            'longevidad_base': resultado['longevidad_base'],
            'modificadores': {
                'habito': resultado['modificador_habito'],
                'clase': resultado['modificador_clase'],
                'eventos': resultado['modificador_eventos']
            },
            'longevidad_final': resultado['longevidad_final']
        }

        # Actualizar campo personalidad (asumiendo que puede ser NULL o TEXT JSON)
        self.execute_query('''
            SELECT notas_especiales FROM personas WHERE id = %s
        ''', (persona_id,))
        
        # Usamos notas_especiales, ya que 'personalidad' no estaba en el schema anterior
        pers_raw = self.fetchone()
        pers = pers_raw['notas_especiales'] if pers_raw else None 

        if pers:
            # Manejar el caso de que el campo sea realmente un JSON string
            try:
                pers_dict = json.loads(pers)
            except json.JSONDecodeError:
                pers_dict = {}
        else:
            pers_dict = {}

        pers_dict['info_longevidad'] = info_longevidad

        self.execute_query('''
            UPDATE personas
            SET notas_especiales = %s
            WHERE id = %s
        ''', (json.dumps(pers_dict), persona_id))

        self.commit()
        return True

    def actualizar_longevidad_masiva(self, limite: int = None):
        """Actualiza longevidad para todos los humanos en la BD"""
        print("\n" + "="*70)
        print("ACTUALIZACIÓN MASIVA DE LONGEVIDAD POR OFICIO")
        print("="*70)

        # Obtener todos los humanos (usando JOIN)
        query = '''
            SELECT p.id
            FROM personas p
            JOIN especies e ON p.especie_id = e.id
            WHERE e.nombre = 'Humanos I'
        '''

        if limite:
            query += f" LIMIT {limite}"

        self.execute_query(query)
        # Acceso por clave de diccionario
        humanos_ids = [row['id'] for row in self.fetchall()]

        print(f"\n📊 Total humanos a procesar: {len(humanos_ids)}")
        print("\nActualizando...")

        actualizados = 0
        fallidos = 0

        for i, persona_id in enumerate(humanos_ids):
            if self.actualizar_longevidad_persona(persona_id):
                actualizados += 1
            else:
                fallidos += 1

            if (i + 1) % 100 == 0:
                print(f"  ✓ {i + 1}/{len(humanos_ids)} procesados...")

        print(f"\n{'='*70}")
        print("RESUMEN")
        print(f"{'='*70}")
        print(f"  ✅ Actualizados: {actualizados}")
        print(f"  ❌ Fallidos: {fallidos}")

        # Estadísticas de longevidad
        self.execute_query('''
            SELECT
                AVG(p.año_muerte - p.año_nacimiento) as promedio,
                MIN(p.año_muerte - p.año_nacimiento) as minimo,
                MAX(p.año_muerte - p.año_nacimiento) as maximo
            FROM personas p
            JOIN especies e ON p.especie_id = e.id
            WHERE e.nombre = 'Humanos I'
            AND p.año_muerte IS NOT NULL
        ''')

        # Acceso por clave de diccionario
        stats = self.fetchone()
        prom = stats['promedio']
        minimo = stats['minimo']
        maximo = stats['maximo']

        print(f"\n📈 ESTADÍSTICAS DE LONGEVIDAD:")
        print(f"  Promedio: {prom:.1f} años")
        print(f"  Mínimo: {minimo:.0f} años")
        print(f"  Máximo: {maximo:.0f} años")

        # Distribución por rangos
        print(f"\n📊 DISTRIBUCIÓN POR RANGOS:")

        rangos = [
            (50, 75, 'Muy Corta'),
            (75, 100, 'Corta'),
            (100, 125, 'Media-Baja'),
            (125, 150, 'Media'),
            (150, 175, 'Alta'),
            (175, 200, 'Muy Alta'),
        ]

        for min_r, max_r, etiqueta in rangos:
            self.execute_query('''
                SELECT COUNT(*)
                FROM personas p
                JOIN especies e ON p.especie_id = e.id
                WHERE e.nombre = 'Humanos I'
                AND (p.año_muerte - p.año_nacimiento) >= %s
                AND (p.año_muerte - p.año_nacimiento) < %s
            ''', (min_r, max_r))

            count = self.fetchone()['count']
            porcentaje = (count / len(humanos_ids)) * 100 if humanos_ids else 0
            print(f"  {min_r:3d}-{max_r:3d} años ({etiqueta:12s}): {count:5d} ({porcentaje:5.1f}%)")

    def generar_reporte_oficios(self):
        """Genera reporte de longevidad por oficio"""
        print("\n" + "="*70)
        print("REPORTE: LONGEVIDAD PROMEDIO POR OFICIO")
        print("="*70)

        self.execute_query('''
            SELECT
                o.nombre as oficio,
                COUNT(DISTINCT p.id) as cantidad,
                AVG(p.año_muerte - p.año_nacimiento) as promedio_vida,
                MIN(p.año_muerte - p.año_nacimiento) as min_vida,
                MAX(p.año_muerte - p.año_nacimiento) as max_vida
            FROM personas p
            JOIN especies e ON p.especie_id = e.id
            JOIN persona_oficios po ON p.id = po.persona_id
            JOIN oficios o ON po.oficio_id = o.id
            WHERE e.nombre = 'Humanos I'
            AND p.año_muerte IS NOT NULL
            GROUP BY o.nombre
            HAVING COUNT(DISTINCT p.id) > 0
            ORDER BY promedio_vida DESC
        ''')

        print(f"\n{'Oficio':<25s} {'Cant.':>6s} {'Prom.':>7s} {'Min':>6s} {'Max':>6s}")
        print("-" * 70)

        # Acceso por clave de diccionario
        for row in self.fetchall():
            print(f"{row['oficio']:<25s} {row['cantidad']:6d} {row['promedio_vida']:7.1f} {row['min_vida']:6.0f} {row['max_vida']:6.0f}")

def main():
    """Función principal"""
    print("="*70)
    print("SISTEMA DE LONGEVIDAD POR OFICIO Y HÁBITOS")
    print("Portales del Quinto Sol")
    print("="*70)

    calculador = CalculadorLongevidad()

    # Menú interactivo
    print("\nOpciones:")
    print("  1. Actualizar longevidad de todos los humanos")
    print("  2. Actualizar longevidad de N humanos (prueba)")
    print("  3. Generar reporte por oficios")
    print("  4. Ver configuración del sistema")

    opcion = input("\nSelecciona opción (1-4): ").strip()

    if opcion == '1':
        confirm = input("\n⚠️  ¿Actualizar TODOS los humanos? (s/n): ").strip().lower()
        if confirm == 's':
            calculador.actualizar_longevidad_masiva()
            calculador.generar_reporte_oficios()
    elif opcion == '2':
        try:
            n = int(input("¿Cuántos humanos? "))
            calculador.actualizar_longevidad_masiva(limite=n)
        except:
            print("❌ Número inválido")
    elif opcion == '3':
        calculador.generar_reporte_oficios()
    elif opcion == '4':
        print("\n" + "="*70)
        print("CONFIGURACIÓN: LONGEVIDAD POR OFICIO")
        print("="*70)
        for oficio, (min_v, max_v) in sorted(LONGEVIDAD_OFICIOS.items(), key=lambda x: x[1][1], reverse=True):
            print(f"  {oficio:<30s}: {min_v:3d}-{max_v:3d} años")

    calculador.close() # Usar el método close adaptado
    print("\n✅ Proceso completado")

if __name__ == '__main__':
    main()