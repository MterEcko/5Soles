#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup PostgreSQL - Portales del Quinto Sol
Configura PostgreSQL desde cero para el proyecto
"""

import os
import sys
import getpass

try:
    import psycopg2
    from psycopg2 import sql
except ImportError:
    print("❌ psycopg2 no instalado")
    print("   Instalar con: pip install psycopg2-binary")
    sys.exit(1)


def crear_archivo_env():
    """Crea archivo .env con configuración PostgreSQL"""
    print("\n" + "=" * 70)
    print("CONFIGURACIÓN POSTGRESQL")
    print("=" * 70)

    print("\nIngresa los datos de conexión PostgreSQL:")

    # Pedir datos
    host = input("Host [localhost]: ").strip() or "localhost"
    port = input("Puerto [5432]: ").strip() or "5432"
    database = input("Nombre base de datos [quinto_sol]: ").strip() or "quinto_sol"
    user = input("Usuario [quinto_sol_user]: ").strip() or "quinto_sol_user"
    password = getpass.getpass("Password: ").strip()

    # Crear contenido .env
    env_content = f"""# Configuración Base de Datos - Portales del Quinto Sol
# PostgreSQL Configuration

DB_TYPE=postgres
PG_HOST={host}
PG_PORT={port}
PG_DATABASE={database}
PG_USER={user}
PG_PASSWORD={password}

