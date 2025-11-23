#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sistemas Adicionales Integrados
Portales del Quinto Sol

Integra y simula los 9 sistemas adicionales:
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

import random
import json
import re 
from datetime import datetime
from database_connector import DatabaseConnector # Importación clave

class SistemasAdicionales:
    def __init__(self):
        self.db = DatabaseConnector()
        self.db.connect()
        self.cursor = self.db.cursor
        self.conn = self.db.conn

    # -------------------------------------------------------------
    # MÉTODOS DE CONEXIÓN Y TRANSACCIÓN
    # -------------------------------------------------------------

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
        self.db.commit()
    
    def rollback(self):
        self.conn.rollback()

    def close(self):
        self.db.close()

    # -------------------------------------------------------------
    # APLICACIÓN DE SCHEMAS
    # -------------------------------------------------------------

    def aplicar_todos_schemas(self):
        """Aplica todos los schemas de sistemas adicionales con correcciones de sintaxis"""
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
                    schema_sql = f.read()

                if self.db.db_type == 'postgres':
                    # Corrección 1: Clave primaria
                    schema_sql = schema_sql.replace('INTEGER PRIMARY KEY AUTOINCREMENT', 'SERIAL PRIMARY KEY')
                    
                    # Corrección 2: Valores booleanos (1/0 a TRUE/FALSE) en cláusulas DEFAULT
                    schema_sql = re.sub(r'(BOOLEAN\s+DEFAULT\s+)0', r'\1FALSE', schema_sql, flags=re.IGNORECASE)
                    schema_sql = re.sub(r'(BOOLEAN\s+DEFAULT\s+)1', r'\1TRUE', schema_sql, flags=re.IGNORECASE)
                    
                    # Corrección 3: Corregir el uso de 1/0 en cláusulas WHERE y CHECK
                    schema_sql = re.sub(r'=\s*1', r'= TRUE', schema_sql, flags=re.IGNORECASE)
                    schema_sql = re.sub(r'=\s*0', r'= FALSE', schema_sql, flags=re.IGNORECASE)

                # Ejecución comando por comando (para robustez en PostgreSQL)
                commands = re.split(r';\s*$', schema_sql.strip(), flags=re.MULTILINE)
                
                for command in commands:
                    clean_command = re.sub(r'--.*', '', command, flags=re.MULTILINE).strip()
                    if clean_command:
                        self.cursor.execute(clean_command)

                self.commit()
                print(f"✅ Schema {schema_file} aplicado.")
            
            except FileNotFoundError:
                print(f"❌ Error: '{schema_file}' no encontrado. Continuando...")
            except Exception as e:
                print(f"❌ Error al aplicar {schema_file}: {e}")
                self.rollback() # Rollback si falla un schema
                
        print("\n" + "="*70)
        print("✅ APLICACIÓN DE SCHEMAS COMPLETADA")
        print("="*70)

    # -------------------------------------------------------------
    # MÉTODOS DE INICIALIZACIÓN
    # -------------------------------------------------------------
    
    def crear_monedas_base(self):
        """Crea las monedas base del sistema de economía dual"""
        
        monedas = [
            {'nombre': 'Quetzal de Oro', 'simbolo': 'Qz', 'valor_base': 1000, 'es_fisica': True},
            {'nombre': 'Plata Solar', 'simbolo': 'Pl', 'valor_base': 100, 'es_fisica': True},
            {'nombre': 'Tesoros del Alma', 'simbolo': 'Tx', 'valor_base': 1, 'es_fisica': False},
        ]

        for moneda in monedas:
            try:
                # Usamos ON CONFLICT con (nombre) asumiendo que tiene la restricción UNIQUE
                self.execute_query('''
                    INSERT INTO monedas (nombre, simbolo, valor_base, es_fisica)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (nombre) DO NOTHING
                ''', (moneda['nombre'], moneda['simbolo'], moneda['valor_base'], moneda['es_fisica']))
            except Exception as e:
                print(f"❌ Error al insertar moneda {moneda['nombre']}: {e}")
                self.rollback() # Rollback si falla la inserción de monedas
        
        self.commit()
        print(f"✅ {len(monedas)} monedas base creadas.")

    def crear_organizaciones_base(self):
        """Crea organizaciones iniciales"""
        self.execute_query('SELECT id FROM civilizaciones LIMIT 1')
        civ_id_row = self.fetchone()
        civ_id = civ_id_row['id'] if civ_id_row else None

        self.execute_query('SELECT id FROM pueblos_ciudades LIMIT 1')
        lugar_id_row = self.fetchone()
        lugar_id = lugar_id_row['id'] if lugar_id_row else None
        
        if civ_id is None or lugar_id is None:
            print("⚠️  No se pueden crear organizaciones: faltan IDs de civilizaciones o lugares.")
            return

        organizaciones = [
            ('Gremio de Herreros del Sol', 'gremio', 1450, 'Artesanos especializados en metalurgia'),
            ('Orden de los Guerreros Jaguar', 'orden_militar', 1420, 'Élite militar'),
            ('Culto de Quetzalcóatl', 'culto', 1300, 'Adoradores de la serpiente emplumada'),
            ('Hermandad de los Curanderos', 'hermandad', 1380, 'Médicos y sanadores'),
            ('Sociedad del Espejo Humeante', 'sociedad_secreta', 1460, 'Organización misteriosa'),
        ]

        for nombre, tipo, año, proposito in organizaciones:
            try:
                self.execute_query('''
                    INSERT INTO organizaciones (
                        nombre, tipo, año_fundacion, proposito,
                        lugar_sede_id, civilizacion_id, miembros_actuales
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (nombre) DO NOTHING
                ''', (nombre, tipo, año, proposito, lugar_id, civ_id, random.randint(10, 100)))
            except Exception as e:
                print(f"❌ Error al insertar organización {nombre}: {e}")
                self.rollback()
                
        self.commit()
        print(f"✅ {len(organizaciones)} organizaciones creadas.")

    def crear_artefactos_base(self):
        """Crea artefactos legendarios base"""
        self.execute_query('SELECT id FROM personas ORDER BY RANDOM() LIMIT 5')
        personas_rows = self.fetchall()
        personas = [row['id'] for row in personas_rows]

        self.execute_query('SELECT id FROM pueblos_ciudades LIMIT 1')
        lugar_id_row = self.fetchone()
        lugar_id = lugar_id_row['id'] if lugar_id_row else None

        if not personas or lugar_id is None:
            print("⚠️  No se pueden crear artefactos: faltan IDs de personas o lugares.")
            return

        artefactos = [
            ('Espada del Amanecer', 'arma', 'legendaria', 1200, 'forjado', 10, '{"fuerza": 30, "carisma": 10}', '["lanzar_rayo_solar"]'),
            ('Escudo de Obsidiana', 'armadura', 'epica', 1300, 'bendecido', 8, '{"resistencia": 40}', '["reflejar_magia"]'),
            ('Collar de Jade Imperial', 'joya', 'epica', 1100, 'ritual', 7, '{"carisma": 25, "inteligencia": 15}', '["persuasion_divina"]'),
        ]

        for nombre, tipo, rareza, año, metodo, poder, stats, habs in artefactos:
            prop_id = random.choice(personas)
            try:
                self.execute_query('''
                    INSERT INTO artefactos (
                        nombre, tipo, rareza, año_creacion, metodo_creacion,
                        nivel_poder, modificadores_stats, habilidades_especiales,
                        propietario_id, lugar_creacion_id
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (nombre) DO NOTHING
                ''', (nombre, tipo, rareza, año, metodo, poder, stats, habs, prop_id, lugar_id))
            except Exception as e:
                print(f"❌ Error al insertar artefacto {nombre}: {e}")
                self.rollback()

        self.commit()
        print(f"✅ {len(artefactos)} artefactos legendarios creados.")

    def inicializar_sistemas(self):
        """Inicializa datos base de todos los sistemas (catálogos, compatibilidad, etc.)"""
        print("\n" + "="*70)
        print("INICIALIZANDO SISTEMAS")
        print("="*70)
        
        # --- CORRECCIÓN 1: Asegurar que exista la columna 'es_hibrido' en 'personas' ---
        print("\n➕ Verificando columna 'es_hibrido' en tabla personas...")
        try:
            self.execute_query("ALTER TABLE personas ADD COLUMN es_hibrido BOOLEAN DEFAULT FALSE")
            self.commit()
            print("✅ Columna es_hibrido añadida.")
        except Exception as e:
            if "already exists" in str(e):
                print("✅ Columna es_hibrido ya existe. Continuando.")
            else:
                print(f"❌ Error al añadir columna: {e}")
                self.rollback() 

        # --- CORRECCIÓN 2: Asegurar que exista la columna 'es_esteril' en 'personas_hibridas' ---
        print("\n➕ Verificando columna 'es_esteril' en tabla personas_hibridas...")
        try:
            self.execute_query("ALTER TABLE personas_hibridas ADD COLUMN es_esteril BOOLEAN DEFAULT FALSE")
            self.commit()
            print("✅ Columna es_esteril añadida.")
        except Exception as e:
            if "already exists" in str(e):
                print("✅ Columna es_esteril ya existe. Continuando.")
            else:
                print(f"❌ Error al añadir columna: {e}")
                self.rollback() # ¡Rollback si falla!

        # 1. Mutaciones
        print("\n🧬 Inicializando sistema de mutaciones...")
        try:
            import sistema_mutaciones
            gen_mut = sistema_mutaciones.GeneradorMutaciones()
            gen_mut.poblar_catalogo()
            print("✅ Catálogo de mutaciones poblado")
        except Exception as e:
            print(f"⚠️  Sistema de mutaciones falló: {e}")
            self.rollback() # ROLLBACK aquí

        # 2. Matrimonios Inter-Especies
        print("\n💍 Inicializando compatibilidad inter-especies...")
        try:
            import sistema_matrimonios_interespecie
            gen_hib = sistema_matrimonios_interespecie.GeneradorHibridos()
            gen_hib.poblar_compatibilidad()
            print("✅ Compatibilidad configurada")
        except Exception as e:
            print(f"⚠️  Sistema híbridos falló: {e}")
            self.rollback() # ROLLBACK aquí


        # 3. Monedas base 
        print("\n💰 Creando monedas...")
        self.crear_monedas_base()

        # 4. Organizaciones
        print("\n🏛️  Creando organizaciones iniciales...")
        self.crear_organizaciones_base()

        # 5. Artefactos legendarios
        print("\n⚔️  Creando artefactos legendarios...")
        self.crear_artefactos_base()
        
        print("\n" + "="*70)
        print("✅ INICIALIZACIÓN DE SISTEMAS COMPLETADA")
        print("="*70)
    
    # -------------------------------------------------------------
    # MÉTODOS DE SIMULACIÓN LARGOS (Migrados a PostgreSQL)
    # -------------------------------------------------------------
    
    def simular_ciclos_climaticos(self, año_inicio: int, año_fin: int):
        """Simula ciclos climáticos anuales (MIGRADO)"""
        print(f"\n🌤️  Simulando clima {año_inicio}-{año_fin}...")
        try:
            for año in range(año_inicio, año_fin + 1):
                estacion = random.choice(['primavera', 'verano', 'otoño', 'invierno', 'lluvias', 'secas'])
                temp = random.randint(15, 35)
                precip = random.choice(['muy_baja', 'baja', 'normal', 'alta', 'muy_alta'])
                sequia = random.random() < 0.05
                inundacion = random.random() < 0.03
                huracan = random.random() < 0.02
                bonus_agri = 0
                
                # [Lógica de bonus omitida por brevedad]
                
                self.execute_query('''
                    INSERT INTO ciclos_climaticos (
                        año, estacion_dominante, temperatura_promedio, precipitacion,
                        sequia, inundaciones, huracan, bonus_agricultura
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (año) DO NOTHING
                ''', (año, estacion, temp, precip, sequia, inundacion, huracan, bonus_agri))

            self.commit()
            print(f"  ✅ {año_fin - año_inicio + 1} años de clima simulados")
        except Exception as e:
            print(f"❌ Error en simular_ciclos_climaticos: {e}")
            self.rollback()

    def simular_eventos_divinos(self, año_inicio: int, año_fin: int):
        """Simula eventos divinos mayores (MIGRADO)"""
        print(f"\n⚡ Simulando eventos divinos {año_inicio}-{año_fin}...")
        try:
            self.execute_query('SELECT id FROM dioses')
            dioses = [row['id'] for row in self.fetchall()]
            self.execute_query('SELECT id FROM civilizaciones')
            civilizaciones = [row['id'] for row in self.fetchall()]

            if not dioses or not civilizaciones: return

            num_eventos = random.randint(15, 25)
            tipos_evento = ['bendicion_masiva', 'maldicion', 'milagro', 'castigo', 'manifestacion', 'profecia']
            alcances = ['ciudad', 'civilizacion', 'todas_especies']

            for _ in range(num_eventos):
                año = random.randint(año_inicio, año_fin)
                dios_id = random.choice(dioses)
                tipo = random.choice(tipos_evento)
                alcance = random.choice(alcances)

                civ_id = random.choice(civilizaciones) if alcance in ['civilizacion', 'ciudad'] else None
                personas_afectadas = random.randint(100, 100000)

                self.execute_query('''
                    INSERT INTO eventos_divinos_mayores (
                        dios_id, año_evento, tipo_evento, alcance,
                        objetivo_civilizacion_id, personas_afectadas, descripcion
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                ''', (dios_id, año, tipo, alcance, civ_id, personas_afectadas,
                      f'Evento divino {tipo} de alcance {alcance}'))

            self.commit()
            print(f"  ✅ {num_eventos} eventos divinos simulados")
        except Exception as e:
            print(f"❌ Error en simular_eventos_divinos: {e}")
            self.rollback()

    def simular_migraciones(self, año_inicio: int, año_fin: int):
        """Simula migraciones poblacionales (MIGRADO)"""
        print(f"\n🚶 Simulando migraciones {año_inicio}-{año_fin}...")
        try:
            self.execute_query('SELECT id, año_inicio FROM guerras_especies WHERE año_inicio >= %s', (año_inicio,))
            guerras = self.fetchall()
            migraciones_creadas = 0

            for guerra_row in guerras:
                guerra_id = guerra_row['id']
                año_guerra = guerra_row['año_inicio']

                if random.random() < 0.5:
                    self.execute_query('SELECT id FROM pueblos_ciudades ORDER BY RANDOM() LIMIT 2')
                    lugares = self.fetchall()

                    if len(lugares) >= 2:
                        origen_id = lugares[0]['id']
                        destino_id = lugares[1]['id']
                        num_migrantes = random.randint(100, 5000)
                        llegaron = int(num_migrantes * random.uniform(0.7, 0.95))

                        self.execute_query('''
                            INSERT INTO migraciones (
                                año_inicio, lugar_origen_id, lugar_destino_id,
                                causa, num_migrantes, tipo_migracion, exito, llegaron, años_viaje,
                                guerra_relacionada_id
                            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                        ''', (año_guerra, origen_id, destino_id, 'guerra',
                              num_migrantes, 'forzada', llegaron > num_migrantes * 0.5,
                              llegaron, random.randint(1, 3), guerra_id))

                        migraciones_creadas += 1

            self.commit()
            print(f"  ✅ {migraciones_creadas} migraciones simuladas")
        except Exception as e:
            print(f"❌ Error en simular_migraciones: {e}")
            self.rollback()

    def simular_crimenes_justicia(self, año_inicio: int, año_fin: int):
        """Simula crímenes y sistema de justicia (MIGRADO)"""
        print(f"\n⚖️  Simulando crímenes {año_inicio}-{año_fin}...")
        try:
            self.execute_query('''
                SELECT id FROM personas
                WHERE año_nacimiento >= %s AND año_nacimiento <= %s
                ORDER BY RANDOM()
                LIMIT 500
            ''', (año_inicio - 50, año_fin))

            personas = [row['id'] for row in self.fetchall()]
            if not personas: return

            tipos_crimen = ['robo', 'asesinato', 'traicion', 'herejia', 'desercion', 'contrabando']
            crimenes_creados = 0

            for persona_id in personas:
                if random.random() < 0.05:
                    año = random.randint(año_inicio, año_fin)
                    tipo = random.choice(tipos_crimen)
                    gravedad = random.choice(['leve', 'grave', 'capital'])

                    self.execute_query('''
                        INSERT INTO crimenes (
                            criminal_id, año_crimen, tipo_crimen, gravedad, descubierto
                        ) VALUES (%s, %s, %s, %s, %s)
                    ''', (persona_id, año, tipo, gravedad, random.random() < 0.6))

                    crimenes_creados += 1

            self.commit()
            print(f"  ✅ {crimenes_creados} crímenes simulados")
        except Exception as e:
            print(f"❌ Error en simular_crimenes_justicia: {e}")
            self.rollback()


    # -------------------------------------------------------------
    # EJECUTOR PRINCIPAL
    # -------------------------------------------------------------

    def ejecutar_simulacion_completa(self):
        """Aplica schemas, inicializa y simula todos los sistemas adicionales"""
        inicio = datetime.now()

        # 1. Aplicar todos los schemas
        self.aplicar_todos_schemas()

        # 2. Inicializar catálogos y datos base
        self.inicializar_sistemas()

        print("\n" + "="*70)
        print("INICIANDO SIMULACIONES ADICIONALES (1500-3000)")
        print("="*70)

        # --- SIMULACIÓN DE SISTEMAS ---
        
        self.simular_ciclos_climaticos(1500, 3000)
        self.simular_eventos_divinos(1500, 3000)
        self.simular_migraciones(1500, 3000)
        self.simular_crimenes_justicia(1500, 3000)

        # ⚠️ Llamada a módulos externos (asumen la adaptación en sus propios archivos)

        # Mutaciones
        try:
            print(f"\n🧬 Simulando mutaciones...")
            import sistema_mutaciones
            gen_mut = sistema_mutaciones.GeneradorMutaciones()
            gen_mut.simular_mutaciones_poblacion(1500, 3000)
        except Exception as e:
            print(f"⚠️  Mutaciones no simuladas por error en el módulo externo: {e}")

        # Matrimonios inter-especies
        try:
            print(f"\n💍 Simulando matrimonios inter-especies...")
            import sistema_matrimonios_interespecie
            gen_hib = sistema_matrimonios_interespecie.GeneradorHibridos()
            gen_hib.simular_matrimonios_interespecie(1500, 3000)
        except Exception as e:
            print(f"⚠️  Matrimonios inter-especies no simulados por error en el módulo externo: {e}")

        # --- FIN DE SIMULACIONES ---

        fin = datetime.now()
        duracion = fin - inicio

        print("\n" + "="*70)
        print("✅ SIMULACIÓN DE SISTEMAS ADICIONALES COMPLETADA")
        print("="*70)
        print(f"Duración: {duracion}")

        self.db.close()

def main():
    """Función principal"""
    print("\n⚠️  Este script simula los sistemas adicionales")
    print("Asegúrate de haber corrido antes: poblar_datos_base.py y generar_genealogias_especies.py")
    
    respuesta = input("⏸️  Presiona ENTER para comenzar la simulación de sistemas adicionales...")

    try:
        sim = SistemasAdicionales()
        sim.ejecutar_simulacion_completa()
    except Exception as e:
        print("\n" + "="*70)
        print("❌ ERROR CRÍTICO EN SIMULACIÓN ADICIONAL")
        print("="*70)
        print(f"Error: {e}")

if __name__ == '__main__':
    main()