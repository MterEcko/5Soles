#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Helper para cargar .env automáticamente
Portales del Quinto Sol
"""

import os
import sys
from pathlib import Path

def cargar_env():
    """Carga variables del archivo .env"""
    env_file = Path(__file__).parent / '.env'

    if not env_file.exists():
        print("⚠️  Archivo .env no encontrado")
        print(f"   Esperado en: {env_file}")
        return False

    print(f"📖 Cargando configuración desde: {env_file}")

    with open(env_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()

            # Saltar comentarios y líneas vacías
            if not line or line.startswith('#'):
                continue

            # Parsear variable
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()

                # Remover comillas si existen
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]

                # Setear variable de entorno
                os.environ[key] = value
                print(f"   ✅ {key} = {value if key != 'PG_PASSWORD' else '***'}")

    print("\n✅ Variables de entorno cargadas\n")
    return True

if __name__ == '__main__':
    # Cargar .env
    if not cargar_env():
        sys.exit(1)

    # Verificar que DB_TYPE esté configurado
    db_type = os.getenv('DB_TYPE', 'sqlite')
    print(f"🗄️  Tipo de BD configurado: {db_type}")

    if db_type == 'postgres':
        print(f"   Host: {os.getenv('PG_HOST')}")
        print(f"   Puerto: {os.getenv('PG_PORT')}")
        print(f"   Base de datos: {os.getenv('PG_DATABASE')}")
        print(f"   Usuario: {os.getenv('PG_USER')}")

    print("\n" + "="*70)
    print("Ahora puedes ejecutar tus scripts")
    print("="*70)
    print("\nEjemplo:")
    print("  python run_with_env.py database_connector.py")
    print("  python run_with_env.py simulacion_mundo_completo.py")

    # Si hay argumentos, ejecutar el script indicado
    if len(sys.argv) > 1:
        script_to_run = sys.argv[1]
        script_args = sys.argv[2:]

        print(f"\n▶️  Ejecutando: {script_to_run} {' '.join(script_args)}\n")
        print("="*70 + "\n")

        # Ejecutar script (UTF-8 para compatibilidad Windows)
        with open(script_to_run, encoding='utf-8') as f:
            code = compile(f.read(), script_to_run, 'exec')
            # Modificar sys.argv para el script ejecutado
            sys.argv = [script_to_run] + script_args
            exec(code, {'__name__': '__main__', '__file__': script_to_run})
