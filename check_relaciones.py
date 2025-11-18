#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('quinto_sol.db')
cursor = conn.cursor()

# Check especies
cursor.execute("SELECT id, nombre FROM especies")
print("=== ESPECIES ===")
for row in cursor.fetchall():
    print(f"  {row[0]}: {row[1]}")

# Check if especies_civilizaciones table exists
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='especies_civilizaciones'")
if cursor.fetchone():
    print("\n=== TABLA especies_civilizaciones EXISTE ===")
    cursor.execute("SELECT COUNT(*) FROM especies_civilizaciones")
    print(f"Total registros: {cursor.fetchone()[0]}")

    cursor.execute("SELECT * FROM especies_civilizaciones LIMIT 5")
    print("\nPrimeros 5 registros:")
    for row in cursor.fetchall():
        print(f"  {row}")
else:
    print("\n❌ Tabla especies_civilizaciones NO EXISTE")

conn.close()