# Opcionales
# PG_SSLMODE=require  # Descomentar para conexión SSL
"""

    # Guardar .env
    with open('.env', 'w') as f:
        f.write(env_content)

    print("\n✅ Archivo .env creado")

    return {
        'host': host,
        'port': port,
        'database': database,
        'user': user,
        'password': password
    }


def verificar_postgres_instalado():
    """Verifica que PostgreSQL esté instalado y corriendo"""
    print("\n🔍 Verificando PostgreSQL...")

    import subprocess

    try:
        result = subprocess.run(['psql', '--version'],
                              capture_output=True,
                              text=True,
                              timeout=5)
        version = result.stdout.strip()
        print(f"✅ PostgreSQL instalado: {version}")
        return True
    except:
        print("❌ PostgreSQL no está instalado o no está en PATH")
        print("\nInstalar PostgreSQL:")
        print("  Ubuntu/Debian: sudo apt install postgresql postgresql-contrib")
        print("  macOS: brew install postgresql@15")
        print("  Windows: https://www.postgresql.org/download/windows/")
        return False


def crear_base_datos_y_usuario(config):
    """Crea base de datos y usuario si no existen"""
    print("\n" + "=" * 70)
    print("CREANDO BASE DE DATOS Y USUARIO")
    print("=" * 70)

    print("\n⚠️  Necesitas credenciales de superusuario de PostgreSQL")
    print("   (Usuario: postgres)\n")

    pg_password = getpass.getpass("Password de postgres: ").strip()

    try:
        # Conectar como postgres
        conn = psycopg2.connect(
            host=config['host'],
            port=config['port'],
            database='postgres',  # Conectar a DB default
            user='postgres',
            password=pg_password
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Verificar si usuario existe
        cursor.execute(
            "SELECT 1 FROM pg_roles WHERE rolname = %s",
            (config['user'],)
        )

        if cursor.fetchone():
            print(f"✅ Usuario '{config['user']}' ya existe")
        else:
            # Crear usuario
            cursor.execute(
                sql.SQL("CREATE USER {} WITH ENCRYPTED PASSWORD %s").format(
                    sql.Identifier(config['user'])
                ),
                (config['password'],)
            )
            print(f"✅ Usuario '{config['user']}' creado")

        # Verificar si base de datos existe
        cursor.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            (config['database'],)
        )

        if cursor.fetchone():
            print(f"✅ Base de datos '{config['database']}' ya existe")
        else:
            # Crear base de datos
            cursor.execute(
                sql.SQL("CREATE DATABASE {} OWNER {}").format(
                    sql.Identifier(config['database']),
                    sql.Identifier(config['user'])
                )
            )
            print(f"✅ Base de datos '{config['database']}' creada")

        cursor.close()
        conn.close()

        # Conectar a la nueva base de datos para configurar permisos
        conn = psycopg2.connect(
            host=config['host'],
            port=config['port'],
            database=config['database'],
            user='postgres',
            password=pg_password
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Dar permisos en schema public (PostgreSQL 15+)
        cursor.execute(
            sql.SQL("GRANT ALL ON SCHEMA public TO {}").format(
                sql.Identifier(config['user'])
            )
        )
        cursor.execute(
            sql.SQL("GRANT ALL ON ALL TABLES IN SCHEMA public TO {}").format(
                sql.Identifier(config['user'])
            )
        )
        cursor.execute(
            sql.SQL("ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO {}").format(
                sql.Identifier(config['user'])
            )
        )

        print("✅ Permisos configurados")

        cursor.close()
        conn.close()

        return True

    except psycopg2.Error as e:
        print(f"❌ Error: {e}")
        print("\nSi el usuario postgres no tiene password, intenta:")
        print("  sudo -u postgres psql")
        print("  ALTER USER postgres PASSWORD 'nuevo_password';")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False


def verificar_conexion(config):
    """Verifica que la conexión funcione"""
    print("\n" + "=" * 70)
    print("VERIFICANDO CONEXIÓN")
    print("=" * 70)

    try:
        conn = psycopg2.connect(
            host=config['host'],
            port=config['port'],
            database=config['database'],
            user=config['user'],
            password=config['password']
        )

        cursor = conn.cursor()
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]

        print(f"\n✅ Conexión exitosa!")
        print(f"   {version}")

        cursor.close()
        conn.close()

        return True

    except Exception as e:
        print(f"\n❌ Error de conexión: {e}")
        return False


def cargar_variables_entorno():
    """Carga variables de entorno desde .env"""
    if not os.path.exists('.env'):
        return False

    with open('.env', 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key] = value

    return True


def main():
    """Setup completo PostgreSQL"""
    print("\n" + "=" * 70)
    print("SETUP POSTGRESQL - PORTALES DEL QUINTO SOL")
    print("=" * 70)

    print("\n📋 Este script:")
    print("   1. Verifica instalación PostgreSQL")
    print("   2. Crea archivo .env con configuración")
    print("   3. Crea base de datos y usuario")
    print("   4. Configura permisos")
    print("   5. Verifica conexión")

    # Paso 1: Verificar PostgreSQL
    if not verificar_postgres_instalado():
        print("\n❌ Instala PostgreSQL primero")
        sys.exit(1)

    # Paso 2: Configuración
    if os.path.exists('.env'):
        print("\n⚠️  Ya existe archivo .env")
        respuesta = input("¿Sobrescribir? (s/n): ").strip().lower()
        if respuesta != 's':
            print("📖 Cargando configuración existente...")
            cargar_variables_entorno()
            config = {
                'host': os.getenv('PG_HOST', 'localhost'),
                'port': os.getenv('PG_PORT', '5432'),
                'database': os.getenv('PG_DATABASE', 'quinto_sol'),
                'user': os.getenv('PG_USER', 'quinto_sol_user'),
                'password': os.getenv('PG_PASSWORD', '')
            }
        else:
            config = crear_archivo_env()
    else:
        config = crear_archivo_env()

    # Paso 3: Crear BD y usuario
    print("\n¿Necesitas crear la base de datos y usuario?")
    print("(Si ya los creaste manualmente, di 'n')")
    respuesta = input("Crear BD y usuario? (s/n): ").strip().lower()

    if respuesta == 's':
        if not crear_base_datos_y_usuario(config):
            print("\n❌ No se pudo crear BD/usuario")
            print("\nPuedes crearlos manualmente con:")
            print(f"  sudo -u postgres psql")
            print(f"  CREATE DATABASE {config['database']};")
            print(f"  CREATE USER {config['user']} WITH PASSWORD '{config['password']}';")
            print(f"  GRANT ALL PRIVILEGES ON DATABASE {config['database']} TO {config['user']};")
            sys.exit(1)

    # Paso 4: Verificar conexión
    if not verificar_conexion(config):
        print("\n❌ Verifica configuración en .env")
        sys.exit(1)

    # Paso 5: Cargar variables de entorno
    cargar_variables_entorno()

    # Resumen final
    print("\n" + "=" * 70)
    print("✅ SETUP COMPLETADO")
    print("=" * 70)

    print(f"\n📝 Configuración guardada en .env:")
    print(f"   Host: {config['host']}")
    print(f"   Puerto: {config['port']}")
    print(f"   Base de datos: {config['database']}")
    print(f"   Usuario: {config['user']}")

    print("\n🚀 Próximos pasos:")
    print("   1. Exportar variables de entorno:")
    print("      source <(cat .env | grep -v '^#' | sed 's/^/export /')")
    print("   ")
    print("   2. O en cada terminal:")
    print("      export $(cat .env | grep -v '^#' | xargs)")
    print("   ")
    print("   3. Verificar conexión:")
    print("      python3 database_connector.py")
    print("   ")
    print("   4. Ejecutar simulación:")
    print("      python3 simulacion_mundo_completo.py")

    print("\n⚠️  IMPORTANTE:")
    print("   - Archivo .env contiene passwords, NO subir a git")
    print("   - Agregar .env a .gitignore")

    # Agregar .env a .gitignore si no está
    if os.path.exists('.gitignore'):
        with open('.gitignore', 'r') as f:
            gitignore = f.read()

        if '.env' not in gitignore:
            with open('.gitignore', 'a') as f:
                f.write('\n# Environment variables\n.env\n')
            print("   - .env agregado a .gitignore ✅")
    else:
        with open('.gitignore', 'w') as f:
            f.write('# Environment variables\n.env\n')
        print("   - .gitignore creado ✅")


if __name__ == '__main__':
    main()
