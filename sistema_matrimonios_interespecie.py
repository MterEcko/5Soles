#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Matrimonios Inter-Especies e Híbridos
Portales del Quinto Sol
ADAPTADO A POSTGRESQL (DatabaseConnector)
"""

import random
import json
import re 
from typing import List, Tuple, Optional, Dict
from database_connector import DatabaseConnector # Importación clave

# ================================================================
# CONFIGURACIÓN DE COMPATIBILIDAD
# ================================================================

COMPATIBILIDAD_BASE = {
    # (Especie1, Especie2): {reproducirse, prob_concepcion, prob_esterilidad, aceptacion_social, vigor, taboo, bendicion_req}

    # HUMANOS con especies sirvientes (ALTA compatibilidad - mismo origen divino)
    ('Humanos I', 'Tlacatl de Luz'): {
        'reproducirse': True,
        'prob_concepcion': 0.5,
        'prob_esterilidad': 0.15,
        'aceptacion': 65,
        'vigor': True,
        'taboo': False,
        'bendicion_req': False
    },
    ('Humanos I', 'Sombra-Coyotes'): {
        'reproducirse': True,
        'prob_concepcion': 0.4,
        'prob_esterilidad': 0.25,
        'aceptacion': 40,
        'vigor': True,
        'taboo': True,
        'bendicion_req': False
    },
    ('Humanos I', 'Bio-Constructores'): {
        'reproducirse': True,
        'prob_concepcion': 0.55,
        'prob_esterilidad': 0.10,
        'aceptacion': 70,
        'vigor': True,
        'taboo': False,
        'bendicion_req': False
    },
    ('Humanos I', 'Acuátiles'): {
        'reproducirse': True,
        'prob_concepcion': 0.45,
        'prob_esterilidad': 0.20,
        'aceptacion': 60,
        'vigor': True,
        'taboo': False,
        'bendicion_req': False
    },
    ('Humanos I', 'Guerreros Solares'): {
        'reproducirse': True,
        'prob_concepcion': 0.40,
        'prob_esterilidad': 0.18,
        'aceptacion': 75,
        'vigor': True,
        'taboo': False,
        'bendicion_req': False
    },

    # ENTRE ESPECIES SIRVIENTES (Compatibilidad MEDIA)
    ('Tlacatl de Luz', 'Bio-Constructores'): {
        'reproducirse': True,
        'prob_concepcion': 0.30,
        'prob_esterilidad': 0.35,
        'aceptacion': 55,
        'vigor': True,
        'taboo': False,
        'bendicion_req': True
    },
    ('Sombra-Coyotes', 'Guerreros Solares'): {
        'reproducirse': True,
        'prob_concepcion': 0.20,
        'prob_esterilidad': 0.50,
        'aceptacion': 25,
        'vigor': False,
        'taboo': True,
        'bendicion_req': True
    },
    ('Acuátiles', 'Bio-Constructores'): {
        'reproducirse': True,
        'prob_concepcion': 0.40,
        'prob_esterilidad': 0.25,
        'aceptacion': 60,
        'vigor': True,
        'taboo': False,
        'bendicion_req': False
    },
}

# Rasgos físicos por especie
RASGOS_ESPECIES = {
    'Humanos I': ['piel_normal', 'estatura_media', 'sin_rasgos_especiales'],
    'Tlacatl de Luz': ['plumas_brazos', 'ojos_verticales', 'piel_escamosa', 'alta_estatura'],
    'Sombra-Coyotes': ['orejas_coyote', 'ojos_espejo', 'piel_manchas', 'cola_50%'],
    'Bio-Constructores': ['piel_corteza', 'cabello_hojas', 'flores_cuerpo', 'conexion_naturaleza'],
    'Acuátiles': ['branquias', 'manos_palmeadas', 'ojos_grandes', 'piel_azul_verde'],
    'Guerreros Solares': ['piel_dorada', 'sangre_dorada', 'ojos_fuego', 'aura_calor']
}

# Habilidades únicas de híbridos
HABILIDADES_HIBRIDAS = {
    ('Humanos I', 'Tlacatl de Luz'): ['volar_cortas_distancias', 'vision_mejorada', 'carisma_diplomatico'],
    ('Humanos I', 'Sombra-Coyotes'): ['sigilo_excepcional', 'vision_nocturna_parcial', 'olfato_agudo'],
    ('Humanos I', 'Bio-Constructores'): ['curar_plantas', 'resistencia_toxinas', 'longevidad_extendida'],
    ('Humanos I', 'Acuátiles'): ['respirar_agua_limitado', 'nadar_rapido', 'resistencia_presion'],
    ('Humanos I', 'Guerreros Solares'): ['fuerza_aumentada', 'resistencia_calor', 'presencia_imponente'],
    ('Tlacatl de Luz', 'Bio-Constructores'): ['comunion_natural', 'alas_vegetales', 'sabiduria_ancestral'],
    ('Acuátiles', 'Bio-Constructores'): ['controlar_plantas_acuaticas', 'anfibio_perfecto', 'regeneracion'],
}

# ================================================================
# GENERADOR DE HÍBRIDOS (ADAPTADO A POSTGRESQL)
# ================================================================

class GeneradorHibridos:
    def __init__(self):
        self.db = DatabaseConnector()
        self.conn = self.db.connect()
        self.cursor = self.db.cursor
        self.cargar_especies()

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
    
    def close(self):
        self.db.close()


    def cargar_especies(self):
        """Carga especies de la BD"""
        self.execute_query("SELECT id, nombre FROM especies")
        self.especies = {row['nombre']: row['id'] for row in self.fetchall()}
        print(f"✅ {len(self.especies)} especies cargadas")

    def poblar_compatibilidad(self):
        """Pobla tabla de compatibilidad"""
        print("\n🧬 Poblando compatibilidad entre especies...")

        for (esp1, esp2), config in COMPATIBILIDAD_BASE.items():
            esp1_id = self.especies.get(esp1)
            esp2_id = self.especies.get(esp2)

            if not esp1_id or not esp2_id:
                continue

            # Insertar en ambas direcciones
            for e1, e2 in [(esp1_id, esp2_id), (esp2_id, esp1_id)]:
                # Uso de %s y ON CONFLICT DO UPDATE
                self.execute_query('''
                    INSERT INTO compatibilidad_especies (
                        especie_1_id, especie_2_id, puede_reproducirse,
                        probabilidad_concepcion, probabilidad_esterilidad_hibrido,
                        aceptacion_social, vigor_hibrido, taboo_cultural,
                        bendicion_divina_requerida
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (especie_1_id, especie_2_id) DO UPDATE
                    SET probabilidad_concepcion = EXCLUDED.probabilidad_concepcion
                ''', (
                    e1, e2, config['reproducirse'],
                    config['prob_concepcion'], config['prob_esterilidad'],
                    config['aceptacion'], config['vigor'],
                    config['taboo'], config['bendicion_req']
                ))

        self.commit()
        print(f"✅ Compatibilidad configurada para {len(COMPATIBILIDAD_BASE)} parejas de especies")

    def verificar_compatibilidad(self, especie1_id: int, especie2_id: int) -> Optional[Dict]:
        """Verifica si dos especies pueden tener hijos"""
        # Asegurar el orden de búsqueda para clave única
        if especie1_id > especie2_id:
             especie1_id, especie2_id = especie2_id, especie1_id

        self.execute_query('''
            SELECT puede_reproducirse, probabilidad_concepcion,
                   probabilidad_esterilidad_hibrido, aceptacion_social,
                   vigor_hibrido, taboo_cultural, bendicion_divina_requerida
            FROM compatibilidad_especies
            WHERE especie_1_id = %s AND especie_2_id = %s
        ''', (especie1_id, especie2_id))

        result = self.fetchone()

        if not result or not result['puede_reproducirse']:
            return None

        return {
            'prob_concepcion': result['probabilidad_concepcion'],
            'prob_esterilidad': result['probabilidad_esterilidad_hibrido'],
            'aceptacion': result['aceptacion_social'],
            'vigor': result['vigor_hibrido'],
            'taboo': result['taboo_cultural'],
            'bendicion_req': result['bendicion_divina_requerida']
        }

    def crear_matrimonio_interespecie(self, persona1_id: int, persona2_id: int,
                                     año_union: int) -> Optional[int]:
        """Crea matrimonio entre especies diferentes"""

        self.execute_query('''
            SELECT especie_id FROM personas WHERE id = %s
        ''', (persona1_id,))
        esp1_id = self.fetchone()['especie_id']

        self.execute_query('''
            SELECT especie_id FROM personas WHERE id = %s
        ''', (persona2_id,))
        esp2_id = self.fetchone()['especie_id']

        if esp1_id == esp2_id:
            return None
        
        # Asegurar orden para verificar compatibilidad (especie_1_id < especie_2_id)
        esp_comp1_id = min(esp1_id, esp2_id)
        esp_comp2_id = max(esp1_id, esp2_id)

        compat = self.verificar_compatibilidad(esp_comp1_id, esp_comp2_id)

        if not compat:
            return None

        self.execute_query('''
            SELECT lugar_residencia_id FROM personas WHERE id = %s
        ''', (persona1_id,))
        lugar_id = self.fetchone()['lugar_residencia_id']

        # Crear matrimonio normal (con RETURNING id)
        query_matrimonio = '''
            INSERT INTO matrimonios (persona1_id, persona2_id, año_union, lugar_union_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        '''
        self.execute_query(query_matrimonio, (persona1_id, persona2_id, año_union, lugar_id))
        matrimonio_id = self.fetchone()['id']

        # Reacción social
        aprobacion_base = compat['aceptacion']
        aprobacion_1 = aprobacion_base + random.randint(-20, 20)
        aprobacion_2 = aprobacion_base + random.randint(-20, 20)

        escandalo = compat['taboo'] and random.random() < 0.3

        # Bendición divina
        bendicion = False
        dios_bendijo = None
        dios_maldijo = None

        if compat['bendicion_req'] or random.random() < 0.15:
            if random.random() < 0.7:
                bendicion = True
                self.execute_query('SELECT id FROM dioses ORDER BY RANDOM() LIMIT 1')
                dios_bendijo = self.fetchone()['id']
            else:
                self.execute_query('SELECT id FROM dioses ORDER BY RANDOM() LIMIT 1')
                dios_maldijo = self.fetchone()['id']

        # Registrar evento
        self.execute_query('''
            INSERT INTO matrimonios_interespecie_eventos (
                matrimonio_id, especie_1_id, especie_2_id, año_union,
                aprobacion_familia_1, aprobacion_familia_2, escandalo_publico,
                bendicion_divina, dios_bendijo_id, dios_maldijo_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            matrimonio_id, esp1_id, esp2_id, año_union,
            aprobacion_1, aprobacion_2, escandalo,
            bendicion, dios_bendijo, dios_maldijo
        ))

        # Mejorar relación diplomática entre especies
        self.execute_query('''
            UPDATE diplomacia_especies
            SET nivel_relacion = nivel_relacion + 5
            WHERE (especie_id = %s AND especie_objetivo_id = %s)
               OR (especie_id = %s AND especie_objetivo_id = %s)
        ''', (esp1_id, esp2_id, esp2_id, esp1_id))

        self.commit()
        return matrimonio_id

    def crear_hibrido(self, nombre: str, genero: str, año_nacimiento: int,
                     padre_id: int, madre_id: int) -> int:
        """Crea un hijo híbrido"""

        # Obtener info de los padres
        self.execute_query('''
            SELECT especie_id, civilizacion_id, lugar_residencia_id
            FROM personas WHERE id = %s
        ''', (padre_id,))
        padre_info = self.fetchone()
        esp_padre_id, civ_id, lugar_id = padre_info['especie_id'], padre_info['civilizacion_id'], padre_info['lugar_residencia_id']

        self.execute_query('''
            SELECT especie_id FROM personas WHERE id = %s
        ''', (madre_id,))
        esp_madre_id = self.fetchone()['especie_id']
        
        # Asegurar orden para verificar compatibilidad
        esp_comp1_id = min(esp_padre_id, esp_madre_id)
        esp_comp2_id = max(esp_padre_id, esp_madre_id)

        compat = self.verificar_compatibilidad(esp_comp1_id, esp_comp2_id)
        if not compat: return 0

        if random.random() > compat['prob_concepcion']: return 0

        # Obtener nombres de especies
        self.execute_query('SELECT nombre FROM especies WHERE id = %s', (esp_padre_id,))
        esp_padre_nombre = self.fetchone()['nombre']

        self.execute_query('SELECT nombre FROM especies WHERE id = %s', (esp_madre_id,))
        esp_madre_nombre = self.fetchone()['nombre']

        # Seleccionar especie "dominante" para el campo especie_id
        especie_dominante_id = random.choice([esp_padre_id, esp_madre_id])

        # Stats
        stats_base = self.calcular_stats_hibrido(esp_padre_id, esp_madre_id, compat['vigor'])

        # Longevidad
        self.execute_query('''
            SELECT AVG(año_muerte - año_nacimiento) AS avg_life
            FROM personas
            WHERE especie_id IN (%s, %s) AND año_muerte IS NOT NULL
            LIMIT 100
        ''', (esp_padre_id, esp_madre_id))

        longevidad_promedio_row = self.fetchone()
        # Convertir a float para cálculo seguro
        longevidad_promedio = float(longevidad_promedio_row['avg_life']) if longevidad_promedio_row['avg_life'] is not None else 150.0

        # Apellido del padre
        self.execute_query('SELECT apellido FROM personas WHERE id = %s', (padre_id,))
        apellido = self.fetchone()['apellido']

        # ----------------------------------------------------------------------
        # CORRECCIÓN CRÍTICA: Eliminar 'nombre_completo' de la inserción
        # ----------------------------------------------------------------------
        query_hibrido = '''
            INSERT INTO personas (
                nombre, apellido, genero, 
                especie_id, año_nacimiento, año_muerte,
                padre_id, madre_id,
                civilizacion_id, lugar_residencia_id,
                fuerza, agilidad, inteligencia, resistencia, carisma,
                es_hibrido
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        '''
        # Ejecución sin el campo ni el valor de nombre_completo (16 placeholders)
        self.execute_query(query_hibrido, (
            nombre, apellido, genero,
            especie_dominante_id, año_nacimiento, año_nacimiento + int(longevidad_promedio),
            padre_id, madre_id,
            civ_id, lugar_id,
            stats_base['fuerza'], stats_base['agilidad'],
            stats_base['inteligencia'], stats_base['resistencia'],
            stats_base['carisma'],
            True # es_hibrido
        ))

        persona_id = self.fetchone()['id']

        # Verificar esterilidad
        es_esteril = random.random() < compat['prob_esterilidad']

        # Rasgos mezclados
        rasgos_padre = self.seleccionar_rasgos(esp_padre_nombre, 2)
        rasgos_madre = self.seleccionar_rasgos(esp_madre_nombre, 2)
        habilidades = self.obtener_habilidades_hibridas(esp_padre_nombre, esp_madre_nombre)

        # Registrar como híbrido (uso de %s)
        self.execute_query('''
            INSERT INTO personas_hibridas (
                persona_id, especie_padre_id, especie_madre_id,
                longevidad_esperada, fertilidad_mixta,
                rasgos_especie_padre, rasgos_especie_madre,
                habilidades_hibridas, identificacion_cultural, es_esteril
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (persona_id) DO NOTHING
        ''', (
            persona_id, esp_padre_id, esp_madre_id,
            int(longevidad_promedio), not es_esteril,
            json.dumps(rasgos_padre), json.dumps(rasgos_madre),
            json.dumps(habilidades), 'hibrido', es_esteril
        ))

        self.commit()
        return persona_id

    def calcular_stats_hibrido(self, esp1_id: int, esp2_id: int, vigor: bool) -> Dict:
        """Calcula stats promedio de un híbrido"""
        stats = {}
        mod = 1.10 if vigor else 0.90

        for stat in ['fuerza', 'agilidad', 'inteligencia', 'resistencia', 'carisma']:
            self.execute_query(f'''
                SELECT AVG({stat}) AS avg_stat
                FROM personas
                WHERE especie_id IN (%s, %s)
                LIMIT 100
            ''', (esp1_id, esp2_id))

            promedio_row = self.fetchone()
            
            # CORRECCIÓN CRÍTICA: Convertir a FLOAT para evitar error con decimal.Decimal
            promedio_decimal = promedio_row['avg_stat'] 
            promedio = float(promedio_decimal) if promedio_decimal is not None else 50.0

            promedio *= mod 
            stats[stat] = int(promedio)

        return stats

    def seleccionar_rasgos(self, especie_nombre: str, num_rasgos: int) -> List[str]:
        """Selecciona rasgos aleatorios de una especie"""
        rasgos = RASGOS_ESPECIES.get(especie_nombre, [])
        if not rasgos: return []
        num_rasgos = min(num_rasgos, len(rasgos))
        return random.sample(rasgos, num_rasgos)

    def obtener_habilidades_hibridas(self, esp1: str, esp2: str) -> List[str]:
        """Obtiene habilidades únicas del híbrido"""
        key1 = (esp1, esp2)
        key2 = (esp2, esp1)
        habilidades = HABILIDADES_HIBRIDAS.get(key1) or HABILIDADES_HIBRIDAS.get(key2) or []
        return habilidades

    def simular_matrimonios_interespecie(self, año_inicio: int = 1500, año_fin: int = 3000):
        """Simula matrimonios inter-especies durante el período"""
        print(f"\n{'='*70}")
        print(f"SIMULANDO MATRIMONIOS INTER-ESPECIES: {año_inicio}-{año_fin}")
        print(f"{'='*70}\n")

        self.execute_query('''
            SELECT especie_id, especie_objetivo_id, nivel_relacion
            FROM diplomacia_especies
            WHERE nivel_relacion >= 20
        ''')

        relaciones = self.fetchall()
        print(f"📊 {len(relaciones)} relaciones diplomáticas permiten matrimonios\n")

        matrimonios_creados = 0
        hibridos_nacidos = 0

        for año in range(año_inicio, año_fin, 10):
            num_intentos = random.randint(1, 5)

            for _ in range(num_intentos):
                if not relaciones: break

                rel = random.choice(relaciones)
                esp1_id, esp2_id = rel['especie_id'], rel['especie_objetivo_id']

                edad_min, edad_max = 20, 60

                # Soltero 1 (Masculino - Especie 1)
                self.execute_query('''
                    SELECT id FROM personas
                    WHERE especie_id = %s
                    AND genero = 'masculino'
                    AND año_nacimiento <= %s AND año_nacimiento >= %s
                    AND (año_muerte IS NULL OR año_muerte >= %s)
                    AND id NOT IN (SELECT persona1_id FROM matrimonios UNION SELECT persona2_id FROM matrimonios)
                    ORDER BY RANDOM()
                    LIMIT 1
                ''', (esp1_id, año - edad_min, año - edad_max, año))

                persona1 = self.fetchone()
                if not persona1: continue

                # Soltera 2 (Femenino - Especie 2)
                self.execute_query('''
                    SELECT id FROM personas
                    WHERE especie_id = %s
                    AND genero = 'femenino'
                    AND año_nacimiento <= %s AND año_nacimiento >= %s
                    AND (año_muerte IS NULL OR año_muerte >= %s)
                    AND id NOT IN (SELECT persona1_id FROM matrimonios UNION SELECT persona2_id FROM matrimonios)
                    ORDER BY RANDOM()
                    LIMIT 1
                ''', (esp2_id, año - edad_min, año - edad_max, año))

                persona2 = self.fetchone()
                if not persona2: continue

                mat_id = self.crear_matrimonio_interespecie(persona1['id'], persona2['id'], año)

                if mat_id:
                    matrimonios_creados += 1
                    num_hijos = random.randint(0, 4)

                    for i in range(num_hijos):
                        año_nac = año + random.randint(1, 10)
                        if año_nac > año_fin: break

                        genero = random.choice(['masculino', 'femenino'])
                        nombre = f"Híbrido{random.randint(1000, 9999)}"

                        if self.crear_hibrido(nombre, genero, año_nac, persona1['id'], persona2['id']):
                            hibridos_nacidos += 1

            if (año - año_inicio + 10) % 100 == 0:
                print(f"  ✓ Año {año}... Matrimonios: {matrimonios_creados}, Híbridos: {hibridos_nacidos}")

        print(f"\n{'='*70}")
        print("RESUMEN")
        print(f"{'='*70}")
        print(f"  💍 Matrimonios inter-especies: {matrimonios_creados}")
        print(f"  🧬 Híbridos nacidos: {hibridos_nacidos}")

    def generar_reporte(self):
        """Genera reporte de híbridos"""
        print(f"\n{'='*70}")
        print("REPORTE DE HÍBRIDOS")
        print(f"{'='*70}\n")

        self.execute_query('SELECT COUNT(*) AS total FROM personas_hibridas')
        total = self.fetchone()['total']
        print(f"🧬 Total híbridos: {total}\n")

        print("📊 HÍBRIDOS POR COMBINACIÓN:")
        self.execute_query('''
            SELECT e1.nombre AS especie_1, e2.nombre AS especie_2, COUNT(*) AS count
            FROM personas_hibridas ph
            JOIN especies e1 ON ph.especie_padre_id = e1.id
            JOIN especies e2 ON ph.especie_madre_id = e2.id
            GROUP BY e1.nombre, e2.nombre
            ORDER BY COUNT(*) DESC
        ''')

        for row in self.fetchall():
            print(f"  {row['especie_1']:20s} × {row['especie_2']:20s}: {row['count']:4d}")

def main():
    """Función principal (para ejecución directa del módulo)"""
    print("="*70)
    print("SISTEMA DE MATRIMONIOS INTER-ESPECIES E HÍBRIDOS (STANDALONE)")
    print("Portales del Quinto Sol")
    print("="*70)

    try:
        generador = GeneradorHibridos()
    except Exception as e:
        print(f"❌ Error al inicializar GeneradorHibridos: {e}")
        return

    # Menú
    print("\nOpciones:")
    print("  1. Simular matrimonios inter-especies (1500-3000)")
    print("  2. Ver compatibilidad entre especies")
    print("  3. Generar reporte de híbridos")

    opcion = input("\nSelecciona opción (1-3): ").strip()

    if opcion == '1':
        generador.simular_matrimonios_interespecie()
        generador.generar_reporte()
    elif opcion == '2':
        print("\nCOMPATIBILIDAD BASE:")
        for (esp1, esp2), config in COMPATIBILIDAD_BASE.items():
            print(f"  {esp1} x {esp2}: Concebible={config['reproducirse']}, Aceptación={config['aceptacion']}, Vigor={config['vigor']}")
    elif opcion == '3':
        generador.generar_reporte()

    generador.close()
    print("\n✅ Proceso completado")

if __name__ == '__main__':
    main()