#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistemas Adicionales Integrados
Portales del Quinto Sol

Integra y simula los 7 sistemas adicionales:
1. Mutaciones
2. Matrimonios Inter-Especies e Híbridos
3. Artefactos Legendarios
4. Organizaciones
5. Eventos Divinos Expandidos
6. Migraciones
7. Justicia
8. Clima y Estaciones
9. Economía Dual
"""

import sqlite3
import random
import json
from datetime import datetime

DB_PATH = 'quinto_sol.db'

class SistemasAdicionales:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()

    def aplicar_todos_schemas(self):
        """Aplica todos los schemas de sistemas adicionales"""
        print("\n" + "="*70)
        print("APLICANDO SCHEMAS DE SISTEMAS ADICIONALES")
        print("="*70)

        schemas = [
            'schema_mutaciones.sql',
            'schema_matrimonios_interespecie.sql',
            'schema_artefactos_organizaciones_eventos.sql',
            'schema_migraciones_justicia_clima_economia.sql'
        ]

        for schema_file in schemas:
            print(f"\n📋 Aplicando {schema_file}...")
            try:
                with open(schema_file, 'r', encoding='utf-8') as f:
                    self.conn.executescript(f.read())
                print(f"✅ {schema_file} aplicado")
            except FileNotFoundError:
                print(f"❌ {schema_file} no encontrado")
            except Exception as e:
                print(f"❌ Error: {e}")

        self.conn.commit()
        print("\n✅ Todos los schemas aplicados")

    def inicializar_sistemas(self):
        """Inicializa datos base de todos los sistemas"""
        print("\n" + "="*70)
        print("INICIALIZANDO SISTEMAS")
        print("="*70)

        # 1. Mutaciones
        print("\n🧬 Inicializando sistema de mutaciones...")
        try:
            import sistema_mutaciones
            gen_mut = sistema_mutaciones.GeneradorMutaciones()
            gen_mut.poblar_catalogo()
            print("✅ Catálogo de mutaciones poblado")
        except:
            print("⚠️  Sistema de mutaciones no disponible")

        # 2. Matrimonios Inter-Especies
        print("\n💍 Inicializando compatibilidad inter-especies...")
        try:
            import sistema_matrimonios_interespecie
            gen_hib = sistema_matrimonios_interespecie.GeneradorHibridos()
            gen_hib.poblar_compatibilidad()
            print("✅ Compatibilidad configurada")
        except:
            print("⚠️  Sistema híbridos no disponible")

        # 3. Monedas base
        print("\n💰 Creando monedas...")
        self.crear_monedas_base()

        # 4. Organizaciones iniciales
        print("\n🏛️  Creando organizaciones iniciales...")
        self.crear_organizaciones_base()

        # 5. Artefactos legendarios
        print("\n⚔️  Creando artefactos legendarios...")
        self.crear_artefactos_base()

        print("\n✅ Inicialización completada")

    def crear_monedas_base(self):
        """Crea monedas base del sistema"""
        monedas = [
            ('Cacao', '🌰', 'fisica', 'npcs', None, 1.0),
            ('Jade', '💎', 'fisica', 'npcs', None, 10.0),
            ('Oro', '🟡', 'fisica', 'npcs', None, 100.0),
            ('QuintoSol Coin', 'QSC', 'cripto', 'jugadores', None, 1000.0),
            ('Bendición Divina', '✨', 'divina', 'especial', None, 10000.0),
        ]

        for nombre, simbolo, tipo, uso, civ_id, valor in monedas:
            self.cursor.execute('''
                INSERT OR IGNORE INTO monedas (nombre, simbolo, tipo, usada_por, valor_relativo, es_cripto)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nombre, simbolo, tipo, uso, valor, tipo == 'cripto'))

        self.conn.commit()
        print(f"  ✓ {len(monedas)} monedas creadas")

    def crear_organizaciones_base(self):
        """Crea organizaciones iniciales"""
        self.cursor.execute('SELECT id FROM civilizaciones LIMIT 1')
        civ_id = self.cursor.fetchone()[0]

        self.cursor.execute('SELECT id FROM pueblos_ciudades LIMIT 1')
        lugar_id = self.cursor.fetchone()[0]

        organizaciones = [
            ('Gremio de Herreros del Sol', 'gremio', 1450, 'Artesanos especializados en metalurgia'),
            ('Orden de los Guerreros Jaguar', 'orden_militar', 1420, 'Élite militar'),
            ('Culto de Quetzalcóatl', 'culto', 1300, 'Adoradores de la serpiente emplumada'),
            ('Hermandad de los Curanderos', 'hermandad', 1380, 'Médicos y sanadores'),
            ('Sociedad del Espejo Humeante', 'sociedad_secreta', 1460, 'Organización misteriosa'),
        ]

        for nombre, tipo, año, proposito in organizaciones:
            self.cursor.execute('''
                INSERT OR IGNORE INTO organizaciones (
                    nombre, tipo, año_fundacion, proposito,
                    lugar_sede_id, civilizacion_id, miembros_actuales
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (nombre, tipo, año, proposito, lugar_id, civ_id, random.randint(10, 100)))

        self.conn.commit()
        print(f"  ✓ {len(organizaciones)} organizaciones creadas")

    def crear_artefactos_base(self):
        """Crea artefactos legendarios base"""
        self.cursor.execute('SELECT id FROM personas ORDER BY RANDOM() LIMIT 5')
        personas = [row[0] for row in self.cursor.fetchall()]

        self.cursor.execute('SELECT id FROM pueblos_ciudades LIMIT 1')
        lugar_id = self.cursor.fetchone()[0]

        artefactos = [
            ('Espada del Amanecer', 'arma', 'legendaria', 1200, 'forjado', 10, '{"fuerza": 30, "carisma": 10}', '["lanzar_rayo_solar"]'),
            ('Escudo de Obsidiana', 'armadura', 'epica', 1300, 'bendecido', 8, '{"resistencia": 40}', '["reflejar_magia"]'),
            ('Collar de Jade Imperial', 'joya', 'epica', 1100, 'ritual', 7, '{"carisma": 25, "inteligencia": 15}', '["persuasion_divina"]'),
            ('Lanza del Trueno', 'arma', 'legendaria', 1250, 'bendecido', 10, '{"fuerza": 35, "agilidad": 10}', '["invocar_tormenta"]'),
            ('Mascara del Jaguar', 'reliquia', 'divina', 1000, 'encontrado', 10, '{"fuerza": 20, "agilidad": 30}', '["transformacion_jaguar"]'),
        ]

        for nombre, tipo, rareza, año, metodo, poder, stats, habs in artefactos:
            prop_id = random.choice(personas) if personas else None

            self.cursor.execute('''
                INSERT OR IGNORE INTO artefactos (
                    nombre, tipo, rareza, año_creacion, metodo_creacion,
                    nivel_poder, modificadores_stats, habilidades_especiales,
                    propietario_id, lugar_creacion_id
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (nombre, tipo, rareza, año, metodo, poder, stats, habs, prop_id, lugar_id))

        self.conn.commit()
        print(f"  ✓ {len(artefactos)} artefactos legendarios creados")

    def simular_ciclos_climaticos(self, año_inicio: int, año_fin: int):
        """Simula ciclos climáticos anuales"""
        print(f"\n🌤️  Simulando clima {año_inicio}-{año_fin}...")

        for año in range(año_inicio, año_fin + 1):
            estacion = random.choice(['primavera', 'verano', 'otoño', 'invierno', 'lluvias', 'secas'])
            temp = random.randint(15, 35)
            precip = random.choice(['muy_baja', 'baja', 'normal', 'alta', 'muy_alta'])

            # Eventos climáticos raros
            sequia = random.random() < 0.05  # 5%
            inundacion = random.random() < 0.03  # 3%
            huracan = random.random() < 0.02  # 2%

            # Impacto
            bonus_agri = 0
            if precip in ['alta', 'muy_alta'] and not inundacion:
                bonus_agri = random.randint(10, 30)
            elif sequia:
                bonus_agri = random.randint(-50, -20)

            self.cursor.execute('''
                INSERT OR IGNORE INTO ciclos_climaticos (
                    año, estacion_dominante, temperatura_promedio, precipitacion,
                    sequia, inundaciones, huracan, bonus_agricultura
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (año, estacion, temp, precip, sequia, inundacion, huracan, bonus_agri))

        self.conn.commit()
        print(f"  ✅ {año_fin - año_inicio + 1} años de clima simulados")

    def simular_eventos_divinos(self, año_inicio: int, año_fin: int):
        """Simula eventos divinos mayores"""
        print(f"\n⚡ Simulando eventos divinos {año_inicio}-{año_fin}...")

        self.cursor.execute('SELECT id FROM dioses')
        dioses = [row[0] for row in self.cursor.fetchall()]

        self.cursor.execute('SELECT id FROM civilizaciones')
        civilizaciones = [row[0] for row in self.cursor.fetchall()]

        # ~20 eventos divinos en 1500 años
        num_eventos = random.randint(15, 25)

        tipos_evento = ['bendicion_masiva', 'maldicion', 'milagro', 'castigo', 'manifestacion', 'profecia']
        alcances = ['ciudad', 'civilizacion', 'todas_especies']

        for _ in range(num_eventos):
            año = random.randint(año_inicio, año_fin)
            dios_id = random.choice(dioses)
            tipo = random.choice(tipos_evento)
            alcance = random.choice(alcances)

            civ_id = random.choice(civilizaciones) if alcance in ['civilizacion', 'ciudad'] else None

            personas_afectadas = random.randint(100, 10000) if alcance == 'ciudad' else random.randint(10000, 100000)

            self.cursor.execute('''
                INSERT INTO eventos_divinos_mayores (
                    dios_id, año_evento, tipo_evento, alcance,
                    objetivo_civilizacion_id, personas_afectadas,
                    descripcion
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (dios_id, año, tipo, alcance, civ_id, personas_afectadas,
                  f'Evento divino {tipo} de alcance {alcance}'))

        self.conn.commit()
        print(f"  ✅ {num_eventos} eventos divinos simulados")

    def simular_migraciones(self, año_inicio: int, año_fin: int):
        """Simula migraciones poblacionales"""
        print(f"\n🚶 Simulando migraciones {año_inicio}-{año_fin}...")

        # Migraciones por guerras (ya existen en el sistema)
        self.cursor.execute('SELECT id, año_inicio FROM guerras_especies WHERE año_inicio >= ?', (año_inicio,))
        guerras = self.cursor.fetchall()

        migraciones_creadas = 0

        for guerra_id, año_guerra in guerras:
            # 50% de probabilidad de generar refugiados
            if random.random() < 0.5:
                self.cursor.execute('SELECT id FROM pueblos_ciudades ORDER BY RANDOM() LIMIT 2')
                lugares = self.cursor.fetchall()

                if len(lugares) >= 2:
                    origen_id = lugares[0][0]
                    destino_id = lugares[1][0]

                    num_migrantes = random.randint(100, 5000)
                    llegaron = int(num_migrantes * random.uniform(0.7, 0.95))  # 70-95% llegan

                    self.cursor.execute('''
                        INSERT INTO migraciones (
                            año_inicio, lugar_origen_id, lugar_destino_id,
                            causa, num_migrantes, tipo_migracion, exito, llegaron, años_viaje
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (año_guerra, origen_id, destino_id, 'guerra',
                          num_migrantes, 'forzada', llegaron > num_migrantes * 0.5,
                          llegaron, random.randint(1, 3)))

                    migraciones_creadas += 1

        self.conn.commit()
        print(f"  ✅ {migraciones_creadas} migraciones simuladas")

    def simular_crimenes_justicia(self, año_inicio: int, año_fin: int):
        """Simula crímenes y sistema de justicia"""
        print(f"\n⚖️  Simulando crímenes {año_inicio}-{año_fin}...")

        # Seleccionar muestra de personas para crímenes
        self.cursor.execute('''
            SELECT id FROM personas
            WHERE año_nacimiento >= ? AND año_nacimiento <= ?
            ORDER BY RANDOM()
            LIMIT 500
        ''', (año_inicio - 50, año_fin))

        personas = [row[0] for row in self.cursor.fetchall()]

        tipos_crimen = ['robo', 'asesinato', 'traicion', 'herejia', 'desercion', 'contrabando']
        gravedades = ['leve', 'grave', 'capital']

        crimenes_creados = 0

        for persona_id in personas:
            # 5% comete algún crimen
            if random.random() < 0.05:
                año = random.randint(año_inicio, año_fin)
                tipo = random.choice(tipos_crimen)
                gravedad = random.choice(gravedades)

                self.cursor.execute('''
                    INSERT INTO crimenes (
                        criminal_id, año_crimen, tipo_crimen, gravedad, descubierto
                    ) VALUES (?, ?, ?, ?, ?)
                ''', (persona_id, año, tipo, gravedad, random.random() < 0.6))  # 60% descubiertos

                crimenes_creados += 1

        self.conn.commit()
        print(f"  ✅ {crimenes_creados} crímenes simulados")

    def ejecutar_simulacion_completa(self):
        """Ejecuta simulación de todos los sistemas adicionales"""
        print("="*70)
        print("SIMULACIÓN DE SISTEMAS ADICIONALES")
        print("1500 → 3000 (1500 años)")
        print("="*70)

        inicio = datetime.now()

        # Aplicar schemas
        self.aplicar_todos_schemas()

        # Inicializar
        self.inicializar_sistemas()

        # Simulaciones
        self.simular_ciclos_climaticos(1500, 3000)
        self.simular_eventos_divinos(1500, 3000)
        self.simular_migraciones(1500, 3000)
        self.simular_crimenes_justicia(1500, 3000)

        # Mutaciones (si disponible)
        try:
            print(f"\n🧬 Simulando mutaciones...")
            import sistema_mutaciones
            gen_mut = sistema_mutaciones.GeneradorMutaciones()
            gen_mut.simular_mutaciones_poblacion(1500, 3000)
        except:
            print("⚠️  Mutaciones no simuladas")

        # Matrimonios inter-especies (si disponible)
        try:
            print(f"\n💍 Simulando matrimonios inter-especies...")
            import sistema_matrimonios_interespecie
            gen_hib = sistema_matrimonios_interespecie.GeneradorHibridos()
            gen_hib.simular_matrimonios_interespecie(1500, 3000)
        except:
            print("⚠️  Matrimonios inter-especies no simulados")

        fin = datetime.now()
        duracion = fin - inicio

        print("\n" + "="*70)
        print("✅ SIMULACIÓN DE SISTEMAS ADICIONALES COMPLETADA")
        print("="*70)
        print(f"Duración: {duracion}")

        self.conn.close()

def main():
    """Función principal"""
    print("\n⚠️  Este script simula los sistemas adicionales")
    print("⚠️  Asegúrate de haber ejecutado la simulación principal primero")
    print()

    respuesta = input("¿Continuar? (s/n): ").strip().lower()

    if respuesta == 's':
        sim = SistemasAdicionales()
        sim.ejecutar_simulacion_completa()
    else:
        print("❌ Cancelado")

if __name__ == '__main__':
    main()
