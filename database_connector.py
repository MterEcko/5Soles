#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Database Connector - Soporte para SQLite y PostgreSQL
Portales del Quinto Sol

Módulo unificado de conexión a base de datos.
Soporta SQLite (desarrollo/testing) y PostgreSQL (producción).
"""

import os
from typing import Optional, Tuple, Any
from contextlib import contextmanager

# Configuración
DB_TYPE = os.getenv('DB_TYPE', 'sqlite')  # 'sqlite' o 'postgres'
DB_PATH = os.getenv('DB_PATH', 'quinto_sol.db')

# PostgreSQL config
PG_HOST = os.getenv('PG_HOST', 'localhost')
PG_PORT = os.getenv('PG_PORT', '5432')
PG_DATABASE = os.getenv('PG_DATABASE', 'quinto_sol')
PG_USER = os.getenv('PG_USER', 'postgres')
PG_PASSWORD = os.getenv('PG_PASSWORD', '')


class DatabaseConnector:
    """
    Conector unificado para SQLite y PostgreSQL

    Uso:
        # Opción 1: Usar como context manager
        with DatabaseConnector() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM personas LIMIT 10")

        # Opción 2: Crear instancia
        db = DatabaseConnector()
        conn = db.connect()
        cursor = conn.cursor()
        # ... hacer queries
        db.close()
    """

    def __init__(self, db_type: Optional[str] = None):
        """
        Inicializa conector

        Args:
            db_type: 'sqlite' o 'postgres'. Si None, usa variable de entorno DB_TYPE
        """
        self.db_type = db_type or DB_TYPE
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establece conexión según el tipo de base de datos"""
        if self.db_type == 'sqlite':
            return self._connect_sqlite()
        elif self.db_type == 'postgres':
            return self._connect_postgres()
        else:
            raise ValueError(f"Tipo de DB no soportado: {self.db_type}")

    def _connect_sqlite(self):
        """Conexión a SQLite"""
        import sqlite3

        self.conn = sqlite3.connect(DB_PATH)
        self.conn.row_factory = sqlite3.Row  # Acceso por nombre de columna
        self.cursor = self.conn.cursor()

        print(f"✅ Conectado a SQLite: {DB_PATH}")
        return self.conn

    def _connect_postgres(self):
        """Conexión a PostgreSQL"""
        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor
        except ImportError:
            raise ImportError(
                "psycopg2 no está instalado. Instalar con: pip install psycopg2-binary"
            )

        self.conn = psycopg2.connect(
            host=PG_HOST,
            port=PG_PORT,
            database=PG_DATABASE,
            user=PG_USER,
            password=PG_PASSWORD
        )
        self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)

        print(f"✅ Conectado a PostgreSQL: {PG_USER}@{PG_HOST}:{PG_PORT}/{PG_DATABASE}")
        return self.conn

    def execute(self, query: str, params: Optional[Tuple] = None) -> Any:
        """
        Ejecuta query y retorna cursor

        Args:
            query: SQL query
            params: Parámetros (opcional)
        """
        if not self.cursor:
            self.connect()

        # Convertir placeholders si es necesario (SQLite usa ?, Postgres usa %s)
        if self.db_type == 'postgres' and '?' in query:
            query = self._convert_placeholders(query)

        if params:
            self.cursor.execute(query, params)
        else:
            self.cursor.execute(query)

        return self.cursor

    def executemany(self, query: str, params_list: list):
        """Ejecuta query múltiples veces con diferentes parámetros"""
        if not self.cursor:
            self.connect()

        if self.db_type == 'postgres' and '?' in query:
            query = self._convert_placeholders(query)

        self.cursor.executemany(query, params_list)

    def executescript(self, script: str):
        """Ejecuta script SQL (múltiples statements)"""
        if not self.cursor:
            self.connect()

        if self.db_type == 'sqlite':
            self.conn.executescript(script)
        else:
            # PostgreSQL no tiene executescript, ejecutar línea por línea
            statements = script.split(';')
            for statement in statements:
                statement = statement.strip()
                if statement:
                    self.cursor.execute(statement)

    def commit(self):
        """Commit de transacción"""
        if self.conn:
            self.conn.commit()

    def rollback(self):
        """Rollback de transacción"""
        if self.conn:
            self.conn.rollback()

    def fetchone(self):
        """Fetch un resultado"""
        return self.cursor.fetchone() if self.cursor else None

    def fetchall(self):
        """Fetch todos los resultados"""
        return self.cursor.fetchall() if self.cursor else []

    def fetchmany(self, size: int):
        """Fetch varios resultados"""
        return self.cursor.fetchmany(size) if self.cursor else []

    def lastrowid(self) -> Optional[int]:
        """Obtiene ID del último row insertado"""
        if self.db_type == 'sqlite':
            return self.cursor.lastrowid
        else:
            # PostgreSQL requiere RETURNING id
            return None

    def close(self):
        """Cierra conexión"""
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

        print(f"✅ Conexión cerrada ({self.db_type})")

    def _convert_placeholders(self, query: str) -> str:
        """Convierte placeholders de SQLite (?) a PostgreSQL (%s)"""
        # Simple conversión - para casos complejos usar prepared statements
        return query.replace('?', '%s')

    # Context manager support
    def __enter__(self):
        """Entrada a context manager"""
        self.connect()
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Salida de context manager"""
        if exc_type is not None:
            self.rollback()
        else:
            self.commit()
        self.close()


@contextmanager
def get_db_connection(db_type: Optional[str] = None):
    """
    Context manager para obtener conexión de BD

    Uso:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM personas")
            results = cursor.fetchall()
    """
    db = DatabaseConnector(db_type)
    try:
        conn = db.connect()
        yield conn
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def execute_query(query: str, params: Optional[Tuple] = None, db_type: Optional[str] = None):
    """
    Ejecuta query simple y retorna resultados

    Uso:
        results = execute_query("SELECT * FROM personas WHERE id = ?", (123,))
    """
    with get_db_connection(db_type) as conn:
        cursor = conn.cursor()

        # Convertir placeholders si es postgres
        if (db_type or DB_TYPE) == 'postgres' and '?' in query:
            query = query.replace('?', '%s')

        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        return cursor.fetchall()


def test_connection():
    """Prueba de conexión"""
    print("\n" + "=" * 70)
    print("PRUEBA DE CONEXIÓN A BASE DE DATOS")
    print("=" * 70)

    print(f"\nTipo de BD configurado: {DB_TYPE}")

    try:
        db = DatabaseConnector()
        conn = db.connect()

        # Probar query simple
        cursor = conn.cursor()

        if DB_TYPE == 'sqlite':
            cursor.execute("SELECT sqlite_version()")
            version = cursor.fetchone()[0]
            print(f"SQLite versión: {version}")
        else:
            cursor.execute("SELECT version()")
            version = cursor.fetchone()[0]
            print(f"PostgreSQL versión: {version}")

        # Verificar tablas
        if DB_TYPE == 'sqlite':
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        else:
            cursor.execute("SELECT tablename FROM pg_tables WHERE schemaname='public' ORDER BY tablename")

        tables = cursor.fetchall()
        print(f"\nTablas encontradas: {len(tables)}")

        if tables:
            print("Primeras 10 tablas:")
            for i, table in enumerate(tables[:10], 1):
                print(f"  {i}. {table[0]}")

        db.close()

        print("\n✅ Conexión exitosa")

    except Exception as e:
        print(f"\n❌ Error de conexión: {e}")
        print("\nVerifica:")
        print("  1. Variables de entorno configuradas correctamente")
        print("  2. Base de datos existe y está accesible")
        print("  3. Credenciales correctas (PostgreSQL)")
        print("  4. psycopg2-binary instalado (PostgreSQL)")


if __name__ == '__main__':
    # Configuración de ejemplo
    print("Configuración actual:")
    print(f"  DB_TYPE: {DB_TYPE}")

    if DB_TYPE == 'sqlite':
        print(f"  DB_PATH: {DB_PATH}")
    else:
        print(f"  PG_HOST: {PG_HOST}")
        print(f"  PG_PORT: {PG_PORT}")
        print(f"  PG_DATABASE: {PG_DATABASE}")
        print(f"  PG_USER: {PG_USER}")

    print("\nPara cambiar a PostgreSQL, exporta:")
    print("  export DB_TYPE=postgres")
    print("  export PG_HOST=localhost")
    print("  export PG_PORT=5432")
    print("  export PG_DATABASE=quinto_sol")
    print("  export PG_USER=postgres")
    print("  export PG_PASSWORD=tu_password")

    # Ejecutar prueba
    test_connection()
