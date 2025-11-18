#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('quinto_sol.db')
cursor = conn.cursor()

# Check civilizaciones
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='civilizaciones'")
if cursor.fetchone():
    print("=== CIVILIZACIONES ===")
    cursor.execute("SELECT id, nombre FROM civilizaciones")
    civs = cursor.fetchall()
    if civs:
        for row in civs:
            print(f"  {row[0]}: {row[1]}")
    else:
        print("  ❌ NO HAY CIVILIZACIONES EN LA BASE DE DATOS")
else:
    print("❌ Tabla civilizaciones NO EXISTE")

# Check dioses
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='dioses'")
if cursor.fetchone():
    print("\n=== DIOSES ===")
    cursor.execute("SELECT id, nombre FROM dioses")
    dioses = cursor.fetchall()
    if dioses:
        for row in dioses:
            print(f"  {row[0]}: {row[1]}")
    else:
        print("  ❌ NO HAY DIOSES EN LA BASE DE DATOS")
else:
    print("❌ Tabla dioses NO EXISTE")

conn.close()
