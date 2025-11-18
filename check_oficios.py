#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('quinto_sol.db')
cursor = conn.cursor()

cursor.execute("SELECT id, nombre, categoria, descripcion FROM oficios ORDER BY categoria, nombre")
print("=== OFICIOS POR CATEGORÍA ===\n")

categoria_actual = None
for id, nombre, categoria, desc in cursor.fetchall():
    if categoria != categoria_actual:
        print(f"\n{categoria.upper()}:")
        categoria_actual = categoria
    print(f"  {id:3d}. {nombre:20s} - {desc if desc else 'Sin descripción'}")

conn.close()
