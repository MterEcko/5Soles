#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIMULACIÓN COMPLETA DEL MUNDO - 1500 a 3000
Portales del Quinto Sol - MMORPG

Este script ejecuta la simulación completa integrando todos los sistemas:
1. Relaciones especies-civilizaciones-dioses
2. Genealogías humanas (Humanos I)
3. Genealogías especies sirvientes (5 especies, 300 años longevidad)
4. Sistema de longevidad por oficio (humanos hasta 200 años)
5. Guerras inter-especies

IMPORTANTE: Asegúrate de tener una copia de seguridad de la base de datos
antes de ejecutar esta simulación completa.
"""

import sqlite3
import subprocess
import sys
import os
from datetime import datetime

DB_PATH = 'quinto_sol.db'

class SimulacionMaestra:
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self.log_file = f"simulacion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    def log(self, mensaje):
        """Registra mensaje en consola y archivo"""
        print(mensaje)
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {mensaje}\n")

    def backup_database(self):
        """Crea backup de la base de datos"""
        self.log("\n" + "="*70)
        self.log("PASO 0: BACKUP DE BASE DE DATOS")
        self.log("="*70)

        backup_name = f"quinto_sol_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"

        try:
            import shutil
            shutil.copy2(DB_PATH, backup_name)
            self.log(f"✅ Backup creado: {backup_name}")
            return True
        except Exception as e:
            self.log(f"❌ Error creando backup: {e}")
            return False

    def verificar_prerequisitos(self):
        """Verifica que todos los scripts necesarios existan"""
        self.log("\n" + "="*70)
        self.log("VERIFICACIÓN DE PREREQUISITOS")
        self.log("="*70)

        scripts_requeridos = [
            'poblar_relaciones_especies_civilizaciones.py',
            'generar_poblacion.py',
            'generar_genealogias_especies.py',
            'sistema_longevidad_oficios.py',
            'sistema_guerras_especies.py'
        ]

        schemas_requeridos = [
            'schema_relaciones_especies_civilizaciones.sql',
            'schema_guerras_especies.sql'
        ]

        todos_existen = True

        for script in scripts_requeridos:
            if os.path.exists(script):
                self.log(f"  ✅ {script}")
            else:
                self.log(f"  ❌ {script} NO ENCONTRADO")
                todos_existen = False

        for schema in schemas_requeridos:
            if os.path.exists(schema):
                self.log(f"  ✅ {schema}")
            else:
                self.log(f"  ❌ {schema} NO ENCONTRADO")
                todos_existen = False

        return todos_existen

    def limpiar_datos_previos(self):
        """Limpia datos de simulaciones previas (opcional)"""
        self.log("\n" + "="*70)
        self.log("LIMPIEZA DE DATOS PREVIOS")
        self.log("="*70)

        respuesta = input("\n⚠️  ¿Eliminar genealogías y guerras previas? (s/n): ").strip().lower()

        if respuesta != 's':
            self.log("❌ Limpieza cancelada")
            return False

        try:
            # Eliminar solo humanos y especies sirvientes generados
            self.log("  Eliminando humanos y especies previas...")

            # Obtener especies a limpiar
            self.cursor.execute("SELECT id FROM especies WHERE nombre != 'Humanos II'")
            especies_ids = [row[0] for row in self.cursor.fetchall()]

            if especies_ids:
                placeholders = ','.join('?' * len(especies_ids))
                self.cursor.execute(f"DELETE FROM personas WHERE especie_id IN ({placeholders})", especies_ids)
                personas_eliminadas = self.cursor.rowcount
                self.log(f"    ✓ {personas_eliminadas} personas eliminadas")

            # Limpiar guerras
            self.cursor.execute("DELETE FROM guerras_especies")
            guerras_eliminadas = self.cursor.rowcount
            self.log(f"    ✓ {guerras_eliminadas} guerras eliminadas")

            self.cursor.execute("DELETE FROM escaramuzas_especies")
            escaramuzas_eliminadas = self.cursor.rowcount
            self.log(f"    ✓ {escaramuzas_eliminadas} escaramuzas eliminadas")

            self.conn.commit()
            self.log("✅ Limpieza completada")
            return True

        except Exception as e:
            self.log(f"❌ Error en limpieza: {e}")
            self.conn.rollback()
            return False

    def paso_1_relaciones_especies(self):
        """Paso 1: Crear relaciones especies-civilizaciones-dioses"""
        self.log("\n" + "="*70)
        self.log("PASO 1: RELACIONES ESPECIES-CIVILIZACIONES-DIOSES")
        self.log("="*70)

        try:
            result = subprocess.run(
                ['python3', 'poblar_relaciones_especies_civilizaciones.py'],
                capture_output=True,
                text=True,
                timeout=300
            )

            if result.returncode == 0:
                self.log(result.stdout)
                self.log("✅ Paso 1 completado")
                return True
            else:
                self.log(f"❌ Error: {result.stderr}")
                return False

        except Exception as e:
            self.log(f"❌ Excepción: {e}")
            return False

    def paso_2_genealogias_especies(self):
        """Paso 2: Generar genealogías de especies sirvientes"""
        self.log("\n" + "="*70)
        self.log("PASO 2: GENEALOGÍAS ESPECIES SIRVIENTES (300 años)")
        self.log("="*70)

        self.log("⚠️  Este paso puede tardar varios minutos...")

        try:
            # Ejecutar generador de especies sin interacción
            # Necesitamos modificar el script para modo no interactivo
            result = subprocess.run(
                ['python3', '-c', '''
import sys
sys.path.insert(0, ".")
from generar_genealogias_especies import GeneradorEspecies

generador = GeneradorEspecies()
poblaciones = {
    "Tlacatl de Luz": 150,
    "Sombra-Coyotes": 100,
    "Bio-Constructores": 180,
    "Acuátiles": 140,
    "Guerreros Solares": 200,
}

for especie, cantidad in poblaciones.items():
    generador.simular_especie_completa(especie, cantidad)

generador.conn.close()
print("✅ Genealogías especies completadas")
                '''],
                capture_output=True,
                text=True,
                timeout=3600  # 1 hora máximo
            )

            if result.returncode == 0:
                self.log(result.stdout)
                self.log("✅ Paso 2 completado")
                return True
            else:
                self.log(f"❌ Error: {result.stderr}")
                return False

        except subprocess.TimeoutExpired:
            self.log("❌ Timeout: La simulación tardó más de 1 hora")
            return False
        except Exception as e:
            self.log(f"❌ Excepción: {e}")
            return False

    def paso_3_genealogias_humanos(self):
        """Paso 3: Generar genealogías de humanos"""
        self.log("\n" + "="*70)
        self.log("PASO 3: GENEALOGÍAS HUMANOS (200 años)")
        self.log("="*70)

        self.log("⚠️  Este paso puede tardar bastante tiempo (30+ minutos)...")
        self.log("⚠️  Se recomienda ejecutar generar_poblacion.py manualmente")

        ejecutar = input("\n¿Ejecutar ahora? (s/n): ").strip().lower()

        if ejecutar != 's':
            self.log("⏭️  Paso omitido (ejecutar manualmente después)")
            return True

        try:
            # Este script es muy largo, mejor ejecutarlo manualmente
            self.log("❌ Por favor ejecuta generar_poblacion.py manualmente")
            self.log("   python3 generar_poblacion.py")
            return True

        except Exception as e:
            self.log(f"❌ Excepción: {e}")
            return False

    def paso_4_longevidad_oficios(self):
        """Paso 4: Actualizar longevidad por oficios"""
        self.log("\n" + "="*70)
        self.log("PASO 4: LONGEVIDAD POR OFICIO")
        self.log("="*70)

        try:
            result = subprocess.run(
                ['python3', '-c', '''
import sys
sys.path.insert(0, ".")
from sistema_longevidad_oficios import CalculadorLongevidad

calculador = CalculadorLongevidad()
calculador.actualizar_longevidad_masiva()
calculador.conn.close()
print("✅ Longevidad actualizada")
                '''],
                capture_output=True,
                text=True,
                timeout=600
            )

            if result.returncode == 0:
                self.log(result.stdout)
                self.log("✅ Paso 4 completado")
                return True
            else:
                self.log(f"❌ Error: {result.stderr}")
                return False

        except Exception as e:
            self.log(f"❌ Excepción: {e}")
            return False

    def paso_5_guerras_especies(self):
        """Paso 5: Simular guerras inter-especies"""
        self.log("\n" + "="*70)
        self.log("PASO 5: GUERRAS INTER-ESPECIES (1500-3000)")
        self.log("="*70)

        try:
            result = subprocess.run(
                ['python3', '-c', '''
import sys
sys.path.insert(0, ".")
from sistema_guerras_especies import GeneradorGuerras

generador = GeneradorGuerras()
generador.aplicar_schema()
generador.simular_guerras_periodo(1500, 3000)
generador.generar_reporte_guerras()
generador.conn.close()
print("✅ Guerras simuladas")
                '''],
                capture_output=True,
                text=True,
                timeout=600
            )

            if result.returncode == 0:
                self.log(result.stdout)
                self.log("✅ Paso 5 completado")
                return True
            else:
                self.log(f"❌ Error: {result.stderr}")
                return False

        except Exception as e:
            self.log(f"❌ Excepción: {e}")
            return False

    def resumen_final(self):
        """Genera resumen final de la simulación"""
        self.log("\n" + "="*70)
        self.log("RESUMEN FINAL DE LA SIMULACIÓN")
        self.log("="*70)

        try:
            # Total personas por especie
            self.cursor.execute('''
                SELECT e.nombre, COUNT(p.id)
                FROM especies e
                LEFT JOIN personas p ON e.id = p.especie_id
                GROUP BY e.nombre
                ORDER BY COUNT(p.id) DESC
            ''')

            self.log("\n📊 POBLACIÓN POR ESPECIE:")
            for nombre, cantidad in self.cursor.fetchall():
                self.log(f"  {nombre:25s}: {cantidad:8d} individuos")

            # Total guerras
            self.cursor.execute('SELECT COUNT(*) FROM guerras_especies')
            total_guerras = self.cursor.fetchone()[0]

            self.cursor.execute('SELECT COUNT(*) FROM escaramuzas_especies')
            total_escaramuzas = self.cursor.fetchone()[0]

            self.log(f"\n⚔️  CONFLICTOS:")
            self.log(f"  Guerras: {total_guerras}")
            self.log(f"  Escaramuzas: {total_escaramuzas}")

            # Total relaciones
            self.cursor.execute('SELECT COUNT(*) FROM especies_civilizaciones')
            total_relaciones = self.cursor.fetchone()[0]

            self.cursor.execute('SELECT COUNT(*) FROM diplomacia_especies')
            total_diplomacia = self.cursor.fetchone()[0]

            self.log(f"\n🤝 DIPLOMACIA:")
            self.log(f"  Relaciones especies-civilizaciones: {total_relaciones}")
            self.log(f"  Relaciones diplomáticas: {total_diplomacia}")

            self.log(f"\n📋 Log guardado en: {self.log_file}")

        except Exception as e:
            self.log(f"❌ Error generando resumen: {e}")

    def ejecutar_simulacion_completa(self):
        """Ejecuta toda la simulación en orden"""
        self.log("="*70)
        self.log("SIMULACIÓN COMPLETA DEL MUNDO")
        self.log("Portales del Quinto Sol")
        self.log("1500 → 3000 (1500 años)")
        self.log("="*70)

        inicio = datetime.now()

        # Paso 0: Backup
        if not self.backup_database():
            self.log("❌ No se pudo crear backup. Abortando.")
            return False

        # Verificar prerequisitos
        if not self.verificar_prerequisitos():
            self.log("❌ Faltan archivos necesarios. Abortando.")
            return False

        # Limpieza opcional
        self.limpiar_datos_previos()

        # Paso 1: Relaciones
        if not self.paso_1_relaciones_especies():
            self.log("❌ Error en Paso 1. Abortando.")
            return False

        # Paso 2: Genealogías especies
        if not self.paso_2_genealogias_especies():
            self.log("❌ Error en Paso 2. Continuar? (s/n): ")
            if input().strip().lower() != 's':
                return False

        # Paso 3: Genealogías humanos (manual)
        self.paso_3_genealogias_humanos()

        # Paso 4: Longevidad
        if not self.paso_4_longevidad_oficios():
            self.log("❌ Error en Paso 4. Continuar? (s/n): ")
            if input().strip().lower() != 's':
                return False

        # Paso 5: Guerras
        if not self.paso_5_guerras_especies():
            self.log("❌ Error en Paso 5. Continuar? (s/n): ")
            if input().strip().lower() != 's':
                return False

        # Resumen
        self.resumen_final()

        fin = datetime.now()
        duracion = fin - inicio

        self.log("\n" + "="*70)
        self.log("✅ SIMULACIÓN COMPLETADA")
        self.log("="*70)
        self.log(f"Duración total: {duracion}")
        self.log(f"Log completo: {self.log_file}")

        self.conn.close()
        return True

def main():
    simulacion = SimulacionMaestra()

    print("\n⚠️  ADVERTENCIA: Esta simulación puede tardar varias horas.")
    print("⚠️  Asegúrate de tener suficiente espacio en disco y tiempo.")
    print()

    respuesta = input("¿Continuar con la simulación completa? (s/n): ").strip().lower()

    if respuesta == 's':
        simulacion.ejecutar_simulacion_completa()
    else:
        print("❌ Simulación cancelada")

if __name__ == '__main__':
    main()
