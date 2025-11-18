#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('quinto_sol.db')
cursor = conn.cursor()

# Get ALL civilizations
cursor.execute("SELECT id, nombre, tipo FROM civilizaciones ORDER BY nombre")
print("=== TODAS LAS CIVILIZACIONES ===")
for row in cursor.fetchall():
    print(f"  ID {row[0]:2d}: {row[1]:30s} (Tipo: {row[2]})")

conn.close()
