#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistema de Matrimonios Inter-Especies e Híbridos
Portales del Quinto Sol

Permite matrimonios entre especies y genera híbridos:
- Verificación de compatibilidad
- Híbridos con stats promedio
- Rasgos mezclados
- Aceptación social variable
- Comunidades híbridas
"""

import sqlite3
import random
import json
from typing import List, Tuple, Optional, Dict

# ================================================================
# CONFIGURACIÓN DE COMPATIBILIDAD
# ================================================================

COMPATIBILIDAD_BASE = {
    # (Especie1, Especie2): {puede_reproducirse, prob_concepcion, prob_esterilidad, aceptacion_social, vigor}

    # HUMANOS con especies sirvientes (ALTA compatibilidad - mismo origen divino)
    ('Humanos I', 'Tlacatl de Luz'): {
        'reproducirse': True,
        'prob_concepcion': 0.5,  # 50% vs 70% normal
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
        'aceptacion': 40,  # Menos aceptados (nocturnas)
        'vigor': True,
        'taboo': True,  # Algo tabú
        'bendicion_req': False
    },
    ('Humanos I', 'Bio-Constructores'): {
        'reproducirse': True,
        'prob_concepcion': 0.55,
        'prob_esterilidad': 0.10,  # Muy fértiles
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
        'aceptacion': 75,  # Muy respetados
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
        'bendicion_req': True  # Requiere bendición
    },
    ('Sombra-Coyotes', 'Guerreros Solares'): {
        'reproducirse': True,
        'prob_concepcion': 0.20,  # Opuestos (noche/día)
        'prob_esterilidad': 0.50,
        'aceptacion': 25,  # Mal visto
        'vigor': False,  # Debilidad híbrida
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
# GENERADOR DE HÍBRIDOS
# ================================================================

class GeneradorHibridos:
    def __init__(self, db_path='quinto_sol.db'):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cargar_especies()

    def cargar_especies(self):
        """Carga especies de la BD"""
        self.cursor.execute("SELECT id, nombre FROM especies")
        self.especies = {nombre: id for id, nombre in self.cursor.fetchall()}
        print(f"✅ {len(self.especies)} especies cargadas")

    def aplicar_schema(self):
        """Aplica schema de matrimonios inter-especies"""
        print("\n📋 Aplicando schema de matrimonios inter-especies...")

        with open('schema_matrimonios_interespecie.sql', 'r', encoding='utf-8') as f:
            schema_sql = f.read()

        self.conn.executescript(schema_sql)
        self.conn.commit()
        print("✅ Schema aplicado")

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
                self.cursor.execute('''
                    INSERT OR REPLACE INTO compatibilidad_especies (
                        especie_1_id, especie_2_id, puede_reproducirse,
                        probabilidad_concepcion, probabilidad_esterilidad_hibrido,
                        aceptacion_social, vigor_hibrido, taboo_cultural,
                        bendicion_divina_requerida
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    e1, e2, config['reproducirse'],
                    config['prob_concepcion'], config['prob_esterilidad'],
                    config['aceptacion'], config['vigor'],
                    config['taboo'], config['bendicion_req']
                ))

        self.conn.commit()
        print(f"✅ Compatibilidad configurada para {len(COMPATIBILIDAD_BASE)} parejas de especies")

    def verificar_compatibilidad(self, especie1_id: int, especie2_id: int) -> Optional[Dict]:
        """Verifica si dos especies pueden tener hijos"""
        self.cursor.execute('''
            SELECT puede_reproducirse, probabilidad_concepcion,
                   probabilidad_esterilidad_hibrido, aceptacion_social,
                   vigor_hibrido, taboo_cultural, bendicion_divina_requerida
            FROM compatibilidad_especies
            WHERE especie_1_id = ? AND especie_2_id = ?
        ''', (especie1_id, especie2_id))

        result = self.cursor.fetchone()

        if not result or not result[0]:
            return None

        return {
            'prob_concepcion': result[1],
            'prob_esterilidad': result[2],
            'aceptacion': result[3],
            'vigor': result[4],
            'taboo': result[5],
            'bendicion_req': result[6]
        }

    def crear_matrimonio_interespecie(self, persona1_id: int, persona2_id: int,
                                     año_union: int) -> Optional[int]:
        """Crea matrimonio entre especies diferentes"""

        # Obtener especies de ambos
        self.cursor.execute('''
            SELECT especie_id FROM personas WHERE id = ?
        ''', (persona1_id,))
        esp1_id = self.cursor.fetchone()[0]

        self.cursor.execute('''
            SELECT especie_id FROM personas WHERE id = ?
        ''', (persona2_id,))
        esp2_id = self.cursor.fetchone()[0]

        # Misma especie = matrimonio normal
        if esp1_id == esp2_id:
            return None

        # Verificar compatibilidad
        compat = self.verificar_compatibilidad(esp1_id, esp2_id)

        if not compat:
            return None  # No pueden casarse

        # Crear matrimonio normal
        self.cursor.execute('''
            SELECT lugar_residencia_id FROM personas WHERE id = ?
        ''', (persona1_id,))
        lugar_id = self.cursor.fetchone()[0]

        self.cursor.execute('''
            INSERT INTO matrimonios (persona1_id, persona2_id, año_union, lugar_union_id)
            VALUES (?, ?, ?, ?)
        ''', (persona1_id, persona2_id, año_union, lugar_id))

        matrimonio_id = self.cursor.lastrowid

        # Reacción social
        aprobacion_base = compat['aceptacion']
        aprobacion_1 = aprobacion_base + random.randint(-20, 20)
        aprobacion_2 = aprobacion_base + random.randint(-20, 20)

        escandalo = compat['taboo'] and random.random() < 0.3

        # Bendición divina (si es requerida o por suerte)
        bendicion = False
        dios_bendijo = None
        dios_maldijo = None

        if compat['bendicion_req'] or random.random() < 0.15:
            if random.random() < 0.7:  # 70% bendición, 30% maldición
                bendicion = True
                self.cursor.execute('SELECT id FROM dioses ORDER BY RANDOM() LIMIT 1')
                dios_bendijo = self.cursor.fetchone()[0]
            else:
                self.cursor.execute('SELECT id FROM dioses ORDER BY RANDOM() LIMIT 1')
                dios_maldijo = self.cursor.fetchone()[0]

        # Registrar evento
        self.cursor.execute('''
            INSERT INTO matrimonios_interespecie_eventos (
                matrimonio_id, especie_1_id, especie_2_id, año_union,
                aprobacion_familia_1, aprobacion_familia_2, escandalo_publico,
                bendicion_divina, dios_bendijo_id, dios_maldijo_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            matrimonio_id, esp1_id, esp2_id, año_union,
            aprobacion_1, aprobacion_2, escandalo,
            bendicion, dios_bendijo, dios_maldijo
        ))

        # Mejorar relación diplomática entre especies
        self.cursor.execute('''
            UPDATE diplomacia_especies
            SET nivel_relacion = nivel_relacion + 5
            WHERE (especie_id = ? AND especie_objetivo_id = ?)
               OR (especie_id = ? AND especie_objetivo_id = ?)
        ''', (esp1_id, esp2_id, esp2_id, esp1_id))

        self.conn.commit()
        return matrimonio_id

    def crear_hibrido(self, nombre: str, genero: str, año_nacimiento: int,
                     padre_id: int, madre_id: int) -> int:
        """Crea un hijo híbrido"""

        # Obtener info de los padres
        self.cursor.execute('''
            SELECT especie_id, civilizacion_id, lugar_residencia_id
            FROM personas WHERE id = ?
        ''', (padre_id,))
        esp_padre_id, civ_id, lugar_id = self.cursor.fetchone()

        self.cursor.execute('''
            SELECT especie_id FROM personas WHERE id = ?
        ''', (madre_id,))
        esp_madre_id = self.cursor.fetchone()[0]

        # Verificar compatibilidad
        compat = self.verificar_compatibilidad(esp_padre_id, esp_madre_id)

        if not compat:
            return 0  # No pueden tener hijos

        # Probabilidad de concepción
        if random.random() > compat['prob_concepcion']:
            return 0  # No conciben

        # Obtener nombres de especies
        self.cursor.execute('SELECT nombre FROM especies WHERE id = ?', (esp_padre_id,))
        esp_padre_nombre = self.cursor.fetchone()[0]

        self.cursor.execute('SELECT nombre FROM especies WHERE id = ?', (esp_madre_id,))
        esp_madre_nombre = self.cursor.fetchone()[0]

        # Seleccionar especie "dominante" para la persona (campo especie_id)
        # 50/50 pero podría ser por dominancia genética
        especie_dominante_id = random.choice([esp_padre_id, esp_madre_id])

        # Stats promedio de ambas especies + vigor/debilidad
        stats_base = self.calcular_stats_hibrido(esp_padre_id, esp_madre_id, compat['vigor'])

        # Longevidad promedio
        self.cursor.execute('''
            SELECT AVG(año_muerte - año_nacimiento)
            FROM personas
            WHERE especie_id IN (?, ?) AND año_muerte IS NOT NULL
            LIMIT 100
        ''', (esp_padre_id, esp_madre_id))

        longevidad_promedio = self.cursor.fetchone()[0] or 150

        # Apellido del padre
        self.cursor.execute('SELECT apellido FROM personas WHERE id = ?', (padre_id,))
        apellido = self.cursor.fetchone()[0]

        # Crear persona híbrida
        self.cursor.execute('''
            INSERT INTO personas (
                nombre, apellido, nombre_completo, genero,
                especie_id, año_nacimiento, año_muerte,
                padre_id, madre_id,
                civilizacion_id, lugar_residencia_id,
                fuerza, agilidad, inteligencia, resistencia, carisma
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            nombre, apellido, f"{nombre} {apellido}", genero,
            especie_dominante_id, año_nacimiento, año_nacimiento + int(longevidad_promedio),
            padre_id, madre_id,
            civ_id, lugar_id,
            stats_base['fuerza'], stats_base['agilidad'],
            stats_base['inteligencia'], stats_base['resistencia'],
            stats_base['carisma']
        ))

        persona_id = self.cursor.lastrowid

        # Verificar esterilidad
        es_esteril = random.random() < compat['prob_esterilidad']

        # Rasgos mezclados
        rasgos_padre = self.seleccionar_rasgos(esp_padre_nombre, 2)
        rasgos_madre = self.seleccionar_rasgos(esp_madre_nombre, 2)

        # Habilidades híbridas
        habilidades = self.obtener_habilidades_hibridas(esp_padre_nombre, esp_madre_nombre)

        # Registrar como híbrido
        self.cursor.execute('''
            INSERT INTO personas_hibridas (
                persona_id, especie_padre_id, especie_madre_id,
                longevidad_esperada, fertilidad_mixta,
                rasgos_especie_padre, rasgos_especie_madre,
                habilidades_hibridas, identificacion_cultural
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            persona_id, esp_padre_id, esp_madre_id,
            int(longevidad_promedio), not es_esteril,
            json.dumps(rasgos_padre), json.dumps(rasgos_madre),
            json.dumps(habilidades), 'hibrido'
        ))

        self.conn.commit()
        return persona_id

    def calcular_stats_hibrido(self, esp1_id: int, esp2_id: int, vigor: bool) -> Dict:
        """Calcula stats promedio de un híbrido"""

        stats = {}

        for stat in ['fuerza', 'agilidad', 'inteligencia', 'resistencia', 'carisma']:
            self.cursor.execute(f'''
                SELECT AVG({stat})
                FROM personas
                WHERE especie_id IN (?, ?)
                LIMIT 100
            ''', (esp1_id, esp2_id))

            promedio = self.cursor.fetchone()[0] or 50

            # Vigor híbrido (+10%) o debilidad (-10%)
            if vigor:
                promedio *= 1.10
            else:
                promedio *= 0.90

            stats[stat] = int(promedio)

        return stats

    def seleccionar_rasgos(self, especie_nombre: str, num_rasgos: int) -> List[str]:
        """Selecciona rasgos aleatorios de una especie"""
        rasgos = RASGOS_ESPECIES.get(especie_nombre, [])

        if not rasgos:
            return []

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

        # Obtener todas las relaciones que permiten matrimonio inter-especies
        self.cursor.execute('''
            SELECT especie_id, especie_objetivo_id, nivel_relacion
            FROM diplomacia_especies
            WHERE nivel_relacion >= 20
        ''')

        relaciones = self.cursor.fetchall()
        print(f"📊 {len(relaciones)} relaciones diplomáticas permiten matrimonios\n")

        matrimonios_creados = 0
        hibridos_nacidos = 0

        # Cada 10 años, intentar crear algunos matrimonios inter-especies
        for año in range(año_inicio, año_fin, 10):
            # Número de intentos (muy bajo, 1% de todos los matrimonios)
            num_intentos = random.randint(1, 5)

            for _ in range(num_intentos):
                # Seleccionar par de especies compatible
                if not relaciones:
                    break

                esp1_id, esp2_id, _ = random.choice(relaciones)

                # Buscar solteros en edad de matrimonio
                edad_min = 20
                edad_max = 60

                self.cursor.execute('''
                    SELECT id FROM personas
                    WHERE especie_id = ?
                    AND genero = 'masculino'
                    AND año_nacimiento <= ? AND año_nacimiento >= ?
                    AND año_muerte >= ?
                    AND id NOT IN (SELECT persona1_id FROM matrimonios UNION SELECT persona2_id FROM matrimonios)
                    ORDER BY RANDOM()
                    LIMIT 1
                ''', (esp1_id, año - edad_min, año - edad_max, año))

                persona1 = self.cursor.fetchone()

                if not persona1:
                    continue

                self.cursor.execute('''
                    SELECT id FROM personas
                    WHERE especie_id = ?
                    AND genero = 'femenino'
                    AND año_nacimiento <= ? AND año_nacimiento >= ?
                    AND año_muerte >= ?
                    AND id NOT IN (SELECT persona1_id FROM matrimonios UNION SELECT persona2_id FROM matrimonios)
                    ORDER BY RANDOM()
                    LIMIT 1
                ''', (esp2_id, año - edad_min, año - edad_max, año))

                persona2 = self.cursor.fetchone()

                if not persona2:
                    continue

                # Crear matrimonio
                mat_id = self.crear_matrimonio_interespecie(persona1[0], persona2[0], año)

                if mat_id:
                    matrimonios_creados += 1

                    # Intentar tener hijos
                    num_hijos = random.randint(0, 4)  # Menos hijos que normal

                    for i in range(num_hijos):
                        año_nac = año + random.randint(1, 10)

                        if año_nac > año_fin:
                            break

                        genero = random.choice(['masculino', 'femenino'])
                        nombre = f"Híbrido{random.randint(1000, 9999)}"  # Nombre temporal

                        if self.crear_hibrido(nombre, genero, año_nac, persona1[0], persona2[0]):
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

        # Total híbridos
        self.cursor.execute('SELECT COUNT(*) FROM personas_hibridas')
        total = self.cursor.fetchone()[0]
        print(f"🧬 Total híbridos: {total}\n")

        # Por combinación de especies
        print("📊 HÍBRIDOS POR COMBINACIÓN:")
        self.cursor.execute('''
            SELECT e1.nombre, e2.nombre, COUNT(*)
            FROM personas_hibridas ph
            JOIN especies e1 ON ph.especie_padre_id = e1.id
            JOIN especies e2 ON ph.especie_madre_id = e2.id
            GROUP BY e1.nombre, e2.nombre
            ORDER BY COUNT(*) DESC
        ''')

        for esp1, esp2, count in self.cursor.fetchall():
            print(f"  {esp1:20s} × {esp2:20s}: {count:4d}")

def main():
    """Función principal"""
    print("="*70)
    print("SISTEMA DE MATRIMONIOS INTER-ESPECIES E HÍBRIDOS")
    print("Portales del Quinto Sol")
    print("="*70)

    generador = GeneradorHibridos()

    # Aplicar schema
    generador.aplicar_schema()

    # Poblar compatibilidad
    generador.poblar_compatibilidad()

    # Menú
    print("\nOpciones:")
    print("  1. Simular matrimonios inter-especies (1500-3000)")
    print("  2. Ver compatibilidad entre especies")
    print("  3. Generar reporte de híbridos")

    opcion = input("\nSelecciona opción (1-3): ").strip()

    if opcion == '1':
        confirm = input("\n⚠️  ¿Simular matrimonios inter-especies? (s/n): ").strip().lower()
        if confirm == 's':
            generador.simular_matrimonios_interespecie()
            generador.generar_reporte()
    elif opcion == '2':
        print(f"\n{'='*70}")
        print("COMPATIBILIDAD ENTRE ESPECIES")
        print(f"{'='*70}\n")
        for (esp1, esp2), config in COMPATIBILIDAD_BASE.items():
            print(f"🧬 {esp1} × {esp2}")
            print(f"   Concepción: {config['prob_concepcion']*100:.0f}%")
            print(f"   Aceptación social: {config['aceptacion']}/100")
            print(f"   Vigor: {'Sí' if config['vigor'] else 'No'}")
            print(f"   Tabú: {'Sí' if config['taboo'] else 'No'}\n")
    elif opcion == '3':
        generador.generar_reporte()

    generador.conn.close()
    print("\n✅ Proceso completado")

if __name__ == '__main__':
    main()
