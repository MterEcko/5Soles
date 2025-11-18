#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Migración SQLite → PostgreSQL
Portales del Quinto Sol

Migra datos desde SQLite a PostgreSQL manteniendo integridad referencial.
"""

import sqlite3
import sys
from datetime import datetime
from typing import List, Dict, Tuple

try:
    import psycopg2
    from psycopg2.extras import execute_batch
except ImportError:
    print("❌ psycopg2 no instalado")
    print("   Instalar con: pip install psycopg2-binary")
    sys.exit(1)

# Configuración
SQLITE_DB = 'quinto_sol.db'

# PostgreSQL config (ajustar según tu configuración)
PG_CONFIG = {
    'host': 'localhost',
    'port': 5432,
    'database': 'quinto_sol',
    'user': 'quinto_sol_user',
    'password': 'tu_password'  # CAMBIAR
}


class MigradorSQLitePostgres:
    """Migra datos de SQLite a PostgreSQL"""

    def __init__(self, sqlite_path: str, pg_config: Dict):
        self.sqlite_path = sqlite_path
        self.pg_config = pg_config

        # Conexiones
        self.sqlite_conn = None
        self.pg_conn = None

        # Estadísticas
        self.stats = {
            'tablas_migradas': 0,
            'registros_migrados': 0,
            'errores': 0
        }

    def conectar(self):
        """Establece conexiones a ambas bases de datos"""
        print("\n🔌 Conectando a bases de datos...")

        # SQLite
        try:
            self.sqlite_conn = sqlite3.connect(self.sqlite_path)
            self.sqlite_conn.row_factory = sqlite3.Row
            print(f"✅ SQLite conectado: {self.sqlite_path}")
        except Exception as e:
            print(f"❌ Error conectando a SQLite: {e}")
            sys.exit(1)

        # PostgreSQL
        try:
            self.pg_conn = psycopg2.connect(**self.pg_config)
            print(f"✅ PostgreSQL conectado: {self.pg_config['user']}@{self.pg_config['host']}/{self.pg_config['database']}")
        except Exception as e:
            print(f"❌ Error conectando a PostgreSQL: {e}")
            print("\nVerifica:")
            print("  1. PostgreSQL está corriendo")
            print("  2. Base de datos existe")
            print("  3. Usuario y password correctos")
            print("  4. Permisos otorgados")
            sys.exit(1)

    def obtener_tablas(self) -> List[str]:
        """Obtiene lista de tablas de SQLite"""
        cursor = self.sqlite_conn.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        return [row[0] for row in cursor.fetchall()]

    def obtener_columnas(self, tabla: str) -> List[str]:
        """Obtiene nombres de columnas de una tabla"""
        cursor = self.sqlite_conn.cursor()
        cursor.execute(f"PRAGMA table_info({tabla})")
        return [row[1] for row in cursor.fetchall()]

    def convertir_valor(self, valor):
        """Convierte valores de SQLite a PostgreSQL"""
        if valor is None:
            return None

        # Convertir booleanos (SQLite usa 0/1)
        if isinstance(valor, int) and valor in [0, 1]:
            # Podría ser boolean o int, dejar como está
            return valor

        return valor

    def migrar_tabla(self, tabla: str) -> Tuple[int, int]:
        """
        Migra una tabla completa

        Returns:
            (registros_migrados, registros_con_error)
        """
        print(f"\n📋 Migrando tabla: {tabla}")

        # Obtener datos de SQLite
        sqlite_cursor = self.sqlite_conn.cursor()
        sqlite_cursor.execute(f"SELECT * FROM {tabla}")

        rows = sqlite_cursor.fetchall()
        total_rows = len(rows)

        if total_rows == 0:
            print(f"   ⚠️  Tabla vacía, saltando")
            return 0, 0

        # Obtener nombres de columnas
        columnas = [description[0] for description in sqlite_cursor.description]

        print(f"   📊 {total_rows:,} registros encontrados")
        print(f"   📝 {len(columnas)} columnas: {', '.join(columnas[:5])}{'...' if len(columnas) > 5 else ''}")

        # Preparar INSERT para PostgreSQL
        placeholders = ', '.join(['%s'] * len(columnas))
        columns_str = ', '.join(columnas)
        insert_query = f"INSERT INTO {tabla} ({columns_str}) VALUES ({placeholders})"

        # Migrar en batches
        pg_cursor = self.pg_conn.cursor()
        batch_size = 1000
        migrados = 0
        errores = 0

        for i in range(0, total_rows, batch_size):
            batch = rows[i:i + batch_size]

            # Convertir valores
            batch_values = []
            for row in batch:
                valores = [self.convertir_valor(row[col]) for col in columnas]
                batch_values.append(tuple(valores))

            # Insertar batch
            try:
                execute_batch(pg_cursor, insert_query, batch_values)
                self.pg_conn.commit()

                migrados += len(batch)
                print(f"   ✅ {migrados:,}/{total_rows:,} migrados ({migrados*100//total_rows}%)")

            except Exception as e:
                print(f"   ❌ Error en batch {i}-{i+len(batch)}: {e}")
                errores += len(batch)

                # Rollback este batch
                self.pg_conn.rollback()

                # Intentar uno por uno para identificar problema
                for row in batch:
                    valores = [self.convertir_valor(row[col]) for col in columnas]
                    try:
                        pg_cursor.execute(insert_query, valores)
                        self.pg_conn.commit()
                        migrados += 1
                    except Exception as e2:
                        print(f"     ❌ Error en registro: {e2}")
                        self.pg_conn.rollback()

        return migrados, errores

    def verificar_schemas(self) -> bool:
        """Verifica que schemas de PostgreSQL existan"""
        print("\n🔍 Verificando schemas PostgreSQL...")

        pg_cursor = self.pg_conn.cursor()

        # Obtener tablas de PostgreSQL
        pg_cursor.execute("""
            SELECT tablename FROM pg_tables
            WHERE schemaname = 'public'
            ORDER BY tablename
        """)
        pg_tables = set(row[0] for row in pg_cursor.fetchall())

        # Obtener tablas de SQLite
        sqlite_tables = set(self.obtener_tablas())

        # Comparar
        faltantes = sqlite_tables - pg_tables

        if faltantes:
            print(f"\n⚠️  ADVERTENCIA: {len(faltantes)} tablas no existen en PostgreSQL:")
            for tabla in sorted(faltantes):
                print(f"   • {tabla}")

            print("\n❌ Ejecuta primero los schemas en PostgreSQL:")
            print("   Ejemplo:")
            print("   psql -U quinto_sol_user -d quinto_sol -f schema.sql")
            print("   psql -U quinto_sol_user -d quinto_sol -f schema_*.sql")

            return False

        print(f"✅ Todas las tablas existen en PostgreSQL ({len(sqlite_tables)} tablas)")
        return True

    def migrar_todo(self, verificar: bool = True):
        """Migra todas las tablas"""
        print("\n" + "=" * 70)
        print("MIGRACIÓN SQLITE → POSTGRESQL")
        print("=" * 70)

        inicio = datetime.now()

        # Conectar
        self.conectar()

        # Verificar schemas
        if verificar:
            if not self.verificar_schemas():
                print("\n❌ Migración cancelada")
                return

        # Obtener tablas
        tablas = self.obtener_tablas()
        print(f"\n📊 Total de tablas a migrar: {len(tablas)}")

        # Orden de migración (respetando foreign keys)
        # Tablas sin dependencias primero
        orden_preferido = [
            'especies', 'civilizaciones', 'dioses',
            'pueblos_ciudades', 'especies_civilizaciones',
            'personas', 'mutaciones_catalogo',
            'artefactos', 'organizaciones', 'monedas'
        ]

        # Ordenar tablas
        tablas_ordenadas = []
        for tabla in orden_preferido:
            if tabla in tablas:
                tablas_ordenadas.append(tabla)
                tablas.remove(tabla)

        # Añadir resto
        tablas_ordenadas.extend(sorted(tablas))

        print(f"\n📋 Orden de migración: {', '.join(tablas_ordenadas[:5])}...")

        # Confirmar
        respuesta = input("\n¿Continuar con migración? (s/n): ").strip().lower()
        if respuesta != 's':
            print("❌ Migración cancelada")
            return

        # Migrar cada tabla
        for i, tabla in enumerate(tablas_ordenadas, 1):
            print(f"\n[{i}/{len(tablas_ordenadas)}]", end=' ')

            migrados, errores = self.migrar_tabla(tabla)

            self.stats['tablas_migradas'] += 1
            self.stats['registros_migrados'] += migrados
            self.stats['errores'] += errores

        fin = datetime.now()
        duracion = fin - inicio

        # Resumen
        print("\n" + "=" * 70)
        print("✅ MIGRACIÓN COMPLETADA")
        print("=" * 70)
        print(f"\n📊 Estadísticas:")
        print(f"   • Tablas migradas: {self.stats['tablas_migradas']}")
        print(f"   • Registros migrados: {self.stats['registros_migrados']:,}")
        print(f"   • Errores: {self.stats['errores']}")
        print(f"   • Duración: {duracion}")

        # Verificar conteos
        print("\n🔍 Verificando conteos...")
        self.verificar_conteos(tablas_ordenadas)

    def verificar_conteos(self, tablas: List[str]):
        """Verifica que los conteos coincidan"""
        sqlite_cursor = self.sqlite_conn.cursor()
        pg_cursor = self.pg_conn.cursor()

        diferencias = []

        for tabla in tablas:
            # Contar en SQLite
            sqlite_cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
            count_sqlite = sqlite_cursor.fetchone()[0]

            # Contar en PostgreSQL
            pg_cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
            count_pg = pg_cursor.fetchone()[0]

            if count_sqlite != count_pg:
                diferencias.append((tabla, count_sqlite, count_pg))

        if diferencias:
            print("\n⚠️  Diferencias en conteos:")
            for tabla, sqlite_count, pg_count in diferencias:
                print(f"   • {tabla}: SQLite={sqlite_count:,}, PostgreSQL={pg_count:,}")
        else:
            print("✅ Todos los conteos coinciden")

    def cerrar(self):
        """Cierra conexiones"""
        if self.sqlite_conn:
            self.sqlite_conn.close()
        if self.pg_conn:
            self.pg_conn.close()

        print("\n✅ Conexiones cerradas")


def main():
    """Función principal"""
    print("\n" + "=" * 70)
    print("MIGRACIÓN SQLITE → POSTGRESQL")
    print("Portales del Quinto Sol")
    print("=" * 70)

    print("\n⚠️  IMPORTANTE:")
    print("   1. Asegúrate de haber creado la base de datos en PostgreSQL")
    print("   2. Asegúrate de haber aplicado todos los schemas")
    print("   3. Configura PG_CONFIG en este script")
    print("   4. Haz backup de tu base de datos SQLite")

    print(f"\n📁 SQLite DB: {SQLITE_DB}")
    print(f"🐘 PostgreSQL: {PG_CONFIG['user']}@{PG_CONFIG['host']}/{PG_CONFIG['database']}")

    # Crear migrador
    migrador = MigradorSQLitePostgres(SQLITE_DB, PG_CONFIG)

    try:
        migrador.migrar_todo(verificar=True)
    except KeyboardInterrupt:
        print("\n\n⚠️  Migración interrumpida por usuario")
    except Exception as e:
        print(f"\n❌ Error durante migración: {e}")
    finally:
        migrador.cerrar()


if __name__ == '__main__':
    main()
